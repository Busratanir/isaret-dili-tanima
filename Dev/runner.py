import cv2
import numpy as np


import mss
import mss.tools

# Load Yolo
net = cv2.dnn.readNet("yolov4-custom_best.weights","yolov4-custom.cfg")
classes = []
with open("object.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()

output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

vid= cv2.VideoCapture(0)
while True:
    #with mss.mss() as sct:
            # The screen part to capture
            #monitor = {"top": 44, "left": 0, "width": 1000, "height": 1000}
                
                
                # Grab the data
            #sct_img = sct.grab(monitor)
    ret, sct_img = vid.read()


            
            
            
    screen =  np.array(sct_img)
    img = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    img = np.flip(img[:, :, :3], 2)
    img = cv2.resize(img, None, fx=0.8, fy=0.8)
    height, width, channels = img.shape
    
    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
    
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
    
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
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
    
    
    cv2.imshow("Image", img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
cv2.destroyAllWindows()