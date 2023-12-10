import sys
sys.path.append("/home/clara/Documents/ltfat_development_code/ltfatpy")
sys.path.append("/home/clara/Documents/ltfat_development_code/oct2py/")
sys.path.append("/home/clara/Documents/ltfat_development_code/")
sys.path.append("/home/clara/Documents/ltfat_development_code/metakernel")
sys.path.append("/home/clara/Documents/ltfat_development_code/octave_kernel")
import numpy as np
from ltfatpy import Gabor
import unittest

gabor = Gabor(10, 20)

#testsignal 1: generated in Octave
#f = gabor.randn(100,1)
f2 = np.random.rand(100,1)
f=f2
gabor.push('f', f)
a = 10
M = 20
L = 100
#s = frozenset({'dual',frozenset({'hann',20})})
#gtest=gabor.gabwin(s,a,M,L)
gtest=gabor.gabwin("{'dual',{'hann',20}}",a,M,L)
print(gtest)

#calculate transform in Python
#original: [c,Ls]=dgt(f,g,a,M);
cp = gabor.transform(f)
gabor.push('cp', cp)
gabor.eval("co = dgt(f, 'gauss', 10, 20);")
gabor.eval("isequal(cp, co);")

#inverse transform: f=idgt(c,g,a);
fp = gabor.inverse(cp)
gabor.push('fp', fp)
gabor.eval("gd = gabdual('gauss',10,20);")
gabor.eval("fo = idgt(co, gd, 10);")
gabor.eval("isequal(fp, fo);")

#now, compare directly in Python
co = gabor.pull('co')
assert((cp == co).all())

fo = gabor.pull('fo')
#assert((fp == fo).all())
#assertAlmostEqual(fp, fo)
s = sum(fp -fo)
print(s)

s = sum(fo -f)
print(s)
#assert((fp == f).all())
#assertAlmostEqual(fp, f)
s = sum(fp -f)
print(s)

#es geht (bei double) keine Praezision verloren.
#es gibt sicher noch Optimierungspotential, indem man bspw. manche Funktionen direkter aufruft => spaeter
#weiteres Optimierungspotential gaebe es, wenn man immer den feval() syntax verwenden wuerde. aber das
#ist schlecht fuer die lesbarkeit des codes und bringt nicht sooo viel (es spart nur ein paar python calls),
#darum will ich das nicht.
#immer noch: custom error message
#mit der funktionsbenennung muss ich auch aufpassen. es sollte keine duplikate geben. nicht mit existierenden
#octave funktionen, und auch nicht zwischen den modulen (bsp. framebounds => fixed)
#minimaler performancegewinn, aber auch eine image-frage: ist real oder complex der default?
