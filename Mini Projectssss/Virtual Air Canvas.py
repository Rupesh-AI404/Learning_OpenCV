import cv2
import mediapipe as mp
import numpy as np
from collections import deque

# ─── Initialize MediaPipe Hand module (newer versions) ───
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Rest of your code remains the same...
# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)   # width
cap.set(4, 720)    # height

# Canvas to draw on (white background)
canvas = np.ones((720, 1280, 3), dtype=np.uint8) * 255

# Colors (BGR format)
colors = {
    'blue':   (255, 0, 0),
    'green':  (0, 255, 0),
    'red':    (0, 0, 255),
    'yellow': (0, 255, 255),
    'black':  (0, 0, 0)   # for eraser kind of effect
}
current_color = 'blue'
brush_thickness = 8

# To smooth drawing → store last few positions
prev_x, prev_y = 0, 0
drawing = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip horizontally so it feels like mirror
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks (optional – helps debugging)
            # mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get index finger tip (landmark 8) and thumb tip (landmark 4)
            index_tip = hand_landmarks.landmark[8]
            thumb_tip  = hand_landmarks.landmark[4]

            # Convert to pixel coordinates
            ix = int(index_tip.x * w)
            iy = int(index_tip.y * h)
            tx = int(thumb_tip.x  * w)
            ty = int(thumb_tip.y  * h)

            # Calculate distance between thumb and index
            distance = np.sqrt((ix - tx)**2 + (iy - ty)**2)

            # ─── Gesture logic ───
            if distance > 50:   # fingers apart → DRAW
                drawing = True
                if prev_x != 0 and prev_y != 0:
                    cv2.line(canvas, (prev_x, prev_y), (ix, iy),
                             colors[current_color], brush_thickness)
                prev_x, prev_y = ix, iy
            else:               # thumb + index close → ERASE / STOP
                drawing = False
                prev_x, prev_y = 0, 0   # reset to avoid random lines

            # Show a circle at finger tip for feedback
            cv2.circle(frame, (ix, iy), 12, colors[current_color], -1)

    # Merge canvas with camera feed (so you see yourself + drawing)
    output = cv2.addWeighted(frame, 0.6, canvas, 0.9, 0)

    # ─── Simple UI controls ───
    cv2.rectangle(output, (10, 10), (150, 60), (200, 200, 200), -1)
    cv2.putText(output, f"Color: {current_color}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)

    cv2.putText(output, "Press 1=blue 2=green 3=red 4=yellow 5=black(c)  q=quit",
                (10, h-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

    cv2.imshow("Air Canvas - You + Drawing", output)
    # cv2.imshow("Canvas only", canvas)   # uncomment if you want separate window

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('1'):
        current_color = 'blue'
    elif key == ord('2'):
        current_color = 'green'
    elif key == ord('3'):
        current_color = 'red'
    elif key == ord('4'):
        current_color = 'yellow'
    elif key == ord('c') or key == ord('5'):
        current_color = 'black'   # acts like thick eraser if you want
    elif key == ord('e'):         # full clear
        canvas = np.ones((720, 1280, 3), dtype=np.uint8) * 255

cap.release()
cv2.destroyAllWindows()