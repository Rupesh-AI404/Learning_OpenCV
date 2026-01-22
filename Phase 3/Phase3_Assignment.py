import cv2

image = None

while True:
    if image is None:
        img_add = input("Enter the address of the image (or 'q' to quit): ")
        if img_add.lower() == 'q':
            break
        image = cv2.imread(img_add)
        if image is None:
            print("Error: Could not read the image. Please try again.")
            continue

    print('''
    1. Create shapes/text
    2. View output
    3. Save image
    4. Exit
    ''')

    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number from the menu.")
        continue

    match choice:
        case 1:
            print('''
            1. Line
            2. Rectangle
            3. Circle
            4. Text
            5. Back
            ''')
            try:
                inner_choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue

            match inner_choice:
                case 1:
                    try:
                        pt1_str = input("Enter pt1 in (x,y) format: ")
                        pt2_str = input("Enter pt2 in (x,y) format: ")
                        x1, y1 = map(int, pt1_str.strip('()').split(','))
                        x2, y2 = map(int, pt2_str.strip('()').split(','))
                        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
                        print("Line drawn successfully.")
                    except (ValueError, IndexError):
                        print("Invalid point format. Please use '(x,y)'.")
                case 2:
                    try:
                        pt1_str = input("Enter pt1 in (x,y) format: ")
                        pt2_str = input("Enter pt2 in (x,y) format: ")
                        x1, y1 = map(int, pt1_str.strip('()').split(','))
                        x2, y2 = map(int, pt2_str.strip('()').split(','))
                        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        print("Rectangle drawn successfully.")
                    except (ValueError, IndexError):
                        print("Invalid point format. Please use '(x,y)'.")
                case 3:
                    try:
                        pt1_str = input("Enter center pt in (x,y) format: ")
                        radius = int(input("Enter radius: "))
                        x, y = map(int, pt1_str.strip('()').split(','))
                        cv2.circle(image, (x, y), radius, (0, 255, 255), 2)
                        print("Circle drawn successfully.")
                    except (ValueError, IndexError):
                        print("Invalid input. Please use '(x,y)' for the point and a number for the radius.")
                case 4:
                    try:
                        text_to_add = input("Enter the text: ")
                        pt1_str = input("Enter starting pt in (x,y) format: ")
                        x, y = map(int, pt1_str.strip('()').split(','))
                        cv2.putText(image, text_to_add, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                        print("Text added successfully.")
                    except (ValueError, IndexError):
                        print("Invalid point format. Please use '(x,y)'.")
                case 5:
                    print("Going back to main menu.")
                case _:
                    print("Invalid choice. Returning to main menu.")
        case 2:
            if image is None:
                print("No image loaded to display.")
            else:
                cv2.imshow("Image", image)
                print("Press any key to close the image window...")
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        case 3:
            if image is None:
                print("No image loaded to save.")
            else:
                save_name = input("Enter the filename to save the image (e.g., my_image.png): ")
                cv2.imwrite(save_name, image)
                print(f"Image saved as '{save_name}'.")
        case 4:
            print("Exiting...")
            break
        case _:
            print("Invalid choice. Please enter a number from the menu.")