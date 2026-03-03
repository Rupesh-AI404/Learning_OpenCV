import cv2

image = cv2.imread("school.jpg")

if image is None:
    print("Error loading image")
else:
    print("Image loaded successfully")

    resized_image = cv2.resize(image, (500, 600))

    cv2.imshow("Original Image", image)
    cv2.imshow("Resized Image", resized_image)

    cv2.imwrite("resized_school.jpg", resized_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("Image saved successfully")
