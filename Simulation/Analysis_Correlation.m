
clear all;
userpath('E:\Git-Repository\Acoustic-Detection\Simulation\urbansound8k-gunshot')

% [sig,fs] = audioread('urbansound_gunshot_1.wav');
% sz_sig = size(sig(:,1)')
% ref = [sig(:,1)',zeros(1,2*10^5-sz_sig(2))];
load MB_sig239_357_shot01.mat
sig = MB_sig239_357_shot01(3.03*10^6:3.07*10^6,1)';
sz_sig = size(sig);
ref = [sig zeros(1,2*10^5-sz_sig(2))];

corr = [max(xcorr(ref,ref,'coeff'))];
gunshot = [];
for i = 1:338
    filename = strcat('urbansound_gunshot_',num2str(i),'.wav');
    [sig,fs] = audioread(filename);
    sz_sig = size(sig(:,1)');
    y = [sig(:,1)' zeros(1,2*10^5-sz_sig(2))];
    
    gunshot = [gunshot;y];
    
    corr = [corr max(xcorr(ref,y,'coeff'))];
    fprintf('gunshot %d corr = %f\n',i,corr(i));
end

plot(corr)
