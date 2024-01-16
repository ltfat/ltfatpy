The repository is under development. Hence, everything written here is temporary.
If you encounter any errors, please write an issue.

Current requirements:
------------------------

Python (3.10 or 3.11 is recommended), with packages
- numpy
- scipy
- oct2py

Octave
- GNU Octave installed (version 8.4.0 is recommended)
- for Debian/Ubuntu and MacOS only: mkoctfile (do: $apt install liboctave-dev)


How to use:
------------------------

The top folder of the ltfatpy package must be available in your (Python) pathe.g., do

```
import sys 
sys.path.append("/home/clara/Documents/ltfat_development_code/ltfatpy")
```

at the top of your Python code. From there, import ltfat as below:

```
from ltfatpy import ltfat
```
This instantiates the ltfat object with Octave running in the background. 
From now on, you can again change your working directory freely.

LTFATPY has been written such that its syntax nearly equals that of LTFAT in Octave.
So you can use it as
```
[outArg1, ..., outArgn] = ltfat.functionname(...)
```
and use the documentation the same way as you would when working with Octave. 
You find the documentation [here](ltfat.org/doc/).

Things to keep in mind:
------------------------
1. Keep in mind that in Python, ltfat is an object, not a filename.
Without this object, there is no Octave, and without Octave, there is no LTFAT functionality.
It is therefore not advisable to get rid of the ltfat object, or to otherwise manipulate it
without further consideration.

2. Instead of cell arrays, use sets.
Example: Octave code
```
gt = gabwin({'tight', 'gauss'}, 10, 20, 100);
```
Python code
```
gt = ltfat.gabwin(('tight', 'gauss'), 10, 20, 100)
```
3. Always use all available output arguments.
Example:
```
[g, a] = ltfat.cqtfilters(fs,fmin,fmax,bins,L)
```
will not work. To find out how many function arguments are needed,
check the Python file that corresponds to the module you are working with (here: filterbank.py).
```
[g, a, fc, L] = ltfat.cqtfilters(fs,fmin,fmax,bins,L)
```
works.

4. Function handles (e.g. many filter functions 'g') are parsed by LTFATPY, and interpreted
by Python as OctaveVariablePointers, but they can not be numerically evaluated. If you try
to do so, you get an error.
