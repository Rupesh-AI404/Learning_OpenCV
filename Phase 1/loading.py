import cv2

image = cv2.imread("school.jpg")

if image is not None:
    print("Error loading image")
else:
    print("Image loaded successfully")