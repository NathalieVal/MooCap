import cv2
import mediapipe as mp


# What do I need for motion capture?
# 1) Camera input
# 2) Camera frames into MediaPipe
# 3) MediaPipe pose/ face/ hand tracking model running at same time (keep it to one for now)
# 4) Print MediaPipe landmarkers