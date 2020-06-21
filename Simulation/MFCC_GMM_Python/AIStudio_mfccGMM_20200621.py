#!/usr/bin/env python
# coding: utf-8

# In[2]:


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


# In[3]:


######################################## 查看DCASE数据 #########################################################
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


# In[44]:


######################################## MFCC+GMM训练 #########################################################

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


# In[54]:


######################################## MFCC+GMM测试 #########################################################

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
        print('\n')

print('\ndone\n')


# In[39]:


estimator.get_params()
np.shape(MFCCMatrix[1])
np.shape(np.reshape(MFCCMatrix[1],(1,20)))
estimator.score_samples(np.reshape(MFCCMatrix[1],(1,20)))
d = estimator.score_samples(MFCCMatrix)
for i in range(0,len(d)):
    print(d[i])


# In[9]:


from sklearn import datasets 
from sklearn import model_selection
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

iris = datasets.load_iris()
# 2.取特征空间中的4个维度（切片操作，":"表示从第0行到最后一行，":4"表示从第0列到第3列）
#有的教程说"4"是取四个数据列，这种说法是错误的。4是3后面的，是结尾标志，否则和"2:4"这种取两个数据不一致了
X = iris.data[:,:4]  
# 3.搭建模型，构造KMeans聚类器
estimator = KMeans(n_clusters=3)
#开始聚类训练   
estimator.fit(X)
# 获取聚类标签
label_pred = estimator.labels_ 
# 绘制数据分布图（以花萼长度和宽度为展示依据）
plt.scatter(X[:, 0], X[:, 1], c="red", marker='o', label='see')  
plt.xlabel('calyx length')  
plt.ylabel('calyx width')  
plt.legend(loc=2)  
plt.show()  
# 绘制k-means结果
x0 = X[label_pred == 0]
x1 = X[label_pred == 1]
x2 = X[label_pred == 2]
plt.scatter(x0[:, 0], x0[:, 1], c="red", marker='o', label='label0')  
plt.scatter(x1[:, 0], x1[:, 1], c="green", marker='*', label='label1')  
plt.scatter(x2[:, 0], x2[:, 1], c="blue", marker='+', label='label2')  
#花萼的长宽
plt.xlabel('calyx length')  
plt.ylabel('calyx width')  
plt.legend(loc=2)  
plt.show()


# In[10]:


iris


# In[28]:


a = np.array([1,2,3])
b = np.array([4,5,6])
np.append(a,b,axis=0)


# 请点击[此处](https://ai.baidu.com/docs#/AIStudio_Project_Notebook/a38e5576)查看本环境基本用法.  <br>
# Please click [here ](https://ai.baidu.com/docs#/AIStudio_Project_Notebook/a38e5576) for more detailed instructions. 
