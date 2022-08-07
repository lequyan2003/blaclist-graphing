from pprint import pprint
import requests
import config
import json
import pprint

def get_cryptoscam():
    r = requests.get(config.CRYPTOSCAMDB, allow_redirects=True)
    open('csv/cryptoscam.json', 'wb').write(r.content)

get_cryptoscam()

f = open('csv/cryptoscam.json')
data = json.load(f)

pprint.pprint(data)