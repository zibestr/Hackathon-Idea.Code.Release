import base64
from pathlib import Path
from io import BytesIO
from PIL import Image
import asyncio
import aiofiles
from config import settings


async def _process_and_save_image(file_path: Path, base64_str: str):
    image_data = base64.b64decode(base64_str.split(",")[-1])
    image = Image.open(BytesIO(image_data)).convert("RGB")

    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    async with aiofiles.open(file_path, 'wb') as image_file:
        await image_file.write(buffer.getvalue())


async def save_image(user_id: int, base64_str: str, category: str) -> str:
    user_dir = Path(settings.data_path) / str(user_id)
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
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _process_and_save_image, file_path, base64_str)
    except Exception as e:
        raise ValueError(f"Ошибка при обработке изображения: {e}")

    return str(file_path)
