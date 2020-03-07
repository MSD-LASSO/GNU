import filterDemod_ref
from os import walk
from os import mkdir

def main(top=filterDemod_ref, options=None):
    directoryToFiles = "C:/Users/awian/Desktop/MSD/3_6_test/"

    sampleRate = 20000000
    cutoff_freq = 80000

    for i in range(2):
        #Get all file names
        mkdir(directoryToFiles+'/pi'+str(i+1)+'_filtered/')
        files = []
        for (dirpath, dirnames, filenames) in walk(directoryToFiles+'pi'+str(i+1)+'/'):
            files.extend(filenames)
            break

        j=0
        while(j<len(files)):
            inputFile=files[j]
            if ~inputFile.__contains__("hdr"):

                outputName = directoryToFiles+'/pi'+str(i+1)+'_filtered/'+inputFile+".wav"

                tb = top(cutoff_freq=cutoff_freq, samp_rate=sampleRate, save_file=outputName,
                         source_file=inputFile, trans_width=2000)
                tb.start()
                tb.wait()
                del tb
            j+=1

if __name__ == '__main__':
    main()
