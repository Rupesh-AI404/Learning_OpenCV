# using first function from the note

import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read() #ret = True or False   frame = image

    if not ret:
        print("Failed to grab frame.")
        break

    cv2.imshow("Webcam Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):    #113 == 113 TRUE
        print("Exiting...")
        break


cap.release()
cv2.destroyAllWindows()