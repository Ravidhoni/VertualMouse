import cv2
import mediapipe as mp
from UI import launch_config_ui
import threading
from Controller import Controller

# Initialize webcam
cap = cv2.VideoCapture(0)
# Initialize Mediapipe hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2,
	min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils
def start_hand_traking():
    while True:
        # Capture frame-by-frame
        success, img = cap.read()
        img = cv2.flip(img, 1)  # Flip horizontally for a mirror effect

        # Convert image to RGB format
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the hand landmarks
        results = hands.process(imgRGB)

        # If hand landmarks are detected
        if results.multi_hand_landmarks:
            # Use the first hand landmark (assuming only one hand is present)
            Controller.hand_Landmarks = results.multi_hand_landmarks[0]

            # Draw landmarks and connections on the image
            mpDraw.draw_landmarks(img, Controller.hand_Landmarks, mpHands.HAND_CONNECTIONS)

            # Update finger status and perform actions
            Controller.update_fingers_status()
            Controller.cursor_moving()
            Controller.detect_scrolling()
            Controller.detect_zooming()
            Controller.detect_clicking()
            Controller.detect_dragging()
            #srm.recognize_voice_command(recognizer)

        # Display the resulting image with landmarks
        cv2.imshow('Hand Tracker', img)

        # Break the loop when 'Esc' key is pressed
        key = cv2.waitKey(25)
        if key == 27:
            break
    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
config_thread = threading.Thread(target=launch_config_ui())
config_thread.start()
start_hand_traking()
