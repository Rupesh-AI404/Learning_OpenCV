import cv2

image = cv2.imread("school.jpg")

if image is not None:
    cv2.imshow("school picture", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("could not load image")