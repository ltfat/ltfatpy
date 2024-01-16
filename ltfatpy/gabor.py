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

#Basic Time/Frequency analysis
#   not implemented, to comply with future restructuring

#Gabor systems
@register_method
def dgt(self, f, g, a, M, *args, nout = 1):

    if f.size == 0:
        #L = self.dgtlength(len(f), a, M)
        return self.feval('_dgt_synthesismatrix', g, a, M, *args, nout = nout)

    c = self.feval('dgt', f, g, a, M, *args, nout=nout)
    return c

@register_method
def idgt(self, c, g, a, *args, nout = 1):
    argg = inspect.getfullargspec(idgt)
    inargs = argg[0]
    f = self.feval('idgt',c, g, a, *args, nout=nout)
    return f

@register_method
def isgram(self, s, g, a, *args, nout = 3):
    argg = inspect.getfullargspec(isgram)
    inargs = argg[0]
    [f, relres, iter] = self.feval('isgram', s, g, a, *args, nout=nout)
    return f

@register_method
def isgramreal(self, s, g, a, M, *args, nout = 3):
    argg = inspect.getfullargspec(isgramreal)
    inargs = argg[0]
    [f, relres, iter] = self.feval('isgramreal', s, g, a, M,*args, nout=nout)
    return f

@register_method
def dgt2(self, f, g, a, M, *args, nout = 1):
    #not implemented: overload with several window functions
    argg = inspect.getfullargspec(dgt2)
    inargs = argg[0]
    c = self.feval('dgt2', f, g, a, M, *args, nout=nout)
    return c

@register_method
def idgt2(self, c, g, a, *args, nout = 1):
    #not implemented: overload with several window functions
    argg = inspect.getfullargspec(idgt2)
    inargs = argg[0]
    f = self.feval('idgt2', c, g, a, *args, nout=nout)
    return f

@register_method
def dgtreal(self, f, g, a, M, *args, nout = 1):
    argg = inspect.getfullargspec(dgtreal)
    inargs = argg[0]
    c = self.feval('dgtreal', f, g, a, M, *args, nout=nout)
    return c

@register_method
def idgtreal(self, c, g, a, M, *args, nout = 1):
    argg = inspect.getfullargspec(idgtreal)
    inargs = argg[0]
    f = self.feval('idgtreal', c, g, a, M, *args, nout=nout)
    return f

@register_method
def gabwin(self, g, a, M, L, *args, nout = 2):
    argg = inspect.getfullargspec(gabwin)
    inargs = argg[0]
    [g, info] = self.feval('gabwin', g, a, M, L, *args, nout=nout)
    return g

#@register_method
#def projkern(self, cin, g, a, nout = 1):
    #not implemented: overload with second window
#    cout = self.feval('projkern', cin, g, a, nout)

@register_method
def dgtlength(self, Ls, a, M, *args, nout = 1):
    argg = inspect.getfullargspec(dgtlength)
    inargs = argg[0]
    L = self.feval('dgtlength', Ls, a, M, *args, nout=nout)
    return L

#Multi-Gabor systems
@register_method
def multidgtrealmp(self, f, dicts, errdb, maxit, *args, nout = 3):
    argg = inspect.getfullargspec(multidgtrealmp)
    inargs = argg[0]
    c = self.feval('multidgtrealmp', f,dicts,errdb,maxit, *args, nout=nout)
    return c

#Wilson bases and WMDCT
#   not implemented, to comply with future restructuring

#Reconstructing windows
@register_method
def gabdual(self, g, a, M, *args, nout = 1):
    argg = inspect.getfullargspec(gabdual)
    inargs = argg[0]
    gd = self.feval('gabdual', g, a, M, *args, nout=nout)
    return gd

@register_method
def gabtight(self, g, a, M, *args, nout = 1):
    argg = inspect.getfullargspec(gabtight)
    inargs = argg[0]
    gt = self.feval('gabtight', g, a, M, *args, nout=nout)
    return gt

@register_method
def gabfirdual(self, Ldual, g, a, M, *args, nout = 1):
    argg = inspect.getfullargspec(gabfirdual)
    inargs = argg[0]
    gd = self.feval('gabfirdual', Ldual, g, a, M, *args, nout=nout)
    return gd

@register_method
def gabfirtight(self, Ldual, g, a, M, *args, nout = 1):
    argg = inspect.getfullargspec(gabfirtight)
    inargs = argg[0]
    gt = self.feval('gabfirtight', Ldual, g, a, M, *args, nout=nout)
    return gt

@register_method
def gabprojdual(self, g1, g2, a, M, *args, nout = 1):
    argg = inspect.getfullargspec(gabprojdual)
    inargs = argg[0]
    gamma = self.feval('gabprojdual', g1, g2, a, M, *args, nout=nout)
    return gamma

@register_method
def gabmixdual(self, gm, g, a, M, L, *args, nout = 1):
    argg = inspect.getfullargspec(gabmixdual)
    inargs = argg[0]
    gd = self.feval('gabmixdual', gm, g, a, M, L, *args, nout=nout)
    return gd


#Condition numbers
@register_method
def gabframebounds(self, g, a, M, *args, nout=2):
    argg = inspect.getfullargspec(gabframebounds)
    inargs = argg[0]
    [A, B] = self.feval('gabframebounds', g, a, M, *args, nout=nout)
    return A, B

@register_method
def gabrieszbounds(self, g, a, M, *args, nout=2):
    argg = inspect.getfullargspec(gabrieszbounds)
    inargs = argg[0]
    [A, B] = self.feval('gabrieszbounds', g, a, M, *args, nout=nout)
    return A, B

@register_method
def gabdualnorm(self, g, gamma, a, M, *args, nout = 1):
    argg = inspect.getfullargspec(gabdualnorm)
    inargs = argg[0]
    dn = self.feval('gabdualnorm', g, gamma, a, M, *args, nout=nout)
    return dn

@register_method
def gabframediag(self, g, a, M, L, *args, nout = 1):
    argg = inspect.getfullargspec(gabframediag)
    inargs = argg[0]
    d = self.feval('gabframediag', g, a, M, L, *args, nout=nout)
    return d


#Phase gradient methods and reassignment
@register_method
def gabphasegrad(self, method, f, g, a, M, *args, nout = 3):
    argg = inspect.getfullargspec(gabphasegrad)
    inargs = argg[0]
    [tgrad,fgrad,c] = self.feval('gabphasegrad', method, f, g, a, M, *args, nout=nout)
    return tgrad, fgrad

@register_method
def gabphasederiv(self, dflag, method, f, g, a, M, *args, nout = 2):
    argg = inspect.getfullargspec(gabphasederiv)
    inargs = argg[0]
    [phased, c] = self.feval('gabphasederiv', dflag, method, f, g, a, M, *args, nout=nout)
    return phased

@register_method
def gabphasederivreal(self, dflag, method, f, g, a, M, *args, nout = 2):
    argg = inspect.getfullargspec(gabphasederivreal)
    inargs = argg[0]
    [phased, c] = self.feval('gabphasederivreal', dflag, method, f, g, a, M, *args, nout=nout)
    return phased

@register_method
def gabreassign(self, s, tgrad, fgrad, a, *args, nout = 1):
    argg = inspect.getfullargspec(gabreassign)
    inargs = argg[0]
    sr = self.feval('gabreassign', s, tgrad, fgrad, a, *args, nout=nout)
    return sr

@register_method
def gabreassignreal(self, s, tgrad, fgrad, a, M, *args, nout = 1):
    argg = inspect.getfullargspec(gabreassignreal)
    inargs = argg[0]
    sr = self.feval('gabreassignreal', s, tgrad, fgrad, a, M, *args, nout=nout)
    return sr

@register_method
def gabreassignadjust(self, s, pderivs, a, mu, *args, nout = 1):
    argg = inspect.getfullargspec(gabreassignadjust)
    inargs = argg[0]
    sr = self.feval('gabreassignadjust', s, pderivs, a, mu, *args, nout=nout)
    return sr


#Phase reconstruction
@register_method
def constructphase(self, s, g, a, *args, nout = 1):
    argg = inspect.getfullargspec(constructphase)
    inargs = argg[0]
    c = self.feval('constructphase', s, g, a, *args, nout=nout)
    return c

@register_method
def constructphasereal(self, s, g, a, M, *args, nout = 1):
    argg = inspect.getfullargspec(constructphasereal)
    inargs = argg[0]
    c = self.feval('constructphasereal', s, g, a, M, *args, nout=nout)
    return c


#Phase conversions
@register_method
def phaselock(self, c, a, *args, nout = 1):
    argg = inspect.getfullargspec(phaselock)
    inargs = argg[0]
    c = self.feval('phaselock', c, a, *args, nout=nout)
    return c

@register_method
def phaseunlock(self, c, a, *args, nout = 1):
    argg = inspect.getfullargspec(phaseunlock)
    inargs = argg[0]
    c = self.feval('phaseunlock', c, a, *args, nout=nout)
    return c

@register_method
def phaselockreal(self, c, a, M, *args, nout = 1):
    argg = inspect.getfullargspec(phaselockreal)
    inargs = argg[0]
    c = self.feval('phaselockreal', c, a, M, *args, nout=nout)
    return c

@register_method
def phaseunlockreal(self, c, a, M, *args, nout = 1):
    argg = inspect.getfullargspec(phaseunlockreal)
    inargs = argg[0]
    c = self.feval('phaseunlockreal', c, a, M, *args, nout=nout)
    return c

@register_method
def symphase(self, c, a, *args, nout = 1):
    argg = inspect.getfullargspec(symphase)
    inargs = argg[0]
    c = self.feval('symphase', c, a, *args, nout=nout)
    return c


#Support for non-separable lattices
@register_method
def matrix2latticetype(self, L, V, *args, nout = 3):
    argg = inspect.getfullargspec(matrix2latticetype)
    inargs = argg[0]
    [a,M,lt] = self.feval('matrix2latticetype', L, V, *args, nout=nout)
    return a, M, lt

@register_method
def latticetype2matrix(self, L, a, M, lt, *args, nout = 1):
    argg = inspect.getfullargspec(latticetype2matrix)
    inargs = argg[0]
    V = self.feval('latticetype2matrix', L, a, M, lt, *args, nout=nout)
    return V

@register_method
def shearfind(self, L, a, M, lt, *args, nout = 3):
    argg = inspect.getfullargspec(shearfind)
    inargs = argg[0]
    [s0,s1,br] = self.feval('shearfind', L,a,M,lt, *args, nout=nout)
    return s0, s1, br

@register_method
def noshearlength(self, Ls, a, M, lt, *args, nout = 1):
    argg = inspect.getfullargspec(noshearlength)
    inargs = argg[0]
    L = self.feval('noshearlength', Ls,a,M,lt, *args, nout=nout)
    return L


#Plots
    #not yet implemented

