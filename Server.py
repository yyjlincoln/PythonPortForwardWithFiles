import SuproMain as s
import time
print('Server')
s.server(('localhost',int(input('Please input the server port>'))))
while 1:
    time.sleep(1000)
