#first, you import an ltfat object that manages an Octave session in the background.
from ltfatpy import ltfat
import numpy as np


L = 100
f = np.random.randn(L, 1)

g = 'gauss'
a = 10
M = 20

#optional arguments should be supported, but have not been exhaustively tested
c = ltfat.dgt(f, g, a, M, 'lt', [0, 1], 'freqinv')
#now, you can do LTFAT stuff here
#once you are finished, you can type
ltfat.exit()
#so the Octave session will be closed.

#If you then want to continue, you need to restart the session.
ltfat.restart()

try:
    e = ltfat.dgt(f, g, a, M)
except:
    print("this does not work, as the octave session is closed now")
    print("we need to restart Octave")
    ltfat.restart()
    e = ltfat.dgt(f, g, a, M)


#You can query if the session is still running via:
if ltfat._engine:
    print("session is still running")
else:
    print("you need to restart Octave")



#however, it might be more comfortable to use LTFAT as a context manager.a
#this way, all related resources will be freed automatically
with ltfat:
    d = ltfat.dgt(f, g, a, M)


try:
    e = ltfat.dgt(f, g, a, M)
except:
    print("this does not work, as the octave session is closed now")
    print("we need to restart Octave")
    ltfat.restart()
    e = ltfat.dgt(f, g, a, M)


#special functionality: retrieve the synthesis matrix by passing an empty numpy array as an input
f_none = np.empty((L, 1))
g = ltfat.dgt(f_none, g, a, M)

#print(g)
#fs = 22050
#fmin = 100
#fmax = 4000
#bins = 4

#fb_1 = ltfat.cqtfilterbank(f, fs, fmin, fmax, bins, L)
#fb_2 = ltfat.audfilterbank(f, fs, L)
#fb_3 = ltfat.waveletfilterbank(f, L, fs, fmin, fmax, bins)
#print(fb_2)