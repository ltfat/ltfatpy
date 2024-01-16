from ltfatpy import ltfat
import numpy as np
import matplotlib.pyplot as plt

Ls = 5880
f = np.random.randn(Ls, 1)

fs = 22050
fmin = 100
fmax = fs
bins = 8

[g, a, fc, L] = ltfat.cqtfilters(fs,fmin,fmax,bins,Ls, 'fractional')
#be careful: 'g' is passed as a pointer because it comprises Octave data types
# that do not have a correspondence in Python. you can not
#directly evaluate it in Python.

#L = ltfat.filterbanklength(L, a) #not needed here
c = ltfat.filterbank(f, g, a, Ls)

gd = ltfat.filterbankrealdual(g, a, L)

#for this example, the framebounds are too unstable
[A, B] = ltfat.filterbankrealbounds(g, a, L)
print(B)
print(A)

frec = ltfat.ifilterbank(c, gd, a, 'real')

f_none = np.array([])
c_op = ltfat.filterbank(f_none, g, a, L)

#plot the synthesis matrix
mat = np.reshape(np.abs(c_op),np.shape(c_op))
plt.imshow(mat, origin='lower')
plt.show()

#plot the input and output signal
plt.figure(figsize=(5, 2.7), layout='constrained')
plt.plot(f, label='input')  # Plot some data on the (implicit) axes.
plt.plot(frec, label='reconstruction')  # etc.
plt.plot(f-frec, label='difference')
plt.xlabel('Time [samples]')
plt.ylabel('Amplitude [samples]')
plt.title("Input and Output signal")
plt.legend()
plt.show()