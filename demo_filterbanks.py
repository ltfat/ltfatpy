from ltfatpy import ltfat
import numpy as np


L = 1000
f = np.random.randn(L, 1)

fs = 22050
fmin = 100
fmax = 4000
bins = 4

#there are three types of filterbank available. optional input arguments
#are not yet supported yet for them.
#for the time being, you can add the arguments you need manually in filterbank.py
#if you found implemented a permanent solution, please consider pushing them to our
#github repository: github.com/ltfat/ltfatpy
[fb_1,g_1,a_1] = ltfat.cqtfilterbank(f, fs, fmin, fmax, bins, L)
frec = ltfat.ifilterbank(fb_1, g_1, a_1)

[fb_2,g_2,a_2] = ltfat.audfilterbank(f, fs, L)
frec = ltfat.ifilterbank(fb_2, g_2, a_2)

[fb_3,g_3,a_3] = ltfat.waveletfilterbank(f, L, fs, fmin, fmax, bins)
frec = ltfat.ifilterbank(fb_3, g_3, a_3)


f_none = np.array([])
fb_1_op = ltfat.cqtfilterbank(f_none, fs, fmin, fmax, bins, L)
fb_2_op = ltfat.audfilterbank(f_none, fs, L)
fb_3_op = ltfat.waveletfilterbank(f_none, L, fs, fmin, fmax, bins)

print(fb_1_op)