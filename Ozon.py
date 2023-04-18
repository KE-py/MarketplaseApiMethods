import json
from requests import Session
from datetime import datetime
from Config.configLog import logEventHandler, logMessage
from Config.configFileFunction import Marketplace, getWriteDataToExcel

key = Marketplace('OZ').getKey()

@logEventHandler
def reportOzonOrders(dateFrom: str = "2023-01-01T00:00:00Z", dateTo: str = datetime.strftime(datetime.now(), '%Y-%m-%d')+"T23:59:59Z", limit: int = 1000):
    requestBody = {
        'filter': {
            'since': dateFrom,
            'to': dateTo
        },
        'limit': limit,
        'offset': 0,
        'with':{
            'financial_data':True
        }
    }
    requestUrl = 'https://api-seller.ozon.ru/v3/posting/fbs/list'
    with Session() as s:
        
        responses = s.post(url=requestUrl,headers=key, body= json.dumps(requestBody))