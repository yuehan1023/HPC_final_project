import numpy as np
import matplotlib.pyplot as plt
import pickle

f = open('heatResults/dt_Tcool_Thot.txt','rb')
parameters = pickle.load(f)
f.close

dt = parameters[0]
Tcool = parameters[1]
Thot = parameters[2]
mfig = parameters[3] 
print(mfig)

fig = plt.figure()
for fignum in range(1,len(mfig)+1): # [ )
    m = mfig[fignum-1]
    print(m, fignum)
    ax = fig.add_subplot(220 + fignum) #may modify
    f = open('heatResults/result'+str(fignum)+'.txt','rb')
    u = pickle.load(f)
    f.close
    im = ax.imshow(u.copy(), cmap=plt.get_cmap('rainbow'), vmin=Tcool,vmax=Thot)
    ax.set_axis_off()   
    ax.set_title('{:.1f} ms'.format(m*dt*1000))

fig.subplots_adjust(right=0.85)
cbar_ax = fig.add_axes([0.9, 0.15, 0.03, 0.7])
cbar_ax.set_xlabel('$T$ / K', labelpad=20)
fig.colorbar(im, cax=cbar_ax)
plt.show()