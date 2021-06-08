import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import pickle

MHz = 2601.
Mcycle = 1

f = open('timeRecords/size_nsteps_lenTrank.txt','rb')
parameters = pickle.load(f)
f.close

# load parameters
size = parameters[0]
nsteps = parameters[1]
lenTrank_body = 2+nsteps*4
# lenTrank_body = parameters[2]
lenTrank_ends = 2+nsteps*2
timeRecord = np.ones((size, lenTrank_body)) # lenTrank_body>lenTrank_ends
print('size, nsteps, lenTrank_body, lenTrank_ends = ', end="")
print(parameters,end=""),
print('  '+str(lenTrank_ends))
# if size==1:
#     quit()


# load time stamp record
for i in range(size):
    f = open('timeRecords/T_rank'+str(i)+'.txt','rb')
    if i==0 or i==size-1:
        timeRecord[i, 0:lenTrank_ends] = pickle.load(f)
    else:
        timeRecord[i, :] = pickle.load(f)
    f.close

    print('rank '+str(i)+': ')
    print('    start at '+str(timeRecord[i, 0])+'s    ',end="")
    if i==0 or i==size-1:
        print('end at '+str(timeRecord[i, lenTrank_ends-1])+'s')
    else:
        print('end at '+str(timeRecord[i, lenTrank_body-1])+'s')
    

# derive when the application starts and when ends. use system absolute time
tmin = timeRecord[:, 0].min()
tmin_i = timeRecord[:, 0].argmin()
print('the application start at ', end="")
print(tmin,end=""),
print('s')
tmax = timeRecord[1:size-1, lenTrank_body-1].max()
tmax_i = timeRecord[1:size-1, lenTrank_body-1].argmax()

tmp1 = timeRecord[0,lenTrank_ends-1]
tmp2 = timeRecord[size-1,lenTrank_ends-1]
if tmax<tmp1 or tmax<tmp2:
    if tmp1>=tmp2:     
        tmax = tmp1
        tmax_i = 0 # the first rank
    else:
        tmax = tmp2
        tmax_i = size-1  # the last rank
print('the application end at  ', end="")
print(tmax,end=""),
print('s')


timeRecord = timeRecord - tmin # normalize. absolute time -> relative time
tInterval = Mcycle/MHz # represent the elasped time for each single Mcycle. unit: s
N = int((tmax-tmin)/tInterval)# number of time intervals on the x-axis
print('the relative longest running time = ', end="")
print(tmax-tmin)
print('time interval = '+str(Mcycle)+' Mcycles/', end="")
print(MHz, end=""),
print(' MHz = ', end="")
print(tInterval)
print('N = ', end="")
print(N)


# transform the timeRecords into timeTable (i.e. idle-period plot)
timeTable = np.ones((size,N))
for i in range(size):    
    if i==0 or i==size-1:
        lenTrank = lenTrank_ends
    else:
        lenTrank = lenTrank_body

    jj=1    
    for j in range(int((lenTrank-2)/2)): # range(number of idle periods)
        istart = int(timeRecord[i, jj]/tInterval)
        iend = int(timeRecord[i, jj+1]/tInterval)
        timeTable[i, istart:iend] = 0 # mark idle period as 0, mark computing period as 1
        jj+=2
    tmp = int(timeRecord[i, lenTrank-1]/tInterval)
    timeTable[i,tmp:] = 0 #mark termination as 0
# print(timeTable)

plt.figure(figsize=(size,N))
bi_cmap = matplotlib.colors.ListedColormap(['blue','yellow'])# yellow==1==computing, blue==0==idling
plt.imshow(timeTable,cmap=bi_cmap,extent=[0,N,size,0]) # display data as an image
plt.show()
