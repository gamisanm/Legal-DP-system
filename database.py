import pymongo
from config import MONGODB_URI, DB_NAME
from bson.binary import Binary

client = pymongo.MongoClient(MONGODB_URI)
db = client[DB_NAME]