from datetime import datetime as dt, date, time
import datetime as bigDT
import time
import os
from optparse import OptionParser



def createText(startTime,interval,numEntries):
    f = open("./InputTimes.txt", "w+")

    f.write(startTime+'     '+'437.0000000000'+'\n')

    dateObj=dt.strptime(startTime, "%Y-%m-%dT%H:%M:%S.%f")
    for i in range(numEntries):
        dateObj+= bigDT.timedelta(seconds=interval)
        f.write(str(dateObj.date())+'T'+str(dateObj.time()) +'     '+'437.0000000000'+ '\n')


    # f.write('%f' % x.Lat + ' %f' % x.Lon + ' %f' % x.Alt + ' %0.f:' % x.Time_H + '%0.f:' % x.Time_M + '%.2f' % x.Time_S + '\n')


def argument_parser():
    parser = OptionParser(usage="%prog: [options]")
    parser.add_option(
        "", "--startTime", dest="startTime", type="string", default=str(dt.now().date())+'T'+str((dt.now()+bigDT.timedelta(hours=5,minutes=3)).time()),
        help="Set DateTime in form 'YY-MM-DDTHH-MM-SS.fff' [default=%default]")
    parser.add_option(
        "", "--interval", dest="interval", type="float", default=20,
        help="Set interval between scheduled times [default=%default]")
    parser.add_option(
        "", "--numEntries", dest="numEntries", type="int", default=4,
        help="Number of entries in the text file [default=%default]")
    return parser


def main(options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    createText(options.startTime,options.interval,options.numEntries)


if __name__ == '__main__':
    main()