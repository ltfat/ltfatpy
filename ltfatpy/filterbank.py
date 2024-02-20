import inspect 
import collections 

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

    if not f.any():
        return self.feval('_fb_synthesismatrix', g, a, *args, nout = nout)

    c = self.feval('filterbank', f, g, a, *args, nout=nout)
    return c

@register_method
def ufilterbank(self, f,g,a, *args, nout = 1):

    if not f.any():
        return self.feval('_fb_synthesismatrix', g, a, M, *args, nout = nout)

    c = self.feval('ufilterbank', f, g, a, *args, nout=nout)
    return c

@register_method
def ifilterbank(self, c, g, a, *args, nout = 1):

    f = self.feval('ifilterbank', c, g, a, *args, nout=nout)

    return f

@register_method
def ifilterbankiter(self, c, g, a, *args, nout = 1):

    f = self.feval('ifilterbankiter', c, g, a, *args, nout=nout)

    return f

@register_method
def filterbankwin(self, g, a, L, *args, nout = 1):

    g = self.feval('filterbankwin', g, a, L, *args, nout=nout)

    return g

@register_method
def filterbanklength(self, Ls, a, *args, nout = 1):

    L = self.feval('filterbanklength', Ls, a, *args, nout=nout)

    return L

@register_method
def filterbanklengthcoef(self, coef, a, *args, nout = 1):

    L = self.feval('filterbanklengthcoef', coef, a, *args, nout=nout)

    return L

#Filter generators
@register_method
def cqtfilters(self, fs,fmin,fmax,bins,Ls,*args, nout = 4):

    self.feval('cqtfilters', fs,fmin,fmax,bins,Ls, *args, store_as="result_strct", nout=nout)

    g = self.get_pointer('result_strct.par')
    a = self.pull('result_strct.par1')
    fc = self.pull('result_strct.par2')
    L = self.pull('result_strct.par3')

    return g, a, fc, L 


@register_method
def erbfilters(self, fs,Ls,*args, nout = 4):

    self.feval('erbfilters', fs,Ls, *args, store_as="result_strct", nout=nout)

    g = self.get_pointer('result_strct.par')
    a = self.pull('result_strct.par1')
    fc = self.pull('result_strct.par2')
    L = self.pull('result_strct.par3')

    return g, a, fc, L 

@register_method
def warpedfilters(self, freqtoscale,scaletofreq,fs,fmin,fmax,bins,Ls,*args, nout = 4):

    self.feval('warpedfilters', freqtoscale,scaletofreq,fs,fmin,fmax,bins,Ls, *args, store_as="result_strct", nout=nout)

    g = self.get_pointer('result_strct.par')
    a = self.pull('result_strct.par1')
    fc = self.pull('result_strct.par2')
    L = self.pull('result_strct.par3')

    return g, a, fc, L 

@register_method
def audfilters(self, fs,Ls,*args, nout = 4):

    self.feval('audfilters', fs,Ls, *args, store_as="result_strct", nout=nout)

    g = self.get_pointer('result_strct.par')
    a = self.pull('result_strct.par1')
    fc = self.pull('result_strct.par2')
    L = self.pull('result_strct.par3')

    return g, a, fc, L 

@register_method
def gabfilters(self, Ls, g, a, M, *args, nout = 4):

    self.feval('gabfilters', Ls, g, a, M, *args, store_as="result_strct", nout=nout)

    g = self.get_pointer('result_strct.par')
    a = self.pull('result_strct.par1')
    fc = self.pull('result_strct.par2')
    L = self.pull('result_strct.par3')

    return g, a, fc, L 

@register_method
def waveletfilters(self, Ls,scales,*args, nout = 4):

    self.feval('waveletfilters', Ls,scales, *args, store_as="result_strct", nout=nout)

    g = self.get_pointer('result_strct.par')
    a = self.pull('result_strct.par1')
    fc = self.pull('result_strct.par2')
    L = self.pull('result_strct.par3')

    return g, a, fc, L 

#Window construction and bounds
@register_method
def filterbankdual(self, g,a,*args, nout = 1):

    gd = self.feval('filterbankdual', g, a, *args, nout=nout)

    return gd 

@register_method
def filterbanktight(self, g,a,*args, nout = 1):

    gt = self.feval('filterbanktight', g, a, *args, nout=nout)

    return gt

@register_method
def filterbankrealdual(self, g,a,*args, nout = 1):

    gd = self.feval('filterbankrealdual', g, a, *args, nout=nout)

    return gd 

@register_method
def filterbankrealtight(self, g,a,*args, nout = 1):

    gt = self.feval('filterbankrealtight', g, a, *args, nout=nout)

    return gt 

@register_method
def filterbankbounds(self, g,a,*args, nout = 2):

    [A, B] = self.feval('filterbankbounds', g, a, *args, nout=nout)

    return A, B

@register_method
def filterbankrealbounds(self, g,a,*args, nout = 2):

    [A, B] = self.feval('filterbankbounds', g, a, *args, nout=nout)

    return A, B 

@register_method
def filterbankresponse(self, g,a, L, *args, nout = 1):

    gf = self.feval('filterbankresponse', g, a, L, *args, nout=nout)

    return gf

#Auxiliary
@register_method
def filterbankfreqz(self, g,a, L, *args, nout = 1):

    gf = self.feval('filterbankfreqz', g, a, L, *args, nout=nout)

    return gf

@register_method
def filterbankscale(self, g, scal, *args, nout = 1):

    g = self.feval('filterbankscale', g, scal, *args, nout=nout)

    return g

@register_method
def nonu2ufilterbank(self, g,a, *args, nout = 1):

    gf = self.feval('nonu2ufilterbank', g, a, *args, nout=nout)

    return gf

@register_method
def u2nonucfmt(self, cu,pk, *args, nout = 1):

    c = self.feval('u2nonucfmt', cu, pk, *args, nout=nout)

    return c

@register_method
def nonu2ucfmt(self, cu,pk, *args, nout = 1):

    cu = self.feval('nonu2ucfmt', cu, pk, *args, nout=nout)

    return cu

#Reassignment and phase gradient
@register_method
def filterbankphasegrad(self, f,g,a, *args, nout = 4):

    [tgrad,fgrad,s,c] = self.feval('filterbankphasegrad', f, g, a, *args, nout=nout)
    return tgrad,fgrad,s,c

@register_method
def filterbankreassign(self, s,tgrad,fgrad, a, g, *args, nout = 3):

    [sr,repos,Lc] = self.feval('filterbankreassign', s,tgrad,fgrad, a, g, *args, nout=nout)
    return sr,repos,Lc

@register_method
def filterbankreassign(self, c,tgrad,fgrad, *args, nout = 3):

    [sr,repos,Lc] = self.feval('filterbankreassign', c,tgrad,fgrad, *args, nout=nout)
    return sr,repos,Lc

#Phase reconstruction
@register_method
def filterbankconstphase(self, s, a, fc, tfr, *args, nout = 5):

    [c,newphase,usedmask,tgrad,fgrad] = self.feval('filterbankconstphase', s, a, fc, tfr,  *args, nout=nout)
    return c,newphase,usedmask,tgrad,fgrad

#-------------------------------------------------------------------------
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