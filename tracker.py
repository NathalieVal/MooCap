import cv2
import time
import mediapipe as mp

from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions


# 1) Camera input
class Camera:
    def __init__(self, idx=5):
        self.cap = cv2.VideoCapture(idx)
        if not self.cap.isOpened():
            raise RuntimeError("Could not start webcam")
        
    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

        
cam = Camera()

previous_time = time.time()

while True:
    frame = cam.read()
    if frame is None:
        break

    # FPS calculation
    current_time = time.time()
    fps = 1/ (current_time - previous_time)
    previous_time = current_time

    cv2.putText(frame, f"{fps:.2f}", (10, 30),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()

# What do I need for motion capture?
# 2) Camera frames into MediaPipe
# 3) MediaPipe pose/ face/ hand tracking model running at same time (keep it to one for now)
# 4) Print MediaPipe landmarkers