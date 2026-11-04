
import asyncio
from pathlib import Path

import edge_tts
import pygame


ROOT_DIR = Path(__file__).resolve().parents[2]
AUDIO_DIR = ROOT_DIR / "outputs" / "audio"

ALERT_MESSAGES = {
    "Person": "người",
    "Vehicle": "phương tiện",
    "Obstacle": "vật cản",
    "Pothole": "ổ gà",
    "Stairs": "bậc thang",
    "Pole": "cột",
    "Road-barrier": "rào chắn",
    "Railway": "đường ray"
}

THREAT_MESSAGES = {
    "Cao": "Cảnh báo! Có {object} rất gần ở {position}!",
    "TrungBinh": "Chú ý! Có {object} ở {position}!",
    "Thap": "Có {object} ở {position}!"
}


async def generate_alert(file_name, message):
    audio_path = AUDIO_DIR / f"{file_name}.mp3"

    for attempt in range(3):
        try:
            communicate = edge_tts.Communicate(
                text=message,
                voice="vi-VN-HoaiMyNeural"
            )

            await communicate.save(str(audio_path))

            print(f"Da tao am thanh: {file_name}")
            return True

        except Exception as error:
            print(
                f"Thu lan {attempt + 1} that bai: "
                f"{file_name} - {error}"
            )

            if attempt < 2:
                await asyncio.sleep(2 * (attempt + 1))

    print(f"Khong the tao am thanh: {file_name}")
    return False


async def generate_alert_files():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    positions = {
        "Left": "Bên trái",
        "Center": "Ở giữa",
        "Right": "Bên phải"
    }

    for class_name, object_name in ALERT_MESSAGES.items():
        for position_code, position_text in positions.items():
            for threat_code, message_template in THREAT_MESSAGES.items():

                full_message = message_template.format(
                    object=object_name,
                    position=position_text
                )

                file_name = (
                    f"{class_name}_{position_code}_{threat_code}"
                )

                audio_path = AUDIO_DIR / f"{file_name}.mp3"

                if audio_path.exists() and audio_path.stat().st_size > 0:
                    print(f"Da ton tai: {file_name}.mp3")
                    continue

                await generate_alert(file_name, full_message)

def initialize_audio():
    pygame.mixer.init()


def play_audio(audio_path):
    if pygame.mixer.music.get_busy():
        return False

    pygame.mixer.music.load(str(audio_path))
    pygame.mixer.music.play()

    return True


def stop_audio():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        return True

    return False


def close_audio():
    pygame.mixer.music.stop()
    pygame.mixer.quit()
def is_audio_playing():
    return pygame.mixer.music.get_busy()

if __name__ == "__main__":
    asyncio.run(generate_alert_files())
    print("Hoan tat tao cac file am thanh.")
