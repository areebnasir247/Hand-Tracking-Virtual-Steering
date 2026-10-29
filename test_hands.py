"""
Virtual Steering Wheel - Step 2: Hand Tracking & Steering Angle Test (Enhanced Sensitivity)
Features:
- Video-stream temporal tracking (smooth, no flickering)
- Lowered confidence threshold (detects angled & gripped hands)
- Labeled hand tags ("Left Hand" / "Right Hand")
- Visual steering wheel HUD & angle calculation
"""

import cv2
import math
import time
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 1. Setup MediaPipe Hand Landmarker with VIDEO mode for temporal continuity
MODEL_PATH = "hand_landmarker.task"

base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.25,  # Lowered from 0.5 to catch hands at an angle
    min_hand_presence_confidence=0.25,   # Keeps tracking even if fingers are partially curled
    min_tracking_confidence=0.25
)
detector = vision.HandLandmarker.create_from_options(options)

# 2. Hand connections for drawing skeleton
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index
    (5, 9), (9, 10), (10, 11), (11, 12),   # Middle
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring
    (13, 17), (17, 18), (18, 19), (19, 20),# Pinky
    (0, 17)                                # Palm base
]

# 3. Parameters
DEAD_ZONE_ANGLE = 10.0   # Degrees: within +/- 10 degrees is considered STRAIGHT
SMOOTHING_ALPHA = 0.3    # Exponential smoothing
smoothed_angle = 0.0

# Webcam setup
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not camera.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("=" * 65)
print("Enhanced Hand Tracking Started!")
print("- Hold BOTH hands up in front of the camera (about chest height).")
print("- Tip: Keep fingers slightly relaxed (not in a tight fist).")
print("- Press 'q' on your keyboard to close.")
print("=" * 65)

prev_time = time.time()
start_time_ms = int(time.time() * 1000)

while camera.isOpened():
    success, frame = camera.read()
    if not success:
        break

    # Flip horizontally for natural mirror preview
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Calculate FPS
    curr_time = time.time()
    fps = 1.0 / max(curr_time - prev_time, 1e-5)
    prev_time = curr_time

    # Timestamp for VIDEO mode
    frame_timestamp_ms = int(time.time() * 1000) - start_time_ms

    # Convert frame to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Detect hands using Video stream mode
    detection_result = detector.detect_for_video(mp_image, frame_timestamp_ms)

    detected_hands = []

    # Process detected hands
    if detection_result.hand_landmarks:
        for hand_landmarks in detection_result.hand_landmarks:
            pixel_landmarks = []
            for lm in hand_landmarks:
                px = int(lm.x * w)
                py = int(lm.y * h)
                pixel_landmarks.append((px, py))

            # Draw bones/connections
            for start_idx, end_idx in HAND_CONNECTIONS:
                cv2.line(frame, pixel_landmarks[start_idx], pixel_landmarks[end_idx], (0, 255, 180), 2)

            # Draw landmark dots
            for px, py in pixel_landmarks:
                cv2.circle(frame, (px, py), 4, (0, 120, 255), -1)

            # Center point of hand
            center_x = (pixel_landmarks[0][0] + pixel_landmarks[9][0]) // 2
            center_y = (pixel_landmarks[0][1] + pixel_landmarks[9][1]) // 2

            detected_hands.append({
                "center": (center_x, center_y),
                "landmarks": pixel_landmarks
            })

    # Sort hands by screen X coordinate: 0 = Screen Left, 1 = Screen Right
    detected_hands.sort(key=lambda h_data: h_data["center"][0])

    # Draw individual hand labels
    for i, h_data in enumerate(detected_hands):
        cx, cy = h_data["center"]
        if len(detected_hands) == 2:
            label = "LEFT HAND" if i == 0 else "RIGHT HAND"
            color = (255, 200, 0) if i == 0 else (0, 200, 255)
        else:
            # Single hand visible: determine by screen half
            label = "LEFT HAND" if cx < (w // 2) else "RIGHT HAND"
            color = (0, 255, 255)

        cv2.circle(frame, (cx, cy), 14, color, -1)
        cv2.putText(frame, label, (cx - 45, cy - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

    # Steering logic if both hands are detected
    if len(detected_hands) == 2:
        left_pos = detected_hands[0]["center"]
        right_pos = detected_hands[1]["center"]

        # Calculate steering angle
        dx = right_pos[0] - left_pos[0]
        dy = right_pos[1] - left_pos[1]

        raw_angle = math.degrees(math.atan2(dy, dx))
        smoothed_angle = (SMOOTHING_ALPHA * raw_angle) + ((1 - SMOOTHING_ALPHA) * smoothed_angle)

        wheel_center = ((left_pos[0] + right_pos[0]) // 2, (left_pos[1] + right_pos[1]) // 2)
        wheel_radius = max(35, int(math.hypot(dx, dy) / 2))

        # Determine steering state
        if smoothed_angle > DEAD_ZONE_ANGLE:
            state = "STEERING RIGHT"
            state_color = (0, 140, 255)  # Orange
        elif smoothed_angle < -DEAD_ZONE_ANGLE:
            state = "STEERING LEFT"
            state_color = (255, 200, 0)  # Cyan
        else:
            state = "STRAIGHT"
            state_color = (0, 255, 0)    # Green

        # Draw steering wheel graphics
        cv2.line(frame, left_pos, right_pos, state_color, 4)
        cv2.circle(frame, wheel_center, wheel_radius, state_color, 2)
        cv2.circle(frame, wheel_center, 8, (255, 255, 255), -1)

        # HUD Text
        cv2.putText(frame, f"Angle: {smoothed_angle:+.1f} deg", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, f"State: {state}", (20, 115),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, state_color, 2)

    elif len(detected_hands) == 1:
        cv2.putText(frame, "Detected 1 hand - raise your other hand!", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 165, 255), 2)
    else:
        cv2.putText(frame, "Hands not detected - raise both hands", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

    # Top banner info
    cv2.rectangle(frame, (0, 0), (w, 45), (30, 30, 30), -1)
    cv2.putText(frame, "Virtual Steering Wheel | Industry 4.0", (15, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    cv2.putText(frame, f"FPS: {int(fps)}", (w - 110, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

    cv2.imshow("Virtual Steering Wheel - Hand & Angle Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
