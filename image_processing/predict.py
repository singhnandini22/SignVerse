import os
import cv2
import joblib
import numpy as np
import pandas as pd

from collections import deque, Counter

from mediapipe.tasks.python import vision

from hand_detector import HandDetector
from landmark_processor import LandmarkProcessor
from feature_extractor_v4 import FeatureExtractor


# ============================================================
# SIGNVERSE - REUSABLE ISL RECOGNIZER
# ============================================================


class ISLRecognizer:

    def __init__(self):

        base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        # ----------------------------------------------------
        # Model paths
        # ----------------------------------------------------

        self.model_path = os.path.join(
            base_dir,
            "models",
            "signverse_v4_gradient_boosting_targeted_OYZ.pkl"
        )

        self.hand_model_path = os.path.join(
            base_dir,
            "models",
            "hand_landmarker.task"
        )

        # ----------------------------------------------------
        # Load classifier
        # ----------------------------------------------------

        print("Loading SignVerse model...")

        self.model = joblib.load(
            self.model_path
        )

        print("Model loaded successfully.")

        # ----------------------------------------------------
        # Initialize IP modules
        # ----------------------------------------------------

        self.detector = HandDetector(
            model_path=self.hand_model_path,
            running_mode=vision.RunningMode.IMAGE
        )

        self.processor = LandmarkProcessor()

        self.extractor = FeatureExtractor()

        # ----------------------------------------------------
        # Feature names
        # ----------------------------------------------------

        self.feature_columns = [
            f"feature_{i}"
            for i in range(288)
        ]

        # ----------------------------------------------------
        # Temporal stabilization
        # ----------------------------------------------------

        self.prediction_history = deque(
            maxlen=7
        )

    # ========================================================
    # PREDICT ONE WEBCAM FRAME
    # ========================================================

    def predict_frame(
        self,
        frame,
        top_k=3
    ):

        # ----------------------------------------------------
        # Detect hands
        # ----------------------------------------------------

        hands = self.detector.detect(
            frame,
            mirror=False
        )

        left_detected = (
            hands["left_hand"] is not None
        )

        right_detected = (
            hands["right_hand"] is not None
        )

        # ----------------------------------------------------
        # No hand
        # ----------------------------------------------------

        if not left_detected and not right_detected:

            self.prediction_history.clear()
            return {
                "success": False,
                "message": "No hand detected.",
                "prediction": None,
                "confidence": 0.0,
                "stable": False,
                "suggestions": [],
                "hands_detected": {
                    "left": False,
                    "right": False
                }
            }

        # ----------------------------------------------------
        # Landmark processing
        # ----------------------------------------------------

        processed_hands = self.processor.process(
            hands
        )

        # ----------------------------------------------------
        # Feature extraction
        # ----------------------------------------------------

        features = self.extractor.extract(
            processed_hands
        )

        # ----------------------------------------------------
        # Feature count check
        # ----------------------------------------------------

        if len(features) != 288:

            return {
                "success": False,
                "message": (
                    f"Expected 288 features, "
                    f"got {len(features)}."
                ),
                "prediction": None,
                "confidence": 0.0,
                "suggestions": []
            }

        # ----------------------------------------------------
        # Prepare model input
        # ----------------------------------------------------

        X = pd.DataFrame(
            [features],
            columns=self.feature_columns
        )

        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        probabilities = self.model.predict_proba(
            X
        )[0]

        top_indices = np.argsort(
            probabilities
        )[::-1][:top_k]

        suggestions = []

        for index in top_indices:

            suggestions.append({
                "label": str(
                    self.model.classes_[index]
                ),
                "confidence": float(
                    probabilities[index]
                )
            })

        best_index = top_indices[0]

        prediction = str(
            self.model.classes_[best_index]
        )

        confidence = float(
            probabilities[best_index]
        )

        # ----------------------------------------------------
        # Temporal stabilization
        # ----------------------------------------------------

        self.prediction_history.append(
            (
                prediction,
                confidence
            )
        )

        # Count recent predictions
        labels = [
            item[0]
            for item in self.prediction_history
        ]

        counts = Counter(labels)

        stable_label, stable_count = (
            counts.most_common(1)[0]
        )

        # Require at least 3 matching predictions
        # within the last 7 frames.
        is_stable = stable_count >= 3

        if is_stable:

            stable_confidences = [
                conf
                for label, conf
                in self.prediction_history
                if label == stable_label
            ]

            stable_confidence = (
                sum(stable_confidences)
                / len(stable_confidences)
            )

        else:

            stable_label = prediction
            stable_confidence = confidence


        # ----------------------------------------------------
        # Return structured result
        # ----------------------------------------------------

        return {
            "success": True,
            "message": "Prediction successful.",
            "prediction": stable_label,
            "confidence": float(
                stable_confidence
            ),
            "stable": is_stable,
            "raw_prediction": prediction,
            "raw_confidence": confidence,
            "suggestions": suggestions,
            "hands_detected": {
                "left": left_detected,
                "right": right_detected
            }
        }


    # ========================================================
    # PREDICT ONE IMAGE
    # ========================================================

    def predict_image(
        self,
        image_path,
        top_k=3
    ):

        # ----------------------------------------------------
        # Read image
        # ----------------------------------------------------

        image = cv2.imread(
            image_path
        )

        if image is None:

            return {
                "success": False,
                "message": "Could not read image.",
                "prediction": None,
                "confidence": 0.0,
                "suggestions": []
            }

        # ----------------------------------------------------
        # Detect hands
        #
        # Dataset convention:
        # no mirroring before detection.
        # ----------------------------------------------------

        hands = self.detector.detect(
            image,
            mirror=False
        )

        left_detected = (
            hands["left_hand"] is not None
        )

        right_detected = (
            hands["right_hand"] is not None
        )

        # ----------------------------------------------------
        # No hand
        # ----------------------------------------------------

        if not left_detected and not right_detected:

            return {
                "success": False,
                "message": "No hand detected.",
                "prediction": None,
                "confidence": 0.0,
                "suggestions": [],
                "hands_detected": {
                    "left": False,
                    "right": False
                }
            }

        # ----------------------------------------------------
        # Landmark processing
        # ----------------------------------------------------

        processed_hands = self.processor.process(
            hands
        )

        # ----------------------------------------------------
        # V4 feature extraction
        # ----------------------------------------------------

        features = self.extractor.extract(
            processed_hands
        )

        # ----------------------------------------------------
        # Feature count check
        # ----------------------------------------------------

        if len(features) != 288:

            return {
                "success": False,
                "message": (
                    f"Expected 288 features, "
                    f"got {len(features)}."
                ),
                "prediction": None,
                "confidence": 0.0,
                "suggestions": []
            }

        # ----------------------------------------------------
        # Prepare model input
        # ----------------------------------------------------

        X = pd.DataFrame(
            [features],
            columns=self.feature_columns
        )

        # ----------------------------------------------------
        # Prediction probabilities
        # ----------------------------------------------------

        probabilities = self.model.predict_proba(
            X
        )[0]

        # ----------------------------------------------------
        # Top predictions
        # ----------------------------------------------------

        top_indices = np.argsort(
            probabilities
        )[::-1][:top_k]

        suggestions = []

        for index in top_indices:

            suggestions.append({
                "label": str(
                    self.model.classes_[index]
                ),
                "confidence": float(
                    probabilities[index]
                )
            })

        # ----------------------------------------------------
        # Final prediction
        # ----------------------------------------------------

        best_index = top_indices[0]

        prediction = str(
            self.model.classes_[best_index]
        )

        confidence = float(
            probabilities[best_index]
        )

        # ----------------------------------------------------
        # Return structured result
        # ----------------------------------------------------

        return {
            "success": True,
            "message": "Prediction successful.",
            "prediction": prediction,
            "confidence": confidence,
            "suggestions": suggestions,
            "hands_detected": {
                "left": left_detected,
                "right": right_detected
            }
        }


    # ========================================================
    # CLEANUP
    # ========================================================

    def close(self):

        self.detector.close()


# ============================================================
# SIMPLE TEST
# ============================================================

if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:

        print()
        print(
            "Usage:"
        )
        print(
            "python predict.py <image_path>"
        )
        print()

        raise SystemExit

    image_path = sys.argv[1]

    recognizer = ISLRecognizer()

    try:

        result = recognizer.predict_image(
            image_path
        )

        print()
        print("=" * 60)
        print("SIGNVERSE PREDICTION")
        print("=" * 60)

        print()

        if not result["success"]:

            print(
                "Result:",
                result["message"]
            )

        else:

            print(
                "Predicted sign:",
                result["prediction"]
            )

            print(
                "Confidence:",
                f"{result['confidence'] * 100:.2f}%"
            )

            print(
                "Hands:",
                result["hands_detected"]
            )

            print()
            print("Possible signs:")

            for suggestion in result["suggestions"]:

                print(
                    f"  {suggestion['label']} "
                    f"({suggestion['confidence'] * 100:.2f}%)"
                )

    finally:

        recognizer.close()