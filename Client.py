import SuMa as s
import time
print('Client')
s.client(('localhost',int(input('Please enter the server port>'))),('localhost',81),id=str(input('Please input an id>')))
while 1:
    time.sleep(1000)
