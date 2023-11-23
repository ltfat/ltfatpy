Current requirements:

Python packages
------------------------
- numpy
- scipy
- oct2py

Octave
------------------------
- GNU Octave installed
- for Debian/Ubuntu and MacOS only: mkoctfile (do: $apt install liboctave-dev)


HOW TO USE:
Please note that this section may undergo heavy changes during the course of
development. There is no guarantee that it is up to date. If you encounter
any errors, please write an issue (those issues are not even public for the
time being).

Currently, there are 3 supported options:
Preliminary for all 3: the top folder of the ltfatpy package must be available in your (Python) path
e.g., do

import sys 
sys.path.append("/home/clara/Documents/ltfat_development_code/ltfatpy")

at the top of your Python code

1) FULL ACCESS TO LTFAT:
This includes every function, including plotting functionality, and the ability
to return all output arguments supported by that function. However,
it demands quite some expertise from the user (including the willingness
to look into the Python source code), to handle everything properly.

Basic syntax:

from ltfatpy import ltfat

[outArg1, ..., outArgn] = ltfat.feval('functionName', inArg1, ..., inArgn, nout=numberOutArgs)

2) FULL ACCESS TO LTFAT BUT ONLY TO THE FIRST OUTPUT ARGUMENT PER FUNCTION
This mode is simpler to use than 1), but you can only access the first output argument of each
function directly when using it.

Basic syntax:

from ltfatpy import ltfat

outArg = ltfat.functionname(inArg1, ..., inArgn)

3) CLASS ACCESS
This is intended as the user-friendly native Python mode.
In this mode, you are able to access the important functionality of LTFAT, but there may be
gaps (either, because whatever you want to do is too "special purpose", or because I simply
have not yet implemented it - ask in any case).

Basic syntax (specific example):

import numpy as np
from ltfatpy import Gabor

L = 144
a = 12
M = 24
g = np.random.rand(L,1)
f = np.random.rand(L,1)

#instantiate a Gabor object
gabor = Gabor(a, M, g)

#the transform will be calculated based on the constructor parameters
c = gabor.transform(f)

#calculate the dual window (note that the syntax is very different to Matlab)
gd=gabor.window("dual")
gabor.setdualwindow(gd)

f = gabor.inverse(c)

