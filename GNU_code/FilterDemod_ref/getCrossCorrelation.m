% This script will calculate time_delays and adjust for clock
% desynchronization based on the times given in the input files. The script
% reads folders named pi1_filtered and pi2_filtered, both must be located
% in the same directory, specified by mainPath.

% For 20 different data files, the outputs are time_delay and offset.
% Time_delay is a 20xn matrix of the raw time_delays calculated from cross
% correlation. Offset is a 20xn*2 vector where the first half is time_delay
% and the second half columns adjust the time_delay by some constant,
% calculated from the file names.
%n is 1/FractionOfData, which is the percentage of the data file used in
%one cross-correlation. 

% The current accuracy of this method is ~3ms.

%To plot the cross correlations, go into abs_xcov_IQ.m and uncomment the
%plot lines. 

clearvars
close all
addpath('../TdoaSim/')

% Example Paths. These will need to be changed for your specific data
% files.
mainPath='C:\Users\awian\Desktop\MSD\3_9_ref_only';
% mainPath='C:\Users\awian\Desktop\MSD\3_12_ref_same_pi';
% mainPath='C:\Users\awian\Desktop\MSD\3_13_same_pi_APS';
% mainPath='C:\Users\awian\Desktop\MSD\hailMary';

% NOTE: we are reading the whole directory. VERIFY there are only data
% files in these directories and there are equal numbers of them. If there
% are other files or a rogue data file, cross-correlation may be comparing
% different data sets!
pi1_directory=dir([mainPath '\pi1_filtered']);
pi2_directory=dir([mainPath '\pi2_filtered']);
max = size(pi2_directory, 1);

%% Inputs
% FractionOfData is what % of the data should be used for
% cross-correlation. The percent you pick should be divisble by 100. For
% example, 0.2 will split the data into 5 segments 0->20%, 20->40%, etc.
%0.7 would be an unacceptable input as it doesn't split the data! 0->70%,
%70% -> ?
fractionOfData=0.2;

% The -2 comes from the fact we are reading a directory using MATLAB. The
% first 2 entries in the directory are '.' and '..' which are not data
% files.

%NOTE: for the offset based on the pi filenames, ONLY afterSetup is used.
%This has proven to be the most accurate one to use based on our tests.
%This data can be seen on EDGE under 
%Integrated Build and Test/P20151 Time Sync Test Results.xlsx/
file_save_time_1 = zeros(max-2, 4); %Array of times based on pi1 filenames
file_save_time_2 = zeros(max-2, 4); %Array of times based on pi2 filenames
delta_file = zeros(max-2,4); %Array of time differences baed on filenames.

sample_delay = zeros(max-2,1/fractionOfData); %calculated from cross-correlation
time_delay = zeros(max-2,1/fractionOfData); %multiply sample_delay by speed of light
offset = zeros(max-2,1/fractionOfData); %take time_delay and subtract delta_file.
%% Process the Data
for i = 3:length(pi1_directory)
    disp(['Iteration Number: ' num2str(i) ' out of ' num2str(length(pi1_directory))])
    
    %Get the Curent file we are on. 
    pi_1_file = [mainPath '\pi1_filtered\' pi1_directory(i).name];
    pi_2_file = [mainPath '\pi2_filtered\' pi2_directory(i).name];
    
    %% Get the times embedded in the file names. 
    str=split(pi1_directory(i).name,'_');
    assumedMin=60*str2double(str{6});
    scheduledTime(i-2)=assumedMin+str2double(str{7})+str2double(str{8})/1e6;
    
    a=assumedMin+str2double(str{10})+str2double(str{11})/1e6;
    b=assumedMin+str2double(str{13})+str2double(str{14})/1e6;
    c=assumedMin+str2double(str{16})+str2double(str{17})/1e6;
    d=60*str2double(str{19})+str2double(str{20})+str2double(str{21}(1:end-4))/1e6;
    file_save_time_1(i-2,:)=[a,b,c,d];

    str=split(pi2_directory(i).name,'_');
    assumedMin=60*str2double(str{6});
    a=assumedMin+str2double(str{10})+str2double(str{11})/1e6;
    b=assumedMin+str2double(str{13})+str2double(str{14})/1e6;
    c=assumedMin+str2double(str{16})+str2double(str{17})/1e6;
    d=60*str2double(str{19})+str2double(str{20})+str2double(str{21}(1:end-4))/1e6;
    file_save_time_2(i-2,:)=[a,b,c,d];
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % This line gets the common string located in both filenames and is
    % used to title the various plots. THIS ONLY WORKS IN THE YEAR 2020.
    intersect=pi_1_file(strfind(pi_1_file,'2020'):strfind(pi_1_file,'2020')+25);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    delta_file(i-2,:) = file_save_time_1(i-2,:) - file_save_time_2(i-2,:);
    
    %Read in the IQ data for plotting.
    [x1, Fs1, N1] = readIQ(pi_1_file);
    [x2, Fs2, N2] = readIQ(pi_2_file);
    
    %Run the cross correlation.
    [sample_delay(i-2,:), ~, ~, ~, ~] = abs_xcov_IQ(pi_1_file, pi_2_file, 0, intersect,fractionOfData);
    time_delay(i-2,:) = sample_delay(i-2,:) /Fs1;
    
    %We use column 2 of delta_file because "aftersetup" seems to
    %correct the delays the best.
    offset(i-2,:) = time_delay(i-2,:) -  delta_file(i-2,2);
    
    % plot the raw IQ data. Helps with debugging. 
%     t = 0:1/Fs1:(N1-1)/Fs1;

%     figure()
%     plot(t, x1+1, t, x2-1)
%     legend('First Pi', 'Second Pi')
%     xlabel('Time [s]')
%     ylabel('Signals with offsets')
%     ylim([-2.5 2.5]);
%     title(intersect)

    % We clear these variables every iteration because of the large amount
    % of memory they can take up.
    clear x1
    clear x2
    clear t
    
end

%% Debugging Tool.
% plot_fft_IQ(pi_1_file_1);
% plot_fft_IQ(pi_2_file_1);


%% Visual of the offset between the pi clocks
% plot((file_save_time_1+file_save_time_2)/2 - (file_save_time_1(1)+file_save_time_2(1))/2, offset)
% title('Time offsets Bewteen the Pis --- Pi2 time - Pi1 time')
% ylabel('Offset Time [s]')
% xlabel('Test Time [s]')
% offset

%% Output
offset=[time_delay offset];
m=mean(abs(offset));
s=std(abs(offset));
disp(mean(abs(offset))); disp(std(abs(offset)))

%% Save the plots. WARNING: this WILL take a significant amount of time.
%the plots are massive, 0.5gb each usually when saved as a .fig. 
% Another option is to uncomment GraphSaver located in abs_xcov_IQ.m this
% works a little better, but is still slow. 
% GraphSaver({'png'},'Plots',0,0);

close all

%% Save the DATA. Be very careful not to overwrite existing data files. 
% save('getCrossCorrelation1_5sec.mat');
% save('getCC1_5secTD.mat','offset');

