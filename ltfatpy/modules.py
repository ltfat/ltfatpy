import os
from oct2py import Oct2Py

class Ltfat:
    def __init__(self):
        self.octave = Oct2Py()
        self.get_functions()

    #if a method is called, check first if we have it here in the class,
    #and if not, search in the Oct2Py object
    def __getattr__(self, attr):
        if attr in self.__dict__:
            return self.__dict__[attr]
        else: 
            return getattr(self.octave, attr)
            #return self.octave.__dict__[attr]

    #a method for controlling the functions one gets
    def get_functions(self):
        #confirm that octave is running
        if self._engine:
            bp = os.path.dirname(os.path.dirname(__file__))
            filepath = os.path.join(bp, 'ltfatpy', 'octave', 'ltfat')
            self.addpath(filepath)
        #execute the startfile
            with self:
                self.eval('warning ("off", "all");')
                self.eval('ltfatpystart')
                #self.eval('warning ("on", "all");')

    #override help from oct2py because of formatting
    def help(self, str):
        self.eval('help '+str)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        #raise(Exception("LTFAT ERROR"))
        return True
    #a method for custom exceptions
    def ltfaterror(msg):
        #use super()._parse_error() to catch octave errors
        #if there is an octave error, suppress the Python traceback
        pass

#======================================================================================

class Gabor(Ltfat):
    def __init__(self, a, M, g="gauss", isreal=0, lt=[0, 1], phase = 'freqinv'):
        #should check if octave is already running, and if not, instantiate it
        #if not self._engine:
        self.octave = Oct2Py()
        super().get_functions()

        #members are all those parameters that remain constant throughout
        self.a = a
        self.M = M
        self.g = g
        self.real = isreal
        self.lt = lt
        self.phase = phase


    #operations related directly to the transform
    def transform(self, f):
        if f.ndim == 1:
            if self.isreal:
                return self.dgtreal(f, self.g, self.a, self.M)
            else:
                return self.dgt(f, self.g, self.a)
        elif f.ndim == 2:
                return self.dgt2(f, self.g, self.a, self.M)
        else:
            raise(Exception("LTFAT Error: bad array dimension"))

    def inverse(self, c):
        if f.ndim == 1:
            if self.isreal:
                return self.idgtreal(c, self.g, self.a, self.M)
            else:
                return self.idgt(f, self.g, self.a)
        elif f.ndim == 2:
                return self.idgt2(f, self.g, self.a, self.M)
        else:
            raise(Exception("LTFAT Error: bad array dimension"))

    def window(self, type="dual", L=0):
        #L refers here to the length of the dual window - maybe choose another name
        if type=="dual":
            if L:
                return self.gabfirdual(L,self.g,self.a,self.M)
            else:
                return self.gabdual(self.g,self.a,self.M)
        elif type=="tight":
            if L:
                return self.gabfirtight(L,self.g,self.a,self.M)
            else:
                return self.gabtight(self.g,self.a,self.M)
        else:
            raise(Exception("LTFAT Error: window not defined"))

    #operations on the t-f coefficients
    def reassign(self, s, tgrad, fgrad, mu=0):
        if mu:
            return self.gabreassignadjust(s,tgrad,fgrad,self.a, mu)
        else:
            if self.isreal:
                return self.gabreassignreal(s,tgrad,fgrad,self.a)
            else:
                return self.gabreassign(s,tgrad,fgrad,self.a)

    #operations that extract information from the t-f coefficients
    def framebounds(self):
        return self.gabframebounds(self.g,self.a,self.M)

    def phasegradient(self, f):
        #there are several cases
        [tgrad, fgrad,c] = self.feval('gabphasegrad', f, self.g, self.a, self.M, nout=3)
        return tgrad, fgrad, c

    def phasederivative(self, dflag, f):
        #there are several cases, this needs to be fevaled
        return self.gabphasederiv(str(dflag),'dgt',f,self.g,self.a,self.M)

    #operations that apply the t-f coefficients
    #not yet implemented



#engineering-style overload :) - should probably be the other way around, because
#Stft may need fewer methods than Gabor
class Stft(Gabor):
    def conditionnumber(self):
        super().framebounds(self)
