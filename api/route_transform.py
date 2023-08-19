from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile

from utils.auth_session import get_current_user
from utils.custom_routes import FileStreamRoute

trans_router = APIRouter()
trans_router.route_class = FileStreamRoute


@trans_router.post('/files/')
async def create_file(file: Optional[bytes] = File(...), user: str = Depends(get_current_user)):
    return {'file_size': len(file)}


@trans_router.post('/file/upload')
async def create_file_2(file: Optional[UploadFile] = File(...), user: str = Depends(get_current_user)):
    print(file.content_type)
    fs = await file.read()
    return {'file_size': len(fs)}
