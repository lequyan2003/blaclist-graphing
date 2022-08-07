from typing import Union
from fastapi import FastAPI
import pymongo
import requests
import json
import config

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mongodb"]
mycol = mydb["blacklist"]
app = FastAPI()

@app.get("/")
def read_root():
    return "This api use for display user scam address BTC/BCH/ETC/LTC"


@app.get("/blacklist/")
def read_item(address: Union[str, None] = None):
    for value in mycol.find({'address':address},{"_id":0}):
        if(value): return value
    try:
        cryptoscam_data = json.loads(requests.get(config.CRYPTOSCAMDB_API+address).text)
        for value in cryptoscam_data['result']['entries']:
            dict_cryptoscam = {
                'address': cryptoscam_data['input'],
                'name': value['name'],
                'type': value['type'],
                'url': value['url'],
                'hostname': value['hostname'],
                'category': value['category'],
                'subcategory': value['subcategory'],
                'description': value['description'],
                'reporter': value['reporter']
            }
        mycol.insert_one(dict_cryptoscam)
        return cryptoscam_data
    except:
        pass


## API for checking if a address is a scam one by searching in blacklist. 
## If the address is not in blacklist, it will be checked on CRYPTOSCAMDB_API and will be inserted to blacklist if it is a scam one.
## Access API by using command: uvicorn search_blacklist:app --reload
## <link>/docs for checking