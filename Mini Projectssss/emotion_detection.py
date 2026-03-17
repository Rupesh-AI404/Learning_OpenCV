# Install once (run in terminal / cmd)
# pip install opencv-python deepface

import cv2
from deepface import DeepFace

# ────────────────────────────────────────────────
# Real-time webcam emotion detection
# ────────────────────────────────────────────────

cap = cv2.VideoCapture(0)  # 0 = default webcam

# Optional: use faster backend detector (YuNet / SSD / YOLO) if you want
# But DeepFace's default (OpenCV or retinaface) works well

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        # Analyze emotion (and optionally age/gender/race)
        result = DeepFace.analyze(
            frame,
            actions = ['emotion'],          # can add: 'age', 'gender', 'race'
            enforce_detection = False,      # don't crash if no face
            detector_backend = 'opencv'     # fastest: 'opencv' | better: 'retinaface', 'yunet'
        )

        for face in result:
            # face['region'] has x,y,w,h
            x, y, w, h = face['region']['x'], face['region']['y'], \
                         face['region']['w'], face['region']['h']

            # Dominant emotion + confidence
            emotion = face['dominant_emotion']
            score = face['emotion'][emotion]   # percentage

            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Put text above box
            label = f"{emotion} ({score:.0f}%)"
            cv2.putText(frame, label, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    except Exception as e:
        # If no face or error → just skip
        pass

    cv2.imshow("Emotion Detection - Press Q to quit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()