import cv2

from src.detection.detection import load_model, detect_objects

MODEL_PATH = "runs/detect/finetune_safewalkbd/weights/best.pt"

IMAGE_PATHS = [
    "videos/person_far.jpg",
    "videos/person_medium.jpg",
    "videos/person_near.jpg"
]

def main():
    model = load_model(MODEL_PATH)

    for image_path in IMAGE_PATHS:
        frame = cv2.imread(image_path)

        print("\n==========", image_path, "==========")

        if frame is None:
            print("Khong doc duoc anh")
            continue

        detections = detect_objects(model, frame)

        print("So vat the:", len(detections))

        for detection in detections:
            print("Ten:", detection["class_name"])
            print("Do tin cay:", detection["confidence"])
            print("Ty le dien tich:", detection["area_ratio"], "%")
            print("Khoang cach:", detection["distance_level"])
            print("Ty le dien tich:", detection["area_ratio"] * 100, "%")
            print("Ty le chieu cao:", detection["h_ratio"] * 100, "%")
            print("Bounding box:", detection["bbox"])
            print("Chieu cao khung hinh:", frame.shape[0])
if __name__ == "__main__":
    main()