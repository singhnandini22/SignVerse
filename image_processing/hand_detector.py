import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandDetector:
    """
    SignVerse reusable hand detection module.

    Detects up to two hands and organizes them
    according to the physical left/right hand.
    """

    def __init__(
        self,
        model_path="models/hand_landmarker.task",
        running_mode=vision.RunningMode.VIDEO,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5
    ):
        self.model_path = model_path
        self.running_mode = running_mode

        # ----------------------------------------------------
        # MediaPipe configuration
        # ----------------------------------------------------

        base_options = python.BaseOptions(
            model_asset_path=self.model_path
        )

        options = vision.HandLandmarkerOptions(
            base_options=base_options,

            # We will process webcam/video frames.
            running_mode=running_mode,

            # SignVerse supports up to two hands.
            num_hands=2,

            min_hand_detection_confidence=min_hand_detection_confidence,
            min_hand_presence_confidence=min_hand_presence_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

        # ----------------------------------------------------
        # Create MediaPipe hand landmarker
        # ----------------------------------------------------

        self.landmarker = (
            vision.HandLandmarker.create_from_options(
                options
            )
        )

        # Timestamp required by VIDEO mode.
        self.timestamp_ms = 0


    def detect(self, frame, mirror=True):
        """
        Detect hands in one video frame.

        Parameters:
            frame:
                OpenCV BGR image.

        Returns:
            Dictionary containing:

            {
                "left_hand": list of 21 (x, y, z) points
                              or None,

                "right_hand": list of 21 (x, y, z) points
                              or None
            }
        """

        # ----------------------------------------------------
        # Mirror the frame for natural webcam interaction
        # ----------------------------------------------------

        if mirror:
            frame = cv2.flip(frame, 1)

        # ----------------------------------------------------
        # Convert BGR → RGB
        # ----------------------------------------------------

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # ----------------------------------------------------
        # Convert to MediaPipe image
        # ----------------------------------------------------

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # ----------------------------------------------------
        # Detect hands according to running mode
        # ----------------------------------------------------

        if self.running_mode == vision.RunningMode.IMAGE:

            result = self.landmarker.detect(
                mp_image
            )

        else:

            self.timestamp_ms += 33

            result = self.landmarker.detect_for_video(
                mp_image,
                self.timestamp_ms
            )

        # ----------------------------------------------------
        # Prepare SignVerse structure
        # ----------------------------------------------------

        left_hand = None
        right_hand = None

        # ----------------------------------------------------
        # Process detected hands
        # ----------------------------------------------------

        for hand_index, landmarks in enumerate(
            result.hand_landmarks
        ):

            # MediaPipe handedness
            handedness = result.handedness[
                hand_index
            ][0]

            mediapipe_label = (
                handedness.category_name
            )

            # ------------------------------------------------
            # Convert MediaPipe handedness to our convention
            #
            # Because the webcam frame is mirrored before
            # detection, we swap the MediaPipe label so that
            # SignVerse always refers to the physical hand.
            # ------------------------------------------------

            if mirror:

                # Webcam input is mirrored.
                if mediapipe_label == "Left":
                    hand_label = "Right"
                else:
                    hand_label = "Left"

            else:

                # Dataset image is not mirrored.
                hand_label = mediapipe_label

            # ------------------------------------------------
            # Extract 21 landmark coordinates
            # ------------------------------------------------

            hand_landmarks = []

            for landmark in landmarks:

                hand_landmarks.append(
                    (
                        landmark.x,
                        landmark.y,
                        landmark.z
                    )
                )

            # ------------------------------------------------
            # Store according to physical hand
            # ------------------------------------------------

            if hand_label == "Left":

                left_hand = hand_landmarks

            elif hand_label == "Right":

                right_hand = hand_landmarks


        # ----------------------------------------------------
        # Return standardized structure
        # ----------------------------------------------------

        return {
            "left_hand": left_hand,
            "right_hand": right_hand
        }


    def close(self):
        """
        Release the MediaPipe landmarker.
        """

        self.landmarker.close()