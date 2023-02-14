import json
import logging
import os
import sys
import time
from datetime import datetime
from logging import handlers
from pprint import PrettyPrinter
from random import randint
from websocket import create_connection

def openconnection():
        global ws
        global api_data
#       ws = create_connection("wss://api.stage.dydx.exchange/v3/ws")
        ws = create_connection("wss://api.dydx.exchange/v3/ws")
        api_data = {
                "type": "subscribe",
                "channel": "v3_trades",
                "id": market
        }
        ws.send(json.dumps(api_data))
        api_data = ws.recv()
        api_data = json.loads(api_data)
        pp.pprint(api_data)
        api_data = ws.recv()
        api_data = json.loads(api_data)
        pp.pprint(api_data)

def checkwidth(elementname, elementsize):
        global maxwidthtradeprice
        global maxwidthtradesize
        if elementname == 'tradeprice' and elementsize > maxwidthtradeprice:
                fp = open(ramdiskpath+'/'+market+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthtradeprice = elementsize
        elif elementname == 'tradesize' and elementsize > maxwidthtradesize:
                fp = open(ramdiskpath+'/'+market+'/maxwidth'+elementname, "w")
                fp.write(str(elementsize)+'\n')
                fp.close()
                maxwidthtradesize = elementsize

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' dydxtrades.py')
logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)
pp = PrettyPrinter(width = 41, compact = True)
if sys.platform == "linux" or sys.platform == "linux2":
        # linux
        ramdiskpath = '/mnt/ramdisk'
elif sys.platform == "darwin":
        # OS X
        ramdiskpath = '/Volumes/RAMDisk'

if len(sys.argv) < 2:
        market = 'BTC-USD'
else:
        market = sys.argv[1]
handler = logging.handlers.RotatingFileHandler(ramdiskpath+'/dydxtrades'+market+'.log',
        maxBytes = 2097152,
        backupCount = 4
)
logger.addHandler(handler)

if os.path.isdir(ramdiskpath) == False:
        print('Error: Ramdisk', ramdiskpath, 'not mounted')
        sys.exit()
if os.path.ismount(ramdiskpath) == False:
        print('Warning:', ramdiskpath, 'is not a mount point')
if os.path.isdir(ramdiskpath+'/'+market) == False:
        os.system('mkdir -p '+ramdiskpath+'/'+market)

maxwidthtradeprice = 0
maxwidthtradesize = 0
openconnection()
while True:
        try:
                trades = api_data['contents']['trades'][0]
                tradecreatedat = trades['createdAt']
                tradeliquidation = trades['liquidation']
                tradeprice = trades['price']
                tradeside = trades['side']
                tradesize = trades['size']
                if tradeliquidation == True:
                        liquidationstring = 'L'
                        fp = open(ramdiskpath+'/'+market+'/liquidations', "a")
                        fp.write(tradecreatedat+' '+tradeprice+' '+tradeside+' ('+tradesize+')L\n')
                        fp.close()
                else:
                        liquidationstring = ''
                fp = open(ramdiskpath+'/'+market+'/lasttrade', "w")
                fp.write(tradecreatedat+' '+tradeprice+' '+tradeside+' ('+tradesize+')'+liquidationstring+'\n')
                fp.close()
                logger.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' '+tradecreatedat+' '+tradeprice+' '+tradeside.ljust(4)+' ('+tradesize+')'+liquidationstring)
                checkwidth('tradeprice', len(tradeprice))
                checkwidth('tradesize', len(tradesize))
                api_data = ws.recv()
                api_data = json.loads(api_data)
        except KeyboardInterrupt:
                ws.close()
                sys.exit(0)
        except Exception as error:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "WebSocket message failed (%s)" % error)
                ws.close()
                time.sleep(1)
                try:
                        openconnection()
                except Exception as error:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "WebSocket message failed (%s)" % error)
                        ws.close()
                        time.sleep(randint(1,10))
