import cv2

image = cv2.imread("school.jpg")

print(image.shape)

if image is None:
    print("Error loading image")
else:
    print("Image loaded successfully")