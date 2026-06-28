import os
import json
from PIL import Image

GITHUB_USERNAME = "hajithoifah"
REPO_NAME = "katseye"
BRANCH_NAME = "main"

RAW_DIR = "raw_wallpapers"
WEBP_DIR = "wallpapers"
JSON_DIR = "api"
JSON_FILE = os.path.join(JSON_DIR, "wallpapers.json")
BASE_RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{REPO_NAME}/{BRANCH_NAME}"

def process_and_generate():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(WEBP_DIR, exist_ok=True)
    os.makedirs(JSON_DIR, exist_ok=True)

    # 1. Konversi gambar mentah ke WebP
    raw_files = [f for f in os.listdir(RAW_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    for filename in raw_files:
        file_path = os.path.join(RAW_DIR, filename)
        base_name = os.path.splitext(filename)[0]
        webp_path = os.path.join(WEBP_DIR, f"{base_name}.webp")
        
        try:
            with Image.open(file_path) as img:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")
                img.save(webp_path, "webp", quality=80)
            # Hapus file mentah untuk menghemat ruang penyimpanan GitHub
            os.remove(file_path)
        except Exception as e:
            print(f"Gagal memproses {filename}: {e}")

    # 2. Buat JSON berdasarkan semua file WebP yang ada
    webp_files = sorted([f for f in os.listdir(WEBP_DIR) if f.lower().endswith('.webp')])
    wallpaper_data = []

    for index, filename in enumerate(webp_files, start=1):
        base_name = os.path.splitext(filename)[0]
        clean_title = base_name.replace("_", " ").replace("-", " ").title()
        size_kb = round(os.path.getsize(os.path.join(WEBP_DIR, filename)) / 1024)
        
        wallpaper_data.append({
            "id": f"wp_{str(index).zfill(3)}",
            "title": clean_title,
            "category": "Katseye",
            "url_webp": f"{BASE_RAW_URL}/{WEBP_DIR}/{filename}",
            "tags": ["katseye", "kpop"],
            "size_kb": size_kb
        })

    with open(JSON_FILE, "w") as f:
        json.dump({
            "status": "success",
            "total_items": len(wallpaper_data),
            "data": wallpaper_data
        }, f, indent=2)

if __name__ == "__main__":
    process_and_generate()
