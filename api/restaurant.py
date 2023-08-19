import os
from io import BytesIO
from json import dumps, loads

from cryptography.fernet import Fernet
from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import (JSONResponse, PlainTextResponse,
                               RedirectResponse, StreamingResponse)
from fastapi.templating import Jinja2Templates
from PIL import Image, ImageFilter

from config.db import create_db_engine
from models.documentation.response import Error500Model
from models.request.ambiance_rate import AmbianceRateReq
from models.request.feedback import FeedbackReq
from models.request.food_rate import FoodRateReq
from models.request.restaurant import RestaurantReq
from repository.restaurant import RestaurantRepository
from utils.auth_session import get_current_user
from utils.custom_routes import CustomRoute
from utils.json_date import json_datetime_serializer

templates = Jinja2Templates(directory="templates")

key = Fernet.generate_key()

res_router = APIRouter()
res_router.route_class = CustomRoute


@res_router.post(
    "/restaurant/add",
    summary="This API adds new restaurant details",
    description="This operations adds new record to the database.",
    response_description="The message body.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "restaurant_id": 100,
                        "name": "La Playa",
                        "branch": "Manila",
                        "address": "Orosa St.",
                        "province": "NCR",
                        "date_signed": "2022-05-23",
                        "city": "Manila",
                        "country": "Philippines",
                        "zipcode": 1603,
                    }
                }
            },
        },
        404: {
            "description": "An error was encountered during saving.",
            "content": {
                "application/json": {
                    "example": {"message": "insert login unsuccessful"}
                }
            },
        },
    },
    tags=["operation"],
)
async def add_restaurant(req: FeedbackReq, id: int, engine=Depends(create_db_engine), user: str = Depends(get_current_user)):
    feedback_dict = req.dict(exclude_unset=True)
    feedback_json = dumps(feedback_dict, default=json_datetime_serializer)
    repo: RestaurantRepository = RestaurantRepository(engine)
    result = await repo.add_feedback(id, loads(feedback_json))
    if result == True:
        return req
    else:
        return JSONResponse(content={"message": "add feedback unsuccessful"}, status_code=500)


@res_router.post('/restaurant/ambiance/rate/add')
async def add_ambiance_rate(req: AmbianceRateReq, id: int, engine=Depends(create_db_engine), user: str = Depends(get_current_user)):
    ambiance_dict = req.dict(exclude_unset=True)
    ambiance_json = dumps(ambiance_dict, default=json_datetime_serializer)
    repo: RestaurantRepository = RestaurantRepository(engine)
    result = await repo.add_ambience_rating(id, loads(ambiance_json))
    if result == True:
        return req
    else:
        return JSONResponse(content={"message": "add ambiance rating unsuccessful"}, status_code=500)


@res_router.post('/restaurant/upload/logo')
async def logo_upload_png(logo: UploadFile = File(...)):
    original_image = Image.open(logo.file)
    original_image = original_image.filter(ImageFilter.SHARPEN)
    
    filtered_image = BytesIO()
    
    if logo.content_type == 'image/png':
        original_image.save(filtered_image, 'PNG')
        filtered_image.seek(0)
        return StreamingResponse(filtered_image, media_type='image/png')
    elif logo.content_type == 'image/jpeg':
        original_image.save(filtered_image, 'JPEG')
        filtered_image.seek(0)
        return StreamingResponse(filtered_image, media_type="image/jpeg")


@res_router.get('/restaurant/list/all')
async def list_resturant_names(request: Request, engine=Depends(create_db_engine), user: str = Depends(get_current_user)):
    repo: RestaurantRepository = RestaurantRepository(engine)
    result = await repo.get_all_restaurant()
    resto_names = [resto.name for resto in result]
    request.session['resto_name'] = resto_names
    return result


@res_router.get('/restaurant/list/names')
async def list_restaurant_names(request: Request, user: str = Depends(get_current_user)):
    resto_names = request.session['resto_names']
    return resto_names


@res_router.get('/resturant/form/upload/logo')
async def logo_upload_png_form(req: Request, user: str = Depends(get_current_user)):
    return templates.TemplateResponse('upload_file.html', {"request": req})


@res_router.get("/restaurant/upload/video",responses={
        200: {
            "content": {"video/mp4": {}},
            "description": "Return an MP4 encoded video.",
        },
        500:{
            "model": Error500Model, 
            "description": "The item was not found"
        }
    },)
def video_presentation():
    file_path = os.getcwd() + '\\files\\sample.mp4'
    def load_file():
        with open(file_path, mode='rb') as video_file:
            yield from video_file
    return StreamingResponse(load_file(), media_type='video/mp4')


@res_router.get('/resturant/michelin')
def redirect_resturants_rates():
    return RedirectResponse(url='http://guide.michelin.com/en/restaurants')


@res_router.get('/restaurnt/index')
def intro_list_resturants():
    return PlainTextResponse(content='The restaurants')


@res_router.get('/restaurant/enc/details')
async def send_enc_login(engine=Depends(create_db_engine), user: str = Depends(get_current_user)):
    repo: RestaurantRepository = RestaurantRepository(engine)
    result = await repo.get_all_restaurant()
    
    result_json = dumps(jsonable_encoder(result))
    fernet = Fernet(key)
    enc_data = fernet.encrypt(bytes(result_json, encoding='utf-8'))
    
    return {'enc_data': enc_data, 'key': key}
    