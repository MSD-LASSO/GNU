import time
import record_ref
from datetime import datetime, date
from optparse import OptionParser
import os
from os import mkdir

# Run this script when you want to record signals at set times. Use python scheduler_Runner --help to learn more about
# the inputs to the function.

def record(schedDate, center_frequency,channel_frequency,currentTime,sampleRate,sampleLength,fileDirectory,debuggerFile,hackrf_index,GPShandler=None):
    # center_frequency and channel_frequency are both given in mHz.

    # Decide whether we are recording a satellite or reference signal.
    if center_frequency>200:
        ID_tag="Sat"
    else:
        ID_tag="Ref"

    # Call GNUradio to record the signal with the specified inputs. We record several different times during the call
    # to help us better align cross-correlation. The best one to use as a correction factor so far is afterSetup.

    # Instantiate the class.
    top = record_ref
    tb = top.record_ref(center_freq=int(round(center_frequency * 1e6)), channel_freq=int(round(channel_frequency * 1e6)),
                        file_loc=fileDirectory + ID_tag +'_Time' + str(currentTime).replace(" ", "_").replace(":",
                                                                                                         "_").replace(
                            ".", "_"), hackrf_index=hackrf_index, num_samples=int(round(sampleLength * sampleRate)),
                        samp_rate=sampleRate)
    afterSetup, GPS, GPShandler = getCurrentTime(GPShandler, debuggerFile)
    print("After calling class constructor: " + str(afterSetup))
    debuggerFile.write("After calling class constructor: " + str(afterSetup) + '\n')

    # Star the recording.
    tb.start()
    afterStartingGNU, GPS, GPShandler = getCurrentTime(GPShandler, debuggerFile)
    print("After calling tb.start(): " + str(afterStartingGNU))
    debuggerFile.write("After calling tb.start(): " + str(afterStartingGNU) + '\n')

    # Wait till the recording finishes.
    tb.wait()
    afterFinishingGNU, GPS, GPShandler = getCurrentTime(GPShandler, debuggerFile)
    print("After calling tb.wait(): " + str(afterFinishingGNU))
    debuggerFile.write("After calling tb.wait(): " + str(afterFinishingGNU) + '\n')

    # Delete the instance of this class. This is required to stop the hackrf from recording.
    del tb

    # This is a debug string. It is designed to be just like the record_ref call.
    String = 'python /home/pi/GIT_GNU/GNU/GNU_code/Record_ref/record_ref.py --channel-freq=' + str(
        int(round(channel_frequency * 1e6))) + ' --samp-rate=' + str(
        sampleRate) + '--hackrf_index='+ str(hackrf_index) +' --center-freq='+str(
        int(round(center_frequency * 1e6)))+' --num-samples=' + str(
        int(round(sampleLength * sampleRate))) + ' --file-loc="'+fileDirectory + ID_tag + '_Time' + str(
        currentTime).replace(" ","_").replace(":", "_").replace(".", "_") + '"'


    # Various debugging tools.
    # use this to have python pause for 10 seconds. Could be used in place of the record_ref call, for example.
    # time.sleep(10)
    # use this to write a date to a textfile using Linux.
    # String="date >> /home/pi/Documents/debugger.txt 2>&1"
    # os.system("sudo echo "+String+" >> /home/pi/Documents/debugger.txt 2>&1")

    hackrfCompletion, GPS, GPShandler = getCurrentTime(GPShandler, debuggerFile)
    debuggerFile.write("Completed hackRF call. Time: " + str(hackrfCompletion) + '\n')
    debuggerFile.write("HackRf String Call: " + '\n')
    debuggerFile.write(String + '\n')
    print("Completed hackRF call. Time: " + str(hackrfCompletion))
    print("HackRf String Call: ")
    print(String)

    # Goal now is to find the data file we just created and rename it.
    queryString = str(currentTime).replace(" ", "_").replace(":", "_").replace(".", "_")
    files = []
    # Gets all files in the named directory.
    for (dirpath, dirnames, filenames) in os.walk(fileDirectory):
        files.extend(filenames)
        break

    # Iterate through the files in the directory until we find our query string. Rename the filename utilizing all time
    # time information we've gathered.
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

            scheduled = str(schedDate).replace(" ", "_").replace(":", "_").replace(".", "_")
            actuallyRanAt = "%s_%s" % (currentTime.second, str(currentTime.microsecond))
            afterSetupStr = "%s_%s" % (afterSetup.second, str(afterSetup.microsecond))
            afterStartingGNUStr = "%s_%s" % (afterStartingGNU.second, str(afterStartingGNU.microsecond))
            afterFinishingGNUStr = "%s_%s_%s" % (
            afterFinishingGNU.minute, afterFinishingGNU.second, str(afterFinishingGNU.microsecond))

            # Debugging Tool.
            # print("FileName: ")
            # print('/home/pi/Documents/'+
            #           prefix+"Time_Scheduled_"+scheduled+"_atEntry_"+actuallyRanAt+"_afterSetup_"+afterSetupStr+
            #           "_afterStartingGNU_"+afterStartingGNUStr+"_afterFinishingGNU_"+afterFinishingGNUStr+extension)

            os.rename(r'' + fileDirectory + currentFile, r'' + fileDirectory +
                      prefix + "Time_Scheduled_" + scheduled + "_atEntry_" + actuallyRanAt + "_afterSetup_" + afterSetupStr +
                      "_afterStartingGNU_" + afterStartingGNUStr + "_afterFinishingGNU_" + afterFinishingGNUStr + extension)



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
        GPS=True
        # What the output from L76X looks like
        # 2020-3-1
        # 20:17:2.5

        Str=GPShandler.Date+'T'+GPShandler.Time

        # Debugging tools.
        # Str='2020-3-1'+'T'+'20:17:2.5'
        # print(Str)
        try:
            currentTime = datetime.strptime(Str, "%Y-%m-%dT%H:%M:%S.%f")
        except:
            # Sometimes the L76X.get will work but Str will be empty. So we have this try catch here.
            GPS = False
            currentTime = datetime.now()

    else:
        # print('No positioning') #Debugging tool.
        GPS=False
        currentTime=datetime.now()

    debuggerFile.write("Using GPS: "+ str(GPS)+' Time: '+ str(currentTime) + '\n')
    print("Using GPS: "+ str(GPS)+' Time: '+ str(currentTime))

    # Use this to have the os write directly to a textfile.
    # os.system("sudo echo Using GPS "+ str(GPS)+' Time '+ str(currentTime) + " >> /home/pi/Documents/debugger.txt 2>&1")

    return currentTime,GPS,GPShandler


def argument_parser():
    parser = OptionParser(usage="%prog: [options]")

    parser.add_option(
        "", "--schedulerFile", dest="schedulerFile", type="string", default="InputTimes.txt",
        help="Set the text file name to read the schedule from. IMPORTANT: Cannot have extra white space at end of "
             "InputTimes.txt. It will throw index out of range error. Times must be in SEQUENTIAL ORDER! "
             "[default=%default]")

    parser.add_option(
        "", "--scheduler", dest="scheduler", type="int", default=0,
        help="Set to 0 to use unified.py and 1 to use gps_free_APScheduler.py. NOTE: we could only get the BlockingScheduler"
             "to work for APScheduler. The DebuggerFile WILL be empty for this file. [default=%default]")

    parser.add_option(
        "", "--hackrf-index", dest="hackrf_index", type="int", default=0,
        help="Set Set Hackrf to listen to. Only use if 2 hackrfs are plugged into same device. [default=%default]")

    parser.add_option(
        "", "--fileDirectory", dest="fileDirectory", type="string", default='/home/pi/Documents/',
        help="Set path that files will be saved to. Must be in Quotes. [default=%default]")

    return parser


def main(options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    if os.path.exists(options.fileDirectory) == 0:
        mkdir(options.fileDirectory)

    print('PLEASE VERIFY THE FOLLOWING: ')
    print('The hackrf is plugged into this device AND an antenna is PLUGGED into the hackrf')
    print('The LNA is connected correctly, its little light should face the hackrf')
    print('The GPS Hat is securely attached to the Pi and the GPS antenna is connected.')
    if options.scheduler==1:
        print('WARNING: You have selected the APScheduler. The current implementation uses a BlockingScheduler. YOU WILL NOT BE '
              'ABLE TO USE THIS TERMINAL even after the program ends. You will have to close and reopen it.')
    print('Sleeping for 10 seconds')
    time.sleep(10)

    if options.scheduler==0:
        from unified import schedule
    elif options.scheduler==1:
        from gps_free_APScheduler import schedule
    else:
        raise ImportError("Unknown scheduler variable given.")

    schedule(options.schedulerFile, options.hackrf_index, options.fileDirectory)

if __name__ == '__main__':
    main()
