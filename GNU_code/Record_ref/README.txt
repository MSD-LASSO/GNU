Authors: Andrew deVries (ard6268@rit.edu) & Anthony Iannuzzi (awi7573@rit.edu)
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.

https://creativecommons.org/licenses/by-nc-sa/4.0/

Structure of directory:

To do a single recording, run record_ref.py with the desired inputs
To run a sechedule of recordings: create the schedule as a textfile (see ExampleSchedules) then
   run scheduler_Runner.py with the desired inputs
To create a schedule automatically, use CreateTimes.py with specified inputs.

Index of programs:

config.py -- helper script for GPS
CreateTimes.py -- helper script to create a schedule
gps_free_APScheduler.py -- scheduler that uses the python package apscheduler and system time. Does not use GPS. 
			   Not recommended.
InputTimes.txt -- the default schedule file
L76X.py -- interface script for GPS
record_ref.grc -- GNUradio source code for recording signals.
record_ref.py -- GNUradio generated python code for recording signals.
scheduler_Runner.py -- Interfacing program to use when you want to record signals at set times.
Tester.py -- Test script. Use to verify all programs are working correctly.
unified.py -- custom scheduler that reads GPS time using L76X. Recommended.