import os
import json

GITHUB_USERNAME = "hajithoifah"
REPO_NAME = "katseye"
BRANCH_NAME = "main"

MUSIC_DIR = "music"
JSON_DIR = "api"
MUSIC_JSON = os.path.join(JSON_DIR, "music.json")
BASE_RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/{BRANCH_NAME}"

def generate_json():
    os.makedirs(JSON_DIR, exist_ok=True)
    if not os.path.exists(MUSIC_DIR):
        os.makedirs(MUSIC_DIR)

    mp3_files = sorted([f for f in os.listdir(MUSIC_DIR) if f.lower().endswith('.mp3')])
    music_data = []

    for index, filename in enumerate(mp3_files, start=1):
        base_name = os.path.splitext(filename)[0]
        clean_title = base_name.replace("_", " ").replace("-", " ").title()
        
        music_data.append({
            "id": f"song_{str(index).zfill(3)}",
            "title": clean_title,
            "artist": "Katseye",
            "audio_url": f"{BASE_RAW_URL}/{MUSIC_DIR}/{filename}",
            "bpm": 120,
            "duration": "03:00"
        })

    with open(MUSIC_JSON, "w") as f:
        json.dump({
            "status": "success",
            "total_items": len(music_data),
            "data": music_data
        }, f, indent=2)

if __name__ == "__main__":
    generate_json()
