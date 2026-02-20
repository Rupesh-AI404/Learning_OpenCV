import cv2

image = cv2.imread("school.jpg")

if image is not None:
    success = cv2.imwrite("new_school.jpg", image)
    if success:
        print("Image saved successfully")
    else:
        print("Error saving image")
else:
    print("Error loading image...")