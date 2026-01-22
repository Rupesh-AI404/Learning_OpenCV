import cv2

image = cv2.imread("school.jpg")

if image is None:
    print("Error loading image")
else:
    print("Image loaded successfully")

    text = "Hello World"
    org = (10, 500)
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 0, 0)
    thickness = 2
    cv2.putText(image, text, org, font, 1, color, thickness)

    cv2.imshow("Image with Text", image)
    cv2.waitKey(0)