import filterDemod_ref
from os import walk
from os import mkdir
import os

def main(top=filterDemod_ref, options=None):
    # Directory to find the source files. This must be changed every time.
    directoryToFiles = "../../../../Documents/hailMary/"

    # Change the sample rate from 2million if applicable
    sampleRate = 2000000
    # cutoff_Freq is how wide the filter is. Narrower for narrower signals?
    # cutoff_freq = 80000
    cutoff_freq = 5000

    for i in range(2):
        # Make the output directories
        if os.path.exists(directoryToFiles+'/pi'+str(i+1)+'_filtered/')==0:
            mkdir(directoryToFiles+'/pi'+str(i+1)+'_filtered/')

        # Get all file names in the source directories specified by directoryToFiles
        files = []
        print(directoryToFiles+'pi'+str(i+1)+'/')
        for (dirpath, dirnames, filenames) in walk(directoryToFiles+'pi'+str(i+1)+'/'):
            files.extend(filenames)
            break

        # print(files)
        # Iterate through all files in the source directory. If the file is not a header file or a debugger file as
        # identified by "hdr" and "Debugger", then we filter that file.
        # We specify the input and outputh paths and run GNUradio filterDemod_ref.py
        j=0
        while(j<len(files)):
            inputFile=files[j]
            if inputFile.__contains__("hdr")==0 & inputFile.__contains__("Debugger")==0:
                inputPath=directoryToFiles+'/pi'+str(i+1)+'/'+inputFile
                outputName = directoryToFiles+'/pi'+str(i+1)+'_filtered/'+inputFile+".wav"
                # print(outputName)

                # tb = top(cutoff_freq=cutoff_freq, samp_rate=sampleRate, save_file=outputName,
                #          source_file=inputFile, trans_width=2000)
                # tb.start()
                # tb.wait()
                # del tb
                String='python filterDemod_ref.py --save-file='+outputName+' --source-file='+inputPath+' --cutoff-freq='+str(cutoff_freq)+' --samp-rate='+str(sampleRate)+' --trans-width=2000'
                print(String)
                os.system(String)
            j+=1

if __name__ == '__main__':
    main()
