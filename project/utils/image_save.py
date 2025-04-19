import base64
from pathlib import Path
from io import BytesIO
from PIL import Image
import asyncio

def _process_and_save_image(file_path: Path, base64_str: str):
    if "," in base64_str:
        base64_str = base64_str.split(",")[1]

    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data)).convert("RGB")
    image.save(file_path, format="JPEG")

async def save_image(user_id: int, base64_str: str, category: str, base_dir="__data__") -> str:
    user_dir = Path(base_dir) / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    existing_files = list(user_dir.glob(f"{user_id}_{category}_*.jpg"))
    existing_numbers = []

    for f in existing_files:
        try:
            num_part = f.stem.split("_")[-1]
            existing_numbers.append(int(num_part))
        except ValueError:
            continue

    if len(existing_numbers) >= 3:
        raise ValueError("У вас больше 3 изображений")

    next_number = max(existing_numbers, default=0) + 1
    filename = f"{user_id}_{category}_{next_number}.jpg"
    file_path = user_dir / filename

    try:
        # Выполняем сохранение в отдельном потоке
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _process_and_save_image, file_path, base64_str)
    except Exception as e:
        raise ValueError(f"Ошибка при обработке изображения: {e}")

    return str(file_path)


import asyncio

async def main():
    with open("test.png", "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    path = await save_image(1, b64, "cat")
    print("Сохранено в:", path)

asyncio.run(main())

