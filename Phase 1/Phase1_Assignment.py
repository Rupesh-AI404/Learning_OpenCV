# loading image
# Grayscale
# showing
# saving

import cv2

image_location = input("Enter image location: ")
image = cv2.imread(image_location)

if image is not None:
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    action_order = input("Do you want to save or show first? (save/show): ").strip().lower()

    if action_order == 'save':
        # Save first
        save_location = input("Enter location to save grayscale image: ")
        cv2.imwrite(save_location, grayscale)
        print("Grayscale image saved successfully.")

        # Show second
        cv2.imshow("Grayscale Image", grayscale)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        # Show first
        cv2.imshow("Grayscale Image", grayscale)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Save second
        save_location = input("Enter location to save grayscale image: ")
        cv2.imwrite(save_location, grayscale)
        print("Grayscale image saved successfully.")
else:
    print("Error loading image")