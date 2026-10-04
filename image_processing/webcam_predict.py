import cv2

from predict import ISLRecognizer


# ============================================================
# SIGNVERSE - WEBCAM PREDICTION
# ============================================================

recognizer = ISLRecognizer()

camera = cv2.VideoCapture(0)

if not camera.isOpened():

    print("Error: Could not open webcam.")
    recognizer.close()
    raise SystemExit


print()
print("=" * 60)
print("SIGNVERSE - WEBCAM PREDICTION")
print("=" * 60)
print()
print("Show an ISL sign to the camera.")
print("Press Q to quit.")
print()


try:

    while True:

        success, frame = camera.read()

        if not success:

            print("Could not read webcam frame.")
            break

        # ----------------------------------------------------
        # Get prediction from reusable IP module
        # ----------------------------------------------------

        result = recognizer.predict_frame(
            frame
        )

        # ----------------------------------------------------
        # Display prediction
        # ----------------------------------------------------

        if result["success"]:

            prediction_text = (
                f"Sign: {result['prediction']} "
                f"({result['confidence'] * 100:.1f}%)"
            )

            if not result["stable"]:

                prediction_text = (
                    "Stabilizing... "
                    f"{result['prediction']}"
                )

        else:

            prediction_text = result["message"]
        
        # ----------------------------------------------------
        # Hand status
        # ----------------------------------------------------

        hands = result.get(
            "hands_detected",
            {
                "left": False,
                "right": False
            }
        )

        hand_status = (
            f"Left: {'Yes' if hands['left'] else 'No'} | "
            f"Right: {'Yes' if hands['right'] else 'No'}"
        )

        # ----------------------------------------------------
        # Mirror display only
        # ----------------------------------------------------

        display_frame = cv2.flip(
            frame,
            1
        )

        # ----------------------------------------------------
        # Display prediction
        # ----------------------------------------------------

        cv2.putText(
            display_frame,
            prediction_text,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # ----------------------------------------------------
        # Display hand status
        # ----------------------------------------------------

        cv2.putText(
            display_frame,
            hand_status,
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        # ----------------------------------------------------
        # Show webcam
        # ----------------------------------------------------

        cv2.imshow(
            "SignVerse - ISL Recognition",
            display_frame
        )
        # ----------------------------------------------------
        # Quit
        # ----------------------------------------------------

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break


finally:

    camera.release()

    cv2.destroyAllWindows()

    recognizer.close()

    print()
    print("Webcam prediction stopped.")