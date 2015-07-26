# module for logging data somwhere
import csv, datetime

def textLog(FN, T, V1, V2, V3):
	fileH = open(	FN, 'a', newline='') #open with append option to add data to existing file
	fObj = csv.writer(fileH)
	fObj.writerow( [T, V1, V2, V3] )
	del fObj
	fileH.close()

def textLogInit(FN):
	filehandler = open(	FN , 'w', newline='') #option w creates new file for Writing
	fileObject = csv.writer(filehandler)
	fileObject.writerow( [datetime.datetime.now(), 0, 0, 0] )
	del fileObject
	filehandler.close()	
	
