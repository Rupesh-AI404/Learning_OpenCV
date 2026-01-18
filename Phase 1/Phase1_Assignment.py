# loading image
# Grayscale
# showing
# saving

import cv2

image_location = input("Enter image location: ")
image = cv2.imread(image_location)

if image is not None:
    grayscale = cv2.cutColor(image, cv2.COLOR_BGR2GRAY)

    wannaSaveGrayscale = input("Do you want to save the grayscale image? (yes/no): ").strip().lower()
    if wannaSaveGrayscale == 'yes':
        save_location = input("Enter location to save grayscale image: ")
        cv2.imwrite(save_location, grayscale)
        print("Grayscale image saved successfully.")
    else:
        print("Grayscale image not saved.")
        cv2.imshow("Grayscale Image", grayscale)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
else:
    print("Error loading image")