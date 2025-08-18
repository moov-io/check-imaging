import os
import io
import time
from typing import Callable
from functools import wraps
from uuid import uuid4
import pillow_avif
from PIL import Image, ImageOps
from pillow_heif import register_heif_opener
import requests
from fastapi import HTTPException
import ollama
from schemas.schemas import Check

register_heif_opener()

def download_file_from_url(url, output_path):
    '''
        Download file from URL
    '''
    response = requests.get(url, stream=True, timeout=10)

    try:
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded as {output_path}")
        return True
    except:
        return False


def url_to_image(url:str) -> Image.Image:
    if not url:
        return None

    try:
        response = requests.get(url, timeout=5, verify=False)
        response.raise_for_status()

        # Load the image data into a PIL Image object
        image = Image.open(io.BytesIO(response.content))
        image = ImageOps.exif_transpose(image)

        return image
    except:
        return None

def image_upload_decorator(
    image_required: bool = False,
    image_file_param_name:str="image_file",
    image_url_param_name:str="image_url",
    image_file_path_name:str="image_file_path",
    image_obj_name:str="image_obj"):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            asset_id = kwargs.get('asset_id') or str(uuid4())

            image_file = kwargs.get(image_file_param_name)
            image_url = kwargs.get(image_url_param_name)

            input_filename = asset_id + '.png'
            image_file_path = os.path.join('./tmp', input_filename)

            if image_file:
                image_data = image_file.file.read()
                time.sleep(0.1)
                image_data = Image.open(io.BytesIO(image_data)).convert('RGBA')
                image_data = ImageOps.exif_transpose(image_data)
                image_data.save(image_file_path, "PNG", quality=85, optimize=True)
            elif image_url:
                download_file_from_url(image_file_path, image_url)
                image_data = url_to_image(image_url)
            else:
                if image_required:
                    raise HTTPException(status_code=400, detail="Image Required")

            kwargs[image_url_param_name] = image_url
            if image_file_path_name in kwargs:
                kwargs[image_file_path_name] = image_file_path
            if image_obj_name in kwargs:
                kwargs[image_obj_name] = image_data

            result = await func(*args, **kwargs)
            return result

        return wrapper
    return decorator

async def get_check_data_from_image(image_path):
    response = ollama.chat(
        model='llava:7b',
        messages=[
            {
                'role': 'user',
                'content': 'Analyze this image and get bank check information in detail.',
                'images': [image_path]
            },
        ],
        format=Check.model_json_schema()
    )

    print(response['message'])

    try:
        check_data = Check.model_validate_json(response['message'].content)

        return check_data
    except:
        return None
