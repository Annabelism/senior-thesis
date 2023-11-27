import cv2
import numpy as np

# Load screenshots
img1 = cv2.imread('screenshot1.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('screenshot2.png', cv2.IMREAD_GRAYSCALE)

# Edge detection using Canny
edges1 = cv2.Canny(img1, 100, 200)
edges2 = cv2.Canny(img2, 100, 200)

# Compute the absolute difference
difference = cv2.absdiff(edges1, edges2)

# Threshold the difference image
_, thresholded = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw bounding boxes around differing regions and compute areas
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    area = w * h
    cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw on img1 or img2 as per your preference
    print(f"Detected difference area: {area} pixels^2")

cv2.imshow('Difference areas', img1)
cv2.waitKey(0)
cv2.destroyAllWindows()
