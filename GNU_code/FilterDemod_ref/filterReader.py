from os import walk
from os import mkdir
import os
from optparse import OptionParser

# filterReader will automatically filter signals using GNUradio program filterDemod_ref.

def filter(directoryToFiles,sampleRate,cutoff_freq):


    # Iterate once for each pi.
    for i in range(2):
        # Make the output directories pi1_filtered, pi2_filtered only if they don't already exist. This program WILL
        #overwrite existing items in this directory if names match. (happens if you filter back to back, for example).
        if os.path.exists(directoryToFiles+'/pi'+str(i+1)+'_filtered/')==0:
            mkdir(directoryToFiles+'/pi'+str(i+1)+'_filtered/')

        # Get all file names in the source directories specified by directoryToFiles
        files = []
        print(directoryToFiles+'pi'+str(i+1)+'/')
        for (dirpath, dirnames, filenames) in walk(directoryToFiles+'pi'+str(i+1)+'/'):
            files.extend(filenames)
            break

        # print(files) #debugging tool.

        # Iterate through all files in the source directory. If the file is not a header file or a debugger file as
        # identified by "hdr" and "Debugger", then we filter that file.
        # We specify the input and outputh paths and run GNUradio filterDemod_ref.py
        print("past pi_filtered folder creation")
        j=0
        while(j<len(files)):
            # For each file in the directory, get the name of the file.
            inputFile=files[j]
            # If the file does NOT contain hdr (is a header file) or Debugger (is the debugger file) then
            # we filter it.
            if inputFile.__contains__("hdr")==0 & inputFile.__contains__("Debugger")==0:
                inputPath=directoryToFiles+'/pi'+str(i+1)+'/'+inputFile
                outputName = directoryToFiles+'/pi'+str(i+1)+'_filtered/'+inputFile+".wav"
                print("before calling GNU to filter signal")

                # This is exactly how one would call filterDemod_ref.py from the command line.
                # NOTE: you must be in the directory containing filterDemod_ref.py
                String='python filterDemod_ref.py --save-file='+outputName+' --source-file='+inputPath+' --cutoff-freq='+str(cutoff_freq)+' --samp-rate='+str(sampleRate)+' --trans-width=2000'
                print(String)
                os.system(String)
            j+=1

def argument_parser():
    parser = OptionParser(usage="%prog: [options]")
    # Notice timedelta is 4 hours during daylight savings time
    # Eastern Standard Time is 5 hours.
    parser.add_option(
        "", "--directory", dest="directoryToFiles", type="string", default="../../../../",
        help="Set the directory to find the folders labeled pi1 and pi2. ../ means go up 1 directory. THe classic path "
             "to this code is GIT_GNU/GNU/GNU_code/FilterDemod_ref/ so 4 ../ brings us to the directory that"
             "contains GIT_GNU/ [default=%default]")
    parser.add_option(
        "", "--sampleRate", dest="sampleRate", type="int", default=2000000,
        help="The sampleRate that was used to collect the data files. [default=%default]")
    parser.add_option(
        "", "--cutoff_freq", dest="cutoff_freq", type="int", default=80000,
        help="The cutoff frequency to use when filtering. Set narrower for narrower signals. 80,000 for reference, "
             "5,000 for satellites are good starting values. [default=%default]")
    return parser


def main(options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    filter(options.directoryToFiles,options.sampleRate,options.cutoff_freq)


if __name__ == '__main__':
    main()