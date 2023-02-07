from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv('.env')
username=os.getenv('username')
password=os.getenv('password')
client = MongoClient(f'mongodb://{username}:{password}@mongo.exceed19.online:8443/?authMechanism=DEFAULT')

# print(username,password)
db = client['exceed03']