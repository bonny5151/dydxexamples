import datetime
import os
import sys
import time
from os.path import exists
from sys import platform

if platform == "linux" or platform == "linux2":
        # linux
        ramdiskpath = '/mnt/ramdisk'
elif platform == "darwin":
        # OS X
        ramdiskpath = '/Volumes/RAMDisk'
#Note: regular output needs 103 columns, compact 67, ultracompact 39

RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
CYAN = '\033[0;36m'
NC = '\033[0m' # No Color
REDWHITE = '\033[0;31m\u001b[47m'
GREENWHITE = '\033[0;32m\u001b[47m'

sep = " "
if len(sys.argv) < 2:
        market = 'BTC-USD'
else:
        market = sys.argv[1]
if len(sys.argv) < 3:
        depth = 10
else:
        depth = int(sys.argv[2])
if exists(ramdiskpath+'/'+market+'/asks') == False:
        print('Error: Asks directory', ramdiskpath+'/'+market+'/asks', 'not found')
        exit()
if exists(ramdiskpath+'/'+market+'/bids') == False:
        print('Error: Bids directory', ramdiskpath+'/'+market+'/bids', 'not found')
        exit()
if exists(ramdiskpath+'/'+market+'/lasttrade') == False:
        print('Error: lasttrade file', ramdiskpath+'/'+market+'/lasttrade', 'not found')
        exit()
while True:
        with open(ramdiskpath+'/'+market+'/lasttrade') as fp:
                for line in fp:
                        fname = line.strip('\n\r').split(sep)
                        fcreatedat = fname[0]
                        fprice = fname[1]
                        fside = fname[2]
                        fsize = fname[3]
        fp.close()
        askarray = []
        bidarray = []
        os.system('ls '+ramdiskpath+'/'+market+'/asks | sort -n > '+ramdiskpath+'/'+market+'/lista')
        os.system('ls '+ramdiskpath+'/'+market+'/bids | sort -n -r > '+ramdiskpath+'/'+market+'/listb')
        if fside == 'BUY':
                with open(ramdiskpath+'/'+market+'/lista') as fp:
                        for line in fp:
                                line = line.strip('\n\r')
                                if float(line) >= float(fprice):
                                        lowestask = float(line)
                                        break
                fp.close()
                with open(ramdiskpath+'/'+market+'/listb') as fp:
                        for line in fp:
                                line = line.strip('\n\r')
                                if float(line) < float(fprice):
                                        highestbid = float(line)
                                        break
                fp.close()
                count = 1
                with open(ramdiskpath+'/'+market+'/lista') as fp:
                        for line in fp:
                                line = line.strip('\n\r')
                                if count > depth:
                                        break
                                else:
                                        if float(line) > highestbid:
                                                with open(ramdiskpath+'/'+market+'/asks/'+line) as fp2:
                                                        for line2 in fp2:
                                                                fname = line2.strip('\n\r').split(sep)
                                                                faskoffset = fname[0]
                                                                fasksize = fname[1]
                                                                fdate = fname[2]
                                                                ftime = fname[3]
                                                                if fasksize != '0':
                                                                        askarray.append([line, fasksize, faskoffset, fdate, ftime])
                                                                        count += 1
                                                fp2.close()
                fp.close()
                count = 1
                with open(ramdiskpath+'/'+market+'/listb') as fp:
                        for line in fp:
                                line = line.strip('\n\r')
                                if count > depth:
                                        break
                                else:
                                        if float(line) < lowestask:
                                                with open(ramdiskpath+'/'+market+'/bids/'+line) as fp2:
                                                        for line2 in fp2:
                                                                fname = line2.strip('\n\r').split(sep)
                                                                fbidoffset = fname[0]
                                                                fbidsize = fname[1]
                                                                fdate = fname[2]
                                                                ftime = fname[3]
                                                                if fbidsize != '0':
                                                                        bidarray.append([line, fbidsize, fbidoffset, fdate, ftime])
                                                                        count += 1
                                                fp2.close()
                fp.close()
        else:
                with open(ramdiskpath+'/'+market+'/lista') as fp:
                        for line in fp:
                                line = line.strip('\n\r')
                                if float(line) > float(fprice):
                                        lowestask = float(line)
                                        break
                fp.close()
                with open(ramdiskpath+'/'+market+'/listb') as fp:
                        for line in fp:
                                line = line.strip('\n\r')
                                if float(line) <= float(fprice):
                                        highestbid = float(line)
                                        break
                fp.close()
                count = 1
                with open(ramdiskpath+'/'+market+'/lista') as fp:
                        for line in fp:
                                line = line.strip('\n\r')
                                if count > depth:
                                        break
                                else:
                                        if float(line) > highestbid:
                                                with open(ramdiskpath+'/'+market+'/asks/'+line) as fp2:
                                                        for line2 in fp2:
                                                                fname = line2.strip('\n\r').split(sep)
                                                                faskoffset = fname[0]
                                                                fasksize = fname[1]
                                                                fdate = fname[2]
                                                                ftime = fname[3]
                                                                if fasksize != '0':
                                                                        askarray.append([line, fasksize, faskoffset, fdate, ftime])
                                                                        count += 1
                                                fp2.close()
                fp.close()
                count = 1
                with open(ramdiskpath+'/'+market+'/listb') as fp:
                        for line in fp:
                                line = line.strip('\n\r')
                                if count > depth:
                                        break
                                else:
                                        if float(line) < lowestask:
                                                with open(ramdiskpath+'/'+market+'/bids/'+line) as fp2:
                                                        for line2 in fp2:
                                                                fname = line2.strip('\n\r').split(sep)
                                                                fbidoffset = fname[0]
                                                                fbidsize = fname[1]
                                                                fdate = fname[2]
                                                                ftime = fname[3]
                                                                if fbidsize != '0':
                                                                        bidarray.append([line, fbidsize, fbidoffset, fdate, ftime])
                                                                        count += 1
                                                fp2.close()
                fp.close()
        if len(sys.argv) > 3 and ( sys.argv[3] == 'compact' or sys.argv[3] == 'ultracompact' ):
                if sys.argv[3] == 'compact':
                        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), fcreatedat, fprice, fside, fsize)
                        print('Bid                              | Ask')
                elif sys.argv[3] == 'ultracompact':
                        print(fcreatedat[5:], fprice, fside, fsize)
                        print('Bid                | Ask')
        else:
                print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Last trade:', fcreatedat, fprice, fside, fsize)
                print('Bid                                                | Ask')
        count = 0
        highestoffset = 0
        bidsizetotal = 0
        asksizetotal = 0
        while count < depth:
                biditem = bidarray[count]
                biditemprice = biditem[0]
                biditemsize = biditem[1]
                biditemoffset = biditem[2]
                biditemdate = ' '+biditem[3]
                biditemtime = ' '+biditem[4]
                askitem = askarray[count]
                askitemprice = askitem[0]
                askitemsize = askitem[1]
                askitemoffset = askitem[2]
                askitemdate = ' '+askitem[3]
                askitemtime = ' '+askitem[4]
                highestoffset = max(int(biditemoffset), int(askitemoffset), highestoffset)
                bidsizetotal += float(biditemsize)
                asksizetotal += float(askitemsize)
                if count == 0:
                        lowestoffset = min(int(biditemoffset), int(askitemoffset))
                else:
                        lowestoffset = min(int(biditemoffset), int(askitemoffset), lowestoffset)
                if len(sys.argv) > 3 and ( sys.argv[3] == 'compact' or sys.argv[3] == 'ultracompact' ):
                        if sys.argv[3] == 'compact':
                                biditemoffset = ''
                                askitemoffset = ''
                                biditemdate = biditemdate[6:]
                                askitemdate = askitemdate[6:]
                        elif sys.argv[3] == 'ultracompact':
                                biditemoffset = ''
                                askitemoffset = ''
                                biditemdate = ''
                                askitemdate = ''
                                biditemtime = ''
                                askitemtime = ''
                else:
                        biditemoffset = ' '+biditemoffset
                        askitemoffset = ' '+askitemoffset
                print(biditemprice.ljust(7), str('('+biditemsize+')').ljust(10)+biditemoffset+biditemdate+biditemtime+' | '+askitemprice.ljust(7), str('('+askitemsize+')').ljust(10)+askitemoffset+askitemdate+askitemtime, end = '\r')
                if sys.argv[-1] != 'noansi':
                        if biditemprice == fprice:
                                print(REDWHITE+biditemprice+NC, end = '\r')
                        elif askitemprice == fprice:
                                print(biditemprice.ljust(7), str('('+biditemsize+')').ljust(10)+biditemoffset+biditemdate+biditemtime+' | '+GREENWHITE+askitemprice+NC, end = '\r')
                print()
                count += 1
        print('highgestbid:', highestbid)
        print('lowestask:', lowestask)
        print('bidvolume:', bidsizetotal)
        print('askvolume:', asksizetotal)
        print('minoffset:', lowestoffset)
        print('maxoffset:', highestoffset, '(+'+str(highestoffset - lowestoffset)+')')
        time.sleep(1)
