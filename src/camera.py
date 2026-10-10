from hand_landmarks import HAND_LANDMARKS
from gestures import calculate_distance, get_finger_direction, GestureTimer
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


enable_landmarks = True
base_options = python.BaseOptions(model_asset_path='models/gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

stream = cv2.VideoCapture(0)
stream.set(3, 720)
stream.set(4,480)


if not stream.isOpened():
    print("no stream ")
    exit()
gesture_timer = GestureTimer(hold_seconds=2.0)
while(stream.isOpened()):
    ret, frame = stream.read()
    if not ret:
        print("no more stream")
        break


    
    
    #convert the BGR frame to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB ,data=rgb_frame)

    recognition_result = recognizer.recognize(mp_image)
    hand_landmarks = recognition_result.hand_landmarks

    detected_gesture = None

    if hand_landmarks:
        height, width, _ = frame.shape

        for hand in hand_landmarks:
            thumb_tip = hand[HAND_LANDMARKS["thumb"]["tip"]]
            index_tip = hand[HAND_LANDMARKS["index"]["tip"]]
            index_mcp = hand[HAND_LANDMARKS["index"]["mcp"]]

            distance = calculate_distance(
                thumb_tip, index_tip, width, height
            )

            direction = get_finger_direction(
                index_mcp, index_tip, width, height
            )

            #print(f"Index direction: {direction}")

            if distance < 10:
                detected_gesture = "PINCH"
                break

    gesture_timer.update(detected_gesture)
    
    # Draw detected hand landmarks
    if hand_landmarks and enable_landmarks:
        height, width, _ = frame.shape

        for hand in hand_landmarks:
            for landmark in hand:
                x = int(landmark.x * width)
                y = int(landmark.y * height)

                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        

    cv2.imshow("usb camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()