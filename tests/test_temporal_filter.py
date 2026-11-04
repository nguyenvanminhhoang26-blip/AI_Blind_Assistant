from src.detection.temporal_filter import TemporalFilter

temporal_filter = TemporalFilter(history_size=5)

test_frames = [
    [{
        "class_name": "Obstacle",
        "position": "Ở giữa",
        "threat_level": "Trung bình"
    }],
    [{
        "class_name": "Obstacle",
        "position": "Ở giữa",
        "threat_level": "Cao"
    }],
    [{
        "class_name": "Obstacle",
        "position": "Ở giữa",
        "threat_level": "Cao"
    }]
]

for index, frame_detections in enumerate(test_frames):
    temporal_filter.update(frame_detections)

    confirmed = temporal_filter.filter_detections(frame_detections)

    print(
        f"Frame {index + 1}: "
        f"YOLO phát hiện {len(frame_detections)} đối tượng | "
        f"Được xác nhận {len(confirmed)} đối tượng"
    )