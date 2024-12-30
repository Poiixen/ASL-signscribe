import cv2
import mediapipe as mp 
import pickle
import numpy as np

cam = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

model_dictionary = pickle.load(open("./model.p", "rb"))
model = model_dictionary["model"]

labls_dict = {
0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J", 10: "K", 11: "L", 12: "M", 13: "N", 14: "O", 15: "P", 16: "Q", 17: "R", 18: "S", 19: "T", 20: "U", 21: "V", 22: "W", 23: "X", 24: "Y", 25: "Z",
}


while True:

    data_aux = []
    ret, frame = cam.read()
    
    x_ = []
    y_ = []

    Height, Width, _ = frame.shape

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(img_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()    
            )
        for hand_landmarks in results.multi_hand_landmarks:
            for point in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[point].x
                y = hand_landmarks.landmark[point].y
                x_.append(x)
                y_.append(y)
            
            for point in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[point].x
                y = hand_landmarks.landmark[point].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))
        
        x1 = int(min(x_) * Width) - 10
        y1 = int(min(y_) * Height) - 10

        x2 = int(max(x_) * Width) - 10
        y2 = int(max(y_) * Height) - 10

    
        pred = model.predict([np.asarray(data_aux)])
        predicted_label = labls_dict[int(pred[0])]

        cv2. rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
        cv2.putText(frame, predicted_label, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

    cv2.imshow("frame", frame)
    cv2.waitKey(1)

cam.release()
cv2.destroyAllWindows()
