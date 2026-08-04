import cv2
import numpy as np

# Create a blank black image
img = np.zeros((400, 700, 3), dtype=np.uint8)

cv2.putText(
    img,
    "CG & IP Pipeline OK",
    (20, 20),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 255, 0),
    2
)

# Team details
cv2.putText(img, "Rajal Kher - 24000021", (20, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

cv2.putText(img, "Zainab Shaikh - 24000232", (20, 180),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

cv2.putText(img, "Nandini Singh - 24000322", (20, 260),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect edges
edges = cv2.Canny(gray, 100, 200)

# Display
cv2.imshow("Pipeline Test", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()