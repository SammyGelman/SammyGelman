import numpy as np

C = 50
T = np.genfromtxt('T.dat')
# T = delete(T,[0,1,2,-1,-2,-3,-4])
time = np.genfromtxt('time.dat')

def cycle_extract(t,C,r_data):
    t_data = []
    for count in range(len(r_data)):
        if (count % C) == t:
            t_data.append(r_data[count])
    return np.mean(np.array(t_data))

mag_contour = np.zeros([len(time),len(T)])
i=0

for temp in T:
    mag_strip = []
    if temp in [0.1,0.2,0.7,0.8,0.9,1.0]:
        for t in time:
            mag_strip.append(cycle_extract(t,C,np.genfromtxt('phase_diagram_T'+str(temp)+'/curves.dat')[:,3]))
        mag_contour[:,i] = mag_strip
        np.savetxt('mag_time'+str(t)+'_temp'+str(temp)+'.dat',mag_strip)
    else:
        for t in time:
            mag_strip.append(cycle_extract(t,C,np.genfromtxt('transition_T'+str(temp)+'/curves.dat')[:,3]))
        mag_contour[:,i] = mag_strip
        np.savetxt('mag_time'+str(t)+'_temp'+str(temp)+'.dat',mag_strip)
    i += 1
    
np.savetxt('mag_contour.dat',mag_contour)
