import pymongo
# import schedule
# import time

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mongodb"]
mycol = mydb["blacklist"]

def check_eth_address(address):
    if len(address) == 42 and address[0:2] == '0x':
        return True
    else:   
        return False

def get_addresses():
    addresses = []
    elems = mycol.find()
    for _ in range(10):
        if check_eth_address(elems[_]['address']):
            addresses.append(elems[_]['address'])

    return addresses

def get_scam_eth_addresses():
    addresses = get_addresses()

    mydb = myclient["mongodb"]
    mycol = mydb["scam_eth_addresses"]

    mydb["scam_eth_addresses"].drop()
    addresses_dict = {'adrresses': addresses}
    mycol.insert_one(addresses_dict)

get_scam_eth_addresses()

# schedule.every().day.at("23:00").do(get_scam_eth_addresses)

# while True:
#     # Checks whether a scheduled task
#     # is pending to run or not
#     schedule.run_pending()
#     time.sleep(1)