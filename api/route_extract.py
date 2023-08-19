from datetime import date
from typing import Dict, List

from fastapi import APIRouter, Depends, Form, Request

from utils.auth_session import get_current_user
from utils.custom_routes import ExtractContentRoute

exc_router = APIRouter()
exc_router.route_class = ExtractContentRoute


async def json_data():
    return {"name": "abil"}


@exc_router.post("/user/profile")
async def create_profile(
    req: Request,
    firstname: str = Form(..., description="The first name of the user."),
    lastname: str = Form(..., description="The last name of the user."),
    age: int = Form(..., description="The age of the user."),
    birthday: date = Form(..., description="The birthday of the user."),
    user: str = Depends(get_current_user),
):
    user_details = req.session["user_details"]
    return {"profile": user_details}


@exc_router.post('/rating/top/three')
async def set_ratings(req: Request, data: Dict[str, float], user: str = Depends(get_current_user)):
    stats = dict()
    stats['sum'] = req.state.sum
    stats['average'] = req.state.avg
    return {'stats': stats}


@exc_router.post('/rating/data/list')
async def compute_data(req: Request, data: List[float], user: str = Depends(get_current_user)):
    stats = dict()
    stats['sum'] = req.state.sum
    stats['average'] = req.state.avg
    return {'stats': stats}
