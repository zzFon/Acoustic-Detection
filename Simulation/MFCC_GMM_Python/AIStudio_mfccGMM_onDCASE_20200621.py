#!/usr/bin/env python
# coding: utf-8

# In[ ]:


######################################## 服务器初始化 #########################################################

# 查看当前挂载的数据集目录, 该目录下的变更重启环境后会自动还原
# View dataset directory. This directory will be recovered automatically after resetting environment. 
get_ipython().system('ls /home/aistudio/data')

# 查看工作区文件, 该目录下的变更将会持久保存. 请及时清理不必要的文件, 避免加载过慢.
# View personal work directory. All changes under this directory will be kept even after reset. Please clean unnecessary files in time to speed up environment loading.
get_ipython().system('ls /home/aistudio/work')

# 如果需要进行持久化安装, 需要使用持久化路径, 如下方代码示例:
# If a persistence installation is required, you need to use the persistence path as the following:
get_ipython().system('mkdir /home/aistudio/external-libraries')
get_ipython().system('pip install beautifulsoup4 -t /home/aistudio/external-libraries')

# 同时添加如下代码, 这样每次环境(kernel)启动的时候只要运行下方代码即可:
# Also add the following code, so that every time the environment (kernel) starts, just run the following code:
import sys
sys.path.append('/home/aistudio/external-libraries')


# In[ ]:


######################################## 查看DCAS2017E数据 #########################################################
import os
import numpy as np
import soundfile
import matplotlib.pyplot as plt

os.chdir('/home/aistudio/TUT_source/TUT-rare-sound-events-2017-development/data/source_data/events/gunshot')
print('当前路径：')
print(os.getcwd())
FileList = os.listdir(os.getcwd())
for i in range(0,len(FileList)):
    file = os.path.join(os.getcwd(),FileList[i])
    if os.path.isfile(file):
        SplitFileName = os.path.splitext(file)
        if SplitFileName[1] == '.wav':
            data, sample_rate = soundfile.read(file)
            print('文件名：')
            print(file)
            print('文件维度：')
            print(data.shape)
            print('信号波形：')
            plt.plot(data)
            plt.show()


# In[ ]:


######################################## MFCC+GMM训练(基于课设数据) #########################################################

import os
import numpy as np
import soundfile as sf
import librosa
import matplotlib.pyplot as plt
from sklearn import mixture

#调整路径
os.chdir('/home/aistudio/test_data')
print('当前路径：')
print(os.getcwd())

#参数
spk_num = 2
ncentres = 5

#遍历标签
for spk_cyc in range(1,spk_num+1):
    print('\ntraining for speaker',str(spk_cyc))

    #根据样本标签设定样本量
    if spk_cyc == 1:
        Tra_start = 1;
        Tra_end = 6;
    elif spk_cyc == 2:
        Tra_start = 1;
        Tra_end = 6;

    #遍历该标签下的所有样本
    for sph_cyc in range(Tra_start,Tra_end+1):
        #读取文件
        filename = ''
        if spk_cyc == 1:
            filename = 'dataset_gun'
        elif spk_cyc == 2:
            filename = 'dataset_background'
        filename = filename+str(sph_cyc)+'.wav'
        [sig,fs] = librosa.load(filename,mono = True)
        if len(np.shape(sig))>1:
            pre_sph = np.transpose(np.array(sig))[0][:]
        else:
            pre_sph = np.transpose(np.array(sig))
        print('pre-processing data:', filename,'shape:',np.shape(pre_sph))
        #plt.plot(pre_sph)
        #plt.show()

        #特征提取
        cof_num = 20#MFCC系数个数
        mfcc = np.transpose(np.array(librosa.feature.mfcc(pre_sph,fs,n_mfcc=cof_num)))
        #plt.plot(mfcc)
        #plt.show()
        if spk_cyc == 1:
            if sph_cyc == Tra_start:
                MFCCMatrix1 = mfcc
            else:
                MFCCMatrix1 = np.append(MFCCMatrix1,mfcc,axis = 0)
            print('extracing MFCC, MFCC shape:',np.shape(mfcc),'MFCC matrix shape:',np.shape(MFCCMatrix1))
        elif spk_cyc == 2:
            if sph_cyc == Tra_start:
                MFCCMatrix2 = mfcc
            else:
                MFCCMatrix2 = np.append(MFCCMatrix2,mfcc,axis = 0)
            print('extracing MFCC, MFCC shape:',np.shape(mfcc),'MFCC matrix shape:',np.shape(MFCCMatrix2))


        
    #训练GMM
    if spk_cyc == 1:
        estimator1 = mixture.GaussianMixture(n_components=3,init_params='kmeans')
        estimator1.fit(MFCCMatrix1)
        print('\ntraining GMM 1...')
    elif spk_cyc == 2:
        estimator2 = mixture.GaussianMixture(n_components=3,init_params='kmeans')
        estimator2.fit(MFCCMatrix2)
        print('\ntraining GMM 2...')

print('\ndone')


# In[ ]:


######################################## MFCC+GMM测试(基于课设数据)  #########################################################

#调整路径
os.chdir('/home/aistudio/test_data')
print('当前路径：')
print(os.getcwd())

#参数
spk_num = 2
ncentres = 5

#遍历标签
for spk_cyc in range(1,spk_num+1):
    print('\ntesting for speaker',str(spk_cyc))

    #根据样本标签设定样本量
    if spk_cyc == 1:
        Tra_start = 1;
        Tra_end = 3;
    elif spk_cyc == 2:
        Tra_start = 1;
        Tra_end = 3;

    #遍历该标签下的所有样本
    for sph_cyc in range(Tra_start,Tra_end+1):
        #读取文件
        filename = ''
        if spk_cyc == 1:
            filename = 'dataset_gun'
        elif spk_cyc == 2:
            filename = 'dataset_background'
        filename = filename+str(sph_cyc)+'.wav'
        [sig,fs] = librosa.load(filename,mono = True)
        if len(np.shape(sig))>1:
            pre_sph = np.transpose(np.array(sig))[0][:]
        else:
            pre_sph = np.transpose(np.array(sig))
        print('pre-processing data:', filename,'shape:',np.shape(pre_sph))
        #plt.plot(pre_sph)
        #plt.show()

        #特征提取
        cof_num = 20#MFCC系数个数
        mfcc = np.transpose(np.array(librosa.feature.mfcc(pre_sph,fs,n_mfcc=cof_num)))
        #plt.plot(mfcc)
        #plt.show()
        if spk_cyc == 1:
            if sph_cyc == Tra_start:
                MFCCMatrix1 = mfcc
            else:
                MFCCMatrix1 = np.append(MFCCMatrix1,mfcc,axis = 0)
            print('extracing MFCC, MFCC shape:',np.shape(mfcc),'MFCC matrix shape:',np.shape(MFCCMatrix1))
        elif spk_cyc == 2:
            if sph_cyc == Tra_start:
                MFCCMatrix2 = mfcc
            else:
                MFCCMatrix2 = np.append(MFCCMatrix2,mfcc,axis = 0)
            print('extracing MFCC, MFCC shape:',np.shape(mfcc),'MFCC matrix shape:',np.shape(MFCCMatrix2))
        
        #测GMM
        predict1 = sum(estimator1.score_samples(mfcc))
        predict2 = sum(estimator2.score_samples(mfcc))
        print('estimating...')
        print('output of estimators1 = ',predict1,'estimator2 = ',predict2)
        if predict1 >= predict2:
            print('prediction: SPEAKER 1')
        else:
            print('prediction: SPEAKER 2')

print('\ndone\n')


# In[ ]:


######################################## TUT数据(DCASE2017)调整 #########################################################
import os

#程序自定义参数
EventType = 'babycry'
CurrentPath = '/home/aistudio/test_TUT/events/'+EventType#文件所在路径 
NewFileNameHead_Development = 'TUT_train_'+EventType#新前缀
NewFileNameHead_Evaluation = 'TUT_test_'+EventType
NewFileNameRear = '.wav'#新后缀

#切换路径到当前文件夹
os.chdir(CurrentPath)
print('当前路径:')
print(os.getcwd())

#遍历文件夹下文件
FileCount = 0
DevelopmentCount = 0
EvaluationCount = 0
FileList = os.listdir(os.getcwd())
for i in range(0,len(FileList)):
     file = os.path.join(os.getcwd(),FileList[i])
     if os.path.isfile(file):
        SplitFileName = os.path.splitext(file)
        #音频数据重新命名
        if(SplitFileName[1] == '.wav'):
            FileCount += 1
            if FileCount <= 0.8*(len(FileList)/2):
                DevelopmentCount += 1
                NewFileName = NewFileNameHead_Development+str(DevelopmentCount)+NewFileNameRear
            else:
                EvaluationCount += 1
                NewFileName = NewFileNameHead_Evaluation+str(EvaluationCount)+NewFileNameRear
            os.rename(file,os.path.join(os.getcwd(),NewFileName))

print('wav文件总数：',FileCount,',Development = ',DevelopmentCount,',Evaluation = ',EvaluationCount)


# In[ ]:


######################################## MFCC+GMM训练(基于TUT数据) #########################################################

import os
import numpy as np
import soundfile as sf
import librosa
import matplotlib.pyplot as plt
from sklearn import mixture

#调整路径
BasicPath = '/home/aistudio/test_TUT/events/'

#参数
spk_num = 3
DevelopmentCount_babycry = 27
DevelopmentCount_glassbreak = 52
DevelopmentCount_gunshot = 49

#遍历标签
for spk_cyc in range(1,spk_num+1):    
    #根据样本标签设定样本量
    target = ''
    if spk_cyc == 1:#训练babycry
        Tra_start = 1;
        Tra_end = DevelopmentCount_babycry;
        target = 'babycry'
        os.chdir(BasicPath+target)
    elif spk_cyc == 2:#训练glassbreak
        Tra_start = 1;
        Tra_end = DevelopmentCount_glassbreak;
        target = 'glassbreak'
        os.chdir(BasicPath+target)
    elif spk_cyc == 3:#训练gunshot
        Tra_start = 1;
        Tra_end = DevelopmentCount_gunshot;
        target = 'gunshot'
        os.chdir(BasicPath+target)
    print('当前路径:')
    print(os.getcwd())
    print('正在训练speaker ',str(spk_cyc),':',target)

    #遍历该标签下的所有样本
    for sph_cyc in range(Tra_start,Tra_end+1):
        #读取文件
        filename = 'TUT_train_'+target+str(sph_cyc)+'.wav'
        [sig,fs] = librosa.load(filename,mono = True)
        if len(np.shape(sig))>1:
            pre_sph = np.transpose(np.array(sig))[0][:]
        else:
            pre_sph = np.transpose(np.array(sig))
        print('预处理数据:', filename,',shape:',np.shape(pre_sph))
        #plt.plot(pre_sph)
        #plt.show()

        #特征提取
        cof_num = 20#MFCC系数个数
        mfcc = np.transpose(np.array(librosa.feature.mfcc(pre_sph,fs,n_mfcc=cof_num)))
        #plt.plot(mfcc)
        #plt.show()
        if spk_cyc == 1:
            if sph_cyc == Tra_start:
                MFCCMatrix1 = mfcc
            else:
                MFCCMatrix1 = np.append(MFCCMatrix1,mfcc,axis = 0)
            print('提取MFCC, MFCC shape:',np.shape(mfcc),'MFCC matrix shape:',np.shape(MFCCMatrix1))
        elif spk_cyc == 2:
            if sph_cyc == Tra_start:
                MFCCMatrix2 = mfcc
            else:
                MFCCMatrix2 = np.append(MFCCMatrix2,mfcc,axis = 0)
            print('提取MFCC, MFCC shape:',np.shape(mfcc),'MFCC matrix shape:',np.shape(MFCCMatrix2))
        elif spk_cyc == 3:
            if sph_cyc == Tra_start:
                MFCCMatrix3 = mfcc
            else:
                MFCCMatrix3 = np.append(MFCCMatrix3,mfcc,axis = 0)
            print('提取MFCC, MFCC shape:',np.shape(mfcc),'MFCC matrix shape:',np.shape(MFCCMatrix3))
        
    #为当前speaker训练GMM
    if spk_cyc == 1:
        estimator1 = mixture.GaussianMixture(n_components=3,init_params='kmeans')
        estimator1.fit(MFCCMatrix1)
        print('\ntraining GMM 1...')
    elif spk_cyc == 2:
        estimator2 = mixture.GaussianMixture(n_components=3,init_params='kmeans')
        estimator2.fit(MFCCMatrix2)
        print('\ntraining GMM 2...')
    elif spk_cyc == 3:
        estimator3 = mixture.GaussianMixture(n_components=3,init_params='kmeans')
        estimator3.fit(MFCCMatrix3)
        print('\ntraining GMM 3...')
    print('\n')

print('\ndone')


# In[43]:


######################################## MFCC+GMM测试(基于TUT数据)  #########################################################

import os
import numpy as np
import soundfile as sf
import librosa
import matplotlib.pyplot as plt
from sklearn import mixture

#调整路径
BasicPath = '/home/aistudio/test_TUT/events/'

#参数
spk_num = 3
Evaluation_babycry = 7
Evaluation_glassbreak = 13
Evaluation_gunshot = 12

#遍历标签
right = [0,0,0,0]
wrong = [0,0,0,0]
for spk_cyc in range(1,spk_num+1):   
    right[spk_cyc] = 0
    wrong[spk_cyc] = 0

    #根据样本标签设定样本量
    target = ''
    if spk_cyc == 1:#训练babycry
        Tra_start = 1;
        Tra_end = Evaluation_babycry;
        target = 'babycry'
        os.chdir(BasicPath+target)
    elif spk_cyc == 2:#训练glassbreak
        Tra_start = 1;
        Tra_end = Evaluation_glassbreak;
        target = 'glassbreak'
        os.chdir(BasicPath+target)
    elif spk_cyc == 3:#训练gunshot
        Tra_start = 1;
        Tra_end = Evaluation_gunshot;
        target = 'gunshot'
        os.chdir(BasicPath+target)
    print('当前路径:')
    print(os.getcwd())
    print('正在测试speaker ',str(spk_cyc),':',target)

    #遍历该标签下的所有样本
    for sph_cyc in range(Tra_start,Tra_end+1):

        #读取文件
        filename = 'TUT_test_'+target+str(sph_cyc)+'.wav'
        [sig,fs] = librosa.load(filename,mono = True)
        if len(np.shape(sig))>1:
            pre_sph = np.transpose(np.array(sig))[0][:]
        else:
            pre_sph = np.transpose(np.array(sig))
        print('预处理数据:', filename,',shape:',np.shape(pre_sph))
        #plt.plot(pre_sph)
        #plt.show()

        #特征提取
        cof_num = 20#MFCC系数个数
        mfcc = np.transpose(np.array(librosa.feature.mfcc(pre_sph,fs,n_mfcc=cof_num)))
        #plt.plot(mfcc)
        #plt.show()
    
        #测GMM
        predict1 = sum(estimator1.score_samples(mfcc))
        predict2 = sum(estimator2.score_samples(mfcc))
        predict3 = sum(estimator3.score_samples(mfcc))
        print('estimating...')
        print('各GMM输出: baby = ',predict1,',glass = ',predict2,',gun = ',predict3)
        if predict1 >= predict2 and predict1 >= predict3:
            print('预测结果为speaker 1: babycry')
            if target == 'babycry':
                right[spk_cyc] += 1
                print('----------CORRECT----------')
            else:
                wrong[spk_cyc] += 1
                print('-----------WRONG-----------')
        elif predict2 >= predict1 and predict2 >= predict3:
            print('预测结果为speaker 2: glassbreak')
            if target == 'glassbreak':
                right[spk_cyc] += 1
                print('----------CORRECT----------')
            else:
                wrong[spk_cyc] += 1
                print('-----------WRONG-----------')
        elif predict3 >= predict1 and predict3 >= predict2:
            print('预测结果为speaker 3: gunshot')
            if target == 'gunshot':
                right[spk_cyc] += 1
                print('----------CORRECT----------')
            else:
                wrong[spk_cyc] += 1
                print('-----------WRONG-----------')
print('\nbabycry:')
print('\nCorrect Rate = ',right[1]/(right[1]+wrong[1])*100,'%,Error Rate = ',wrong[1]/(right[1]+wrong[1])*100,'%\n')

print('\nglassbreak:')
print('\nCorrect Rate = ',right[2]/(right[2]+wrong[2])*100,'%,Error Rate = ',wrong[2]/(right[2]+wrong[2])*100,'%\n')

print('\ngunshot:')
print('\nCorrect Rate = ',right[3]/(right[3]+wrong[3])*100,'%,Error Rate = ',wrong[3]/(right[3]+wrong[3])*100,'%\n')


print('\ndone\n')


# In[44]:


print('%')


# 请点击[此处](https://ai.baidu.com/docs#/AIStudio_Project_Notebook/a38e5576)查看本环境基本用法.  <br>
# Please click [here ](https://ai.baidu.com/docs#/AIStudio_Project_Notebook/a38e5576) for more detailed instructions. 
