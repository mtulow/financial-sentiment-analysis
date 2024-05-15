import os
import sys
import dlt
import json
import time
import hmac
import duckdb
import base64
import hashlib
import pandas as pd

# import requests
from dlt.sources.helpers import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

# load_dotenv('.env')


def get_currencies():
    """
    Get a list of all known currencies.
    """
    # Load environment variables
    API_KEY     = str(os.environ.get('ACCESS_KEY',''))
    PASSPHRASE  = str(os.environ.get('PASSPHRASE',''))
    SECRET_KEY  = str(os.environ.get('SIGNING_KEY',''))

    # Endpoint URL
    url = 'https://api.exchange.coinbase.com/currencies'

    # Create the signature
    timestamp = str(int(time.time()))
    method = 'GET'

    url_path = urlparse(url).path

    message = timestamp + method + url_path
    hmac_key = base64.b64decode(SECRET_KEY)
    signature = hmac.digest(hmac_key, message.encode('utf-8'), hashlib.sha256)
    signature_b64 = base64.b64encode(signature)

    # Create the headers
    headers = {
        'CB-ACCESS-SIGN': signature_b64,
        'CB-ACCESS-TIMESTAMP': timestamp,
        'CB-ACCESS-KEY': API_KEY,
        'CB-ACCESS-PASSPHRASE': PASSPHRASE,
        'Accept': 'application/json'
    }

    # Send the request
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    for data in response.json():
        yield data


def main():
    # Create a pipeline
    pipeline = dlt.pipeline(
        pipeline_name='coinbase',
        destination='duckdb',
        dataset_name='exchange_api',
    )

    # Load the data
    load_info = pipeline.run(get_currencies(),
                             table_name='currencies',
                             write_disposition='replace',)
    print(load_info)

    # Read the data

    conn = duckdb.connect(database='coinbase')



if __name__ == '__main__':
    print()
    main()
    print()