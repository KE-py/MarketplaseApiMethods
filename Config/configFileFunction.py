import os
import pandas as pd
import openpyxl
from json import load
from .configLog import logEventHandler, logMessage

class Marketplace():
    def __init__(self, mp):
        match mp:
            case 'OZ':
                self.marketplaceName = 'OZ'
            case 'YM':
                self.marketplaceName = 'YM'
            case 'WBStatic':
                self.marketplaceName = 'WBStatic'
            case 'WBStandart':
                self.marketplaceName = 'WBStandart'
            case _:
                raise ValueError('Введено неверное значение')
                
    @logEventHandler    
    def getKey(self):
        filePath = getPath(directory='\Data\keys', filename='Secret-key')+".json"
        fileExist = os.path.isfile(filePath)
        if fileExist:
            logMessage(level=25, content='[SUCCESS] Файл ключей получен')
            with open(file=filePath, mode='r', encoding='utf-8') as file:
                return load(fp=file)[self.marketplaceName]
        else:
            logMessage(level=30, content=f'[WARNING] Отсутвует файл ключей по директории: \n {filePath}')

@logEventHandler
def getPath(directory: str ='\Data\Reports', filename: str = 'Unknow_report'):
    return os.getcwd()+directory+f"\{filename}"      
        
@logEventHandler
def getWriteDataToExcel(filename: str | list | None = None, content: list = None,sheet_name: str | list ='Data', mode: str = 'w'):
    filePath = getPath(directory='\Data\Reports', filename=filename)+".xlsx"
    dfData = []
    dfColumns = list(content[0].keys())
    for order in content:
        x = list(order.values())
        dfData.append(x)
    df = pd.DataFrame(data=dfData,columns=dfColumns)
    with pd.ExcelWriter(filePath, mode = mode) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    logMessage(level=25, content='[SUCCESS] Отчет успешно сформирован')
