import loguru

log = loguru.logger
log.add('Data\Log\logs.log', 
        level=5, 
        catch=True, 
        backtrace=True,
        format="{time:HH:mm:ss} - {name} - {level} - {line} - {function} - {extra} - {message}", 
        encoding='utf-8',
        rotation='15 MB')        
logEventHandler = log.catch()

@logEventHandler
def logMessage(level: str | int = 10,content=None):
    match level:
        case 'trace' | 5:
            log.trace(content)
        case 'debug' | 10:
            log.debug(content)
        case 'info' | 20:
            log.info(content)
        case 'success' | 25:
            log.success(content)
        case 'warning' | 30:
            log.warning(content)
        case 'error' | 40:
            log.error(content)
        case 'critical' | 50:
            log.critical(content)
                        