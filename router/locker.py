from pydantic import BaseModel
from datetime import datetime,timedelta
from fastapi import APIRouter,HTTPException
from config.database import *
from typing import Union,Optional,List
class Container(BaseModel):
    uid:int
    item_in_contain:List[str]
    hours:int
    locker_id:int
    check_in_time:Union[datetime,None]=None
    check_out_time:Union[datetime,None]=None

router = APIRouter(prefix='/locker')

@router.post('/rent')
def rent_locker(locker:Container):
    locker.check_in_time=datetime.now()
    locker.check_out_time=locker.check_in_time+timedelta(hours=locker.hours)
    locker.check_in_time=locker.check_in_time
    if (collection.find_one({"locker_id":locker.locker_id})) or (locker.check_in_time.day!=locker.check_out_time.day) or (locker.check_in_time.year!=locker.check_out_time.year) or (locker.check_in_time.month!=locker.check_out_time.month):
        raise HTTPException(status_code=400)
    else:
        collection.insert_one({"uid":locker.uid,"item_in_contain":locker.item_in_contain,"hours":locker.hours,"locker_id":locker.locker_id,"check_in_time":str(locker.check_in_time),"check_out_time":str(locker.check_out_time)})