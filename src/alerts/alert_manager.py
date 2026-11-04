import time
from pathlib import Path
from src.alerts.voice import AUDIO_DIR, play_audio, stop_audio, is_audio_playing


ALERT_PRIORITY = {
    "Pothole": 1,
    "Obstacle": 2,
    "Road-barrier": 3,
    "Railway": 4,
    "Stairs": 5,
    "Vehicle": 6,
    "Person": 7,
    "Pole": 8
}
POSITION_CODES = {
    "Bên trái": "Left",
    "Ở giữa": "Center",
    "Bên phải": "Right"
}
THREAT_PRIORITY = {
    "Cao": 1,
    "Trung bình": 2,
    "Thấp": 3
}


class AlertManager:
    def __init__(self, cooldown=3, confidence_threshold=0.5):
        self.cooldown = cooldown
        self.confidence_threshold = confidence_threshold
        self.last_alert_time = {}
        self.last_alert_threat = {}
        self.current_audio_threat = None
    def select_alert(self, detections):
        candidates = []

        for detection in detections:
            class_name = detection["class_name"]
            confidence = detection["confidence"]

            if class_name not in ALERT_PRIORITY:
                continue

            if confidence < self.confidence_threshold:
                continue

            candidates.append(detection)

        if not candidates:
            return None

        candidates.sort(
            key=lambda item: (
                THREAT_PRIORITY.get(item["threat_level"], 99),
                ALERT_PRIORITY[item["class_name"]]
            )
        )

        return candidates[0]

    def process_detections(self, detections):
        selected = self.select_alert(detections)

        if selected is None:
            return

        class_name = selected["class_name"]
        position = selected["position"]
        distance_level = selected["distance_level"]
        threat_level = selected["threat_level"]

        position_code = POSITION_CODES.get(position)

        if position_code is None:
            return

        threat_codes = {
            "Cao": "Cao",
            "Trung bình": "TrungBinh",
            "Thấp": "Thap"
        }

        threat_code = threat_codes.get(threat_level)

        if threat_code is None:
            return

        alert_key = (class_name, position_code)

        current_time = time.monotonic()
        last_time = self.last_alert_time.get(alert_key, 0)

        previous_threat = self.last_alert_threat.get(alert_key)
        current_priority = THREAT_PRIORITY[threat_level]

        threat_increased = (
            previous_threat is not None
            and current_priority < THREAT_PRIORITY[previous_threat]
        )
        if not is_audio_playing():
            self.current_audio_threat = None
        interrupt_current = (
            self.current_audio_threat is not None
            and current_priority < THREAT_PRIORITY[self.current_audio_threat]
        )

        if not threat_increased and not interrupt_current:
            if current_time - last_time < self.cooldown:
                return

        audio_path = (
            AUDIO_DIR
            / f"{class_name}_{position_code}_{threat_code}.mp3"
        )

        if not audio_path.exists():
            print(f"Khong tim thay am thanh: {audio_path}")
            return

        if interrupt_current:
            stop_audio()

        if play_audio(audio_path):
            self.last_alert_time[alert_key] = current_time
            self.last_alert_threat[alert_key] = threat_level
            self.current_audio_threat = threat_level

            print(
                f"Dang canh bao: {class_name} - {position} "
                f"- {distance_level} - Nguy hiem: {threat_level}"
            )