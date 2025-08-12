from fastapi import APIRouter, File, UploadFile, Form
from helpers.helpers import image_upload_decorator, get_check_data_from_image
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
    image_file_path=None,
    image_data=None):

    result = await get_check_data_from_image(image_file_path)
    
    if result:
        return JSONResponse(content=jsonable_encoder(result))

    return JSONResponse(status_code=400, content="Failed to parse check.")
