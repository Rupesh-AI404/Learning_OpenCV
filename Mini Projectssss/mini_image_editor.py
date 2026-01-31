import cv2

def get_color():
    print("Enter color (B G R)")
    b = int(input("Blue: "))
    g = int(input("Green: "))
    r = int(input("Red: "))
    return (b, g, r)

def get_thickness():
    return int(input("Enter thickness: "))

def show_image(image, title="Mini Image Editor"):
    cv2.imshow(title, image)
    cv2.waitKey(0)


image_path = input("Enter image path: ")
image = cv2.imread(image_path)

if image is None:
    print("Error: Image not found")
    exit()

while True:
    print("\n--- MINI IMAGE EDITOR ---")
    print("1. Draw Line")
    print("2. Draw Rectangle")
    print("3. Draw Circle")
    print("4. Add Text")
    print("5. Save Image")
    print("6. Exit")

    choice = int(input("Enter choice (1-6): "))

    if choice == 1:
        x1 = int(input("x1: "))
        y1 = int(input("y1: "))
        x2 = int(input("x2: "))
        y2 = int(input("y2: "))
        color = get_color()
        thickness = get_thickness()
        cv2.line(image, (x1, y1), (x2, y2), color, thickness)

    elif choice == 2:
        x1 = int(input("x1: "))
        y1 = int(input("y1: "))
        x2 = int(input("x2: "))
        y2 = int(input("y2: "))
        color = get_color()
        thickness = get_thickness()
        cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

    elif choice == 3:
        x = int(input("Center x: "))
        y = int(input("Center y: "))
        r = int(input("Radius: "))
        color = get_color()
        thickness = get_thickness()
        cv2.circle(image, (x, y), r, color, thickness)

    elif choice == 4:
        text = input("Enter text: ")
        x = int(input("x: "))
        y = int(input("y: "))
        color = get_color()
        thickness = get_thickness()
        cv2.putText(
            image, text, (x, y),
            cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness
        )

    elif choice == 5:
        save_path = input("Enter save path (with filename): ")
        cv2.imwrite(save_path, image)
        print("Image saved successfully!")

    elif choice == 6:
        print("Exiting editor...")
        break

    else:
        print("Invalid choice")

    print("--- IMAGE DISPLAY ---")

    show_image(image)
cv2.destroyAllWindows()

