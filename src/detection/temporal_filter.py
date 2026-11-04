from collections import deque


class TemporalFilter:
    def __init__(self, history_size=5):
        self.history_size = history_size
        self.history = deque(maxlen=history_size)
    def update(self, detections):
        self.history.append(detections)
        return list(self.history)
    def is_confirmed(self, detection):
        class_name = detection["class_name"]
        position = detection["position"]
        threat_level = detection["threat_level"]

        if threat_level == "Cao":
            required_frames = 2
            window_size = 3

        elif threat_level == "Trung bình":
            required_frames = 3
            window_size = 5

        elif threat_level == "Thấp":
            required_frames = 4
            window_size = 5

        else:
            return False

        recent_history = list(self.history)[-window_size:]

        count = 0

        for frame_detections in recent_history:
            for item in frame_detections:
                if (item["class_name"] == class_name and item["position"] == position):
                    count += 1
                    break

        return count >= required_frames
    def filter_detections(self, detections):
        confirmed_detections = []

        for detection in detections:
            if self.is_confirmed(detection):
                confirmed_detections.append(detection)

        return confirmed_detections