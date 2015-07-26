#FermLog.py

import time, datetime #glob, os
import urllib, urllib.request

from LCD import LCDupdate
from CloudLog import textLogInit, textLog 
from DS18B20 import read_temp, OneW_init

THINGSPEAKKEY = '34LFZZ49UNKUFHNV'
THINGSPEAKURL = 'https://api.thingspeak.com/update'
FURL1 = 'https://api.thingspeak.com/update?key=34LFZZ49UNKUFHNV&field1='
FURL2 = '&field2='
FURL3 = '&field3='

print('starting...')    #printing in prompt

df1, df2, df3 = OneW_init()

print("T1: ", read_temp(df1))
print("T2: ", read_temp(df2))
print("T3: ", read_temp(df3))
var=0

#Starting Loop

try:

	while True:
		TempRead1 = read_temp(df1)
		#print("current temperature 1 is ", TempRead1, "degree Celsius" )
				
		TempRead2 = read_temp(df2)
		#print("current temperature 2 is ", TempRead2, "degree Celsius" )
				
		TempRead3 = read_temp(df3)
		#print("current temperature 1-2-3 is ", TempRead3, TempRead2, TempRead3, "degree Celsius at", datetime.datetime.now() )

		out = urllib.request.urlopen((FURL1+str(TempRead1)
                                              +FURL2+str(TempRead2)
                                              +FURL3+str(TempRead3)), None)

		LCDupdate(TempRead1, TempRead2, TempRead3)

		print("cycle",var," processed at", datetime.datetime.now(),
                      "with T1 =", TempRead1, "and T2=", TempRead2,
                      "and T3=", TempRead3)
		var = var + 1
		time.sleep(5)
    
except KeyboardInterrupt:
    #proc1.terminate()
    #proc2.terminate()
    print(" Program interruppted by keyboard!")
#    return


var=0
print( "Goodbye")
