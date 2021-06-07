import numpy as np
import pickle

# plate size, mm
w = 10.  
h = 10.
# intervals in x-, y- directions, mm
dx = dy = 0.1
# Thermal diffusivity of steel, mm2.s-1
D = 4.

#Tcool, Thot = 0., 100.
Tcool, Thot = 300., 700.

nx, ny = int(w/dx), int(h/dy)

dx2, dy2 = dx*dx, dy*dy
dt = dx2 * dy2 / (2 * D * (dx2 + dy2)) #unit:second
# if dt > 0.0001:
#     dt = 0.0001

# Initial conditions - edge = Thot, inside = Tcool
u0 = Thot * np.ones((nx, ny))
u0[1:-1, 1:-1] = Tcool
u = u0.copy()

# Initial conditions - circle of radius r centred at (cx,cy) (mm)
# u0 = Tcool * np.ones((nx, ny))
# r, cx, cy = 2, 5, 5
# r2 = r**2
# for i in range(nx):
#     for j in range(ny):
#         p2 = (i*dx-cx)**2 + (j*dy-cy)**2
#         if p2 < r2:
#             u0[i,j] = Thot
# u = u0.copy()

def do_timestep(u0, u):
    # Propagate with forward-difference in time, central-difference in space
    u[1:-1, 1:-1] = u0[1:-1, 1:-1] + D * dt * (
          (u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/dx2
          + (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/dy2 )

    u0 = u.copy()
    return u0, u

# Number of timesteps
#nsteps = 1501
nsteps = 101
# Output 4 figures at these timesteps
#mfig = [0, 500, 1000, 1500]
mfig = [0, 10, 50, 100]
fignum = 0
for m in range(nsteps):
    u0, u = do_timestep(u0, u)
    if m in mfig:
        fignum += 1
        print(m, fignum)
        f = open('heatResults/result'+str(fignum)+'.txt','wb')
        pickle.dump(u,f)
        f.close()

parameters = [dt, Tcool, Thot, mfig]
f = open('heatResults/dt_Tcool_Thot.txt','wb')
pickle.dump(parameters,f)
f.close()

