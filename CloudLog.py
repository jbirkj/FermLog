# module for logging data somwhere
import csv, datetime

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
	
