import cv2

image = cv2.imread("school.jpg")

if image is None:
    print("Error loading image")
else:
    print("Image loaded successfully")
    center = (200, 200)
    radius = 100
    color = (255, 0, 0)
    thickness = 100
    image = cv2.circle(image, center, radius, color, thickness)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()