import cv2
import mediapipe as mp 

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

    
    cv2.imshow("frame", frame)
    cv2.waitKey(25)




cam.release()
cv2.destroyAllWindows()
