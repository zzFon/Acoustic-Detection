#-*-coding:utf-8-*-

import os
import numpy as np
import soundfile as sf
import librosa
import matplotlib.pyplot as plt

#????
os.chdir('E:\Git-Repository\Acoustic-Detection\Simulation\MFCC_GMM')
print('?????')
print(os.getcwd())

#??
spk_num = 2
ncentres = 5

#????
for spk_cyc in range(1,spk_num+1):
    print('training for speaker',str(spk_cyc))
    #???????????
    if spk_cyc == 1:
        Tra_start = 1;
        Tra_end = 6;
    elif spk_cyc == 2:
        Tra_start = 1;
        Tra_end = 6;
    #???????????
    for sph_cyc in range(Tra_start,Tra_end+1):
        #????
        filename = ''
        if spk_cyc == 1:
            filename = 'dataset_gun'
        elif spk_cyc == 2:
            filename = 'dataset_background'
        filename = filename+str(sph_cyc)+'.wav'

        [sig,fs] = sf.read(filename)
        if len(np.shape(sig))>1:
            pre_sph = np.transpose(np.array(sig))[0][:]
        else:
            pre_sph = np.transpose(np.array(sig))
        print('pre-processing data:', filename,'shape:',np.shape(pre_sph))
    #????
        cof_num = 20#MFCC????
        frm_len = int(fs*0.02)#??
        fil_num = 20#mel?????
        frm_off = int(fs*0.01)#??


        mfcc = librosa.feature.mfcc(pre_sph,fs)

