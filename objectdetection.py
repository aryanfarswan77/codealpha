import torch
import torchvision
import cv2
from torchvision.transforms import functional as F

# Load the pre-trained Faster R-CNN model
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Check if CUDA is available and use GPU if possible
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Define COCO dataset class names (for reference)
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag',
    'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
    'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
    'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table',
    'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
    'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# Function to get predictions from the model
def get_predictions(frame, threshold=0.5):
    # Convert frame to tensor
    frame_tensor = F.to_tensor(frame).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(frame_tensor)

    # Process predictions
    pred_boxes = outputs[0]['boxes'].cpu().numpy()
    pred_scores = outputs[0]['scores'].cpu().numpy()
    pred_labels = outputs[0]['labels'].cpu().numpy()

    # Filter based on confidence threshold
    pred_boxes = pred_boxes[pred_scores >= threshold].astype(int)
    pred_labels = pred_labels[pred_scores >= threshold]

    return pred_boxes, pred_labels

# Initialize webcam (0 is the default webcam index)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Get predictions
    boxes, labels = get_predictions(frame)

    # Draw bounding boxes and labels
    for box, label in zip(boxes, labels):
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        cv2.putText(frame, COCO_INSTANCE_CATEGORY_NAMES[label], (box[0], box[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Object Detection", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
