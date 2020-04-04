Authors: Andrew deVries (ard6268@rit.edu) & Anthony Iannuzzi (awi7573@rit.edu)
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

https://creativecommons.org/licenses/by-nc-sa/4.0/

Structure of directory:

To filter a single dataset, run filterDemod_ref.py
To filter an entire test, place the test in a directory with subdirectories pi1/ and pi2/ and run filterReader.py
   with the appropriate inputs
To run cross-correlation on a dataset or entire test, use getCrossCorrelation.m.

Index of programs:

ExampleTests_FMRadioReference directory has some old data processing.
FinalTest_HailMarty_LUSAT has some old tools for analyzing the LUSAT dataset
abs_xoc_IQ.m used for absolute cross-correlation, called by getCrossCorrelation.m. This function fundamentally uses the matlab function xcov() (line 37) to return the sample delay between two .wav files.
delay_IQ.m add an artificial delay to a datafile.  This function writes a copy of a .wav file with an added delay, used for verifying crosscorrelation/crosscovariane accuracy when adding in "noise".
filterDemod_ref.grc GNU Radio Generated python script for using a low pass filter on baseband IQ data (raw) and then putting it through a wide-band FM reciever to generate "real audio data" that you can listen to (.wav). 
filterDemod_ref.py python generated code by GNU radio.
FilterDemod_ref_Documentation.pptx presentation on how to filter.
filterReader.py automated script to filter a test
getCrossCorrelation.m automated script to run cross-correlation.
GraphSaver.m automated script to save plots.
plot_fft_IQ.m  Used to generate the fft plot of raw IQ data
readIQ.m  Used by other functions to process raw IQ data from binary files