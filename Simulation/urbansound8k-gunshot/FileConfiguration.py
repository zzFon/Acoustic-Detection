

import os

#程序自定义参数
CurrentPath = 'E:/Git-Repository/Acoustic-Detection/Simulation/urbansound8k-gunshot'#文件所在路径 
NewFileNameHead = 'urbansound_gunshot_'#新前缀
NewFileNameRear = '.wav'#新后缀

#切换路径到当前文件夹
os.chdir(CurrentPath)
print('当前路径:')
print(os.getcwd())

#遍历文件夹下文件
FileCount = 0
FileList = os.listdir(os.getcwd())
for i in range(0,len(FileList)):
     file = os.path.join(os.getcwd(),FileList[i])
     if os.path.isfile(file):
          SplitFileName = os.path.splitext(file)
          #音频数据重新命名
          if(SplitFileName[1] == '.wav'):
               FileCount += 1
               NewFileName = NewFileNameHead+str(FileCount)+NewFileNameRear
               os.rename(file,os.path.join(os.getcwd(),NewFileName))

