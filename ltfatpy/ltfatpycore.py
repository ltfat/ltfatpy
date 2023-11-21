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
        raise(Exception("LTFAT ERROR"))
        return True
    #a method for custom exceptions
    def ltfaterror(msg):
        #use super()._parse_error() to catch octave errors
        #if there is an octave error, suppress the Python traceback
        pass


class Gabor(Ltfat):
    def __init__(self):
        #should check if octave is already running, and if not, instantiate it
        #it could have properties, this is not yet decided
        pass

    #it should in any case have its own get_functions method
    def get_functions(self):
        #confirm that octave is running
        bp = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(bp, 'ltfatpy', 'octave', 'ltfat')
        self.addpath(filepath)
        #execute the startfile
        self.eval('warning ("off", "all");')
        self.eval('ltfatpystart')
        #self.eval('warning ("on", "all");')

    #it remains to be seen if the gabor methods should be stored in a dictionary
    #or similar