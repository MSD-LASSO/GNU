import L76X
import time
import record_ref
from datetime import datetime, date
import math
# import os

def getCurrentTime(GPShandler,debuggerFile):
    try:
        GPShandler.L76X_Get()
        status=0
    except:
        debuggerFile.write("Failed To Get GPS. Time:" + str(datetime.now()) + '\n')
        print("Failed To Get GPS. Time:" + str(datetime.now()))
        # os.system("sudo echo Failed To Get GPS >> /home/pi/Documents/debugger.txt 2>&1")
        status=1
    # print('\n')

    #Get the current time to the best of our ability.
    if (status==0):
        # GPS=True
        # # 2020-3-1
        # # 20:17:2.5
        # Str=x.Date+'T'+x.Time
        # # Str='2020-3-1'+'T'+'20:17:2.5'
        # currentTime = datetime.strptime(Str, "%Y-%m-%dT%H:%M:%S.%f")
        GPS=False
        currentTime=datetime.now()

    else:
        # print('No positioning')
        GPS=False
        currentTime=datetime.now()

    debuggerFile.write("Using GPS: "+ str(GPS)+' Time: '+ str(currentTime) + '\n')
    print("Using GPS: "+ str(GPS)+' Time: '+ str(currentTime))
    # os.system("sudo echo Using GPS "+ str(GPS)+' Time '+ str(currentTime) + " >> /home/pi/Documents/debugger.txt 2>&1")
    return currentTime,GPS,GPShandler


debuggerFile = open(str('/home/pi/Documents/schedulerDebugger'+str(datetime.now())+'.txt'), "w+")
debuggerFile.write("Scheduler Starting Up. Time: "+str(datetime.now())+'\n')
print("Scheduler Starting Up. Time: "+str(datetime.now()))
# os.system("sudo echo IRan! >> /home/pi/Documents/debugger.txt 2>&1")
# try:
x = L76X.L76X()
x.L76X_Set_Baudrate(9600)
x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
time.sleep(2)
x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
time.sleep(2)
x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
time.sleep(2)
x.L76X_Set_Baudrate(115200)
x.L76X_Send_Command(x.SET_NMEA_BAUDRATE_115200)
time.sleep(2)

x.L76X_Send_Command(x.SET_POS_FIX_100MS);

# Set output message
x.L76X_Send_Command(x.SET_NMEA_OUTPUT);

debuggerFile.write("Completed GPS Setup. Time: "+str(datetime.now())+'\n')
print("Completed GPS Setup. Time: "+str(datetime.now()))


# x.L76X_Exit_BackupMode();

# f = open("Coordinates.txt", "w+")

i = 1.000;
ALat = 0.000
ALon = 0.000
AAlt = 0.000


# Read the times from the input text file.
Date=[]
Doppler=[]
Length=[]
sampleRate=2000000

#IMPORTANT: Cannot have extra white space at end of InputTimes.txt. It will throw "index out of range" error
fileName='InputTimes.txt'
import csv
with open('/home/pi/GIT_GNU/GNU/GNU_code/Record_ref/'+fileName) as f:
# with open('/home/pi/GPS/Unification_Attempt/'+fileName) as f:
    reader=csv.reader(f,delimiter='\n')
    for row in reader:
        Str=str.split(row[0],",")
        # print("Raw String: "+Str[0])
        h1=datetime.strptime(Str[0],"%Y-%m-%dT%H:%M:%S.%f")
        Date.append(h1)
        Doppler.append(float(Str[1]))
        Length.append(float(Str[2]))
        print("Before Schedule utc: " + str(h1))
        debuggerFile.write("Before Schedule utc: " + str(h1) + '\n')
        # os.system("sudo echo "+"Before Schedule utc: " + str(h1)+" >> /home/pi/Documents/debugger.txt 2>&1")

i=0
currentTime,GPS,x=getCurrentTime(x,debuggerFile)
while i<len(Date):
    if currentTime>=Date[i]:
        i=i+1
    else:
        break



while (i<len(Date)):

    currentTime, GPS,x = getCurrentTime(x,debuggerFile)
    # Compare current time and the set times.
    if currentTime>=Date[i]:
        # print('Scheduled Time: '+str(Date[i]))

        # String = datetime.now()
        # print('Before Function Call: '+str(String))

        ######################### Start Function Call #########################
        if Doppler[i] > 0:
            top=record_ref
            tb=top.record_ref(center_freq=437000000, channel_freq=int(round(Doppler[i]*1e6)), file_loc='/home/pi/Documents/Sat_Time'+str(currentTime).replace(" ","_").replace(":","_").replace(".","_"), num_samples=int(round(Length[i]*sampleRate)),
                                samp_rate=sampleRate)
            afterSetup=datetime.now()
            print("After calling class constructor: " + str(afterSetup))
            debuggerFile.write("After calling class constructor: " + str(afterSetup) + '\n')
            tb.start()
            afterStartingGNU=datetime.now()
            print("After calling tb.start(): " + str(afterStartingGNU))
            debuggerFile.write("After calling tb.start(): "+ str(afterStartingGNU) + '\n')
            tb.wait()
            afterFinishingGNU=datetime.now()
            print("After calling tb.wait(): " + str(afterFinishingGNU))
            debuggerFile.write("After calling tb.wait(): " + str(afterFinishingGNU) + '\n')
            del tb
            String='python /home/pi/GIT_GNU/GNU/GNU_code/Record_ref/record_ref.py --channel-freq='+str(int(round(Doppler[i]*1e6)))+' --samp-rate='+str(sampleRate)+' --center-freq=437000000 --num-samples='+str(int(round(Length[i]*sampleRate)))+' --file-loc="/home/pi/Documents/Sat_Time'+str(currentTime).replace(" ","_").replace(":","_").replace(".","_")+'"'
        else:
            # print("Before Calling GNU Code " + str(datetime.now()))
            # debuggerFile.write("Before Calling GNU Code " + str(datetime.now()) + '\n')
            top=record_ref
            tb=top.record_ref(center_freq=97000000, channel_freq=97900000, file_loc='/home/pi/Documents/Ref_Time'+str(currentTime).replace(" ","_").replace(":","_").replace(".","_"), num_samples=int(round(Length[i]*sampleRate)),
                                samp_rate=sampleRate)
            afterSetup=datetime.now()
            print("After calling class constructor: " + str(afterSetup))
            debuggerFile.write("After calling class constructor: " + str(afterSetup) + '\n')
            tb.start()
            afterStartingGNU=datetime.now()
            print("After calling tb.start(): " + str(afterStartingGNU))
            debuggerFile.write("After calling tb.start(): "+ str(afterStartingGNU) + '\n')
            tb.wait()
            afterFinishingGNU=datetime.now()
            print("After calling tb.wait(): " + str(afterFinishingGNU))
            debuggerFile.write("After calling tb.wait(): " + str(afterFinishingGNU) + '\n')
            del tb
            # print("After calling deleting tb: " + str(datetime.now()))
            # debuggerFile.write("After calling deleting tb: " + str(datetime.now()) + '\n')

            String = 'python /home/pi/GIT_GNU/GNU/GNU_code/Record_ref/record_ref.py --channel-freq=' + '97900000' + ' --samp-rate='+str(sampleRate)+' --center-freq=97000000 --num-samples='+str(int(round(Length[i]*sampleRate)))+' --file-loc="/home/pi/Documents/Ref_Time' + str(
                currentTime).replace(" ", "_").replace(":", "_").replace(".", "_") + '"'

        # time.sleep(10)
        # String="date >> /home/pi/Documents/debugger.txt 2>&1"
        # String="date >> /home/pi/Documents/TimingTest.txt 2>&1"
        # print(Doppler)
        # print(String)
        # os.system("sudo echo "+String+" >> /home/pi/Documents/debugger.txt 2>&1")
        debuggerFile.write("Completed hackRF call. Time: " + str(datetime.now()) + '\n')
        debuggerFile.write("HackRf String Call: "+'\n')
        debuggerFile.write(String+'\n')
        print("Completed hackRF call. Time: " + str(datetime.now()))
        print("HackRf String Call: ")
        print(String)


        #Goal now is to find the data file we just created and rename it.
        queryString=str(currentTime).replace(" ","_").replace(":","_").replace(".","_")
        for (dirpath, dirnames, filenames) in os.walk('/home/pi/Documents/'):
            files.extend(filenames)
            break

        for currentFile in files:
            if currentFile.__contains__(queryString):
                # Now we rename the file
                # Time_Scheduled_2020-MM-DD_HH_mm_SS_ffffff_atEntry_SS_fffffff_afterSetup_SS_ffffff_afterStartingGNU_SS_ffffff_afterFinishingGNU_mm_SS_ffffff
                if currentFile.__contains__("."):
                    extension=".hdr"
                else:
                    extension=''

                if currentFile.__contains__("Sat"):
                    prefix="Sat_"
                else:
                    prefix="Ref_"

                scheduled=str(Date[i]).replace(" ", "_").replace(":", "_").replace(".", "_")
                actuallyRanAt="%s_%s" % (currentTime.second, str(currentTime.microsecond))
                afterSetupStr="%s_%s" % (afterSetup.second, str(afterSetup.microsecond))
                afterStartingGNUStr="%s_%s" % (afterStartingGNU.second, str(afterStartingGNU.microsecond))
                afterFinishingGNUStr="%s_%s_%s" % (afterFinishingGNU.minute, afterFinishingGNU.second, str(afterFinishingGNU.microsecond))

                os.rename(r'/home/pi/Documents/'+currentFile+extension, r'/home/pi/Documents/'+
                          prefix+"Time_Scheduled_"+scheduled+"_atEntry_"+actuallyRanAt+"_afterSetup_"+afterSetupStr+
                          "_afterStartingGNU"+afterStartingGNUStr+"_afterFinishingGNU"+afterFinishingGNUStr+extension)


        # os.system(String)
        ######################### End Function Call #########################


        # String = datetime.now()
        # print('After Function Call: '+str(String))

        # print('\n')
        i+=1

        if i>=len(Date):
            # print("All scheduled Times Completed")
            break
    else:
        # Time has not lined up yet, continue.
        continue

# os.system("sudo echo All Scheduled Times Completed >> /home/pi/Documents/debugger.txt 2>&1")
debuggerFile.write("All scheduled Times Completed. Time: " + str(datetime.now()) + '\n')
print("All scheduled Times Completed. Time: " + str(datetime.now()))









