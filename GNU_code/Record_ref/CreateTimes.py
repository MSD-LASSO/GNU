from datetime import datetime as dt, date, time
import datetime as bigDT
import time
import os
from optparse import OptionParser



def createText(startTime,delay,numEntries,oscillate,sampleLength):
    f = open("./InputTimes.txt", "w+")
    
    referenceLength=5
    #Initial Startup
    dateObj=dt.strptime(startTime, "%Y-%m-%dT%H:%M:%S.%f")

    for i in range(numEntries):
        if oscillate==1:
            writeToText(f, dateObj, 0, referenceLength)
            dateObj += bigDT.timedelta(seconds=referenceLength + delay)
            writeToText(f, dateObj, 437, sampleLength)
        else:
            writeToText(f, dateObj, 0, sampleLength)
        dateObj += bigDT.timedelta(seconds=sampleLength + delay)


    # f.write(startTime+'     '+'000.0000000000'+'     '+str(sampleLength)+'\n')
    # 
    # dateObj=dt.strptime(startTime, "%Y-%m-%dT%H:%M:%S.%f")
    # for i in range(numEntries):
    #     if oscillate:
    #         dateObj += bigDT.timedelta(seconds=sampleLength+)
    #         f.write(str(dateObj.date()) + 'T' + str(dateObj.time()) + '     ' + '000.0000000000' + '\n')
    #     #offset date by the delay.
    #     dateObj+= bigDT.timedelta(seconds=delay)
    #     f.write(str(dateObj.date())+'T'+str(dateObj.time()) +'     '+'000.0000000000'+ '\n')


    # f.write('%f' % x.Lat + ' %f' % x.Lon + ' %f' % x.Alt + ' %0.f:' % x.Time_H + '%0.f:' % x.Time_M + '%.2f' % x.Time_S + '\n')

def writeToText(f,dateObj,freq,sampleLength):
    # f.write(str(dateObj.date()) + 'T' + str(dateObj.time()) + '     ' + format(freq,'.12f') + '     ' + format(sampleLength,'.12f') + '\n')
    f.write(str(dateObj.date()) + 'T' + str(dateObj.time()) + ',' + '{: >12f}'.format(freq) + ',' + '{: >12f}'.format(sampleLength) + '\n')


def argument_parser():
    parser = OptionParser(usage="%prog: [options]")
    # Notice timedelta is 4 hours during daylight savings time
    # Eastern Standard Time is 5 hours.
    parser.add_option(
        "", "--startTime", dest="startTime", type="string", default=str(dt.now().date())+'T'+str((dt.now()+bigDT.timedelta(hours=4,minutes=1)).time()),
        help="Set DateTime in form 'YY-MM-DDTHH-MM-SS.fff' [default=%default]")
    parser.add_option(
        "", "--delay", dest="delay", type="float", default=20,
        help="Set delay between scheduled times [default=%default]")
    parser.add_option(
        "", "--numEntries", dest="numEntries", type="int", default=4,
        help="Number of entries in the text file [default=%default]")
    parser.add_option(
        "", "--oscillate", dest="oscillate", type="int", default=0,
        help="Set to true to add a reference call 5 seconds before and after the satellite call [default=%default]")
    parser.add_option(
        "", "--sampleLength", dest="sampleLength", type="float", default=5,
        help="Length of recording. Number of Samples will be Length * Sample Rate of 20,000,000 [default=%default]")
    return parser


def main(options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    createText(options.startTime,options.delay,options.numEntries,options.oscillate,options.sampleLength)


if __name__ == '__main__':
    main()