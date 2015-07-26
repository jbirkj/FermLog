#DS18b20.py

import time, glob, os
import subprocess

from subprocess import Popen, PIPE

#One wire labelling
#//1=build into metal, 2=2nd w short wiremount, 3=3rd w long wiremount, 4=loose 18B20 
#//5=metal tip w silicone tube


def OneW_init():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    device_file1 = '/sys/bus/w1/devices/28-0000049cd8a6/w1_slave'
    device_file2 = '/sys/bus/w1/devices/28-000005454cf7/w1_slave'
    device_file3 = '/sys/bus/w1/devices/28-000004e01b0c/w1_slave'

    return device_file1, device_file2, device_file3
   


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
