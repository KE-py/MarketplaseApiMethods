import os
import pandas as pd
import openpyxl
from json import load
from configLog import logEventHandler, logMessage

@logEventHandler
def getPath(directory: str ='\Data\Reports', filename: str = 'Unknow_report'):
    return os.getcwd()+directory+f"\{filename}"

@logEventHandler
def getKeyHeaders(keyFor: str | None = None):
    filePath = getPath(directory='\Data\keys', filename='Secret-key')+".json"
    fileExist = os.path.isfile(filePath)
    if fileExist:
        logMessage(level=25, content='[SUCCESS] Файл ключей получен')
        with open(file=filePath, mode='r', encoding='utf-8') as file:
            return load(fp=file)[keyFor]
    else:
        logMessage(level=30, content=f'[WARNING] Отсутвует файл ключей по директории: \n {filePath}')
        
        
@logEventHandler
def getWriteDataToExcel(filename: str | None = None, conten: list = None):
    filePath = getPath(directory='\Data\Reports', filename=filename)+".xlsx"
    dfData = []
    dfColumns = list(conten[0].keys())
    for order in conten:
        x = list(order.values())
        dfData.append(x)
    df = pd.DataFrame(data=dfData,columns=dfColumns)
    df.to_excel(filePath, sheet_name='Data',index=False)
    logMessage(level=25, content='[SUCCESS] Отчет успешно сформирован')