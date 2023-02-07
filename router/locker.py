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

@router.get('/')
def view_avail():
    avail_room={1:'Available',2:'Available',3:'Available',4:'Available',5:'Available',6:'Available'}
    for i in collection.find():
        is_avail='Not Available '+str((datetime.fromisoformat(i['check_out_time'])-datetime.now()).seconds//60)+' minutes' 
        avail_room[i['locker_id']]=is_avail
    return avail_room
    
@router.post('/rent')
def rent_locker(locker:Container):
    locker.check_in_time=datetime.now()
    locker.check_out_time=locker.check_in_time+timedelta(hours=locker.hours)
    locker.check_in_time=locker.check_in_time
    if (collection.find_one({'$or':[{"locker_id":locker.locker_id},{"uid":locker.uid}]})) or (locker.check_in_time.day!=locker.check_out_time.day) or (locker.check_in_time.year!=locker.check_out_time.year) or (locker.check_in_time.month!=locker.check_out_time.month) or locker.locker_id>6 or locker.locker_id<1 or locker.hours<0:
        raise HTTPException(status_code=400)
    else:
        collection.insert_one({"uid":locker.uid,"item_in_contain":locker.item_in_contain,"hours":locker.hours,"locker_id":locker.locker_id,"check_in_time":str(locker.check_in_time),"check_out_time":str(locker.check_out_time)})

@router.delete('/checkout/{uid}')
def checkout_locker(uid:int,money:int=0):
    ans=0
    x = collection.find_one({"uid":uid},{'_id':0})
    if not x:
        raise HTTPException(status_code=400)
    x = Container(**x)
    now = datetime.now()
    if(now>x.check_out_time):
        ans+=money
        ans-=max(((x.check_out_time-x.check_in_time).seconds//60//60-2),0)*5
        ans-=((now-x.check_out_time).seconds//600)*20
    else:
        ans+=money
        ans-=max(((x.check_out_time-x.check_in_time).seconds//60//60-2),0)*5
    if ans<0:
        raise HTTPException(status_code=400,detail=f'total = {abs(ans)} bath')
    collection.delete_one({"uid":x.uid})
    if ans:
        return {'change':ans,'contain':x.item_in_contain}
    return {'contain':x.item_in_contain}