from os import walk
from os import mkdir
import os

# filterReader will automatically filter signals using GNUradio program filterDemod_ref.

def main():
    # Path to directory to find the source files. This must be changed every time.
    # The source files should be organized by pi. So under hailMaryLUSAT, there'd be directories pi1 and pi2.
    # NOTE: ../ means go up 1 directory.
    directoryToFiles = "../../../../hailMaryLUSAT/"

    # Change the sample rate from 2million if applicable
    sampleRate = 2000000

    # cutoff_Freq is how wide the filter is. Narrower for narrower signals?
    # cutoff_freq = 80000 #For reference signals
    cutoff_freq = 5000 #For satellite signals

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

if __name__ == '__main__':
    main()
