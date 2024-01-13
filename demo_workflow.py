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
f_none = np.array([])
g = ltfat.dgt(f_none, g, a, M)

#difference between the LTFAT syntax in Octave and Python: cells

#example:
#calculate tight gabor window in Octave:
# gd=gabwin({'tight','gauss'},a,M,L)

#calculate tight gabor window in Python:
gd = ltfat.gabwin(('tight', 'gauss'), 10, 20, 100)

#please note that there are many different ways cell arrays are
#used in LTFAT. Therefore, for the alpha version, it is entirely
#possible that not every combination of input parameters works.
#if you notice some error, please file a bug request on github:
#github.com/ltfat/ltfatpy