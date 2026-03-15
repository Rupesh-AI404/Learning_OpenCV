import cv2
import mediapipe as mp
import numpy as np
import os
import urllib.request

# ─── Download the hand landmarker model if it doesn't exist ───
model_url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
model_path = "hand_landmarker.task"

if not os.path.exists(model_path):
    print("Downloading hand landmarker model...")
    urllib.request.urlretrieve(model_url, model_path)
    print("Download complete!")

# ─── Initialize MediaPipe Hand module ───
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Configure the hand landmarker with the model file
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)

# Create the hand landmarker
hand_landmarker = vision.HandLandmarker.create_from_options(options)

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

# Canvas to draw on (white background)
canvas = np.ones((720, 1280, 3), dtype=np.uint8) * 255

# Colors (BGR format)
colors = {
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'red': (0, 0, 255),
    'yellow': (0, 255, 255),
    'black': (0, 0, 0)  # for eraser kind of effect
}
current_color = 'blue'
brush_thickness = 8

# To smooth drawing → store last few positions
prev_x, prev_y = 0, 0
drawing = False

# For calculating FPS or timing
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip horizontally so it feels like mirror
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    frame_count += 1

    # Convert to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert to MediaPipe Image format
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Process the frame (use frame_count as timestamp for video mode)
    detection_result = hand_landmarker.detect_for_video(mp_image, frame_count)

    if detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:
            # Get index finger tip (landmark 8) and thumb tip (landmark 4)
            index_tip = hand_landmarks[8]
            thumb_tip = hand_landmarks[5]

            # Convert to pixel coordinates
            ix = int(index_tip.x * w)
            iy = int(index_tip.y * h)
            tx = int(thumb_tip.x * w)
            ty = int(thumb_tip.y * h)


            # Calculate distance between thumb and index
            distance = np.sqrt((ix - tx) ** 2 + (iy - ty) ** 2)

            # ─── Gesture logic ───
            if distance > 50:  # fingers apart → DRAW
                drawing = True
                if prev_x != 0 and prev_y != 0:
                    cv2.line(canvas, (prev_x, prev_y), (ix, iy),
                             colors[current_color], brush_thickness)
                prev_x, prev_y = ix, iy
            else:  # thumb + index close → ERASE / STOP
                drawing = False
                prev_x, prev_y = 0, 0  # reset to avoid random lines

            # Show a circle at finger tip for feedback
            cv2.circle(frame, (ix, iy), 12, colors[current_color], -1)

    # Merge canvas with camera feed (so you see yourself + drawing)
    output = cv2.addWeighted(frame, 0.6, canvas, 0.9, 0)

    # ─── Simple UI controls ───
    cv2.rectangle(output, (10, 10), (150, 60), (200, 200, 200), -1)
    cv2.putText(output, f"Color: {current_color}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.putText(output, "Press 1=blue 2=green 3=red 4=yellow 5=black  e=clear  q=quit",
                (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    cv2.imshow("Air Canvas - You + Drawing", output)

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
        current_color = 'black'  # acts like thick eraser if you want
    elif key == ord('e'):  # full clear
        canvas = np.ones((720, 1280, 3), dtype=np.uint8) * 255

# Clean up
hand_landmarker.close()
cap.release()
cv2.destroyAllWindows()