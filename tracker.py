import cv2
import time
import mediapipe as mp

from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions


# 1) Camera input
class Camera:
    def __init__(self, idx=0, width=None, height=None):
        self.cap = cv2.VideoCapture(idx)
        if not self.cap.isOpened():
            raise RuntimeError("Could not start webcam")
        
        if width:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

        if height:
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


        
    def read(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

class PoseTracker:
    def __init__(self, model_path):
        self.options = vision.PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=vision.RunningMode.VIDEO
        )

        self.landmarker = vision.PoseLandmarker.create_from_options(self.options)

    def process(self, frame, timestamp_ms):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = self.landmarker.detect_for_video(mp_image, timestamp_ms)
        return result

        
cam = Camera(idx=5, width=1280, height=720)

previous_time = time.time()

tracker = PoseTracker("pose_landmarker_full.task")

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