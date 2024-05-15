
import json
import hmac
import hashlib
import time
import requests
import base64
import os
import sys
from urllib.parse import urlparse

API_KEY = str(os.environ.get('ACCESS_KEY'))
PASSPHRASE = str(os.environ.get('PASSPHRASE'))
SECRET_KEY = str(os.environ.get('SIGNING_KEY'))

url = 'https://api.exchange.coinbase.com/fees'

timestamp = str(int(time.time()))
method = 'GET'

url_path = urlparse(url).path

message = timestamp + method + url_path
hmac_key = base64.b64decode(SECRET_KEY)
signature = hmac.digest(hmac_key, message.encode('utf-8'), hashlib.sha256)
signature_b64 = base64.b64encode(signature)

headers = {
   'CB-ACCESS-SIGN': signature_b64,
   'CB-ACCESS-TIMESTAMP': timestamp,
   'CB-ACCESS-KEY': API_KEY,
   'CB-ACCESS-PASSPHRASE': PASSPHRASE,
   'Accept': 'application/json'
}

response = requests.get(url, headers=headers)
print(response.status_code)
parse = json.loads(response.text)
print(json.dumps(parse, indent=3))
