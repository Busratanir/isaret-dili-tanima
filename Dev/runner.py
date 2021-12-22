import cv2
import numpy as np
import time
import HandTrackingModule as htm
# Load Yolo
pTime = 0
net = cv2.dnn.readNet("yolov4-custom_best.weights","yolov4-custom.cfg")
classes = []
with open("object.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

colors = np.random.uniform(0, 255, size=(len(classes), 3))

vid= cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.7, maxHands=2)
while True:
    ret, sct_img = vid.read()     


    screen =  np.array(sct_img)
    img = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    img = np.flip(img[:, :, :3], 2)
    img = cv2.resize(img, None, fx=0.8, fy=0.8)
    height, width, channels = img.shape
    
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
    
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
        
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.3, 0.4)
    print(indexes)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            print(label)
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255,0,0), 2)
            cv2.putText(img, label, (x, y + 70), font, 3, (0,255,0), 3)
    temp_img=img
    try:  
        img = detector.findHands(temp_img)
        
        lmList, bbox = detector.findPosition(temp_img, draw=True)
    except:
        img=temp_img
        lmList=[]
    if len(lmList) != 0:
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100
        if 250 < area < 1000:
            length, img, lineInfo = detector.findDistance(4, 8, img)
            smoothness = 10
            fingers = detector.fingersUp()
            if not fingers[4]:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (255, 0, 0), cv2.FILLED)
                colorVol = (255, 0, 0)
            else:
                colorVol = (255, 0, 255)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,1, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
cv2.destroyAllWindows()