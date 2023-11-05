import cv2
import numpy as np

# Load YOLO
net = cv2.dnn.readNet("/home/user/backend/yolofish/fishyolo.weights", "/home/user/backend/yolofish/fishyolo.cfg")
classes = []
with open("/home/user/backend/yolofish/obj.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Function to get the output layer names
def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

# Load image
def detect(image):
    # Preprocess image for YOLO input
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    # Set input for YOLO network
    net.setInput(blob)

    # Run forward pass through network
    outs = net.forward(get_output_layers(net))

    conf_threshold = 0.5
    # Process each output layer
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Filter out weak predictions
            if confidence > conf_threshold:
                return True
    return False