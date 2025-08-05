from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from helpers.helpers import image_upload_decorator
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
router = APIRouter()

@router.post('/check-image',
            tags=["Check"],
            response_model=dict,
            response_description="Check Model",
            include_in_schema=False)
@image_upload_decorator(image_required=True)
async def format_check_image_api(
    image_file: UploadFile = File(None, title="Input Check Image"),
    image_url: str = Form('', title="Check Image URL"),
    image_data=None):


    return JSONResponse(content={'data': None})