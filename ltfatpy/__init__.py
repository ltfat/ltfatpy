from oct2py.utils import Oct2PyError
from .ltfatpycore import Ltfat


try:
    ltfat = Ltfat()
#    ltfat.get_functions()
#throw an error if we can not instantiate ltfat
except Oct2PyError as e:
    print(e)  # noqa


#if __name__ == "__main__":
