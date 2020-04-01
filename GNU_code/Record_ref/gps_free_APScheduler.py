from datetime import datetime, date, time
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
# We can't get the backgroundScheduler to work. :(
from scheduler_Runner import record



def my_job(schedDate, center_frequency, channel_frequency, sampleRate, sampleLength, fileDirectory,
           debuggerFile, hackrf_index):
    ######################### Start Function Call #########################
    currentTime=datetime.now()
    record(schedDate, center_frequency, channel_frequency, currentTime, sampleRate, sampleLength, fileDirectory,
           debuggerFile, hackrf_index, GPShandler=None)


# Function to convert utc to local time, not used.
#https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime
def utc2local(utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset

def schedule(fileName, hackrf_index, fileDirectory):
    startUp = datetime.now()
    debuggerFile = open(
        '/home/pi/Documents/schedulerDebugger' + str(startUp).replace(" ", "_").replace(":", "_").replace(".","_") + '.txt',"w+")
    debuggerFile.write("Scheduler Starting Up. Time: " + str(startUp) + '\n')
    print("Scheduler Starting Up. Time: " + str(startUp))

    sched = BlockingScheduler()
    # BackgroundScheduler may be better suited, but we can't get it work. It'll schedule, but it won't execute.
    # sched = BackgroundScheduler()

    # Read the times from the input text file.
    Date = []
    Doppler = []
    Length = []
    sampleRate = 2000000

    # IMPORTANT: Cannot have extra white space at end of InputTimes.txt. It will throw "index out of range" error
    # fileName = 'InputTimes.txt'
    import csv

    count=0
    with open('/home/pi/GIT_GNU/GNU/GNU_code/Record_ref/' + fileName) as f:
        # with open('/home/pi/GPS/Unification_Attempt/'+fileName) as f:
        reader = csv.reader(f, delimiter='\n')
        for row in reader:
            Str = str.split(row[0], ",")
            # print("Raw String: "+Str[0]) %Debugging.
            h1 = datetime.strptime(Str[0], "%Y-%m-%dT%H:%M:%S.%f")
            Date.append(h1)
            Doppler.append(float(Str[1]))
            Length.append(float(Str[2]))
            print("Before Schedule utc: " + str(h1))
            debuggerFile.write("Before Schedule utc: " + str(h1) + '\n')
            # os.system("sudo echo "+"Before Schedule utc: " + str(h1)+" >> /home/pi/Documents/debugger.txt 2>&1")
            sched.add_job(my_job, 'date', run_date=h1, args=[Date[count],Doppler[count]-0.5,Doppler[count],
                   sampleRate,Length[count],fileDirectory,debuggerFile,hackrf_index])
            count += 1

    sched.start()