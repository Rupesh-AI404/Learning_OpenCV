import cv2

image = cv2.imread("school.jpg")

if image is None:
    print("Error loading image")
else:
    print("Image loaded successfully")
    (h, w) = image.shape[:2]  # :2 takes the first two elements of the tuple

    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, 45, 1)
    rotated_image = cv2.warpAffine(image, M, (w, h))

    cv2.imshow("Original Image", image)
    cv2.imshow("Rotated Image", rotated_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()