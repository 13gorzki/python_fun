import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}

def import_data(what):
    api_link = 'api_link'
    api_key = '?apiKey=api_key'
    requestURL = api_link + what + api_key
    data_raw_requests = requests.get(requestURL, headers=headers)
    data_raw = data_raw_requests.text
    return data_raw

  
