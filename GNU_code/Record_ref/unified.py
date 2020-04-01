import L76X

import time
from datetime import datetime, date
from scheduler_Runner import getCurrentTime
from scheduler_Runner import record

# Unified.py uses the GPS and a custom scheduler (infinite while loop). This is the preferred method currently because
# it is easier to debug and you can use GPS time without setting the system time. Call using scheduler_Runner.py
def schedule(fileName,hackrf_index,fileDirectory):

    startUp=datetime.now()
    debuggerFile = open(fileDirectory+'schedulerDebugger'+str(startUp).replace(" ", "_").replace(":", "_").replace(".", "_")+'.txt', "w+")
    debuggerFile.write("Scheduler Starting Up. Time: "+str(startUp)+'\n')
    print("Scheduler Starting Up. Time: "+str(startUp))

    x=[]

    # ################################################################################
    # Comment out these lines to turn off the GPS
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
    # Comment out above to turn off the GPS
    # ################################################################################

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
    # fileName='InputTimes.txt'
    import csv
    with open('/home/pi/GIT_GNU/GNU/GNU_code/Record_ref/'+fileName) as f:
    # with open('/home/pentoo/Documents/GIT_GNU/GNU/GNU_code/Record_ref/'+fileName) as f: #Example of another directory.
        reader=csv.reader(f,delimiter='\n')
        for row in reader:
            Str=str.split(row[0],",")
            # print("Raw String: "+Str[0]) #For debugging.
            h1=datetime.strptime(Str[0],"%Y-%m-%dT%H:%M:%S.%f")
            Date.append(h1)
            Doppler.append(float(Str[1]))
            Length.append(float(Str[2]))
            print("Before Schedule utc: " + str(h1))
            debuggerFile.write("Before Schedule utc: " + str(h1) + '\n')
            # Use to port output to a textfile using the os.
            # os.system("sudo echo "+"Before Schedule utc: " + str(h1)+" >> /home/pi/Documents/debugger.txt 2>&1")

    i=0
    # Remove times that already passed.
    fountAtLeastOne=0
    currentTime,GPS,x=getCurrentTime(x,debuggerFile)
    while i<len(Date):
        if currentTime>=Date[i]:
            i=i+1
        else:
            fountAtLeastOne=1
            break

    if fountAtLeastOne==0:
        debuggerFile.write("All scheduled times are in the past! Check the dates carefully. If the dates are correct,"
                          "check the internal computer clock. Perhaps it is out of sync.")
        raise ImportError("All scheduled times are in the past! Check the dates carefully. If the dates are correct,"
                          "check the internal computer clock. Perhaps it is out of sync.")

    # Main Loop. The Scheduler.
    while (i<len(Date)):

        currentTime, GPS,x = getCurrentTime(x,debuggerFile)
        # Compare current time and the set times.
        if currentTime>=Date[i]:

            ######################### Start Function Call #########################
            record(schedDate=Date[i],center_frequency=Doppler[i]-0.5,channel_frequency=Doppler[i],currentTime=currentTime,
                   sampleRate=sampleRate,sampleLength=Length[i],fileDirectory=fileDirectory,debuggerFile=debuggerFile,
                   hackrf_index=hackrf_index,GPShandler=x)

            # Count up the Index.
            i+=1

            if i>=len(Date):
                # We've looped through the list.
                break
        else:
            # Time has not lined up yet, continue.
            continue

    # os.system("sudo echo All Scheduled Times Completed >> /home/pi/Documents/debugger.txt 2>&1")
    debuggerFile.write("All scheduled Times Completed. Time: " + str(datetime.now()) + '\n')
    print("All scheduled Times Completed. Time: " + str(datetime.now()))








