from Config.configLog import logEventHandler, logMessage



@logEventHandler
def sum():
    100/0

sum()

print('Hello world')