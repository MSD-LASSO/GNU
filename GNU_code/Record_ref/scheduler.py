from datetime import datetime, date, time
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import os



def my_job(Doppler):
    # f = open("/home/pi/Documents/OutputTimes.txt", "a")
    # print(f)
    # print(text)
    # global sched, count
    # print(datetime.now())
    # sched.remove_job('job'+str(count))
    # count+=1
    # os.system('date')
    if Doppler==440:
        # String='python /home/pi/GIT_GNU/GNU/GNU_code/Record_ref/record_ref.py --channel-freq='+str(int(round(Doppler*1e6)))+' --samp-rate=2000000 --center-freq=437000000 --num-samples=10000000 --file-loc="/home/pi/Documents/Time'+str(datetime.now()).replace(" ","_").replace(":","_").replace(".","_")+'"'
        String='python /home/pi/GIT_GNU/GNU/GNU_code/Record_ref/record_ref.py --channel-freq='+'437200000'+' --samp-rate=2000000 --center-freq=437000000 --num-samples=20000000 --file-loc="/home/pi/Documents/Time'+str(datetime.now()).replace(" ","_").replace(":","_").replace(".","_")+'"'
    else:
        # String='python /home/pi/GIT_GNU/GNU/GNU_code/Record_ref/record_ref.py --channel-freq='+'162400000'+' --samp-rate=2000000 --center-freq=162000000 --num-samples=10000000 --file-loc="/home/pi/Documents/Time'+str(datetime.now()).replace(" ","_").replace(":","_").replace(".","_")+'"'
        String='python /home/pi/GIT_GNU/GNU/GNU_code/Record_ref/record_ref.py --channel-freq='+'97900000'+' --samp-rate=2000000 --center-freq=97000000 --num-samples=10000000 --file-loc="/home/pi/Documents/Time'+str(datetime.now()).replace(" ","_").replace(":","_").replace(".","_")+'"'
    # String='hackrf_transfer -r /home/pi/Documents/Time'+str(datetime.now()).replace(" ","_").replace(":","_").replace(".","_")+' -s 2000000 -f 437250000 -p 1 -n 1200000000'
    # time.sleep(10)
    # String="date >> /home/pi/Documents/TimingTest.txt 2>&1"
    # String=datetime.now()
    print(str(String))
    os.system(String)
    # print(datetime.now())
    # f.write(str(datetime.now())+'\n')
    # f.close()

#https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime
def utc2local(utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset

if __name__=='__main__':
    sched = BlockingScheduler()
    # sched = BackgroundScheduler()

    Date=[]
    Doppler=[]
    import csv
    # with open('/home/pi/GIT_GNU/GNU/GNU_code/Record_ref/Dummy.txt') as f:
    with open('/home/pi/GIT_GNU/GNU/GNU_code/Record_ref/InputTimes.txt') as f:
        reader=csv.reader(f,delimiter='\t')
        for row in reader:
            Str=str.split(row[0],"    ")
            Date.append(Str[0])
            Doppler.append(float(Str[1]))

    # file1 = open("./DopplerAccess35932.txt")
    # transform cannot do decimals or dates.



    # stringAry=["2020-02-22T22:52:50.111","2020-02-22T22:52:50.111"]
    # stringAry=["2020-02-22T18:25:32.436","2020-02-22T18:25:46.352"]

    # The job will be executed on November 6th, 2009
    f = open("/home/pi/Documents/OutputTimes.txt", "w+")

    count=0
    for Str in Date:
        h1=datetime.strptime(Str,"%Y-%m-%dT%H:%M:%S.%f")
        outStr="Before Schedule utc: "+str(h1)
        print(outStr)
        f.write(outStr+'\n')
        # h1=utc2local(h1)
        # print("Before Schedule local: "+str(h1))
        # sched.add_job(my_job,'date',run_date=h1,id='job'+str(count))
        sched.add_job(my_job,'date',run_date=h1,args=[Doppler[count]])
        count+=1
    # sched.add_job(my_job, 'date', run_date=datetime(2020, 2, 22, 12, 36, 33,43534), args=['testing'])

    f.close()
    # count=0
    sched.start()