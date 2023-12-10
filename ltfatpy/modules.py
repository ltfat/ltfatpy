import os, sys
import shutil, atexit, tempfile
from oct2py import Oct2Py

#import traceback
#import logging
#import warnings

from octave_kernel.kernel import OctaveEngine  # type:ignore[import-untyped]

class Ltfat(Oct2Py):
    engine = None
    def __init__(  # noqa
    #overload of oct2py method for Octave object control (oct2py is licensed under the MIT license)
        self,
        logger=None,
        timeout=None,
        oned_as="row",#write 1D numpy arrays as row vectors
        temp_dir=None,#should be shared memory path tmpfs: per default in RAM (theoretically fastest)
        convert_to_float=True,#convert integers to float when communicating with octave
        backend=None,
        mfile = None,
        ):
        """Start Octave and set up the session."""
        self._oned_as = oned_as
        self._engine = None
        self._logger = None
        self.logger = logger
        self.timeout = timeout
        self.backend = backend or "default"
        if temp_dir is None:
            temp_dir_obj = tempfile.mkdtemp()
            self.temp_dir = temp_dir_obj
            atexit.register(shutil.rmtree, self.temp_dir)
        else:
            self.temp_dir = temp_dir
        self.convert_to_float = convert_to_float
        self._user_classes = {}
        self._function_ptrs = {}
        self.mfile = mfile
        self.restart()

    def restart(self):
        #overload of oct2py method for controlling access to LTFAT files in case of a restart
        """Restart an Octave session in a clean state"""
        if self._engine:
            self._engine.repl.terminate()
            engine = self._engine

        if "OCTAVE_EXECUTABLE" not in os.environ and "OCTAVE" in os.environ:
            os.environ["OCTAVE_EXECUTABLE"] = os.environ["OCTAVE"]

        try:
            self._engine = OctaveEngine(stdin_handler=self._handle_stdin, logger=self.logger)
            engine = self._engine
        except Exception as e:
            raise Oct2PyError(str(e)) from None #TODO: replace Oct2PyError

        #add the path to the Octave scripts
        bp = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(bp, 'ltfatpy', 'octave', 'ltfat')
        self._engine.eval('addpath("%s");' % filepath)
        if not self.mfile:
            self._engine.eval('ltfatpystart')
        elif self.mfile == "gabor":
            self._engine.eval('ltfatpystart')

    #def __init__(self):
    #    self.get_functions()

    #if a method is called, check first if we have it here in the class,
    #and if not, search in the Oct2Py object
    #def __getattr__(self, attr):
    #    if attr in self.__dict__:
    #        return self.__dict__[attr]
        #elif value := getattr(self.ltfat, attr):
        #   return value
    #    else:
    #        return None
    #        return super().__dict__[attr]

    #a method for controlling the functions one gets
    #def get_functions(self):
        #confirm that octave is running
        #if not self._engine:
        #    self.octave = Oct2Py()
    #    self.octave = Oct2Py()
    #    if self._engine:
    #        bp = os.path.dirname(os.path.dirname(__file__))
    #        filepath = os.path.join(bp, 'ltfatpy', 'octave', 'ltfat')
    #        self.addpath(filepath)
        #execute the startfile
            #with self:
                
    #        try: 
    #            self.eval('warning ("off", "all");')
    #            self.eval('ltfatpystart')
                #self.eval('warning ("on", "all");')
    #        except Exception as inst:
    #            traceback.print_tb(inst, limit=1, file=None)
            #else:
            #    with self:
            #        pass


    #override help from oct2py because of formatting
    def help(self, str):
        self.eval('help '+str)

    def __enter__(self):
        if not self._engine:
            self.restart()
            bp = os.path.dirname(os.path.dirname(__file__))
            filepath = os.path.join(bp, 'ltfatpy', 'octave', 'ltfat')
            self._engine.eval('addpath("%s");' % filepath)
            self._engine.eval('warning ("off", "all");')
            engine = self._engine
        self._engine.eval('ltfatpystart;')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
    #   include call to ltfatpyerror here (intercept and cut off Traceback)
        if traceback:
            print("\nExecution value:", exc_value)
            #print("\nTraceback:", traceback)

        if self._engine:
            self._engine.repl.terminate()
        self._engine = None
        engine = self._engine
        return True
    #a method for custom exceptions
    #def ltfaterror(Exception):
        #use super()._parse_error() to catch octave errors
        #if there is an octave error, suppress the Python traceback
    #    super()._parse_error(Exception)
        #pass

#======================================================================================

class Gabor(Ltfat):
    def __init__(self,a, M, g='gauss', isreal=0, lt=[0, 1], phase = 'freqinv'):
        #if octave is not already running, instantiate Ltfat
        if not Ltfat.engine:
            Ltfat.__init__(self, logger=None,timeout = None, oned_as="row",temp_dir=None,convert_to_float=True,backend=None,mfile = "gabor")

        #members are all those parameters that remain constant throughout
        self.a = a
        self.M = M
        self.g = g
        self.isreal = isreal
        self.lt = lt
        self.phase = phase
        #these are the parameters that may or may not be calculated later on
        self.c = None
        self.istight = None
        self.A = None
        self.B = None
        self.gd = None
        self.oneD = None
        self.twoD = None
        self.tgrad = None
        self.fgrad = None
        self.c_reassigned = None
        #TODO, lattices: Ideally, one passes the lattice already at construction. this is feasible.


    #operations related directly to the transform
    def transform(self, f, type="oneD", gabdict=[]):
        #TODO: decide on how to pass info on 2D transform; it is theoretically possible to have a = [a1 a2]
        # - should we acommodate for that?
        #TODO: include operator option to speed up later computations
        #TODO: decide on type hinting YES/NO
        #if f.shape[0] == 1 or f.shape[1] == 1:
        if type == "oneD":
            self.oneD = 1
            self.twoD = 0
            if self.isreal:
                return self.dgtreal(f, self.g, self.a, self.M)
            else:
                return self.dgt(f, self.g, self.a, self.M)
        elif type == "twoD":
                self.oneD = 0
                self.twoD = 1
                return self.dgt2(f, self.g, self.a, self.M)
        elif type == "sparse" and gabdict:
            if self.isreal:
                self.oneD = "sparse"
                self.twoD = 0
                return self.multidgtrealmp(f, gabdict)
            else:
                raise(Exception("LTFAT Error: transform not implemented"))
        else:
            raise(Exception("LTFAT Error: transform not implemented"))

    def gabwin(self, winstr, agab, Mgab, Lgab):
        #original syntax: g=gabwin({'dual',{'hann',20}},a,M,L);
        try:
            gtest = self.feval('gabwin', self.eval(winstr), agab, Mgab, Lgab, nout = 1)
        except TypeError as e:
            raise ltfaterror("ERROR")
        #TODO: TypeError: unhashable type: 'set' abfangen: passiert, wenn user nicht mit string uebergeben
        #alternative: abfangen, als frozenset parsen (geschwungene Klammern erkennen), zu string konvertieren,
        #geschwungene Klammern hinzu fuegen, zu einem grossen string zusammenfassen, geschwungene Klammern
        #hinzufuegen, das Ganze beliebig oft verschachtelt, und dann self.eval() verwenden
        return gtest

    def inverse(self, c):
        if not self.gd and not self.istight:
            self.dualwindow()
        if self.oneD: #(TODO in getattr return nan if attribute nonexistent => done)
            if self.isreal:
                return self.idgtreal(c, self.gd, self.a, self.M)
            else:
                return self.idgt(c, self.gd, self.a)
        elif self.twoD:
                return self.idgt2(c, self.gd, self.a, self.M)
        else:
            raise(Exception("LTFAT Error: bad array dimension"))

    def dualwindow(self, type="dual", Lws=0, gm = 0):
        #Lws...len(window_support)
        #when the parameter "tight" is passed, BOTH windows are changed. for all other
        #parameters, only the dual window is set.
        if type == "dual":
            if Lws:
                self.gd = self.gabfirdual(Lws,self.g,self.a,self.M)
                return self.gd
            else:
                self.gd = self.gabdual(self.g,self.a,self.M)
                return self.gd
        elif type == "tight":
            if Lws:
                self.gd = self.gabfirtight(Lws,self.g,self.a,self.M)
                self.g = self.gd
                return self.gd
            else:
                self.gd = self.gabtight(self.g,self.a,self.M)
                self.g = self.gd
                return self.gd
        elif type == "proj" and gm:
            #if the window has already been calculated (i.e. it is not None and not a string)...
            if self.g and not isinstance(self.g, str):
                L = len(g)
            else:
                L = 1
            self.gd = self.gabprojdual(gm,self.g, self.a, self.M, L)
            return self.gd
        elif type == "mix" and gm:
            self.gd = self.gabmixdual(gm,self.g,self.a,self.M)
            return self.gd
        else:
            raise(Exception("LTFAT Error: window not defined"))

    #operations that extract information from the t-f coefficients
    def fbounds(self):
        #gabrieszbounds YES/NO???
        #gabframediag YES/NO???
        #my tendency: they are both not strictly necessary for practical applications.
        #they are both available anyways. so I think, they do not need to be part of this class.
        #also: one may want to use gabframediag on the dual window. this would laxen the class
        #structure. another reason why I do not like it.

        #this more complicated syntax is necessary to get both, A and B
        [A, B] = self.feval('gabframebounds', self.g, self.a, self.M, nout = 2)
        self.A = A
        self.B = B
        if B/A == 1:
            self.istight = 1
        return A, B

    #TODO: get the phase stuff sorted
    #actually, the best thing would probably be to only use gabphasederiv and get rid of *gradient.
    #but honestly, this is tedious. (NICKI)
    #def phasegradient(self, f):
    #    #there are several cases
    #    [tgrad, fgrad,c] = self.feval('gabphasegrad', f, self.g, self.a, self.M, nout=3)
    #    return tgrad, fgrad, c

    def phasederivative(self, f, dflag):
        #I switched the order of input arguments (dflag, f) here, because it seems more "natural" to me.
        #there are several cases, this needs to be fevaled
        return self.gabphasederiv(str(dflag),'dgt',f,self.g,self.a,self.M)

    #operations on the t-f coefficients
    def reassign(self, s, tgrad, fgrad, mu=0):
        if mu:
            return self.gabreassignadjust(s,tgrad,fgrad,self.a, mu)
        else:
            if self.isreal:
                return self.gabreassignreal(s,tgrad,fgrad,self.a)
            else:
                return self.gabreassign(s,tgrad,fgrad,self.a)

    def gabmulappr(self, T):
        return gabmulappr(T, self.a, self.M)

    def tfjigsawsep(self):
        pass

    def plot(self, type = "dgt"):
        pass

    #phase locking and unlocking: strictly necessary in this class?
    #what about symphase?
    #def lockphase(c):
    #    if self.isreal:
    #        return self.phaselockreal(c, self.a, self.M)
    #    else:
    #        return self.phaselock(c, self.a)

    #def unlockphase(c):
    #    if self.isreal:
    #        return self.phaseunlockreal(c, self.a, self.M)
    #    else:
    #        return self.phaseunlock(c, self.a)
    #TODO: operations that apply the t-f coefficients
    #not yet implemented
    #def matchingpursuit(f, dicts=auto):
    #def gabframemul():
    #def tfjigsaw():

    #def plot(type = "dgt"):
    #    if type == "dgt":
    #    elif type == "phase":
    #    else:
    #       print("Not implemented.")


Stft = Gabor
#engineering-style overload :) - should probably be the other way around, because
#Stft may need fewer methods than Gabor
#class Stft(Gabor):
#    def conditionnumber(self):
#        super().fbounds(self)
