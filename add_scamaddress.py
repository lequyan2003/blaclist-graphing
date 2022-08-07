import csv
import pymongo
import requests
import config
import schedule
import time
import json
from bs4 import BeautifulSoup

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["mongodb"]
mycol = mydb["blacklist"]

def clear_duplicate():
    for value in mycol.find():
        count = 0
        for _ in mycol.find({'address':value['address']},{"_id":0}):
            count+=1
        if(count>1):
            mycol.delete_one(value)
            print('delete completed')

def add_bitcoinabuse():
    with open('csv\\records_1d.csv', mode='r', encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            count=0
            for _ in mycol.find({'address':row["address"]},{"_id":0}):
                count+=1
            if count>0 :
                continue
            data = {
                'address': row["address"],
                'abuse_type_id': row["abuse_type_id"]
            }
            mycol.insert_one(data)

def get_csv():
    r = requests.get(config.BITCOINABUSE, allow_redirects=True)
    open('csv/records_1d.csv', 'wb').write(r.content)


def get_cryptoscam():
    r = requests.get(config.CRYPTOSCAMDB, allow_redirects=True)
    open('csv/cryptoscam.json', 'wb').write(r.content)

def add_cryptoscam():
    with open('csv/cryptoscam.json', mode='r') as cryptoscam:
        data = json.load(cryptoscam)
        for result in data['result']:
            print(result)
            for value in data['result'][result]:
                count=0
                for _ in mycol.find({'address':value["address"]},{"_id":0}):
                    count+=1
                if count>0 :
                    continue
                dict_cryptoscam = {
                    'address': value['address'],
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

def add_scam_alert():
    r = requests.get(config.SCAM_ALERT, allow_redirects=True)
    parsed_html = BeautifulSoup(r.text,features="lxml")
    for tag in parsed_html.body.find('section', attrs={'id':'topscammers'}).find_all('span', attrs={'class':'d-none d-md-block'}):
        count=0
        for _ in mycol.find({'address': tag.text},{"_id":0}):
            count+=1
        if count>0 :
            continue
        sa_data = {
            'address': tag.text,
            'reporter': 'scam-alert.io'
        }
        mycol.insert_one(sa_data)

add_scam_alert()
get_cryptoscam()     
add_cryptoscam()
get_csv()
add_bitcoinabuse()

schedule.every().monday.at("08:00").do(add_scam_alert)
schedule.every().day.at("00:00").do(get_csv)
schedule.every().day.at("09:00").do(add_bitcoinabuse)
schedule.every().day.at("00:00").do(get_cryptoscam)
schedule.every().day.at("09:00").do(add_cryptoscam)
schedule.every().day.at("09:30").do(clear_duplicate)

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)