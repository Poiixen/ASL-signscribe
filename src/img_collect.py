import cv2
import os 

data = "./data"

if not os.path.exists(data):
    os.makedirs(data)

size_dataset = 100
amountClass = 26    


capture = cv2.VideoCapture(0)

for i in range(amountClass):
    if not os.path.exists(os.path.join(data, str(i))):
        os.makedirs(os.path.join(data, str(i)))

    print(f"Collecting class {i}")

    done = False
    while True:
        ret, frame = capture.read()
        cv2.putText(frame, "press q to start", (100, 50), cv2.FONT_HERSHEY_PLAIN, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow("frame", frame)
        if cv2.waitKey(25) == ord("q"):
            break
    
    counter = 0 

    while counter < size_dataset:
        ret, frame = capture.read()
        cv2.imshow("frame", frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(data, str(i), f"{counter}.jpg"), frame)

        counter += 1

capture.release()
cv2.destroyAllWindows()

 