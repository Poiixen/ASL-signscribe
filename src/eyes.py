#a.k.a. app.py

from flask import Flask, render_template, jsonify, request, Response
import cv2
import mediapipe as mp
import pickle
import numpy as np
import base64
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

model_dictionary = pickle.load(open(os.path.join(os.path.dirname(__file__), "../outputs/model.p"), "rb"))
model = model_dictionary["model"]

labls_dict = {
0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J", 
10: "K", 11: "L", 12: "M", 13: "N", 14: "O", 15: "P", 16: "Q", 17: "R", 18: "S", 
19: "T", 20: "U", 21: "V", 22: "W", 23: "X", 24: "Y", 25: "Z",
}

# REMOVE THIS FUNCTION IF YOU ARE PLANNING TO HOST THE APP ON A PUBLIC SERVER
# This function is only used to generate frames for the local webcam stream
def generate_frames():
    camera = cv2.VideoCapture(0)  # Open the webcam
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = process_frame_data(frame)  # Process each frame
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


#REMOVE THIS ROUTE IF YOU ARE PLANNING TO HOST THE APP ON A PUBLIC SERVER
# This route is only used to generate frames for the local webcam stream
@app.route('/video_feed')
def video_feed():
    
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def process_frame_data(frame):
    data_aux = []    
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
        
        for i in range(len(hand_landmarks.landmark)):
            x_.append(hand_landmarks.landmark[i].x)
            y_.append(hand_landmarks.landmark[i].y)

        for i in range(len(hand_landmarks.landmark)):
            data_aux.append(hand_landmarks.landmark[i].x - min(x_))
            data_aux.append(hand_landmarks.landmark[i].y - min(y_))

        if len(data_aux) < 84:
            data_aux.extend([0] * (84 - len(data_aux)))

        x1 = int(min(x_) * Width) - 10
        y1 = int(min(y_) * Height) - 10

        x2 = int(max(x_) * Width) - 10
        y2 = int(max(y_) * Height) - 10
    
        pred = model.predict([np.asarray(data_aux)])
        predicted_label = labls_dict[int(pred[0])]

        cv2.rectangle(frame, (x1, y1), (x2 + 20, y2 + 20), (0, 0, 0), 3)
        cv2.putText(frame, predicted_label, (x1 + 75, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

    return frame


@app.route('/')
def screen():
    return render_template('screen.html')

@app.route('/process_frames', methods=['POST'])
def process_frames_endpoint():
    """
    Endpoint to receive and process video frames from the frontend.
    """
    frame_data = request.json.get('frame')
    if not frame_data:
        return jsonify({"error": "No frame data received"}), 400

    try:
        frame_bytes = base64.b64decode(frame_data.split(',')[1])
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except Exception as e:
        return jsonify({"error": f"Error decoding frame: {e}"}), 500


    processed_frame = process_frame_data(frame)

    _, buffer = cv2.imencode('.jpg', processed_frame)
    processed_frame_b64 = base64.b64encode(buffer).decode('utf-8')

    return jsonify({'processed_frame': processed_frame_b64})

if __name__ == '__main__':
    app.run(debug=True)