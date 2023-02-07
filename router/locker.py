from pydantic import BaseModel
from datetime import datetime

class Container(BaseModel):
    item_in_contain:str
    minute:int
    locker_id:int
    uid:int
    check_in_time:datetime=datetime(0)
    check_out_time:datetime=datetime(0)
    cost:int = 0