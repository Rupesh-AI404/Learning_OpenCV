# take input from user for the image using file handling and asking them what to make line, circle, rectangle or adding text on the image 
# also taking input of p1 oint and p2 point for line, rectangle and circle and at last asking for whether to save the image or not


import cv2

image = None

while True:
    if image is None:
        image_path = input("Enter the path of the image file: ")
        image = cv2.imread(image_path)
        if image is None:
            print("Could not read the image. Please try again.")
            continue
    
    print("Choose an option to edit the image:")
    print("1. Draw Line")
    print("2. Draw Circle")
    print("3. Draw Rectangle")
    print("4. Add Text")
    print("5. Exit")

    try:
        choice = int(input("Enter your choice (1-5): "))
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")
        continue

    if choice == 1:
        x1 = int(input("Enter x1 coordinate of the line: "))
        y1 = int(input("Enter y1 coordinate of the line: "))
        x2 = int(input("Enter x2 coordinate of the line: "))    
        y2 = int(input("Enter y2 coordinate of the line: "))
        color = (255, 0, 0)  # Blue color in BGR 
        thickness = 2

        cv2.line(image, (x1, y1), (x2, y2), color, thickness)

    elif choice == 2:
        center = input("Enter center coordinates of the circle (x,y): ")
        radius = int(input("Enter radius of the circle: "))
        x, y = map(int, center.split(','))
        color = (0, 255, 0)  # Green color in BGR
        thickness = 2

        cv2.circle(image, (x, y), radius, color, thickness)

    elif choice == 3:
        x1 = int(input("Enter x1 coordinate of the rectangle: "))
        y1 = int(input("Enter y1 coordinate of the rectangle: "))
        x2 = int(input("Enter x2 coordinate of the rectangle: "))
        y2 = int(input("Enter y2 coordinate of the rectangle: "))
        color = (0, 0, 255)  # Red color in BGR
        thickness = 2

        cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

    elif choice == 4:
        text = input("Enter the text to add: ")
        x = int(input("Enter x coordinate for the text: "))
        y = int(input("Enter y coordinate for the text: "))
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (255, 255, 255)  # White color in BGR
        thickness = 2

        cv2.putText(image, text, (x, y), font, font_scale, color, thickness)
    
    elif choice == 5:
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please select a valid option.")
        continue

    cv2.imshow("Edited Image", image)
    cv2.waitKey(0)  
    cv2.destroyAllWindows()

    save_choice = input("Do you want to save the edited image? (yes/no): ").strip().lower()
    if save_choice == 'yes':
        save_path = input("Enter the path to save the edited image (including filename and extension): ")
        cv2.imwrite(save_path, image)
        print(f"Image saved at {save_path}")
    else:
        print("Image not saved.")






