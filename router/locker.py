from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter
class Container(BaseModel):
    uid:int
    item_in_contain:str
    minute:int
    locker_id:int
    check_in_time:datetime=None
    check_out_time:datetime=None
    cost:int = 0

router = APIRouter(prefix='/locker')