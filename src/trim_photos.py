import os 

import mediapipe as mp
import cv2
import matplotlib.pyplot as plt

data = "./data"

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

for dir_ in os.listdir(data):
    for file in os.listdir(os.path.join(data, dir_))[:1]:
        img = cv2.imread(os.path.join(data, dir_, file))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    img_rgb, 
                    hand_landmarks, # models the output
                    mp_hands.HAND_CONNECTIONS, 
                    mp_drawing_styles.get_default_hand_landmarks_style(), 
                    mp_drawing_styles.get_default_hand_connections_style()
                    )
        plt.figure()
        plt.imshow(img_rgb)

plt.show()
