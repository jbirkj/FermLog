
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

ROMCODE1 = [ 0x28, 0xc3, 0xc2, 0x9d, 0x04, 0x00, 0x00, 0x9b]
sRomCode1 = "40 195 194 157 4 0 0 155"
ROMCODE5 = [ 0x28, 0xe8, 0xd4, 0x45, 0x05, 0x00, 0x00, 0x83]
sRomCode5 = "40 232 212 69 5 0 0 131"
ROMCODE2 = [ 0x28, 0x0c, 0x1b, 0xe0, 0x04, 0x00, 0x00, 0xb8]
sRomCode2 = "40 12 27 224 4 0 0 184"
ROMCODE4 = [ 0x28, 0x2f, 0x90, 0x2d, 0x04, 0x00, 0x00, 0xd9]
sRomCode4 = "40 47 144 45 4 0 0 217"
ROMCODE3 = [ 0x28, 0xa6, 0xd8, 0x9c, 0x04, 0x00, 0x00, 0xfd]
sRomCode3 = "40 166 216 156 4 0 0 253"

#//1=build into metal, 2=2nd w short wiremount, 3=3rd w long wiremount, 4=loose 18B20 
#//5=metal tip w silicone tube
#cROMCODE1[0]=0x28;	cROMCODE2[0]=0x28;	cROMCODE3[0]=0x28;	cROMCODE4[0]=0x28;	cROMCODE5[0]=0x28;
#cROMCODE1[1]=0xc3;	cROMCODE2[1]=0x0c;	cROMCODE3[1]=0xa6;	cROMCODE4[1]=0x2f;	cROMCODE5[1]=0xe8;
#cROMCODE1[2]=0xc2;	cROMCODE2[2]=0x1b;	cROMCODE3[2]=0xd8;	cROMCODE4[2]=0x90;	cROMCODE5[2]=0xd4;
#cROMCODE1[3]=0x9d;	cROMCODE2[3]=0xe0;	cROMCODE3[3]=0x9c;	cROMCODE4[3]=0x2d;	cROMCODE5[3]=0x45;
#cROMCODE1[4]=0x04;	cROMCODE2[4]=0x04;	cROMCODE3[4]=0x04;	cROMCODE4[4]=0x04;	cROMCODE5[4]=0x05;
#cROMCODE1[5]=0x00;	cROMCODE2[5]=0x00;	cROMCODE3[5]=0x00;	cROMCODE4[5]=0x00;	cROMCODE5[5]=0x0;
#cROMCODE1[6]=0x00;	cROMCODE2[6]=0x00;	cROMCODE3[6]=0x00;	cROMCODE4[6]=0x00;	cROMCODE5[6]=0x0;
#cROMCODE1[7]=0x9b;	cROMCODE2[7]=0xb8;	cROMCODE3[7]=0xfd;	cROMCODE4[7]=0xd9;	cROMCODE5[7]=0x83;

THINGSPEAKKEY = '34LFZZ49UNKUFHNV'
THINGSPEAKURL = 'https://api.thingspeak.com/update'
FURL1 = 'https://api.thingspeak.com/update?key=34LFZZ49UNKUFHNV&field1='
FURL2 = '&field2='
FURL3 = '&field3='

def I2CWrite(value1) :
    #I2CMaster().transaction( writing_bytes(address, value1) )
    with I2CMaster() as bus:
        bus.transaction( writing_bytes(address, value1) )
#    time.sleep(0.1)
    #self.bus.close()
    #I2CMaster().close()
    return 1

def I2CRead():
    #time.sleep(1)
    #read = I2CMaster().transaction( reading(address, 1) )[0]
    with I2CMaster() as bus:
        read = bus.transaction( reading(address, 1) )[0]
#    time.sleep(1)
    #I2CMaster().close()
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

def sendData( url, key, field1, temp):
    print('1')
    values = {'key' : key, field1 : temp }
    
    postdata = urllib.parse.urlencode(values)
    print(postdata)
    req = urllib.request.Request(url, postdata)
    print(req)  
#    try:
    response = urllib.request.urlopen(req, None, 5)
    html_string = response.read()
    response.close()
    print('done')
#    except:
#        print('wrong')
   

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
'''
# creating lof file
logFileName = datetime.datetime.now().strftime("%y%m%d") + "FermentLogFile.csv"
textLogInit(logFileName)
'''
#Starting Loop

try:

	while True:
		TempRead1 = read_temp(device_file1)
		#print("current temperature 1 is ", TempRead1, "degree Celsius" )
				
		TempRead2 = read_temp(device_file2)
		#print("current temperature 2 is ", TempRead2, "degree Celsius" )
				
		TempRead3 = read_temp(device_file3)
		#print("current temperature 1-2-3 is ", TempRead3, TempRead2, TempRead3, "degree Celsius at", datetime.datetime.now() )
		
		#GoogleSubmit(TempRead1, TempRead2, TempRead3)
		#textLog(logFileName, datetime.datetime.now(), TempRead1, TempRead2, TempRead3 )

		out = urllib.request.urlopen((FURL1+str(TempRead1)
                                              +FURL2+str(TempRead2)
                                              +FURL3+str(TempRead3)), None)
		#out = urllib.request.urlopen((FURL2+str(TempRead2)), None)
		#out = urllib.request.urlopen(FURL1, None)
		
		#print(out)
                #sendData(THINGSPEAKURL, THINGSPEAKKEY, 'field1', 23)
                #sys.stdout.flush()
		#print('CLOUD LOG DONE')
		
		# Write to LCD - clear displa and move cursor to start
		I2CWrite(0xFE)
		I2CWrite(0x58)
		
		# writing LCD line1 with "Temp1="
		for a in range(len(Tekst)):
			I2CWrite(Tekst[a])
		I2CWrite(0x30+(int(TempRead1/10)))      
		I2CWrite(0x30+(int(TempRead1%10)))             
		
		'''#cont line wirting " Temp3=
		for a in range(len(Tekst1)):
			I2CWrite(Tekst1[a])
		I2CWrite(0x30+(int(TempRead3/10)))      
		I2CWrite(0x30+TempRead3%10)             
		'''
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
