import time
import pygame

from src.alerts.voice import initialize_audio, close_audio
from src.alerts.alert_manager import AlertManager


def main():
    initialize_audio()

    alert_manager = AlertManager(
        cooldown=3,
        confidence_threshold=0.5
    )

    detections = [
    {
        "class_name": "Vehicle",
        "confidence": 0.85,
        "position": "Bên phải"
    },
    {
        "class_name": "Person",
        "confidence": 0.90,
        "position": "Bên trái"
    },
    ]

    print("Lan 1:")
    alert_manager.process_detections(detections)

    print("Lan 2:")
    alert_manager.process_detections(detections)

    time.sleep(4)

    print("Lan 3:")
    alert_manager.process_detections(detections)

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    close_audio()


if __name__ == "__main__":
    main()