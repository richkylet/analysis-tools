
import numpy as np
import matplotlib.pyplot as plt
import random 
"""
Generate an animated figure of the pressure field of acoustic point source(s)
"""
#--------------------------------------
# physical parameters
f=850                 # freqeuncy of sources
N=2                   # number of sources
cyc = 30              # number of cycles
t = np.linspace(0,cyc/(2.5*f),cyc)
c = 1480              # [m/s] speed of sound in medium
lambda1 = c/f         # [m] wavelength
rho =998              # [kg/m**3] density of medium
omega = 2*np.pi*f     # radial frequency
k = 2*np.pi*lambda1   # wave number
#------------------------------------------
# some field grid:
x = np.linspace(1,6,256)
y = np.linspace(1,6,256)
#------------------------------------------
#location of a single pt source
def fieldLoc(): 
    global x, y
    # rand index of a given point sources location
    xi = random.randrange(len(x)/2,2*len(x)/3)
    yi = random.randrange(len(y)/2,2*len(y)/2)
    # physical location of rand pt source
    xl = x[xi]
    yl = y[yi]
    # distance from pt source to all other points
    XX, YY = np.meshgrid((xl-x)**2, (yl-y)**2)
    rl = np.sqrt(XX + YY)
    plt.figure(1)
    plt.plot(xi,yi,'yo')
    plt.show 
    return rl
#------------------------------------------
# field of point source(s) at a given time
def pt_fieldt(): 
    global rho, c, k, omega
    Q = .05*random.uniform(1,3) # random source strength[m**3/s] 
    #Qphase= np.exp(-1j*random.uniform(1,3)) # random source strength[m**3/s] 
    #Q = Qamp*Qphase
    rl = fieldLoc()            # location of source
    Pt = np.empty((0,len(rl),len(rl)))
    for i in range(len(t)):
        P = -1j*rho*c*k*Q*np.exp(-1j*(omega*t[i]+k*rl))/(4*np.pi*rl)
        Pt= np.append(Pt, [P], axis=0)
    return Pt
#------------------------------------------
# fig options and plot
def fig_init(i): 
    plt.title('t= #'+str(i))
    plt.pause(cyc/(2.5*f)/5)
    axes = plt.gca()
    axes.set_xlim([0,255])
    axes.set_ylim([0,255])
    axes.get_xaxis().set_visible(False)
    axes.get_yaxis().set_visible(False)
#------------------------------------------  
# run and plot:
plt.close("all")

Pt_n = np.empty((len(t),256,256))
for n in range(N):
    print('n = ' +str(n))
    Pt1 = pt_fieldt()
    Pt_n = Pt_n + Pt1

for i in range(len(t)):
    Pxx = abs(Pt_n.real[i,:,:])
    plt.imshow(Pxx, cmap="hot") #imsx.append([im])
    fig_init(i)


