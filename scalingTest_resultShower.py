import os
import pickle
import numpy as np

existFolder = os.path.exists('scalingTestResults')
if not existFolder:
    print('the folder, scalingTestResults, does not exist')
else:
    init_cdt = 'hotEdge'
    dx = 0.1  ########## to be modified
    tmax = 0.
    tmin = 0.

    num_ranks = np.zeros((1,9))
    for i in range(9):
        num_ranks[0,i] = 2**i
    
        filePath = 'scalingTestResults/'+init_cdt+'_size'+str(int(num_ranks[0,i]))+'.txt'
        existFolder = os.path.exists(filePath)
        if existFolder:
            f = open(filePath,'rb')
            # scalingRecords = np.ones((1,int(num_ranks[0,i])*2))
            scalingRecords = np.ones((int(num_ranks[0,i]),2))
            scalingRecords = pickle.load(f)
            f.close()

            tmin = scalingRecords.min()
            tmax = scalingRecords.max()
            t = tmax - tmin
            print(str(num_ranks[0,i])+'   '+str(t)+' s')
        else:
            print('lack   ',end=""),
            print(filePath)


