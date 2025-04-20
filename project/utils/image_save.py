import base64
from pathlib import Path
from io import BytesIO
from PIL import Image
import asyncio
import aiofiles
from typing import Optional, Literal
from config import settings


async def _process_and_save_image(file_path: Path, base64_str: str):
    image_data = base64.b64decode(base64_str.split(",")[-1])
    image = Image.open(BytesIO(image_data)).convert("RGB")

    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    async with aiofiles.open(file_path, 'wb') as image_file:
        await image_file.write(buffer.getvalue())


async def save_image(user_id: int,
                     base64_str: str,
                     category: Literal['profile', 'habitation']) -> Optional[str]:
    user_dir = Path(settings.data_path) / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    existing_files = list(user_dir.glob(f"{user_id}_{category}_*.jpg"))
    if len(existing_numbers) >= 3:
        return
    
    existing_numbers = [
            int(f.stem.split("_")[-1]) 
            for f in existing_files
            if f.stem.split("_")[-1].isdigit()
    ]

    next_number = max(existing_numbers, default = 0) + 1
    filename = f"{user_id}_{category}_{next_number}.jpg"
    file_path = user_dir / filename
    await asyncio.to_thread(_process_and_save_image, file_path, base64_str)
    return str(file_path)


async def get_images_base64(
    user_id: int,
    category: Literal["profile", "habitation"]
) -> List[str]:
    user_dir = Path(settings.data_path) / str(user_id)
    if not user_dir.exists():
        return []

    image_files = sorted(user_dir.glob(f"{user_id}_{category}_*.jpg"))

    base64_images = []

    for image_path in image_files:
        async with aiofiles.open(image_path, 'rb') as f:
            image_data = await f.read()
            encoded = base64.b64encode(image_data).decode('utf-8')
            base64_images.append(f"data:image/jpeg;base64,{encoded}")

    return base64_images

