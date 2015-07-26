
import time, datetime, sys, os, glob
import gspread
import urllib, urllib.request
import subprocess

sys.path.append("/home/pi/git/quick2wire-python-api")

from subprocess import Popen, PIPE
from quick2wire.i2c import I2CMaster, writing_bytes, reading

#from CloudLog import ThingSpeakLog

address = 0x28
Tekst = [ 0x54, 0x65, 0x6d, 0x70, 0x31, 0x3d ]		#"Temp1="
Tekst1 = [ 0x20, 0x54, 0x65, 0x6d, 0x70, 0x33, 0x3d ]	#" Temp3="
Tekst2 = [ 0xfe, 0x47, 0x01, 0x02, 0x54, 0x65, 0x6d, 0x70, 0x32, 0x3d ]  # næste linie, pos 1, "Temp2="

#One wire labelling
#//1=build into metal, 2=2nd w short wiremount, 3=3rd w long wiremount, 4=loose 18B20 
#//5=metal tip w silicone tube

THINGSPEAKKEY = '34LFZZ49UNKUFHNV'
THINGSPEAKURL = 'https://api.thingspeak.com/update'
FURL1 = 'https://api.thingspeak.com/update?key=34LFZZ49UNKUFHNV&field1='
FURL2 = '&field2='
FURL3 = '&field3='

def I2CWrite(value1) :
    with I2CMaster() as bus:
        bus.transaction( writing_bytes(address, value1) )
    return 1

def I2CRead():
    with I2CMaster() as bus:
        read = bus.transaction( reading(address, 1) )[0]
    return read

def read_temp_raw(deviceF):
#	f=open(device_file, 'r')
#	lines = f.readlines()
#	f.close()
#	return lines
	catdata = subprocess.Popen(['cat',deviceF],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
	out,err = catdata.communicate()
	out_decode = out.decode('utf-8')
	lines = out_decode.split('\n')
	return lines

def read_temp(deviceFile):
	line = read_temp_raw(deviceFile)
	while line[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		line = read_temp_raw()
	equals_pos = line[1].find('t=')
	if equals_pos != -1:
		temp_string = line[1][equals_pos+2:]
		temp_c = float(temp_string)/1000.0
		return temp_c

print('starting...')    #printing in prompt

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
device_file1 = '/sys/bus/w1/devices/28-0000049cd8a6/w1_slave'
device_file2 = '/sys/bus/w1/devices/28-000005454cf7/w1_slave'
device_file3 = '/sys/bus/w1/devices/28-000004e01b0c/w1_slave'

print("T1: ", read_temp(device_file1))
print("T2: ", read_temp(device_file2))
print("T3: ", read_temp(device_file3))
var=0


#Starting Loop

try:

	while True:
		TempRead1 = read_temp(device_file1)
		#print("current temperature 1 is ", TempRead1, "degree Celsius" )
				
		TempRead2 = read_temp(device_file2)
		#print("current temperature 2 is ", TempRead2, "degree Celsius" )
				
		TempRead3 = read_temp(device_file3)
		#print("current temperature 1-2-3 is ", TempRead3, TempRead2, TempRead3, "degree Celsius at", datetime.datetime.now() )
		
		out = urllib.request.urlopen((FURL1+str(TempRead1)
                                              +FURL2+str(TempRead2)
                                              +FURL3+str(TempRead3)), None)
		
		# Write to LCD - clear displa and move cursor to start
		I2CWrite(0xFE)
		I2CWrite(0x58)
		
		# writing LCD line1 with "Temp1="
		for a in range(len(Tekst)):
			I2CWrite(Tekst[a])
		I2CWrite(0x30+(int(TempRead1/10)))      
		I2CWrite(0x30+(int(TempRead1%10)))             
		
		#cont line wirting " Temp3=
		for a in range(len(Tekst1)):
			I2CWrite(Tekst1[a])
		I2CWrite(0x30+(int(TempRead3/10)))      
		I2CWrite(0x30+TempRead3%10)             
		
		# writing LCD line 2 with Temp2
		for a in range(len(Tekst2)):
			I2CWrite(Tekst2[a])
		I2CWrite(0x30+(int(TempRead2/10)))
		I2CWrite(0x30+(int(TempRead2%10)))
		print("cycle",var," processed at", datetime.datetime.now(),
                      "with T1 =", TempRead1, "and T2=", TempRead2,
                      "and T3=", TempRead3)
		var = var + 1
		time.sleep(5)
    
except KeyboardInterrupt:
    #proc1.terminate()
    #proc2.terminate()
    print("program interruppted by keyboard!")
#    return


var=0
print( "Goodbye")
