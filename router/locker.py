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

# def get_locker_detail():
#     for i in range(6):
#         collection.insert_one({'uid':None,'item_in_contain':None,'hour':None,'locker_id':i+1,'check_in_time':None,'check_out_time':None})
#     return "Get Data Success"

@router.get('/')
def view_avail():
    avail_room={1:'Available',2:'Available',3:'Available',4:'Available',5:'Available',6:'Available'}
    for i in collection.find():
        is_avail='Not Available '+str((datetime.fromisoformat(i['check_out_time'])-datetime.now()).seconds//60)+' minutes' 
        avail_room[i['locker_id']]=is_avail
    return avail_room


