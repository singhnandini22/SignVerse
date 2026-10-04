import numpy as np


# ============================================================
# SIGNVERSE - FEATURE EXTRACTOR V4
# ============================================================

class FeatureExtractor:
    """
    SignVerse feature extraction module - Version 4.

    V4 keeps all 234 features from V3 and adds
    targeted hand-shape and inter-hand geometry features.

    V3 per hand:
        115 features

    V3:
        115 + 115 + 4 = 234

    V4 additional per hand:
        24 features

    V4 additional inter-hand:
        6 features

    Total V4:
        234 + (24 * 2) + 6 = 288 features
    """

    def __init__(self):
        self.epsilon = 1e-6

    # ========================================================
    # BASIC GEOMETRY
    # ========================================================

    def calculate_angle(self, a, b, c):

        a = np.array(a, dtype=np.float32)
        b = np.array(b, dtype=np.float32)
        c = np.array(c, dtype=np.float32)

        vector1 = a - b
        vector2 = c - b

        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)

        if norm1 < self.epsilon or norm2 < self.epsilon:
            return 0.0

        cosine = np.dot(vector1, vector2) / (
            norm1 * norm2
        )

        cosine = np.clip(
            cosine,
            -1.0,
            1.0
        )

        angle = np.degrees(
            np.arccos(cosine)
        )

        return float(angle)

    def calculate_distance(self, a, b):

        a = np.array(a, dtype=np.float32)
        b = np.array(b, dtype=np.float32)

        return float(
            np.linalg.norm(a - b)
        )

    # ========================================================
    # V3 FEATURES
    # ========================================================

    def calculate_finger_angles(self, hand):

        if hand is None:
            return np.zeros(5, dtype=np.float32)

        angles = [

            # Thumb
            self.calculate_angle(
                hand[1], hand[2], hand[3]
            ),

            # Index
            self.calculate_angle(
                hand[5], hand[6], hand[7]
            ),

            # Middle
            self.calculate_angle(
                hand[9], hand[10], hand[11]
            ),

            # Ring
            self.calculate_angle(
                hand[13], hand[14], hand[15]
            ),

            # Pinky
            self.calculate_angle(
                hand[17], hand[18], hand[19]
            )
        ]

        return np.array(
            angles,
            dtype=np.float32
        )

    def calculate_distance_features(self, hand):

        if hand is None:
            return np.zeros(6, dtype=np.float32)

        wrist = hand[0]

        thumb_tip = hand[4]
        index_tip = hand[8]
        middle_tip = hand[12]
        ring_tip = hand[16]
        pinky_tip = hand[20]

        distances = [

            self.calculate_distance(
                thumb_tip,
                index_tip
            ),

            self.calculate_distance(
                thumb_tip,
                middle_tip
            ),

            self.calculate_distance(
                thumb_tip,
                ring_tip
            ),

            self.calculate_distance(
                thumb_tip,
                pinky_tip
            ),

            self.calculate_distance(
                wrist,
                index_tip
            ),

            self.calculate_distance(
                wrist,
                middle_tip
            )
        ]

        return np.array(
            distances,
            dtype=np.float32
        )

    def calculate_finger_segment_lengths(self, hand):

        if hand is None:
            return np.zeros(15, dtype=np.float32)

        lengths = [

            self.calculate_distance(hand[1], hand[2]),
            self.calculate_distance(hand[2], hand[3]),
            self.calculate_distance(hand[3], hand[4]),

            self.calculate_distance(hand[5], hand[6]),
            self.calculate_distance(hand[6], hand[7]),
            self.calculate_distance(hand[7], hand[8]),

            self.calculate_distance(hand[9], hand[10]),
            self.calculate_distance(hand[10], hand[11]),
            self.calculate_distance(hand[11], hand[12]),

            self.calculate_distance(hand[13], hand[14]),
            self.calculate_distance(hand[14], hand[15]),
            self.calculate_distance(hand[15], hand[16]),

            self.calculate_distance(hand[17], hand[18]),
            self.calculate_distance(hand[18], hand[19]),
            self.calculate_distance(hand[19], hand[20])
        ]

        return np.array(
            lengths,
            dtype=np.float32
        )

    def calculate_palm_orientation(self, hand):

        if hand is None:
            return np.zeros(3, dtype=np.float32)

        wrist = hand[0]
        index_mcp = hand[5]
        pinky_mcp = hand[17]

        vector1 = index_mcp - wrist
        vector2 = pinky_mcp - wrist

        normal = np.cross(
            vector1,
            vector2
        )

        magnitude = np.linalg.norm(normal)

        if magnitude < self.epsilon:
            return np.zeros(3, dtype=np.float32)

        normal = normal / magnitude

        return normal.astype(np.float32)

    def calculate_wrist_fingertip_distances(self, hand):

        if hand is None:
            return np.zeros(5, dtype=np.float32)

        wrist = hand[0]

        fingertips = [
            hand[4],
            hand[8],
            hand[12],
            hand[16],
            hand[20]
        ]

        distances = [
            self.calculate_distance(
                wrist,
                fingertip
            )
            for fingertip in fingertips
        ]

        return np.array(
            distances,
            dtype=np.float32
        )

    def calculate_adjacent_fingertip_distances(self, hand):

        if hand is None:
            return np.zeros(4, dtype=np.float32)

        fingertips = [
            hand[4],
            hand[8],
            hand[12],
            hand[16],
            hand[20]
        ]

        distances = []

        for i in range(4):

            distances.append(
                self.calculate_distance(
                    fingertips[i],
                    fingertips[i + 1]
                )
            )

        return np.array(
            distances,
            dtype=np.float32
        )

    def calculate_fingertip_palm_distances(self, hand):

        if hand is None:
            return np.zeros(5, dtype=np.float32)

        palm_center = (
            np.array(hand[0], dtype=np.float32)
            + np.array(hand[5], dtype=np.float32)
            + np.array(hand[9], dtype=np.float32)
            + np.array(hand[17], dtype=np.float32)
        ) / 4.0

        fingertips = [
            hand[4],
            hand[8],
            hand[12],
            hand[16],
            hand[20]
        ]

        distances = [
            self.calculate_distance(
                fingertip,
                palm_center
            )
            for fingertip in fingertips
        ]

        return np.array(
            distances,
            dtype=np.float32
        )

    def calculate_total_finger_lengths(self, hand):

        if hand is None:
            return np.zeros(5, dtype=np.float32)

        fingers = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
            [17, 18, 19, 20]
        ]

        total_lengths = []

        for finger in fingers:

            length = 0.0

            for i in range(len(finger) - 1):

                length += self.calculate_distance(
                    hand[finger[i]],
                    hand[finger[i + 1]]
                )

            total_lengths.append(length)

        return np.array(
            total_lengths,
            dtype=np.float32
        )

    def calculate_finger_length_ratios(self, hand):

        if hand is None:
            return np.zeros(4, dtype=np.float32)

        lengths = self.calculate_total_finger_lengths(hand)

        ratios = [

            lengths[1] / max(
                lengths[2],
                self.epsilon
            ),

            lengths[3] / max(
                lengths[2],
                self.epsilon
            ),

            lengths[4] / max(
                lengths[2],
                self.epsilon
            ),

            lengths[0] / max(
                lengths[1],
                self.epsilon
            )
        ]

        return np.array(
            ratios,
            dtype=np.float32
        )

    # ========================================================
    # V4 - ADDITIONAL JOINT ANGLES
    # ========================================================

    def calculate_additional_joint_angles(self, hand):

        if hand is None:
            return np.zeros(10, dtype=np.float32)

        angles = [

            # Index MCP
            self.calculate_angle(
                hand[0],
                hand[5],
                hand[6]
            ),

            # Index DIP
            self.calculate_angle(
                hand[6],
                hand[7],
                hand[8]
            ),

            # Middle MCP
            self.calculate_angle(
                hand[0],
                hand[9],
                hand[10]
            ),

            # Middle DIP
            self.calculate_angle(
                hand[10],
                hand[11],
                hand[12]
            ),

            # Ring MCP
            self.calculate_angle(
                hand[0],
                hand[13],
                hand[14]
            ),

            # Ring DIP
            self.calculate_angle(
                hand[14],
                hand[15],
                hand[16]
            ),

            # Pinky MCP
            self.calculate_angle(
                hand[0],
                hand[17],
                hand[18]
            ),

            # Pinky DIP
            self.calculate_angle(
                hand[18],
                hand[19],
                hand[20]
            ),

            # Thumb MCP
            self.calculate_angle(
                hand[0],
                hand[1],
                hand[2]
            ),

            # Thumb DIP
            self.calculate_angle(
                hand[2],
                hand[3],
                hand[4]
            )
        ]

        return np.array(
            angles,
            dtype=np.float32
        )

    # ========================================================
    # V4 - FINGER STRAIGHTNESS
    # ========================================================

    def calculate_finger_straightness(self, hand):

        if hand is None:
            return np.zeros(5, dtype=np.float32)

        fingers = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16],
            [17, 18, 19, 20]
        ]

        values = []

        for finger in fingers:

            direct_distance = self.calculate_distance(
                hand[finger[0]],
                hand[finger[-1]]
            )

            path_length = 0.0

            for i in range(len(finger) - 1):

                path_length += self.calculate_distance(
                    hand[finger[i]],
                    hand[finger[i + 1]]
                )

            ratio = direct_distance / max(
                path_length,
                self.epsilon
            )

            values.append(ratio)

        return np.array(
            values,
            dtype=np.float32
        )

    # ========================================================
    # V4 - FINGERTIP DIRECTION
    # ========================================================

    def calculate_fingertip_direction(self, hand):

        if hand is None:
            return np.zeros(5, dtype=np.float32)

        finger_pairs = [
            (2, 4),
            (6, 8),
            (10, 12),
            (14, 16),
            (18, 20)
        ]

        wrist = np.array(
            hand[0],
            dtype=np.float32
        )

        directions = []

        for base_idx, tip_idx in finger_pairs:

            finger_vector = (
                np.array(
                    hand[tip_idx],
                    dtype=np.float32
                )
                -
                np.array(
                    hand[base_idx],
                    dtype=np.float32
                )
            )

            palm_vector = (
                np.array(
                    hand[base_idx],
                    dtype=np.float32
                )
                - wrist
            )

            norm1 = np.linalg.norm(
                finger_vector
            )

            norm2 = np.linalg.norm(
                palm_vector
            )

            if (
                norm1 < self.epsilon
                or norm2 < self.epsilon
            ):
                directions.append(0.0)
                continue

            cosine = np.dot(
                finger_vector,
                palm_vector
            ) / (
                norm1 * norm2
            )

            cosine = np.clip(
                cosine,
                -1.0,
                1.0
            )

            directions.append(
                float(
                    np.degrees(
                        np.arccos(cosine)
                    )
                )
            )

        return np.array(
            directions,
            dtype=np.float32
        )

    # ========================================================
    # V4 - FINGER SPREAD RATIOS
    # ========================================================

    def calculate_finger_spread_ratios(self, hand):

        if hand is None:
            return np.zeros(4, dtype=np.float32)

        fingertips = [
            hand[4],
            hand[8],
            hand[12],
            hand[16],
            hand[20]
        ]

        palm_scale = self.calculate_distance(
            hand[5],
            hand[17]
        )

        palm_scale = max(
            palm_scale,
            self.epsilon
        )

        spreads = [

            self.calculate_distance(
                fingertips[0],
                fingertips[1]
            ) / palm_scale,

            self.calculate_distance(
                fingertips[1],
                fingertips[2]
            ) / palm_scale,

            self.calculate_distance(
                fingertips[2],
                fingertips[3]
            ) / palm_scale,

            self.calculate_distance(
                fingertips[3],
                fingertips[4]
            ) / palm_scale
        ]

        return np.array(
            spreads,
            dtype=np.float32
        )

    # ========================================================
    # V4 - HAND FEATURES
    # ========================================================

    def calculate_v4_hand_features(self, hand):

        if hand is None:
            return np.zeros(24, dtype=np.float32)

        features = np.concatenate([

            self.calculate_additional_joint_angles(
                hand
            ),

            self.calculate_finger_straightness(
                hand
            ),

            self.calculate_fingertip_direction(
                hand
            ),

            self.calculate_finger_spread_ratios(
                hand
            )
        ])

        assert len(features) == 24

        return features.astype(
            np.float32
        )

    # ========================================================
    # V3 COMPLETE HAND FEATURES
    # ========================================================

    def extract_hand_features(self, normalized_hand):

        if normalized_hand is None:
            return np.zeros(
                139,
                dtype=np.float32
            )

        landmark_features = (
            normalized_hand.flatten()
        )

        assert len(
            landmark_features
        ) == 63

        angle_features = (
            self.calculate_finger_angles(
                normalized_hand
            )
        )

        distance_features = (
            self.calculate_distance_features(
                normalized_hand
            )
        )

        orientation_features = (
            self.calculate_palm_orientation(
                normalized_hand
            )
        )

        segment_length_features = (
            self.calculate_finger_segment_lengths(
                normalized_hand
            )
        )

        v3_features = np.concatenate([

            self.calculate_wrist_fingertip_distances(
                normalized_hand
            ),

            self.calculate_adjacent_fingertip_distances(
                normalized_hand
            ),

            self.calculate_fingertip_palm_distances(
                normalized_hand
            ),

            self.calculate_total_finger_lengths(
                normalized_hand
            ),

            self.calculate_finger_length_ratios(
                normalized_hand
            )
        ])

        assert len(v3_features) == 23

        v4_features = (
            self.calculate_v4_hand_features(
                normalized_hand
            )
        )

        assert len(v4_features) == 24

        features = np.concatenate([

            landmark_features,
            angle_features,
            distance_features,
            orientation_features,
            segment_length_features,
            v3_features,
            v4_features
        ])

        # 63 + 5 + 6 + 3 + 15 + 23 + 24
        # = 139

        assert len(features) == 139

        return features.astype(
            np.float32
        )

    # ========================================================
    # V4 - INTER-HAND FEATURES
    # ========================================================

    def calculate_inter_hand_features(
        self,
        left_raw,
        right_raw
    ):

        if (
            left_raw is None
            or right_raw is None
        ):
            return np.zeros(
                10,
                dtype=np.float32
            )

        left = np.array(
            left_raw,
            dtype=np.float32
        )

        right = np.array(
            right_raw,
            dtype=np.float32
        )

        left_wrist = left[0]
        right_wrist = right[0]

        left_scale = np.linalg.norm(
            left[9] - left[0]
        )

        right_scale = np.linalg.norm(
            right[9] - right[0]
        )

        if (
            left_scale < self.epsilon
            or right_scale < self.epsilon
        ):
            return np.zeros(
                10,
                dtype=np.float32
            )

        average_scale = (
            left_scale + right_scale
        ) / 2.0

        # ----------------------------------------------------
        # Existing V3 wrist relationship
        # ----------------------------------------------------

        relative = (
            right_wrist - left_wrist
        )

        relative_normalized = (
            relative / average_scale
        )

        wrist_distance = (
            np.linalg.norm(relative)
            / average_scale
        )

        features = [

            wrist_distance,

            relative_normalized[0],
            relative_normalized[1],
            relative_normalized[2]
        ]

        # ----------------------------------------------------
        # V4 - corresponding fingertip distances
        # ----------------------------------------------------

        left_tips = [
            left[4],
            left[8],
            left[12],
            left[16],
            left[20]
        ]

        right_tips = [
            right[4],
            right[8],
            right[12],
            right[16],
            right[20]
        ]

        for left_tip, right_tip in zip(
            left_tips,
            right_tips
        ):

            distance = (
                np.linalg.norm(
                    left_tip - right_tip
                )
                / average_scale
            )

            features.append(
                float(distance)
            )

        # ----------------------------------------------------
        # V4 - palm-center distance
        # ----------------------------------------------------

        left_palm_center = (
            left[0]
            + left[5]
            + left[9]
            + left[17]
        ) / 4.0

        right_palm_center = (
            right[0]
            + right[5]
            + right[9]
            + right[17]
        ) / 4.0

        palm_distance = (
            np.linalg.norm(
                right_palm_center
                - left_palm_center
            )
            / average_scale
        )

        features.append(
            float(palm_distance)
        )

        features = np.array(
            features,
            dtype=np.float32
        )

        assert len(features) == 10

        return features

    # ========================================================
    # COMPLETE V4 FEATURE VECTOR
    # ========================================================

    def extract(self, processed_hands):

        left = processed_hands[
            "left_hand"
        ]

        right = processed_hands[
            "right_hand"
        ]

        # ----------------------------------------------------
        # Left hand
        # ----------------------------------------------------

        left_features = (
            self.extract_hand_features(
                left["normalized"]
            )
        )

        # ----------------------------------------------------
        # Right hand
        # ----------------------------------------------------

        right_features = (
            self.extract_hand_features(
                right["normalized"]
            )
        )

        # ----------------------------------------------------
        # Inter-hand
        # ----------------------------------------------------

        inter_hand_features = (
            self.calculate_inter_hand_features(
                left["raw"],
                right["raw"]
            )
        )

        # ----------------------------------------------------
        # Combine
        # ----------------------------------------------------

        complete_features = np.concatenate([

            left_features,
            right_features,
            inter_hand_features
        ])

        # 139 + 139 + 10
        # = 288

        assert len(
            complete_features
        ) == 288

        return complete_features.astype(
            np.float32
        )