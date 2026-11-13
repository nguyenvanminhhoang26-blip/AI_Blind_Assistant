import cv2
from src.detection.detection import load_model, detect_objects
from src.alerts.alert_manager import AlertManager
from src.alerts.voice import initialize_audio, close_audio
from src.detection.temporal_filter import TemporalFilter

def open_camera(model):
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Khong the mo webcam")
        return
    window_name = "AI Blind Assistant - Camera"

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    cv2.setWindowProperty(
        window_name,
        cv2.WND_PROP_FULLSCREEN,
        cv2.WINDOW_FULLSCREEN
    )
    alert_manager = AlertManager(cooldown=3,confidence_threshold=0.5)
    temporal_filter = TemporalFilter(history_size=5)
    initialize_audio()
    while True:
        frame = get_frame(camera)

        if frame is None:
            print("Khong the doc frame")
            break

        detections = detect_objects(model, frame)
        temporal_filter.update(detections)
        filtered_detections = temporal_filter.filter_detections(detections)
        alert_manager.process_detections(filtered_detections)
        display_frame = frame.copy()
        # display_frame = cv2.flip(display_frame, 1)

        for detection in detections:
            x1, y1, x2, y2 = detection["bbox"]

            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            class_name = detection["class_name"]
            position = detection["position"]
            confidence = detection["confidence"]
            distance_level = detection["distance_level"]
            threat_level = detection["threat_level"]
            cv2.rectangle(
                display_frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                display_frame,
                f"{class_name} - {position} - {confidence:.2f} - {distance_level} - {threat_level}",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        cv2.imshow(window_name, display_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    close_audio()        
    camera.release()
    cv2.destroyAllWindows()


def open_video(video_path, model):
    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        print("Khong the mo video")
        return
    alert_manager = AlertManager(
        cooldown=3,
        confidence_threshold=0.5
    )
    temporal_filter = TemporalFilter(history_size=5)
    initialize_audio()
    while True:
        frame = get_frame(video)

        if frame is None:
            break

        detections = detect_objects(model, frame)
        temporal_filter.update(detections)
        filtered_detections = temporal_filter.filter_detections(detections)
        alert_manager.process_detections(filtered_detections)
        display_frame = frame.copy()

        for detection in detections:
            x1, y1, x2, y2 = detection["bbox"]

            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            class_name = detection["class_name"]
            position = detection["position"]
            confidence = detection["confidence"]
            distance_level = detection["distance_level"]
            threat_level = detection["threat_level"]

            cv2.rectangle(
                display_frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                display_frame,
                f"{class_name} - {position} - {confidence:.2f} - {distance_level} - {threat_level}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

        display_frame = cv2.resize(display_frame, (960, 540))

        cv2.imshow("AI Blind Assistant - Video", display_frame)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

    close_audio()
    video.release()
    cv2.destroyAllWindows()


def get_frame(source):
    ret, frame = source.read()

    if not ret:
        return None

    return frame


if __name__ == "__main__":
    from pathlib import Path

    ROOT_DIR = Path(__file__).resolve().parents[2]

    model_path = ROOT_DIR / "weights" / "best.pt"
    model = load_model(str(model_path))

    VIDEO_PATH = ROOT_DIR / "videos" / "video_test.mp4"

    # open_video(str(VIDEO_PATH), model)
    open_camera(model)
    
