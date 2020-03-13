from datetime import datetime, date, time
import time
import record_ref
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import os



def my_job(Date,Doppler,Length,debuggerFile):
    ######################### Start Function Call #########################
    currentTime=datetime.now()
    fileDirectory = '/home/pi/Documents/'
    if Doppler > 0:
        top = record_ref
        tb = top.record_ref(center_freq=437000000, channel_freq=int(round(Doppler * 1e6)),
                                          file_loc=fileDirectory + 'Sat_Time' + str(currentTime).replace(" ",
                                                                                                         "_").replace(
                                              ":", "_").replace(".", "_"),
                                          num_samples=int(round(Length * sampleRate)),
                                          samp_rate=sampleRate)
        afterSetup = datetime.now()
        print("After calling class constructor: " + str(afterSetup))
        debuggerFile.write("After calling class constructor: " + str(afterSetup) + '\n')
        tb.start()
        afterStartingGNU = datetime.now()
        print("After calling tb.start(): " + str(afterStartingGNU))
        debuggerFile.write("After calling tb.start(): " + str(afterStartingGNU) + '\n')
        tb.wait()
        afterFinishingGNU = datetime.now()
        print("After calling tb.wait(): " + str(afterFinishingGNU))
        debuggerFile.write("After calling tb.wait(): " + str(afterFinishingGNU) + '\n')
        del tb
        String = 'python /home/pi/GIT_GNU/GNU/GNU_code/Record_ref/record_ref.py --channel-freq=' + str(
            int(round(Doppler * 1e6))) + ' --samp-rate=' + str(
            sampleRate) + ' --center-freq=437000000 --num-samples=' + str(
            int(round(Length * sampleRate))) + ' --file-loc="/home/pi/Documents/Sat_Time' + str(currentTime).replace(
            " ", "_").replace(":", "_").replace(".", "_") + '"'
    else:

        top = record_ref
        tb = top.record_ref(center_freq=97000000, channel_freq=97900000,
                                          file_loc=fileDirectory + '/Ref_Time' + str(currentTime).replace(" ",
                                                                                                          "_").replace(
                                              ":", "_").replace(".", "_"),
                                          num_samples=int(round(Length * sampleRate)),
                                          samp_rate=sampleRate)
        afterSetup = datetime.now()
        print("After calling class constructor: " + str(afterSetup))
        debuggerFile.write("After calling class constructor: " + str(afterSetup) + '\n')

        tb.start()
        afterStartingGNU = datetime.now()
        print("After calling tb.start(): " + str(afterStartingGNU))
        debuggerFile.write("After calling tb.start(): " + str(afterStartingGNU) + '\n')

        tb.wait()
        # Use this along with fg.close for timing tests WITHOUT GNU radio.
        # fg=open('/home/pi/Documents/Ref_Time' + str(currentTime).replace(" ", "_").replace(":", "_").replace(".", "_"),'w+')
        afterFinishingGNU = datetime.now()
        print("After calling tb.wait(): " + str(afterFinishingGNU))
        debuggerFile.write("After calling tb.wait(): " + str(afterFinishingGNU) + '\n')

        del tb
        # fg.close()

        String = 'python /home/pi/GIT_GNU/GNU/GNU_code/Record_ref/record_ref.py --channel-freq=' + '97900000' + ' --samp-rate=' + str(
            sampleRate) + ' --center-freq=97000000 --num-samples=' + str(
            int(round(Length * sampleRate))) + ' --file-loc="/home/pi/Documents/Ref_Time' + str(
            currentTime).replace(" ", "_").replace(":", "_").replace(".", "_") + '"'

    # time.sleep(10)
    # String="date >> /home/pi/Documents/debugger.txt 2>&1"
    # String="date >> /home/pi/Documents/TimingTest.txt 2>&1"
    # print(Doppler)
    # print(String)
    # os.system("sudo echo "+String+" >> /home/pi/Documents/debugger.txt 2>&1")
    debuggerFile.write("Completed hackRF call. Time: " + str(datetime.now()) + '\n')
    debuggerFile.write("HackRf String Call: " + '\n')
    debuggerFile.write(String + '\n')
    print("Completed hackRF call. Time: " + str(datetime.now()))
    print("HackRf String Call: ")
    print(String)

    # Goal now is to find the data file we just created and rename it.
    queryString = str(currentTime).replace(" ", "_").replace(":", "_").replace(".", "_")
    files = []
    for (dirpath, dirnames, filenames) in os.walk(fileDirectory):
        files.extend(filenames)
        break

    for currentFile in files:
        if currentFile.__contains__(queryString):
            # Now we rename the file
            # Time_Scheduled_2020-MM-DD_HH_mm_SS_ffffff_atEntry_SS_fffffff_afterSetup_SS_ffffff_afterStartingGNU_SS_ffffff_afterFinishingGNU_mm_SS_ffffff
            if currentFile.__contains__("."):
                extension = ".hdr"
            else:
                extension = ''

            if currentFile.__contains__("Sat"):
                prefix = "Sat_"
            else:
                prefix = "Ref_"

            scheduled = str(Date).replace(" ", "_").replace(":", "_").replace(".", "_")
            actuallyRanAt = "%s_%s" % (currentTime.second, str(currentTime.microsecond))
            afterSetupStr = "%s_%s" % (afterSetup.second, str(afterSetup.microsecond))
            afterStartingGNUStr = "%s_%s" % (afterStartingGNU.second, str(afterStartingGNU.microsecond))
            afterFinishingGNUStr = "%s_%s_%s" % (
            afterFinishingGNU.minute, afterFinishingGNU.second, str(afterFinishingGNU.microsecond))

            # print("FileName: ")
            # print('/home/pi/Documents/'+
            #           prefix+"Time_Scheduled_"+scheduled+"_atEntry_"+actuallyRanAt+"_afterSetup_"+afterSetupStr+
            #           "_afterStartingGNU_"+afterStartingGNUStr+"_afterFinishingGNU_"+afterFinishingGNUStr+extension)

            os.rename(r'' + fileDirectory + currentFile, r'' + fileDirectory +
                      prefix + "Time_Scheduled_" + scheduled + "_atEntry_" + actuallyRanAt + "_afterSetup_" + afterSetupStr +
                      "_afterStartingGNU_" + afterStartingGNUStr + "_afterFinishingGNU_" + afterFinishingGNUStr + extension)



#https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime
def utc2local(utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset

if __name__=='__main__':
    startUp = datetime.now()
    debuggerFile = open(
        '/home/pi/Documents/schedulerDebugger' + str(startUp).replace(" ", "_").replace(":", "_").replace(".","_") + '.txt',"w+")
    debuggerFile.write("Scheduler Starting Up. Time: " + str(startUp) + '\n')
    print("Scheduler Starting Up. Time: " + str(startUp))

    sched = BlockingScheduler()
    # sched = BackgroundScheduler()

    # Read the times from the input text file.
    Date = []
    Doppler = []
    Length = []
    sampleRate = 2000000

    # IMPORTANT: Cannot have extra white space at end of InputTimes.txt. It will throw "index out of range" error
    fileName = 'InputTimes.txt'
    import csv

    with open('/home/pi/GIT_GNU/GNU/GNU_code/Record_ref/' + fileName) as f:
        # with open('/home/pi/GPS/Unification_Attempt/'+fileName) as f:
        reader = csv.reader(f, delimiter='\n')
        for row in reader:
            Str = str.split(row[0], ",")
            # print("Raw String: "+Str[0])
            h1 = datetime.strptime(Str[0], "%Y-%m-%dT%H:%M:%S.%f")
            Date.append(h1)
            Doppler.append(float(Str[1]))
            Length.append(float(Str[2]))
            print("Before Schedule utc: " + str(h1))
            debuggerFile.write("Before Schedule utc: " + str(h1) + '\n')
            # os.system("sudo echo "+"Before Schedule utc: " + str(h1)+" >> /home/pi/Documents/debugger.txt 2>&1")

    # file1 = open("./DopplerAccess35932.txt")
    # transform cannot do decimals or dates.



    # stringAry=["2020-02-22T22:52:50.111","2020-02-22T22:52:50.111"]
    # stringAry=["2020-02-22T18:25:32.436","2020-02-22T18:25:46.352"]

    count=0
    for Str in Date:
        h1=datetime.strptime(Str,"%Y-%m-%dT%H:%M:%S.%f")
        outStr="Before Schedule utc: "+str(h1)
        print(outStr)
        debuggerFile.write(outStr+'\n')
        # h1=utc2local(h1)
        # print("Before Schedule local: "+str(h1))
        # sched.add_job(my_job,'date',run_date=h1,id='job'+str(count))
        sched.add_job(my_job,'date',run_date=h1,args=[Date[count],Doppler[count],Length[count],debuggerFile])
        count+=1
    # sched.add_job(my_job, 'date', run_date=datetime(2020, 2, 22, 12, 36, 33,43534), args=['testing'])

    sched.start()