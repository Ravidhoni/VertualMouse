import pyautogui
import time
import json


CONFIG_FILE = "settings.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # If config file does not exist, create one with default values
        default_config = {
            "cursor_sensitivity": 1.0,
            "scroll_delay": 0.5,
            "scroll_amount": 120,
            "zoom_amount": 50
        }
        save_config(default_config)
        return default_config

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)
config = load_config()
class Controller:
    prev_hand = None
    right_clicked = False
    left_clicked = False
    double_clicked = False
    dragging = False
    hand_Landmarks = None
    little_finger_down = None
    little_finger_up = None
    index_finger_down = None
    index_finger_up = None
    middle_finger_down = None
    middle_finger_up = None
    ring_finger_down = None
    ring_finger_up = None
    Thump_finger_down = None
    Thump_finger_up = None
    all_fingers_down = None
    all_fingers_up = None
    index_finger_within_Thumb_finger = None
    middle_finger_within_Thumb_finger = None
    little_finger_within_Thumb_finger = None
    ring_finger_within_Thumb_finger = None
    screen_width, screen_height = pyautogui.size()

    config = load_config()
    cursor_sensitivity = config["cursor_sensitivity"]
    scroll_delay = config["scroll_delay"]
    scroll_amount = config["scroll_amount"]
    zoom_amount = config["zoom_amount"]

    # Method to update the status of the fingers based on landmarks
    @staticmethod
    def update_fingers_status():
        Controller.little_finger_down = Controller.hand_Landmarks.landmark[20].y > Controller.hand_Landmarks.landmark[17].y
        Controller.little_finger_up = Controller.hand_Landmarks.landmark[20].y < Controller.hand_Landmarks.landmark[17].y
        Controller.index_finger_down = Controller.hand_Landmarks.landmark[8].y > Controller.hand_Landmarks.landmark[5].y
        Controller.index_finger_up = Controller.hand_Landmarks.landmark[8].y < Controller.hand_Landmarks.landmark[5].y
        Controller.middle_finger_down = Controller.hand_Landmarks.landmark[12].y > Controller.hand_Landmarks.landmark[9].y
        Controller.middle_finger_up = Controller.hand_Landmarks.landmark[12].y < Controller.hand_Landmarks.landmark[9].y
        Controller.ring_finger_down = Controller.hand_Landmarks.landmark[16].y > Controller.hand_Landmarks.landmark[13].y
        Controller.ring_finger_up = Controller.hand_Landmarks.landmark[16].y < Controller.hand_Landmarks.landmark[13].y
        Controller.thumb_finger_down = Controller.hand_Landmarks.landmark[4].y > Controller.hand_Landmarks.landmark[13].y
        Controller.thumb_finger_up = Controller.hand_Landmarks.landmark[4].y < Controller.hand_Landmarks.landmark[13].y
        Controller.all_fingers_down = (Controller.index_finger_down and Controller.middle_finger_down and
                                       Controller.ring_finger_down and Controller.little_finger_down)
        Controller.all_fingers_up = (Controller.index_finger_up and Controller.middle_finger_up and
                                     Controller.ring_finger_up and Controller.little_finger_up)
        Controller.index_finger_within_thumb_finger = (Controller.hand_Landmarks.landmark[8].y > Controller.hand_Landmarks.landmark[4].y and
                                                      Controller.hand_Landmarks.landmark[8].y < Controller.hand_Landmarks.landmark[2].y)
        Controller.middle_finger_within_thumb_finger = (Controller.hand_Landmarks.landmark[12].y > Controller.hand_Landmarks.landmark[4].y and
                                                       Controller.hand_Landmarks.landmark[12].y < Controller.hand_Landmarks.landmark[2].y)
        Controller.little_finger_within_thumb_finger = (Controller.hand_Landmarks.landmark[20].y > Controller.hand_Landmarks.landmark[4].y and
                                                       Controller.hand_Landmarks.landmark[20].y < Controller.hand_Landmarks.landmark[2].y)
        Controller.ring_finger_within_thumb_finger = (Controller.hand_Landmarks.landmark[16].y > Controller.hand_Landmarks.landmark[4].y and
                                                     Controller.hand_Landmarks.landmark[16].y < Controller.hand_Landmarks.landmark[2].y)

    # Method to calculate the cursor position based on hand position
    @staticmethod
    def get_position(hand_x_position, hand_y_position):
        old_x, old_y = pyautogui.position()
        current_x = int(hand_x_position * Controller.screen_width)
        current_y = int(hand_y_position * Controller.screen_height)

        ratio = 1
        Controller.prev_hand = (current_x, current_y) if Controller.prev_hand is None else Controller.prev_hand
        delta_x = current_x - Controller.prev_hand[0]
        delta_y = current_y - Controller.prev_hand[1]

        Controller.prev_hand = [current_x, current_y]
        current_x, current_y = old_x + delta_x * ratio, old_y + delta_y * ratio

        threshold = 5
        if current_x < threshold:
            current_x = threshold
        elif current_x > Controller.screen_width - threshold:
            current_x = Controller.screen_width - threshold
        if current_y < threshold:
            current_y = threshold
        elif current_y > Controller.screen_height - threshold:
            current_y = Controller.screen_height - threshold

        return (current_x, current_y)

    # Method to move the cursor based on hand landmarks
    @staticmethod
    def cursor_moving():
        point = 9
        current_x, current_y = Controller.hand_Landmarks.landmark[point].x, Controller.hand_Landmarks.landmark[point].y
        x, y = Controller.get_position(current_x, current_y)
        cursor_freezed = Controller.all_fingers_up and Controller.thumb_finger_down
        if not cursor_freezed:
            pyautogui.moveTo(x, y, duration=0)

    # Method to detect scrolling gestures
    @staticmethod
    def detect_scrolling():
        scrolling_up = (Controller.little_finger_up and Controller.index_finger_down and
                        Controller.middle_finger_down and Controller.ring_finger_down)
        if scrolling_up:
            time.sleep(3)  # Add a delay before scrolling
            pyautogui.scroll(120)
            print("Scrolling UP")

        scrolling_down = (Controller.index_finger_up and Controller.middle_finger_down and
                          Controller.ring_finger_down and Controller.little_finger_down)
        if scrolling_down:
            time.sleep(3)  # Add a delay before scrolling
            pyautogui.scroll(-120)
            print("Scrolling DOWN")

    # Method to detect zooming gestures
    @staticmethod
    def detect_zooming():
        zooming = (Controller.index_finger_up and Controller.middle_finger_up and
                   Controller.ring_finger_down and Controller.little_finger_down)
        window = 0.05
        index_touches_middle = abs(Controller.hand_Landmarks.landmark[8].x - Controller.hand_Landmarks.landmark[12].x) <= window
        zooming_out = zooming and index_touches_middle
        zooming_in = zooming and not index_touches_middle

        if zooming_out:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(-50)
            pyautogui.keyUp('ctrl')
            print("Zooming Out")

        if zooming_in:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(50)
            pyautogui.keyUp('ctrl')
            print("Zooming In")

    # Method to detect clicking gestures
    @staticmethod
    def detect_clicking():
        left_click_condition = (Controller.index_finger_within_thumb_finger and Controller.middle_finger_up and
                                Controller.ring_finger_up and Controller.little_finger_up and
                                not Controller.middle_finger_within_thumb_finger and
                                not Controller.ring_finger_within_thumb_finger and
                                not Controller.little_finger_within_thumb_finger)
        if not Controller.left_clicked and left_click_condition:
            pyautogui.click()
            Controller.left_clicked = True
            print("Left Clicking")
        elif not Controller.index_finger_within_thumb_finger:
            Controller.left_clicked = False

        right_click_condition = (Controller.middle_finger_within_thumb_finger and Controller.index_finger_up and
                                 Controller.ring_finger_up and Controller.little_finger_up and
                                 not Controller.index_finger_within_thumb_finger and
                                 not Controller.ring_finger_within_thumb_finger and
                                 not Controller.little_finger_within_thumb_finger)
        if not Controller.right_clicked and right_click_condition:
            pyautogui.rightClick()
            Controller.right_clicked = True
            print("Right Clicking")
        elif not Controller.middle_finger_within_thumb_finger:
            Controller.right_clicked = False

        double_click_condition = (Controller.ring_finger_within_thumb_finger and Controller.index_finger_up and
                                  Controller.middle_finger_up and Controller.little_finger_up and
                                  not Controller.index_finger_within_thumb_finger and
                                  not Controller.middle_finger_within_thumb_finger and
                                  not Controller.little_finger_within_thumb_finger)
        if not Controller.double_clicked and double_click_condition:
            pyautogui.doubleClick()
            Controller.double_clicked = True
            print("Double Clicking")
        elif not Controller.ring_finger_within_thumb_finger:
            Controller.double_clicked = False

    # Method to detect dragging gestures
    @staticmethod
    def detect_dragging():
        if not Controller.dragging and Controller.all_fingers_down:
            pyautogui.mouseDown(button="left")
            Controller.dragging = True
            print("Dragging")
        elif not Controller.all_fingers_down:
            pyautogui.mouseUp(button="left")
            Controller.dragging = False
