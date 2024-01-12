from ltfatpy import ltfat
import numpy as np


L = 100
f = np.random.randn(L, 1)

fs = 22050
fmin = 100
fmax = 4000
bins = 4

#fb_1 = ltfat.cqtfilterbank(f, fs, fmin, fmax, bins, L)
fb_2 = ltfat.audfilterbank(f, fs, L)
#fb_3 = ltfat.waveletfilterbank(f, L, fs, fmin, fmax, bins)
print(fb_2)