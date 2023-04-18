import json
from requests import Session
from datetime import datetime
from Config.configLog import logEventHandler, logMessage
from Config.configFileFunction import Marketplace, getWriteDataToExcel

key = Marketplace('OZ').getKey

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
        responses = s.post(url=requestUrl, 
                           headers=key(), 
                           data=json.dumps(requestBody))
        posting = responses.json()['result']['postings']
        orders, products = parsereportOzonOrders(posting)
        getWriteDataToExcel(filename='Ozon отчёт по заказам', 
                            content=orders, 
                            sheet_name='Заказы')
        getWriteDataToExcel(filename='Ozon отчёт по заказам', 
                            content=products, 
                            sheet_name='Товары', 
                            mode='a')

def parsereportOzonOrders(orders: list = None):
    outputOrderList = []
    outputProductList = []
    if orders != None:
        for order in orders:
            outputOrderList.append({
                'Номер отправления': order['posting_number'], 
                'ID заказа': order['order_id'], 
                'Номер заказа': order['order_number'], 
                'Статус': order['status'],  
                'Дата создания': order['in_process_at'], 
                'Дата доставки': order['shipment_date'], 
                'дата отправки': order['delivering_date'],  
                'Экспресс': order['is_express'], 
                'Родительский номер отправления': order['parent_posting_number'], 
                'Подстатус': order['substatus'],
                'Отмена влияет на рейтинг': order['cancellation']['affect_cancellation_rating'],
                'Причина отмены': order['cancellation']['cancel_reason'],
                'ID причины отмены': order['cancellation']['cancel_reason_id'],
                'Инициатор отправления': order['cancellation']['cancellation_initiator'],
                'Тип отмены': order['cancellation']['cancellation_type'],
                'Отмена после доставки': order['cancellation']['cancelled_after_ship'],
                'Откуда': order['financial_data']['cluster_from'],
                'Куда': order['financial_data']['cluster_to']
                })
            product = order['products']
            finProduct = order['financial_data']['products']
            for i in range(len(product)):
                outputProductList.append({
                    'ID заказа': order['order_id'],
                    'Сумма комиссии': finProduct[i]['commission_amount'],
                    '% комиссии': finProduct[i]['commission_percent'],
                    'К перечислени': finProduct[i]['payout'],
                    'ID продукта': finProduct[i]['product_id'],
                    'Цена до скидок': finProduct[i]['old_price'],
                    'Цена': finProduct[i]['price'],
                    'Сумма скидки': finProduct[i]['total_discount_value'],
                    '% скидки': finProduct[i]['total_discount_percent'],
                    'Количество': finProduct[i]['quantity'],
                    'Цена для клиета': finProduct[i]['client_price'],
                    'Цена.product': product[i]['price'],
                    'Артикул.product': product[i]['offer_id'],
                    'Наименование.product': product[i]['name'],
                    'SKU.product': product[i]['sku'],
                    'количество.product': product[i]['quantity'],
                    'CIS.product': product[i]['mandatory_mark'],
                    'Последняя миля': finProduct[i]['item_services']["marketplace_service_item_fulfillment"],
                    'Магистраль': finProduct[i]['item_services']["marketplace_service_item_pickup"],
                    'Обработка отправления на ФФ складе': finProduct[i]['item_services']["marketplace_service_item_dropoff_pvz"],
                    'Обработка отправления в ПВЗ': finProduct[i]['item_services']["marketplace_service_item_dropoff_sc"],
                    'Обработка отправления в СЦ': finProduct[i]['item_services']["marketplace_service_item_dropoff_ff"],
                    'Сборка заказа': finProduct[i]['item_services']["marketplace_service_item_direct_flow_trans"],
                    'Забор отправления от адреса продавца': finProduct[i]['item_services']["marketplace_service_item_return_flow_trans"],
                    'Обработка возврата': finProduct[i]['item_services']["marketplace_service_item_deliv_to_customer"],
                    'Обратная магистраль': finProduct[i]['item_services']["marketplace_service_item_return_not_deliv_to_customer"],
                    'Обработка отмен': finProduct[i]['item_services']["marketplace_service_item_return_part_goods_customer"],
                    'Обработка невыкупа': finProduct[i]['item_services']["marketplace_service_item_return_after_deliv_to_customer"]
                })
        return outputOrderList, outputProductList
    else:
        print('Ничего не передано')




if __name__=='__main__':
    reportOzonOrders()    