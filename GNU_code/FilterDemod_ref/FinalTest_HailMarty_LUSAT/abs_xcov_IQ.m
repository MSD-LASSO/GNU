function [sample_delay, corr_factor, lags_matrix, lags, Ts] = abs_xcov_IQ(IQ_data_1, IQ_data_2, max_lag,titleString)
%This function  takes in two IQ data files and returns the complex cross
%correlation results

if nargin<4
    titleString=[]
end

[x1, Fs1, N1] = readIQ(IQ_data_1);
[x2, Fs2, N2] = readIQ(IQ_data_2);
if Fs1 ~= Fs2
    disp('The data sets are sampled at different frequencies');
    return;
end
if max_lag == 0
    if N1 <= N2
        max_lag_f = N1;
    else
        max_lag_f = N2;
    end
else
    max_lag_f = max_lag;
end
Ts = 1 / Fs1;
[d, lags] = xcov(x1, x2, max_lag_f);
d_norm = abs(d)/max(abs(d));
hold off
figure
plot(lags*Ts, abs(d_norm))
xlabel('Time Delay [s]');
ylabel('Normalized Crosscorrelation');
title([titleString 'Absolute Value Cross-covariance Plot']);
legend(strcat('first pi ',' - ',' second pi'));
[corr_factor, index_max] = max(abs(d));
sample_delay = index_max - round(size(lags, 2)/2); 
lags_matrix = d;
end

