import cv2
import os 

data = "./data"

if not os.path.exists(data):
    os.makedirs(data)

size_dataset = 100
amountClass = 3


capture = cv2.VideoCapture(2)

for i in range(amountClass):
    if not os.path.exists(os.path.join(data, str(i))):
        os.makedirs(os.path.join(data, str(i)))

    print(f"Collecting class {i}")

    

 