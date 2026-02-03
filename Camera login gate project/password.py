import cv2
import mediapipe as mp
import time

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
mp_image = mp.Image
reset = True
numbers = []
fingers = 0
wait_time = 0
super_old_fingers = 0
password = [1, 2, 3, 4, 5, 6]
set_password = False


def num(hand_landmarks):
    if not hand_landmarks or len(hand_landmarks) == 0:
        return False
    landmarks = hand_landmarks[0]
    num = 0
    for hand_index, landmarks in enumerate(results.hand_landmarks):
        if landmarks[8].y < landmarks[5].y:
            num += 1
        if landmarks[12].y < landmarks[9].y:
            num += 1
        if landmarks[16].y < landmarks[13].y:
            num += 1
        if landmarks[20].y < landmarks[17].y:
            num += 1
        if landmarks[4].x < landmarks[17].x:
            if landmarks[4].x < landmarks[3].x:
                num += 1
        elif landmarks[4].x > landmarks[17].x:
            if landmarks[4].x > landmarks[3].x:
                num += 1
    return num

# Use VIDEO mode - no callback required
model_path = 'hand_landmarker.task'
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,  # Changed from LIVE_STREAM
    num_hands=2,
    min_hand_detection_confidence=0.7
)

cap = cv2.VideoCapture(0)
with HandLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_frame = mp_image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Process synchronously - works perfectly for webcam
        timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))
        results = landmarker.detect_for_video(mp_frame, timestamp_ms)
        
        if results.hand_landmarks:
            h, w, _ = frame.shape
            # Draw landmarks
            for hand_index, landmarks in enumerate(results.hand_landmarks):
                for landmarks in results.hand_landmarks:
                    for lm in landmarks:
                        x, y = int(lm.x * w), int(lm.y * h)
                        cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)
                    
                    
                    old_fingers = fingers
                    fingers = num(results.hand_landmarks)
                    if fingers == 0:
                        reset = True
                        cv2.putText(frame, "-", (280, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                    if fingers != old_fingers:
                        if fingers == 10:
                            wait_time = time.time() + 1
                        else:
                            wait_time = time.time() + 0.5
                    if (time.time() >= wait_time and fingers > 0 and fingers == old_fingers and reset == True and fingers < 10) or (fingers == super_old_fingers and fingers > 0 and reset == False and fingers < 10):
                        if reset:
                            numbers.append(fingers)
                            super_old_fingers = fingers
                        reset = False
                        cv2.putText(frame, str(fingers), (280, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                    elif fingers > 0 and fingers < 10 or reset == False and fingers < 10:
                        cv2.putText(frame, str(fingers), (280, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                    elif (time.time() >= wait_time and fingers == old_fingers and reset == True and fingers == 10) or (fingers == super_old_fingers and reset == False and fingers == 10):
                        if reset:
                            if numbers == []:
                                set_password = True
                            else:
                                numbers = []
                                super_old_fingers = fingers
                        reset = False
                        cv2.putText(frame, "!", (280, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
                    elif reset == False and fingers == 10 or fingers == 10:
                        cv2.putText(frame, "!", (280, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        if numbers == password or set_password == True:
            cv2.putText(frame, str(numbers), (30, 75), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(frame, str(numbers), (30, 75), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
        if len(numbers) == 6 and set_password == True:
            password = numbers
            set_password = False
        if len(numbers) > 6:
            numbers = []
            
        cv2.imshow(f"Password detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
