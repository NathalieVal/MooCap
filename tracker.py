import cv2
import time
import mediapipe as mp
import numpy as np

from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions

# landmark model: https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker

POSE_CONNECTIONS = frozenset([
    (11, 13), (13, 15), # Left arm
    (12, 14), (14, 16), #Right arm
    (11, 12), # Shoulders
    (23, 24), # Hips
    (11, 23), (12, 24), # Torso
    (23, 25), (25, 27), # Left leg
    (24, 26), (26, 28), # Right leg
])


BONES = {
    "upper_arm.L": {11, 13},
    "lower_arm.L": {13, 15},

    "upper_arm.R": {12, 14},
    "lower_arm.R": {14, 16},

    "upper_leg.L": {23, 25},
    "lower_leg.L": {25, 27},

    "upper_leg.R": {24, 26},
    "lower_leg.R": {26, 28},

    "spine": {24, 12}
}


def get_bone_vectors(landmarks):
    bone_vectors = []

    for bone, idx in BONES.items():
        p = landmarks[idx["parent"]]
        c = landmarks[idx["child"]]

        vec = np.array([c.x - p.x, c.y - p.y, c.z - p.z])

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        
        bone_vectors[bone] = vec

    return bone_vectors

def draw_pose(frame, landmarks, visibility_threshold=0.5):
    h, w, _ = frame.shape

    points = []

    for lm in landmarks: 
        if hasattr(lm, "visibility") and lm.visibility < visibility_threshold:
            points.append(None)
        else:
            x = int(lm.x * w)
            y = int(lm.y * h)
            points.append((x, y))

    for pt in points:
        if pt is not None:
            cv2.circle(frame, pt, 4, (0, 255, 0), -1)

    for start_idx, end_idx in POSE_CONNECTIONS:
        if (start_idx < len(points)
            and end_idx < len(points)
            and points[start_idx] is not None
            and points [end_idx] is not None ):
            cv2.line(frame, points[start_idx], points[end_idx], (255, 0, 0), 2)


    return points

def extract_pose_data(landmarks):
    pose_data = []

    for lm in landmarks:
        pose_data.append({
            "x": lm.x,
            "y": lm.y,
            "z": lm.z,
            "visibility": getattr(lm, "visibility", 1.0)
        })

    return pose_data

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

timestamp_ms = 0

while True:
    frame = cam.read()
    if frame is None:
        break

    current_time = time.time()
    fps = 1/ (current_time - previous_time)
    previous_time = current_time

    result = tracker.process(frame, timestamp_ms)
    timestamp_ms += 1

    if result.pose_landmarks:
        landmarks = result.pose_landmarks[0]
        
        points = draw_pose(frame, landmarks)

        pose_data = extract_pose_data(landmarks)

        # for i, lm in enumerate(result.pose_landmarks[0]):
        #     print(i, lm.x, lm.y, lm.z)


    cv2.putText(frame, f"{fps:.2f}", (10, 30),
                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()