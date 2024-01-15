from ltfatpy import ltfat
import numpy as np
import matplotlib.pyplot as plt

#from oct2py.dynamic import OctaveVariablePtr

L = 1000
f = np.random.randn(L, 1)

fs = 22050
fmin = 100
fmax = 4000
bins = 4

[g, a, fc, L] = ltfat.cqtfilters(fs,fmin,fmax,bins,L)
#be careful: 'g' is passed as a pointer because it comprises Octave data types
# that do not have a correspondence in Python. you can not
#directly evaluate it in Python.

#L = ltfat.filterbanklength(L, a) #not needed
c = ltfat.filterbank(f, g, a)

frec = ltfat.ifilterbank(c, g, a)

f_none = np.array([])
c_op = ltfat.filterbank(f_none, g, a, L)

print(np.abs(c))
#plt.imshow(np.abs(c))
#print(isinstance(c,np.ndarray))
#fig, (ax1, ax2) = plt.subplots(2, 1)
#fig.suptitle('Constant-Q filterbank')
#ax1.plot(x, y)
#ax2.plot(x, y)
#plotting the array
#ax1.imshow(np.abs(c), cmap='binary')
#ax2.imshow(np.abs(c_op), cmap='binary')
#plt.colorbar()
#plt.show()
