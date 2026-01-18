import cv2

image = cv2.imread("school.jpg")

if image is not None:
    h, w, c = image.shape
    print(f"Height: {h}, Width: {w}, Channels: {c}")
else:
    print("Error loading image")
    