import SuproMain as s
import time
print('Client')
s.client(('localhost',int(input('Please enter the server port>'))),('localhost',81))
while 1:
    time.sleep(1000)
