from pydantic import BaseModel
from datetime import datetime
from fastapi import APIRouter
from config.database import *
from typing import Union,Optional
class Container(BaseModel):
    uid:int
    item_in_contain:str
    minute:int
    locker_id:int
    check_in_time:Union[datetime,None]=None
    check_out_time:Union[datetime,None]=None
    cost:int = 0

router = APIRouter(prefix='/locker')