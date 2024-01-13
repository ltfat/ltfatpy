import inspect 
import collections 
#import weakref
#from oct2py.dynamic import OctaveVariablePtr



#Function adapted from https://www.qtrac.eu/pyclassmulti.html .
def register_method(methods):
    def register_method(method):
        methods.append(method)
        return method # Unchanged
    return register_method

__methods__ = []
register_method = register_method(__methods__)


#TODO: add self.eval("clear(var1, var2)") to each function
# (there is no guarantee that the Octave workspace is empty)

#Transforms and basic routines
@register_method
def filterbank(self, f,g,a, *args, nout = 1):
    argg = inspect.getfullargspec(filterbank)
    inargs = argg[0]

    if not f.any():
        return self.feval('_filterbank_synthesismatrix', g, a, M, *args, nout = nout)

    c = self.feval('filterbank', f, g, a, *args, nout=nout)
    return c

def ufilterbank(self, f,g,a, *args, nout = 1):
    argg = inspect.getfullargspec(ufilterbank)
    inargs = argg[0]

    if not f.any():
        return self.feval('_filterbank_synthesismatrix', g, a, M, *args, nout = nout)

    c = self.feval('ufilterbank', f, g, a, *args, nout=nout)
    return c

@register_method
def ifilterbank(self, c, g, a, *args, nout = 1):
    argg = inspect.getfullargspec(ifilterbank)
    inargs = argg[0]

    f = self.feval('ifilterbank', c, g, a, *args, nout=nout)

    return f

@register_method
def ifilterbankiter(self, c, g, a, *args, nout = 1):
    argg = inspect.getfullargspec(ifilterbankiter)
    inargs = argg[0]

    f = self.feval('ifilterbankiter', c, g, a, *args, nout=nout)

    return f

@register_method
def filterbankwin(self, g, a, L, *args, nout = 1):
    argg = inspect.getfullargspec(filterbankwin)
    inargs = argg[0]

    g = self.feval('filterbankwin', g, a, L, *args, nout=nout)

    return g

@register_method
def filterbanklength(self, Ls, a, *args, nout = 1):
    argg = inspect.getfullargspec(filterbanklength)
    inargs = argg[0]

    L = self.feval('filterbanklength', Ls, a, *args, nout=nout)

    return L

@register_method
def filterbanklengthcoef(self, coef, a, *args, nout = 1):
    argg = inspect.getfullargspec(filterbanklengthcoef)
    inargs = argg[0]

    L = self.feval('filterbanklength', coef, a, *args, nout=nout)

    return L

#Some special filterbanks, as they might be useful for ML tasks
@register_method
def cqtfilterbank(self, f, fs, fmin, fmax, bins, Ls):
    argg = inspect.getfullargspec(cqtfilterbank)
    inargs = argg[0]

    #if not f.any():
    #    return self.feval(inargs, '_fb_synthesismatrix', g, a, M, nout)

    self.push('f', f)
    self.push('Ls', Ls)
    self.push('fs', fs)
    self.push('fmin', fmin)
    self.push('fmax', fmax)
    self.push('bins', bins)

    #buf = "[g, a] = cqtfilters( %d , %d, %d, %d, %d); c=filterbank( %s, g, a);" % (fs, fmin, fmax, bins, Ls, str(f))

    #c = self.eval(buf)
    #c = self.pull('c')

    #g = self.get_pointer('g')
    #a = self.get_pointer('a')

    if f.size == 0:
        buf = "[g, a] = cqtfilters( %d , %d, %d, %d, %d); L=filterbanklength(Ls, a); G=_fb_synthesismatrix( g, a, L);" % (fs, fmin, fmax, bins, Ls)
        G = self.eval(buf)
        return self.pull('G')
        #return self.feval('_fb_synthesismatrix', g, a, M, nout=nout)
    else:
        buf = "[g, a] = cqtfilters( %d , %d, %d, %d, %d); c=filterbank( %s, g, a);" % (fs, fmin, fmax, bins, Ls, str(f))

        c = self.eval(buf)
        c = self.pull('c')

        g = self.get_pointer('g')
        a = self.get_pointer('a')

        return c, g, a

@register_method
def audfilterbank(self, f, fs, Ls, *args):
    argg = inspect.getfullargspec(audfilterbank)
    inargs = argg[0]

    self.push('f', f)
    self.push('fs', fs)
    self.push('Ls', Ls)

    if f.size == 0:
        buf = "[g, a] = audfilters( %d , %d); L=filterbanklength(Ls, a); G=_fb_synthesismatrix( g, a, L);" % (fs, Ls)
        G = self.eval(buf)
        return self.pull('G')
    else:
        buf = "[g, a] = audfilters( %d , %d); c=filterbank( %s, g, a);" % (fs, Ls, str(f))

        c = self.eval(buf)
        c = self.pull('c')

        g = self.get_pointer('g')
        a = self.get_pointer('a')

        return c, g, a

@register_method
def waveletfilterbank(self, f, Ls, fs, fmin, fmax, bins, *args):
    argg = inspect.getfullargspec(waveletfilterbank)
    inargs = argg[0]

    self.push('f', f)
    self.push('Ls', Ls)
    self.push('fs', fs)
    self.push('fmin', fmin)
    self.push('fmax', fmax)
    self.push('bins', bins)

    if f.size == 0:
        buf = "[g, a] = waveletfilters( %d , 'bins', %d, %d, %d, %d); L=filterbanklength(Ls, a); G=_fb_synthesismatrix( g, a, L);" % (Ls, fs, fmin, fmax, bins)
        G = self.eval(buf)
        return self.pull('G')
    else:
        buf = "[g, a] = waveletfilters( %d , 'bins', %d, %d, %d, %d); c=filterbank( %s, g, a);" % (Ls, fs, fmin, fmax, bins, str(f))

        c = self.eval(buf)
        c = self.pull('c')

        g = self.get_pointer('g')
        a = self.get_pointer('a')

        return c, g, a

    #buf1 = "[g, a] = waveletfilters( %d , 'bins', %d, %d, %d, %d);" % (Ls, fs, fmin, fmax, bins)
    #buf2 = "c=filterbank(f, g, a);"
    #buf3 = buf1 + ' ' + buf2 
    #self.eval(inargs, buf1)
    #inargs = []
    #c = self.feval(inargs, 'filterbank', f, g, a, nout)