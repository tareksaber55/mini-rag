from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings,Settings
from controllers import DataController
from controllers import ProjectController
import os
import aiofiles
from models import ResponseEnums
import logging

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix='/api/v1/data',
    tags=['api_v1','data']
)


'''
Use POST when the client wants to send data to the server, often to create something or perform an operation.
'''
@data_router.post('/upload/{project_id}')
async def upload_data(project_id:str,
                      file:UploadFile,
                      app_settings:Settings = Depends(get_settings)
                      ):
    is_valid,result_signal = DataController().validate_uploading_files(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal" : result_signal
            }
        )
    file_path,file_id = DataController().generate_unique_file_path(file.filename,project_id)
    try:
        async with aiofiles.open(file_path , 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f'error while uploading file, {e} ')
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                'signal':ResponseEnums.FILE_UPLOAD_FAIL.value
            }
        )
    return JSONResponse(
        content={
            'signal':ResponseEnums.FILE_UPLOAD_SUCCESS.value,
            'file_id':file_id
        }
    )