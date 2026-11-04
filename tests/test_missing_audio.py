import asyncio
import edge_tts
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
AUDIO_DIR = ROOT_DIR / "outputs" / "audio"

ALERT_MESSAGES = {
    "Pole": "Phía trước có cột.",
    "Road-barrier": "Phía trước có rào chắn."
}


async def main():
    for class_name, message in ALERT_MESSAGES.items():
        audio_path = AUDIO_DIR / f"{class_name}.mp3"

        communicate = edge_tts.Communicate(
            text=message,
            voice="vi-VN-HoaiMyNeural"
        )

        try:
            await communicate.save(str(audio_path))
            print(f"Tao thanh cong: {class_name}")
        except Exception as error:
            print(f"That bai: {class_name} - {error}")


if __name__ == "__main__":
    asyncio.run(main())