from mpi4py import MPI
import numpy as np
import pickle


comm = MPI.COMM_WORLD
size = comm.Get_size()# make sure nx is divisible by size
rank = comm.Get_rank()
if rank==0:
    print('size = '+str(size))
    print('timesteps=100, dx=0.1')

w = 25.6  # plate size, mm
h = 32.
dx = dy = 0.1 # intervals in x-, y- directions, mm

nsteps = 101
# Output 4 figures at these timesteps
mfig = [0, 10, 50, 100]

D = 4. # Thermal diffusivity of steel, mm2.s-1
Tcool, Thot = 0., 100.
#Tcool, Thot = 300., 700.

nx, ny = int(w/dx), int(h/dy) 
dx2, dy2 = dx*dx, dy*dy
dt = dx2 * dy2 / (2 * D * (dx2 + dy2)) #unit:second
# if dt > 0.0001:
#     dt = 0.0001


# Initial conditions - edge = Thot, inside = Tcool
# u0_global = Thot * np.ones((nx, ny))
# u0_global[1:-1, 1:-1] = Tcool

# Initial conditions - circle of radius r centred at (cx,cy) (mm)
u0_global = Tcool * np.ones((nx, ny))
r, cx, cy = 2, 5, 5
r2 = r**2
for i in range(nx):
    for j in range(ny):
        p2 = (i*dx-cx)**2 + (j*dy-cy)**2
        if p2 < r2:
            u0_global[i,j] = Thot

nx_local = int(nx/size)
ny_local = ny

if rank==0:
    x_start = 0
    x_end = nx_local
    u0 = u0_global[x_start:(x_end+1),:]
    u_global = u0_global.copy() # for gathering results
    u = u0.copy()
    downGhost = nx_local
elif rank==size-1:
    x_start = rank*nx_local - 1
    x_end = nx - 1
    u0 = u0_global[x_start:(x_end+1),:]
    u = u0.copy()
    downGhost = nx_local
else :
    x_start = rank*nx_local - 1
    x_end = x_start + nx_local + 1
    u0 = u0_global[x_start:(x_end+1),:]
    u = u0.copy()
    downGhost = nx_local + 1


def do_timestep(u0, u):
    # Propagate with forward-difference in time, central-difference in space
    u[1:-1, 1:-1] = u0[1:-1, 1:-1] + D * dt * (
          (u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/dx2
          + (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/dy2 )

    u0 = u.copy()
    return u0, u



fignum = 0
for m in range(nsteps):
    u0, u = do_timestep(u0, u)
    # a process must ask for the value at the ghost cells before next calculation!
    # the point-to-point communication method used here enable multiple send-receive take place simutaneously
    # 1. down, tag=m
    rankIsEven = (rank%2==0)
    if rank==0:
        comm.send(u[downGhost-1,:], dest=1, tag=0)
        #print('rank '+str(rank)+' send to rank '+str(1)+'at m='+str(m))
    elif rank==size-1:
        req = comm.irecv(source=rank-1, tag=0)
        u[0,:] = req.wait()
        #print('rank '+str(rank)+' receive from rank '+str(rank-1)+'at m='+str(m))
    else:
        if rankIsEven:
            comm.send(u[downGhost-1,:], dest=rank+1, tag=0)
            #print('rank '+str(rank)+' send to rank '+str(rank+1)+'at m='+str(m))
            req = comm.irecv(source=rank-1, tag=0)
            u[0,:] = req.wait()
            # print('rank '+str(rank)+' receive from rank '+str(rank-1)+'at m='+str(m))
        else:
            req = comm.irecv(source=rank-1, tag=0)
            u[0,:] = req.wait()
            # print('rank '+str(rank)+' receive from rank '+str(rank-1)+'at m='+str(m))
            comm.send(u[downGhost-1,:], dest=rank+1, tag=0)
            # print('rank '+str(rank)+' send to rank '+str(rank+1)+'at m='+str(m))

    # 2. up, tag=m+1
    if rank==0:
        req = comm.irecv(source=1, tag=1)
        u[downGhost,:] = req.wait()
        # print('rank '+str(rank)+' receive from rank '+str(rank+1)+'at tag='+str(m+1))
    elif rank==size-1:
        comm.send(u[1,:], dest=rank-1, tag=1)
        # print('rank '+str(rank)+' send to rank '+str(rank-1)+'at tag='+str(m+1))
    else:
        if rankIsEven:
            comm.send(u[1,:], dest=rank-1, tag=1)
            # print('rank '+str(rank)+' send to rank '+str(rank-1)+'at tag='+str(m+1))
            req = comm.irecv(source=rank+1, tag=1)
            u[downGhost,:] = req.wait()
            # print('rank '+str(rank)+' receive from rank '+str(rank+1)+'at tag='+str(m+1))
        else:
            req = comm.irecv(source=rank+1, tag=1)
            u[downGhost,:] = req.wait()
            # print('rank '+str(rank)+' receive from rank '+str(rank+1)+'at tag='+str(m+1))
            comm.send(u[1,:], dest=rank-1, tag=1)
            # print('rank '+str(rank)+' send to rank '+str(rank-1)+'at tag='+str(m+1))
    u0 = u.copy()

    if m in mfig:
        fignum += 1
        if rank==0:
            print(m, fignum)
            u_global[0:nx_local,:] = u[0:nx_local,:]
            for k in range(1,size): #[)
                u_global[nx_local*k:nx_local*(k+1),:] = comm.recv(source=k, tag=2)
            
            f = open('heatResults/result'+str(fignum)+'.txt','wb')
            pickle.dump(u_global,f)
            f.close()
        else:
            comm.send(u[1:nx_local+1, :], dest=0, tag=2)
            #print('rank '+str(rank)+' finally send to rank0')


parameters = [dt, Tcool, Thot, mfig]
f = open('heatResults/dt_Tcool_Thot.txt','wb')
pickle.dump(parameters,f)
f.close()


