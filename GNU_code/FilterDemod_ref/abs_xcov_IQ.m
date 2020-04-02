function [sample_delay, corr_factor, lags_matrix, lags, Ts] = abs_xcov_IQ(IQ_data_1, IQ_data_2, max_lag,titleString,fractionOfData)
%This function  takes in two IQ data files and returns the complex cross
%correlation results

% This is really for compability. We recommend you input these in future
% scripts.
if nargin<4
    titleString=[];
    fractionOfData=1;
end

[x1, Fs1, N1All] = readIQ(IQ_data_1);
[x2, Fs2, N2All] = readIQ(IQ_data_2);

percents=0:fractionOfData:1-fractionOfData;
sample_delay=zeros(length(percents),1);
for p=1:length(percents)
    sa=ceil(percents(p)*N1All)+1;
    en=ceil((percents(p)+fractionOfData)*N2All);
    N1=size(x1(sa:en),1);
    N2=size(x2(sa:en),1);
    
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
    [d, lags] = xcov(x1(sa:en), x2(sa:en), max_lag_f);
    d_norm = abs(d)/max(abs(d));
    
      %Uncomment to plot the cross-correlation.
%     hold off
%     figure()
%     plot(lags*Ts, abs(d_norm))
%     xlabel('Time Delay [s]');
%     ylabel('Normalized Crosscorrelation');
%     title([titleString 'Absolute Value Cross-covariance Plot at ' num2str(percents(p)*100) '%']);
%     legend(strcat('first pi ',' - ',' second pi'));

    [corr_factor, index_max] = max(abs(d));
    sample_delay(p) = index_max - round(size(lags, 2)/2); 
    lags_matrix = d;
end
%% Save The Plots intermediately. This works a little better than waiting till
% the very end to save the plots, but is still slow. 
% GraphSaver({'png'},'Plots/OneHalfSecondIntervals',0,1);
end

