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
def dgt(self, f, g, a, M, nout = 1):
    argg = inspect.getfullargspec(dgt)
    inargs = argg[0]
    c = self.feval(inargs, 'dgt', f, g, a, M, nout)
    if nout == 1:
        return c
    else:
        return c, L

@register_method
def idgt(self, c, g, a, Ls = "", lt = [0, 1], nout = 1):
    f = self.feval('idgt',c, g, a, Ls, lt, nout)
    return f

@register_method
def isgram(self, s, g, a, Ls ="", nout = 1):
    [f, relres, iter] = self.feval('isgram', s, g, a, Ls, nout = 1)

@register_method
def isgramreal(self, s, g, a, M, Ls ="", nout = 1):
    [f, relres, iter] = self.feval('isgramreal', s, g, a, M, Ls, nout = 1)

@register_method
def dgt2(self, f, g, a, M, nout = 1):
    #not implemented: overload with several window functions
    [c, Ls] = self.feval('dgt2', f, g, a, M, nout = 1)

@register_method
def idgt2(self, c, g, a, nout = 1):
    #not implemented: overload with several window functions
    f = self.feval('idgt2', c, g, a, nout = 1)
    return f

@register_method
def dgtreal(self, f, g, a, M, L ="", nout = 1):
    [c, Ls] = self.feval('dgtreal', f, g, a, M, L, nout = 1)

@register_method
def idgtreal(self, c, g, a, M, Ls ="", nout = 1):
    [f, relres, iter] = self.feval('idgtreal', c, g, a, M, Ls, nout = 1)

@register_method
def gabwin(self, g, a, M, L ="", nout = 1):
    [g, info] = self.feval('gabwin', g, a, M, L, nout = 1)

@register_method
def projkern(self, cin, g, a, nout = 1):
    #not implemented: overload with second window
    cout = self.feval('projkern', cin, g, a, nout = 1)

@register_method
def dgtlength(self, Ls, a, M, lt = [0, 1], nout = 1):
    L = self.feval('dgtlength', Ls, a, M, lt, nout = 1)
    return L

#Multi-Gabor systems
@register_method
def multidgtrealmp(self, f, dicts, errdb, maxit, nout = 1):
    [c,frec,info] = self.feval('multidgtrealmp', f,dicts,errdb,maxit, nout = 3)

#Wilson bases and WMDCT
#   not implemented, to comply with future restructuring

#Reconstructing windows
@register_method
def gabdual(self, g, a, M, lt, nout = 1):
    gd = self.feval('gabdual', g, a, M,'lt',lt, nout)
    return gd

@register_method
def gabtight(self, g, a, M, lt, nout = 1):
    gt = self.feval('gabtight', g, a, M,'lt',lt, nout)
    return gt

@register_method
def gabfirdual(self, Ldual, g, a, M, nout = 1):
    gd = self.feval('gabfirdual', Ldual, g, a, M, nout)
    return gd

@register_method
def gabfirtight(self, Ldual, g, a, M, nout = 1):
    gt = self.feval('gabfirtight', Ldual, g, a, M, nout)
    return gt

@register_method
def gabprojdual(self, g1, g2, a, M, nout = 1):
    gamma = self.feval('gabprojdual', g1, g2, a, M, nout)
    return gamma

@register_method
def gabmixdual(self, gm, g, a, M, L, nout = 1):
    gd = self.feval('gabmixdual', gm, g, a, M, L, nout)
    return gd


#Conditions numbers
@register_method
def gabframebounds(self, g, a, M, nout=2):
    [A, B] = self.feval('gabframebounds', g, a, M, nout = 2)
    return A, B

@register_method
def gabrieszbounds(self, g, a, M, nout=2):
    [A, B] = self.feval('gabrieszbounds', g, a, M, nout = 2)
    return A, B

@register_method
def gabdualnorm(self, g, gamma, a, M, lt, nout = 1):
    dn = self.feval('gabdualnorm', g, gamma, a, M, lt, nout)
    return dn

@register_method
def gabframediag(self, g, a, M, L, lt, nout = 1):
    d = self.feval('gabframediag', g, a, M, L, lt, nout)
    return d


#Phase gradient methods and reassignment
@register_method
def gabphasegrad(self, method, f, g, a, M, nout = 2):
    [tgrad,fgrad,c] = self.feval('gabphasegrad', method, f, g, a, M, nout)

@register_method
def gabphasederiv(self, dflag, method, f, g, a, M, nout = 2):
    [phased, c] = self.feval('gabphasederiv', dflag, method, f, g, a, M, nout)

@register_method
def gabphasederivreal(self, dflag, method, f, g, a, M, nout = 2):
    [phased, c] = self.feval('gabphasederivreal', dflag, method, f, g, a, M, nout)

@register_method
def gabreassign(self, s, tgrad, fgrad, a, nout = 1):
    sr = self.feval('gabreassign', s, tgrad, fgrad, a, nout)
    return sr

@register_method
def gabreassignreal(self, s, tgrad, fgrad, a, M, nout = 1):
    sr = self.feval('gabreassignreal', s, tgrad, fgrad, a, M, nout)
    return sr

@register_method
def gabreassignadjust(self, s, pderivs, a, mu, nout = 1):
    sr = self.feval('gabreassignadjust', s, pderivs, a, mu, nout)
    return sr


#Phase reconstruction
@register_method
def constructphase(self, s, g, a, tol, mask, usephase, nout = 1):
    [c,newphase,usedmask,tgrad,fgrad] = self.feval('constructphase', s, g, a, tol, mask, usephase, nout)

@register_method
def constructphasereal(self, s, g, a, M, tol, mask, usephase, nout = 1):
    [c,newphase,usedmask,tgrad,fgrad] = self.feval('constructphasereal', s, g, a, M, tol, mask, usephase, nout)


#Phase conversions
@register_method
def phaselock(self, c, a, nout = 1):
    c = self.feval('phaselock', c, a, nout)
    return c

@register_method
def phaseunlock(self, c, a, nout = 1):
    c = self.feval('phaseunlock', c, a, nout)
    return c

@register_method
def phaselockreal(self, c, a, M, nout = 1):
    c = self.feval('phaselock', c, a, M, nout)
    return c

@register_method
def phaseunlockreal(self, c, a, M, nout = 1):
    c = self.feval('phaseunlock', c, a, M, nout)
    return c

@register_method
def symphase(self, c, a, nout = 1):
    c = self.feval('symphase', c, a, nout)
    return c


#Support for non-separable lattices
@register_method
def matrix2latticetype(self, L, V, nout = 1):
    [a,M,lt] = self.feval('matrix2latticetype', L, V, nout = 3)

@register_method
def latticetype2matrix(self, L, a, M, lt, nout = 1):
    V = self.feval('latticetype2matrix', L, a, M, lt, nout = 1)
    return V

@register_method
def shearfind(self, L, a, M, lt, nout = 1):
    [s0,s1,br] = self.feval('shearfind', L,a,M,lt, nout)

@register_method
def noshearlength(Ls, a, M, lt, nout):
    L = self.feval('noshearlength', Ls,a,M,lt, nout)
    return L


#Plots
    #not yet implemented

