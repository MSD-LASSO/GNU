import os
from datetime import datetime
import datetime as timeshifter
from CreateTimes import createText

# Using this Test script. See the below output.

def allScheduledTimesAlreadyHappenedTest():
    None

def noHackrfPluggedInTest():
    None

def basicTest():
    fileDirectory="/home/pi/Documents/basicTest/"
    scheduler=0
    hackrf_index=0
    schedulerFile="InputTimes.txt"
    runTest(fileDirectory,scheduler,hackrf_index,schedulerFile)


def runTest(fileDirectory,scheduler,hackrf_index,schedulerFile):

    if fileDirectory is "/home/pi/Documents/":
        raise ImportError("Cannot Test using the Documents/ Directory. Make a subdirectory.")

    numEntries=4 #for create schedule.
    currentTime=datetime.now()
    # Translation of the createText
    # Begin schedule 1 minute from now.
    # Delay 1 second between sampling intervals.
    # Create 4 recording times
    # Do not oscillate between recording a satellite and a reference signal
    # Record for 5 seconds
    shiftedTime=currentTime+timeshifter.timedelta(minutes=1)
    createText(str(shiftedTime.date())+'T'+str(shiftedTime.time()),1,numEntries,0,5)

    # Run the scheduler with the specified inputs
    strCmd="python /home/pi/GIT_GNU/GNU/GNU_code/Record_ref/scheduler_Runner.py --fileDirectory='"+fileDirectory+"' --scheduler="+str(scheduler)+" --hackrf-index="+str(hackrf_index)+" --schedulerFile="+str(schedulerFile)
    print(strCmd)
    # os.system(strCmd)
    #
    # # Check our answer. We check if all file sizes are of correct size and the number of files.
    #
    # files = []
    # # Gets all files in the named directory.
    # for (dirpath, dirnames, filenames) in os.walk(fileDirectory):
    #     files.extend(filenames)
    #     break
    #
    # assert files.__len__() == numEntries
    #
    # for currentFile in files:
    #     # Check file sizes for data sets. Ignore header files.
    #     if currentFile.__contains__(".hdr")==0:
    #         assert os.stat(fileDirectory+currentFile).st_size==80e6
    #
    # # os.stat_result(st_mode=33188, st_ino=6419862, st_dev=16777220, st_nlink=1, st_uid=501, st_gid=20, st_size=1564,
    # #                st_atime=1584299303, st_mtime=1584299400, st_ctime=1584299400)

    # Clean up.
    if deleteDirectories==1:
        os.remove(fileDirectory)



if __name__ == '__main__':

    deleteDirectories=0 #Set to 0 to keep data and directories created by this script.

    print("Use of this test script is as follows:")
    print("Make sure the system is fully connected. Antenna, Hackrf, LNA, GPS are all connected to the Raspberry Pi")
    print("Run this script using python Tester.py in its folder or by specfiying the absolute path")
    print("This script will throw an Assertion Error if there's a problem with the system.")
    print("This script WILL take ~10 minutes to run with intermediate progress reports.")
    print("This script WILL OVERWRITE the following: InputTimes.txt, /home/pi/Documents/basicTest/, /home/pi/Documents/Erred")
    basicTest()
    allScheduledTimesAlreadyHappenedTest()
    noHackrfPluggedInTest()
