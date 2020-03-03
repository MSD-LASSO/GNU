clearvars

expectedDelay=10;

fid = fopen('Pi1_100_3_3_9am.txt');
data1 = textscan(fid,'%s%s%s%s%s');
fclose(fid);

fid = fopen('Pi2_100_3_3_9am.txt');
data2 = textscan(fid,'%s%s%s%s%s');
fclose(fid);

for i=1:length(data1{4})
    charAry=data1{4}(i);
    if isempty(charAry{1})==1
        divider=i;
        break
    end
end

refDate=data1{4}(1:divider-1)
refTimes=data1{5}(1:divider-1)
pi1Date=data1{1}(divider:end)
pi1Times=data1{2}(divider:end)
pi2Date=data2{1}(divider:end)
pi2Times=data2{2}(divider:end)


for i=1:length(pi1Date)
    reference(i,1)=datetime([refDate{i} ' ' refTimes{i}],'InputFormat','yyyy-MM-dd HH:mm:ss.SSSSSS', 'Format', 'yyyy-MM-dd HH:mm:ss.SSSSSS');
    h1(i,1)=datetime([pi1Date{i} ' ' pi1Times{i}],'InputFormat','yyyy-MM-dd HH:mm:ss.SSSSSS', 'Format', 'yyyy-MM-dd HH:mm:ss.SSSSSS');
    h2(i,1)=datetime([pi2Date{i} ' ' pi2Times{i}],'InputFormat','yyyy-MM-dd HH:mm:ss.SSSSSS', 'Format', 'yyyy-MM-dd HH:mm:ss.SSSSSS');
end

absErr1=seconds(reference-h1)+expectedDelay;
absErr2=seconds(reference-h2)+expectedDelay;
relErr=seconds(h2-h1);

figure()
boxplot([absErr1 absErr2 relErr])
figure()
subplot(1,3,1)
histogram(absErr1)
title('Abs Err Pi 1')
subplot(1,3,2)
histogram(absErr2)
title('Abs Err Pi 2')
subplot(1,3,3)
histogram(relErr)
title('Rel Err Pi 1 and 2')

figure()
plot(relErr)
grid on

figure()
plot(h1.Second)
hold on
plot(h2.Second)
grid on




