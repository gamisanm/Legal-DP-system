import pymongo
from config import MONGODB_URI, DB_NAME

client = pymongo.MongoClient(MONGODB_URI)
db = client[DB_NAME]