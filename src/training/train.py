
from pathlib import Path
from ultralytics import YOLO


ROOT_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    ROOT_DIR / "datasets" / "SafeWalkBD" / "data.yaml"
)

def main():
    model = YOLO("yolov8n.pt")

    model.train(
        data=str(DATASET_PATH),
        epochs=50,
        imgsz=640,
        batch=4,
        device=0,
        workers=2,
        patience=15,
        pretrained=True,
        project=str(ROOT_DIR / "runs" / "detect"),
        name="finetune_safewalkbd",
        exist_ok=False,
        save=True,
        plots=True
    )


if __name__ == "__main__":
    main()
