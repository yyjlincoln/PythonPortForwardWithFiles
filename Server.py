import SuproMain as s
import time
print('Server')
s.server(('localhost',int(input('Please input the server port>'))),id=str(input('Please input an id (same as the server)>')))
while 1:
    time.sleep(1000)
