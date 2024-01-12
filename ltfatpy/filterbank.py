import inspect 
import collections 
import weakref
from oct2py.dynamic import OctaveVariablePtr

#Function adapted from https://www.qtrac.eu/pyclassmulti.html .
def register_method(methods):
    def register_method(method):
        methods.append(method)
        return method # Unchanged
    return register_method

__methods__ = []
register_method = register_method(__methods__)

#Some special filterbanks, as they might be useful for ML tasks
@register_method
def cqtfilterbank(self, f, fs, fmin, fmax, bins, Ls, nout = 1):
    argg = inspect.getfullargspec(cqtfilterbank)
    inargs = argg[0]

    #if not f.any():
    #    return self.feval(inargs, '_dgt_synthesismatrix', g, a, M, nout)
    buf1 = "[g, a] = cqtfilters( %d , %d, %d, %d, %d);" % (fs, fmin, fmax, bins, Ls)
    buf2 = "filterbank(f, g, a);"
    buf3 = buf1 + ' ' + buf2 
    c = self.eval(buf3)
    #c = self.feval(inargs, 'cqtfilters', fs, fmin, fmax, bins, Ls, nout)
    return c

@register_method
def audfilterbank(self, f, fs, Ls, nout = 1):
    argg = inspect.getfullargspec(audfilterbank)
    inargs = argg[0]
    #inargs = []
    #if not f.any():
    #    return self.feval(inargs, '_dgt_synthesismatrix', g, a, M, nout)

    self.push('f', f)
    self.push('fs', fs)
    self.push('Ls', Ls)


    buf = "[g, a] = audfilters( %d , %d); c=filterbank( %s, g, a);" % (fs, Ls, str(f))

    c = self.eval(buf)
    c = self.pull('c')
    return c

@register_method
def waveletfilterbank(self, f, Ls, fs, fmin, fmax, bins, nout = 1):
    argg = inspect.getfullargspec(waveletfilterbank)
    inargs = argg[0]

    #if not f.any():
    #    return self.feval(inargs, '_dgt_synthesismatrix', g, a, M, nout)

    buf1 = "[g, a] = waveletfilters( %d , 'bins', %d, %d, %d, %d);" % (Ls, fs, fmin, fmax, bins)
    buf2 = "c=filterbank(f, g, a);"
    buf3 = buf1 + ' ' + buf2 
    self.eval(inargs, buf1)
    inargs = []
    c = self.feval(inargs, 'filterbank', f, g, a, nout)

    return c

#...and their inversion
@register_method
def ifilterbank(self, c, g, a, nout = 1):
    argg = inspect.getfullargspec(ifilterbank)
    inargs = argg[0]

    f = self.feval(inargs, 'ifilterbank', c, g, a, nout)
    return f