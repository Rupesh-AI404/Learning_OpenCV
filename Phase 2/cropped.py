import cv2

image = cv2.imread("school.jpg")

if image is not None:
    cropped_image = image[300:400, 100:400]
    cv2.imshow("Original Image", image)
    cv2.imshow("Cropped Image", cropped_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()