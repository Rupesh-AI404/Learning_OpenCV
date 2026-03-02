import cv2

image = cv2.imread("school.jpg")

if image is None:
    print("Error loading image")
else:
    print("Image loaded successfully")

    pt1 = (200, 200)
    pt2 = (500, 500)
    color = (255, 0, 0)
    thickness = 5

    cv2.line(image, pt1, pt2, color, thickness)

    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()