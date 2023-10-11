import os
import oct2py
from oct2py.core import Oct2Py
from oct2py.utils import Oct2PyError, get_log
from oct2py._version import __version__
from oct2py.demo import demo
from oct2py.io import Cell, Struct, StructArray
from oct2py.speed_check import speed_check
from oct2py.thread_check import thread_check
from oct2py import octave

__all__ = [
    "Oct2Py",
    "Oct2PyError",
    "octave",
    "Struct",
    "Cell",
    "StructArray",
    "demo",
    "speed_check",
    "thread_check",
    "__version__",
    "get_log",
]

try:
    os.chdir('./ltfatpy/ltfat')
    octave = Oct2Py()
    octave.eval('warning ("off", "all");')
    octave.eval('ltfatstart')
    #octave.eval('warning ("on", "all");')
except Oct2PyError as e:
    print(e)  # noqa


def kill_octave():
    """Kill all octave instances (cross-platform).

    This will restart the "octave" instance.  If you have instantiated
    Any other Oct2Py objects, you must restart them.
    """
    os.system("killall -9 octave")  # noqa
    os.system("killall -9 octave-cli")  # noqa
    octave.restart()