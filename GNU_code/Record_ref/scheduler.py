from datetime import datetime, date, time
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import os



def my_job(Doppler):
    # print(text)
    # global sched, count
    # print(datetime.now())
    # sched.remove_job('job'+str(count))
    # count+=1
    # os.system('date')
    print('python record_ref.py --channel-freq='+str(int(round(Doppler*1e6)))+' --samp-rate=2000000 --center-freq=437 --num-samples=6000000 --file-loc="/home/pi/Documents/Time'+str(datetime.now())+'"')
    os.system('python record_ref.py --channel-freq='+str(int(round(Doppler*1e6)))+' --samp-rate=2000000 --center-freq=437 --num-samples=6000000 --file-loc="/home/pi/Documents/Time"'+str(datetime.now()))

#https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime
def utc2local(utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset

if __name__=='__main__':
    sched = BlockingScheduler()

    Date=[]
    Doppler=[]
    import csv
    with open('./Dummy.txt') as f:
    # with open('./DopplerAccess35932.txt') as f:
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
    count=0
    for Str in Date:
        h1=datetime.strptime(Str,"%Y-%m-%dT%H:%M:%S.%f")
        print("Before Schedule utc: "+str(h1))
        h1=utc2local(h1)
        print("Before Schedule local: "+str(h1))
        # sched.add_job(my_job,'date',run_date=h1,id='job'+str(count))
        sched.add_job(my_job,'date',run_date=h1,args=[Doppler[count]])
        count+=1
    # sched.add_job(my_job, 'date', run_date=datetime(2020, 2, 22, 12, 36, 33,43534), args=['testing'])

    # count=0
    sched.start()