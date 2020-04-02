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
abs_xoc_IQ.m used for absolute cross-correlation, called by getCrossCorrelation.m  ---Andrew--- identify this please
delay_IQ.m add an artificial delay to a datafile.  ---Andrew--- identify this please
filter_sig.py --- Andrew -- identify this please
filterDemod_ref.grc GNU radio source code for filtering.
filterDemod_ref.py python generated code by GNU radio.
FilterDemod_ref_Documentation.pptx presentation on how to filter.
filterReader.py automated script to filter a test
getCrossCorrelation.m automated script to run cross-correlation.
gr_read_file_metadata.gz ---Andrew--- identify this please
GraphSaver.m automated script to save plots.
plot_fft_IQ.m   ---Andrew--- identify this please
readIQ.m  ---Andrew--- identify this please