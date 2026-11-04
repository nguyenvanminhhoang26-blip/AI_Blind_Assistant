
import numpy as np
from ultralytics import YOLO


def validate_frame(frame):
    if frame is None:
        return False

    if not isinstance(frame, np.ndarray):
        return False

    if frame.size == 0:
        return False

    return True


def load_model(model_path):
    model = YOLO(model_path)
    return model


def format_results(results, model, frame_width, frame_height):
    detections = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = model.names[class_id]
            bbox = box.xyxy[0].tolist()
            position = get_object_position(bbox, frame_width)
            area_ratio = calculate_box_area_ratio(bbox, frame_width, frame_height)
            h_ratio = calculate_box_height_ratio(bbox, frame_height)
            distance_level = estimate_distance(area_ratio, h_ratio)
            threat_level = assess_threat(position, distance_level)
            detection = {
                "class_id": class_id,
                "class_name": class_name,
                "confidence": confidence,
                "bbox": bbox,
                "position": position,
                "area_ratio": area_ratio,
                "h_ratio": h_ratio,
                "distance_level": distance_level,
                "threat_level": threat_level
            }

            detections.append(detection)

    return detections


def detect_objects(model, frame):
    if not validate_frame(frame):
        return []

    results = model.predict(
        source=frame,
        conf=0.25,
        verbose=False
    )
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]
    detections = format_results(results, model, frame_width, frame_height)

    return detections
def get_object_position(bbox, frame_width):
    x1, y1, x2, y2 = bbox

    center_x = (x1 + x2) / 2

    if center_x < frame_width / 3:
        return "Bên trái"

    elif center_x < frame_width * 2 / 3:
        return "Ở giữa"

    else:
        return "Bên phải"
def calculate_box_area_ratio(bbox, frame_width, frame_height):
    x1, y1, x2, y2 = bbox

    box_width = x2 - x1
    box_height = y2 - y1

    box_area = box_width * box_height
    frame_area = frame_width * frame_height

    ratio = box_area / frame_area

    return ratio
def calculate_box_height_ratio(bbox, frame_height):
    x1, y1, x2, y2 = bbox

    box_height = y2 - y1
    ratio = box_height / frame_height

    return ratio
def estimate_distance(area_ratio, h_ratio):
    if area_ratio > 0.22 or h_ratio > 0.55:
        return "Rất gần"

    elif area_ratio > 0.08 or h_ratio > 0.30:
        return "Gần"

    else:
        return "Xa"
def assess_threat(position, distance_level):
    if position == "Ở giữa":
        if distance_level == "Rất gần":
            return "Cao"
        elif distance_level == "Gần":
            return "Trung bình"
        else:
            return "Thấp"

    elif position in ["Bên trái", "Bên phải"]:
        if distance_level == "Rất gần":
            return "Trung bình"
        else:
            return "Thấp"

    return "Không xác định"