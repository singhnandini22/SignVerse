import numpy as np


# ============================================================
# SIGNVERSE - LANDMARK PROCESSOR
# ============================================================


class LandmarkProcessor:
    """
    Processes raw MediaPipe hand landmarks.

    For each detected hand, this module keeps:

    1. Raw landmarks
    2. Normalized landmarks

    The raw landmarks are preserved for inter-hand
    relationship features.

    The normalized landmarks are used for hand-shape
    features such as angles and distances.
    """


    def __init__(self):

        # Small value used to prevent division by zero.
        self.epsilon = 1e-6


    def normalize_hand(self, hand_landmarks):
        """
        Normalize one hand.

        Steps:
            1. Use wrist (landmark 0) as origin.
            2. Use wrist → Middle MCP (landmark 9)
               as scale reference.

        Parameters:
            hand_landmarks:
                List of 21 (x, y, z) landmarks.

        Returns:
            NumPy array containing 21 normalized
            (x, y, z) landmarks.
        """

        if hand_landmarks is None:
            return None


        # ----------------------------------------------------
        # Convert to NumPy array
        # ----------------------------------------------------

        points = np.array(
            hand_landmarks,
            dtype=np.float32
        )


        # ----------------------------------------------------
        # Check that we actually received 21 landmarks
        # ----------------------------------------------------

        if points.shape != (21, 3):

            raise ValueError(
                "Expected 21 landmarks with "
                "(x, y, z) coordinates."
            )


        # ----------------------------------------------------
        # Landmark 0 = Wrist
        # ----------------------------------------------------

        wrist = points[0].copy()


        # ----------------------------------------------------
        # Translation normalization
        #
        # Move wrist to the origin.
        # ----------------------------------------------------

        normalized = points - wrist


        # ----------------------------------------------------
        # Landmark 9 = Middle MCP
        #
        # Use Wrist → Middle MCP distance as scale.
        # ----------------------------------------------------

        scale = np.linalg.norm(
            normalized[9]
        )


        # ----------------------------------------------------
        # Prevent division by zero
        # ----------------------------------------------------

        if scale < self.epsilon:

            return None


        # ----------------------------------------------------
        # Scale normalization
        # ----------------------------------------------------

        normalized = normalized / scale


        return normalized


    def process_hand(self, hand_landmarks):
        """
        Process one hand and return both raw and
        normalized landmarks.
        """

        if hand_landmarks is None:

            return {
                "raw": None,
                "normalized": None
            }


        # Keep raw landmarks exactly as received.
        raw = np.array(
            hand_landmarks,
            dtype=np.float32
        )


        # Create normalized version.
        normalized = self.normalize_hand(
            hand_landmarks
        )


        return {
            "raw": raw,
            "normalized": normalized
        }


    def process(self, hands):
        """
        Process the output of HandDetector.

        Expected input:

        {
            "left_hand": [...21 landmarks...] or None,
            "right_hand": [...21 landmarks...] or None
        }

        Returns:

        {
            "left_hand": {
                "raw": ...,
                "normalized": ...
            },

            "right_hand": {
                "raw": ...,
                "normalized": ...
            }
        }
        """

        left_hand = hands["left_hand"]
        right_hand = hands["right_hand"]


        return {
            "left_hand": self.process_hand(
                left_hand
            ),

            "right_hand": self.process_hand(
                right_hand
            )
        }