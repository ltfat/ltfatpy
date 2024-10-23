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

#Fourier
@register_method
def firwin(self, name, M, *args, nout = 1):
    return self.feval('firwin', name, M, *args, nout=nout)

