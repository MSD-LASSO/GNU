%tester
clearvars
close all
mainPath='C:\Users\devri\Documents\RIT\Sixth Semester\MSD I\GIT\GNU_non_git\3_9_ref_onlyu';
pi1_directory=dir([mainPath '\pi1_filtered']);
pi2_directory=dir([mainPath '\pi2_filtered']);
max = size(pi2_directory, 1);
time_delay = zeros(max-2,1);
sample_delay = zeros(max-2,1);
offset = zeros(max-2,1);
delta_scheduler = zeros(max-2,1);
delta_file = zeros(max-2,1);
file_save_time_1 = zeros(max-2, 1);
file_save_time_2 = zeros(max-2, 1);
test_start = zeros(max-2, 1);
GNU_save_time_1 = zeros(max-2, 1);
GNU_save_time_2 = zeros(max-2, 1);
delta_GNU = zeros(max-2, 1);
for i = 3:22
    pi_1_file = [mainPath '\pi1_filtered\' pi1_directory(i).name];
    pi_2_file = [mainPath '\pi2_filtered\' pi2_directory(i).name];
    sched_start = strfind(pi1_directory(i).name, '_atEntry');
    test_start(i-2) = 60*str2double(extractBetween(pi1_directory(i).name, sched_start - 12, sched_start - 11)) + str2double(extractBetween(pi1_directory(i).name, sched_start - 9, sched_start - 8)) + 1e-6 * str2double(extractBetween(pi1_directory(i).name, sched_start - 6, sched_start - 1));
    GNU_start_index_1 = strfind(pi1_directory(i).name, '_afterFinishingGNU');
    GNU_start_index_2 = strfind(pi2_directory(i).name, '_afterFinishingGNU');
    GNU_start_1 = str2double(replace(extractBetween(pi1_directory(i).name, GNU_start_index_1 - 9, GNU_start_index_1 -1), '_', '.'));
    GNU_start_2 = str2double(replace(extractBetween(pi2_directory(i).name, GNU_start_index_2 - 9, GNU_start_index_2 -1), '_', '.'));
    GNU_end_1 = str2double(replace(extractBetween(pi1_directory(i).name, GNU_start_index_1 + 21, GNU_start_index_1 + 30), '_', '.'));
    GNU_end_2 = str2double(replace(extractBetween(pi2_directory(i).name, GNU_start_index_2 + 21, GNU_start_index_2 + 30), '_', '.'));
    if isnan(GNU_start_1)
        GNU_start_1 = str2double(replace(extractBetween(pi1_directory(i).name, GNU_start_index_1 - 8, GNU_start_index_1 -1), '_', '.'));
    end
    if isnan(GNU_start_2)
        GNU_start_2 = str2double(replace(extractBetween(pi2_directory(i).name, GNU_start_index_2 - 8, GNU_start_index_2 -1), '_', '.'));
    end
    if isnan(GNU_end_1)
        GNU_end_1 = str2double(replace(extractBetween(pi1_directory(i).name, GNU_start_index_1 + 22, GNU_start_index_1 + 29), '_', '.'));
    end
    if isnan(GNU_end_2)
        GNU_end_2 = str2double(replace(extractBetween(pi2_directory(i).name, GNU_start_index_2 + 22, GNU_start_index_2 + 29), '_', '.'));
    end
    file_save_time_1(i-2) = GNU_start_1;
    file_save_time_2(i-2) = GNU_start_2;
    GNU_save_time_1(i-2) = GNU_end_1;
    GNU_save_time_2(i-2) = GNU_end_2;
    delta_file(i-2) = file_save_time_1(i-2) - file_save_time_2(i-2);
    delta_GNU(i-2) = GNU_save_time_1(i-2) - GNU_save_time_2(i-2);
    [~, Fs1, N1] = readIQ(pi_1_file);
    [~, Fs2, N2] = readIQ(pi_2_file);
    [sample_delay(i-2), ~, ~, ~, ~] = abs_xcov_IQ(pi_1_file, pi_2_file, 0);
    time_delay(i-2) = sample_delay(i-2) /Fs1;
    offset(i-2) = -1 * time_delay(i-2) -  delta_file(i-2);
%     t = 0:1/Fs1:(N1-1)/Fs1;
%     figure
%     plot(t, x1+1, t, x2-1)
%     legend('First Pi', 'Second Pi')
%     xlabel('Time [s]')
%     ylabel('Signals with offsets')
%     ylim([-2.5 2.5]);
end

% plot_fft_IQ(pi_1_file_1);
% plot_fft_IQ(pi_2_file_1);




plot(test_start, offset)
hold on
% plot(test_start, delta_GNU)
title('Time offsets Bewteen the Pis --- Pi2 time - Pi1 time')
ylabel('Offset Time [s]')
xlabel('Test Time [s]')
offset


save('Ref_3_9_onlyu.mat');


% input_delay = -27;
% 
% orig_data = 'new_file_IQ.wav';
% my_data = 'myData.wav';
% delayed_data = 'myDataDelayed.wav';
% [~, Fs, N1] = readIQ(orig_data);
% plot_fft_IQ(orig_data);
% 



















% [x2, Fs1, N2] = readIQ(gen_IQ);
% y1 = lowpass(x2, 50e3, Fs);
% y2(:, 1) = real(y1);
% y2(:, 2) = imag(y1);
% audiowrite(new_IQ_name, y2, Fs);
% plot_fft_IQ(gen_IQ);
% plot_fft_IQ(new_IQ_name);

% cmplx_xcorr_IQ(gen_IQ, new_IQ_name, 0);





















% 
% 
% 
% SNR_try = 40000;
%     
% BW_try = 100e3;
% make_IQ(BW_try, Fs, Time, file_name_2)
% add_noise_IQ(file_name_2, SNR_try, file_name_3);
% plot_fft_IQ(file_name_3);
% add_noise_IQ(file_name_2, SNR_try, file_name_4);
% % plot_fft_IQ(file_name_4);
% delay_IQ(file_name_4, input_delay, file_name_5);
% plot_fft_IQ(file_name_5);
% 
% 
% 
% 
% 
% 
% % 
% [delay1, ~, ~, ~, ~] = cmplx_xcorr_IQ(file_name_3, file_name_5, 0);
% [delay2, ~, ~, ~, ~] = cmplx_xcov_IQ(file_name_3, file_name_5, 0);
% [delay3, ~, ~, ~, ~] = abs_xcorr_IQ(file_name_3, file_name_5, 0);
% [delay4, ~, ~, ~, ~] = abs_xcov_IQ(file_name_3, file_name_5, 0);
% [delay5, ~, ~, ~, ~] = phase_xcorr_IQ(file_name_3, file_name_5, 0);
% [delay6, ~, ~, ~, ~] = phase_xcov_IQ(file_name_3, file_name_5, 0);
% [delay7, ~, ~, ~, ~] = phase_diff_xcorr_IQ(file_name_3, file_name_5, 0);
% [delay8, ~, ~, ~, ~] = phase_diff_xcov_IQ(file_name_3, file_name_5, 0);
% 
% 
% 
% 
% 
% 
% num_success = 0;
% success = zeros(2, 20);
% 
% for k = 1:20
%     SNR_try = 10;
%     
%     BW_try = 5e3*k;
%     make_IQ(Fs, SNR, Time, file_name_2)
%     
%     add_noise_IQ(file_name_2, SNR_try, file_name_3);
%     plot_fft_IQ(file_name_3);
%     add_noise_IQ(file_name_2, SNR_try, file_name_4);
%     plot_fft_IQ(file_name_4);
%     delay_IQ(file_name_4, input_delay, file_name_5);
%     plot_fft_IQ(file_name_5);
% 
%     [delay, ~, ~, ~, ~] = cmplx_xcov_IQ(file_name_3, file_name_5, 0);
% 
%     if delay == input_delay
%         num_success = num_success + 1;
%         success(1, k) = 0;
%     else
%         success(1, k) = abs(delay - input_delay);
%     end
%     
%     success(2, k) = BW_try;
%     close all
% end
% 
% 
% 
% 
% 
% 
% % clc;
% % clear all;
% % close all;
% % t=0:.001:1;
% % fm=1;
% % fc=100;
% % m=sin(2*pi*fm*t);
% % subplot(311);
% % plot(m);
% % title('Message signal');
% % c=cos(2*pi*fc*t+5*sin(2*pi*fm*t));
% % subplot(313);
% % plot(c);
% % title('fm signal');
% % subplot(312);
% % plot(cos(2*pi*fc*t));
% % title('Carrier signal');
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% % delay_set = -150000;
% % SNR = 1;
% % file_name_2 = strcat('NOISY_', file_name_1);
% % file_name_3 = strcat('DELAYED_', file_name_2);
% % 
% % add_noise_IQ(file_name_1, SNR, file_name_2);
% % 
% % plot_fft_IQ(file_name_2);
% % 
% % delay_IQ(file_name_2, delay_set, file_name_3);
% % [delay, corr_factor, lags_matrix, lags, Ts] = phase_diff_xcov_IQ(file_name_1, file_name_3, 0);