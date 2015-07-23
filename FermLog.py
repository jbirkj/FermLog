
import time, datetime, sys
import gspread
#from tkinter import *

sys.path.append("/home/pi/git/quick2wire-python-api")

from subprocess import Popen, PIPE
from quick2wire.i2c import I2CMaster, writing_bytes, reading

from Logging import textLog, textLogInit

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

def I2CWrite(value1) :
    I2CMaster().transaction( writing_bytes(address, value1) )
    time.sleep(0.1)
    return 1

def I2CRead():
    time.sleep(1)
    read = I2CMaster().transaction( reading(address, 1) )[0]
    time.sleep(1)
    return read

def GoogleSubmit(value1, value2, value3):
    try:
        gs = gspread.login('jesperbirkp@gmail.com', 'zxkfdgmtpslbqpzg')
    except:
        print('fail')
        sys.exit
    wks = gs.open("TempLog1").sheet1
    
    #writing to Google sheet
    values = [ datetime.datetime.now(), 'sensor', value1, value2, value3]
    wks.append_row(values)
    
    #wks.close()
    

print('starting...')    #printing in prompt

path = "./DS18b20read.a "
path1 = path + sRomCode5
path2 = path + sRomCode2
path3 = path + sRomCode3
print(path1)
print(path2)
print(path3)

# creating lof file
logFileName = datetime.datetime.now().strftime("%y%m%d") + "FermentLogFile.csv"
textLogInit(logFileName)

#Starting Loop

try:

	while True:
		#proc = Popen(["sudo ./DS18b20read.a "],
		proc1 = Popen(path1 ,shell=True, stdout=PIPE)
		stdoutvalue = proc1.communicate()
		TempRead1 = eval(stdoutvalue[0])
		#print("current temperature 1 is ", TempRead1, "degree Celsius" )
				
		proc2 = Popen(path2 , shell=True, stdout=PIPE)
		stdoutvalue = proc2.communicate()
		TempRead2 = eval(stdoutvalue[0])
		#print("current temperature 2 is ", TempRead2, "degree Celsius" )
				
		proc3 = Popen(path3 , shell=True, stdout=PIPE)
		stdoutvalue = proc3.communicate()
		TempRead3 = eval(stdoutvalue[0])
		print("current temperature 1-2-3 is ", TempRead3, TempRead2, TempRead3, "degree Celsius at", datetime.datetime.now() )
		
		#GoogleSubmit(TempRead1, TempRead2, TempRead3)
		textLog(logFileName, datetime.datetime.now(), TempRead1, TempRead2, TempRead3 )


		# Write to LCD - clear displa and move cursor to start
		I2CWrite(0xFE)
		I2CWrite(0x58)
		
		# writing LCD line1 with "Temp1="
		for a in range(len(Tekst)):
			I2CWrite(Tekst[a])
		I2CWrite(0x30+(int(TempRead1/10)))      
		I2CWrite(0x30+TempRead1%10)             
		
		#cont line wirting " Temp3=
		for a in range(len(Tekst1)):
			I2CWrite(Tekst1[a])
		I2CWrite(0x30+(int(TempRead3/10)))      
		I2CWrite(0x30+TempRead3%10)             
		
		# writing LCD line 2 with Temp2
		for a in range(len(Tekst2)):
			I2CWrite(Tekst2[a])
		I2CWrite(0x30+(int(TempRead2/10)))
		I2CWrite(0x30+TempRead2%10)
		
		time.sleep(3600)
    
except KeyboardInterrupt:
    #proc1.terminate()
    #proc2.terminate()
    print("program interruppted by keyboard!")
#    return


var=0
print( "Goodbye")
