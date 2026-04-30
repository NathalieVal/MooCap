import cv2
import time
import mediapipe as mp

from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions


# 1) Camera input

cap = cv2.VideoCapture(5)

if not cap.isOpened():
    raise RuntimeError("Could not start webcam")

previous_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    #FPS 
    current_time = time.time()
    fps = 1/ (current_time - previous_time) if previous_time != 0 else 0
    previous_time = current_time

    cv2.imshow("Webcam Test", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

# What do I need for motion capture?
# 2) Camera frames into MediaPipe
# 3) MediaPipe pose/ face/ hand tracking model running at same time (keep it to one for now)
# 4) Print MediaPipe landmarkers