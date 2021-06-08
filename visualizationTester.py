import time
from mpi4py import MPI
import numpy as np
import pickle
import os

t_init = time.perf_counter()

# for Beskow
comm = MPI.COMM_WORLD
size = comm.Get_size()# make sure nx is divisible by size
rank = comm.Get_rank()
# # for personal laptop
# rank = 0 
# size = 1

nsteps = 10
len_T_rank = 2+nsteps*2
T_rank = np.ones((1, len_T_rank))
pT = 0
T_rank[rank, pT] = t_init
pT +=1
for i in range(nsteps):
    time.sleep(rank*0.001) #simulate "computing for some micro seconds"
    time.sleep(0.001)
    T_rank[rank, pT] = time.perf_counter()
    pT +=1
    time.sleep(0.001) # simulate idle period
    T_rank[rank, pT] = time.perf_counter()
    pT +=1

if rank==0:
    existFolder = os.path.exists('timeRecords')
    if not existFolder:
        directoryNow = os.getcwd()
        os.mkdir(directoryNow+'//timeRecords')
    
    parameters = [size, nsteps, len_T_rank]
    f = open('timeRecords/size_nsteps_lenTrank.txt','wb')
    pickle.dump(parameters,f)
    f.close()
    print('size, nsteps, lenTrank = '),
    print(parameters)

T_rank[rank, pT] = time.perf_counter() # record the termination time


f = open('timeRecords/T_rank'+str(rank)+'.txt','wb')
pickle.dump(T_rank,f)
f.close()
    
