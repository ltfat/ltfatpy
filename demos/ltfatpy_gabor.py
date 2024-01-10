#prerequisites: numpy, scipy, oct2py (for now), Octave installed
#matplotlib is not required, but highly useful

#so one can run it without having ltfatpy installed...
import sys, os
from pathlib import Path
#bp = os.path.dirname(os.path.dirname(__file__))
#tp = Path(os.path.dirname(os.path.dirname(__file__))).parent
#print(tp)
#sys.path.append(tp)
#sys.path.append("/home/clara/Documents/ltfat_development_code/ltfatpy")

#the necessary imports
from ltfatpy import ltfat
import numpy as np
from numpy import linalg as LA

import matplotlib.pyplot as plt

#define some complex random input signal
f_real = np.random.rand(44100,1) 
f_cpx = f_real + 1j * np.random.rand(44100,1) 


plt.figure(1)

plt.subplot(211)
plt.plot(f_cpx.real)
plt.yscale('linear')
plt.title('Real part of the signal')
plt.xlabel('Time [samples]')
plt.ylabel('Amplitude [samples]')
plt.grid(True)

plt.subplot(212)
plt.plot(f_cpx.imag)
plt.yscale('linear')
plt.xlabel('Time [samples]')
plt.ylabel('Amplitude [samples]')
plt.title('Complex part of the signal')
plt.grid(True)

plt.show()


#and some Gabor parameters
a = 10 #hopsize
M = 20 #number of frequency channels
g = 'gauss' #window type

#let's start with a DGT...
c_cpx = ltfat.dgt(f_cpx, g, a, M)

#convert the tuple into a numpy array and
#calculate the absolute value of the coeffs
#c_cpx = c_cpx.asarray()
s_cpx = np.abs(c_cpx)

datasize = np.shape(s_cpx)

rows = datasize[0]
cols = datasize[1]

#...plot the absolute value of the coefficients...

plt.figure(2)
plt.imshow(s_cpx, aspect=(cols/rows), origin='lower')
plt.show()

#...and invert them.
f_hat = ltfat.idgt(c_cpx, g, a)

print(LA.norm(f_cpx-f_hat, 2))

#we can also do this for real signals...
c_real = ltfat.dgtreal(f_real, g, a, M)
f_hat_real = ltfat.idgtreal(c_real, g, a, M)

print(LA.norm(f_real-f_hat_real, 2))

#...in 2D...
f_2D = np.random.rand(100, 100)
win = np.ones(M) #this yields a 1D-array in numpy

c_2D = ltfat.dgt2(f_2D, win, a, M)
f_2D = ltfat.idgt2(c_2D, win, a)

#...and we can invert the absolute values of the coefficients.
#these calculations take a while...
#f_iter_cpx = ltfat.isgram(s_cpx, g, a)
#f_iter_real = ltfat.isgramreal(np.abs(c_real), g, a, M)

#print(LA.norm(f_real-f_iter_real, 2))
#print(LA.norm(f_cpx-f_iter_cpx, 2))

#we can not yet generate a sparse Gabor-style representation...
#(because I have not yet found a way to neatly parse the dictionaries)

#dicts = {{'hann',128,512},
#    {'hann',128,512,'tria',64,256},
#    {'hann',128,512,'tria',64,256,'tria',256,1024}
#    }
#errdb = -40
#maxit = 100
#c_sparse  = multidgtrealmp(self, f, dicts, errdb, maxit, nout = 3)

#...but in the absence of iterative methods, it may be difficult to invert.


#ltfat.projkern() has some problems on the Octave-side of things...


#there are several possibilities for designing windows...
L = ltfat.dgtlength(len(f_cpx), a, M)

orig_win = ltfat.gabwin(g, a, M, L)


plt.figure(3)
plt.plot(orig_win)
plt.yscale('linear')
plt.xlabel('Time [samples]')
plt.ylabel('Amplitude [samples]')
plt.title('The original Gauss window')
plt.grid(True)
plt.show()

dual_win = ltfat.gabdual(g, a, M)
tight_win = ltfat.gabtight(g, a, M)


#these calculations take very long...uncomment with care
#Lws = L - round(0.2*L)
#g1 = 'gauss'
#g2 = 'hann'

#dual_win_spec = ltfat.gabfirdual(Lws, orig_win, a, M)
#tight_win_spec = ltfat.gabfirtight(Lws, orig_win, a, M)
#dual_win_proj = ltfat.gabprojdual(g1, g2, a, M)
#dual_win_mix = ltfat.gabmixdual(g1, g2, a, M, L)

#we can check if the window is indeed a dual window
out_1 = ltfat.gabdualnorm(orig_win, dual_win, a, M)
out_2 = ltfat.gabdualnorm(orig_win, tight_win, a, M)

#print dual norms
print(out_1)
print(out_2)


#we can of course calculate the framebounds and rieszbounds...
[A, B] = ltfat.gabframebounds(g, a, M)
[A, B] = ltfat.gabrieszbounds(g, a, M)

#...and, we can extract the diagonal of the Gabor frame operator...
diag = ltfat.gabframediag(g, a, M, L)


#calculations based on the phase of the Gabor transform...

