#The code in this file was largely adapted from the oct2py project.

#Using IO management from oct2py...
#from oct2py.io import Cell, StructArray, read_file#, write_file
from .dynamic import (
    OctavePtr,
    _make_function_ptr_instance,
    _make_user_class,
    _make_variable_ptr_instance,
)
#the IO management is largely taken from oct2py as well...
from .io import Cell, StructArray, read_file, write_file

#these are all Python standard libs...
import logging
import os, sys, atexit
import os.path as osp
import shutil
import tempfile
import warnings

#numpy is a key dependency of ltfatpy
import numpy as np
#metakernel (more specifically: pexpect) handles the spawning of the Octave session
#as a subprocess of the Python session
from metakernel.pexpect import EOF, TIMEOUT  # type:ignore[import-untyped]
#the OctaveEngine is the same as for Jupyter
from octave_kernel.kernel import OctaveEngine

bp = os.path.dirname(os.path.dirname(__file__))
filepath = os.path.join(bp, 'ltfatpy')
sys.path.append(filepath)
import gabor as Gabor
import filterbank as Filterbank
import fourier as Fourier
import sigproc as Sigproc

def add_methods_from(*modules):
    def decorator(Class):
        for module in modules:
            for method in getattr(module, "__methods__"):
                setattr(Class, method.__name__, method)
        return Class
    return decorator

@add_methods_from(Gabor)
@add_methods_from(Filterbank)
@add_methods_from(Fourier)
@add_methods_from(Sigproc)
class Ltfat():

    """Manages an Octave session. based on Oct2Py

    Uses MAT files to pass data between Octave and Numpy.
    The function must either exist as an m-file in this directory or
    on Octave's path.
    The first command will take about 0.5s for Octave to load up.
    The subsequent commands will be faster.

    You may provide a logger object for logging events, or the oct2py.get_log()
    default will be used.  When calling commands, logger.info() will be used
    to stream output, unless a `stream_handler` is provided.

    Parameters
    ----------
    logger : logging object, optional
        Optional logger to use for Oct2Py session
    timeout : float, optional
        Timeout in seconds for commands
    oned_as : {'row', 'column'}, optional
        If 'column', write 1-D numpy arrays as column vectors.
        If 'row', write 1-D numpy arrays as row vectors.}
    temp_dir : str, optional
        If specified, the session's MAT files will be created in the
        directory, otherwise a default directory is used.  This can be
        a shared memory (tmpfs) path.
    convert_to_float : bool, optional
        If true, convert integer types to float when passing to Octave.
    backend: string, optional
        The graphics_toolkit to use for plotting.
    """

    def __init__(  # noqa
        self,
        logger=None,
        timeout=None,
        oned_as="row",
        temp_dir=None,
        convert_to_float=True,
        backend=None,
    ):
        """Start Octave and set up the session."""
        print("Setting up your Octave session in the background. This may take a while...")

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
        self.restart()

    @property
    def logger(self):
        """The logging instance used by the session."""
        return self._logger

    @logger.setter
    def logger(self, value):
        self._logger = value or get_log()
        if self._engine:
            self._engine.logger = self._logger

    def __getattr__(self, attr):
        
        if attr in self.__dict__:
            return self.__dict__[attr]
        else: 
            raise LtfatError("LTFATPY Error: Functionality not implemented in ltfatpy.")

    def __enter__(self):
        """Return octave object, restart session if necessary"""
        if not self._engine:
            self.restart()
        return self

    def __exit__(self, type_, value, traceback):
        """Close session"""
        self.exit()

    def __del__(self):
        """Delete session"""
        self.exit()

    def exit(self):  # noqa
        """Quits this octave session and cleans up."""
        if self._engine:
            self._engine.repl.terminate()
        self._engine = None

    def restart(self):
        """Restart an Octave session in a clean state"""
        if self._engine:
            self._engine.repl.terminate()

        if "OCTAVE_EXECUTABLE" not in os.environ and "OCTAVE" in os.environ:
            os.environ["OCTAVE_EXECUTABLE"] = os.environ["OCTAVE"]

        try:
            self._engine = OctaveEngine(logger=self.logger)
        except Exception as e:
            raise LtfatError(str(e)) from None

        # Add local Octave scripts.
        bp = os.path.dirname(os.path.dirname(__file__))
        filepath = os.path.join(bp, 'ltfatpy', 'octave', 'ltfat')
        sys.path.append(filepath)
        self._engine.eval('addpath("%s");' % filepath)
        self._engine.eval('addpath("%s");' % self.temp_dir)
        self._engine.eval('warning ("off", "all");')
        self._engine.eval("ltfatpystart;")

    def feval(self, func_path, *func_args, **kwargs):
        """Run a function in Octave and return the result.

        Parameters
        ----------
        func_path: str
            Name of function to run or a path to an m-file.
        func_args: object, optional
            Args to send to the function.
        nout: int or str, optional.
            The desired number of returned values, defaults to 1. If nout
            value is 'max_nout', _get_max_nout() will be used.
        store_as: str, optional
            If given, saves the result to the given Octave variable name
            instead of returning it.
        verbose : bool, optional
            Log Octave output at INFO level.  If False, log at DEBUG level.
        stream_handler: callable, optional
            A function that is called for each line of output from the
            evaluation.
        timeout: float, optional
            The timeout in seconds for the call.
        plot_dir: str, optional
            If specified, save the session's plot figures to the plot
            directory instead of displaying the plot window.
        plot_backend: str, optional
            The plotting back end to use.
        plot_name : str, optional
            Saved plots will start with `plot_name` and
            end with "_%%.xxx' where %% is the plot number and
            xxx is the `plot_format`.
        plot_format: str, optional
            The format in which to save the plot.
        plot_width: int, optional
            The plot with in pixels.
        plot_height: int, optional
            The plot height in pixels.

        Notes
        -----
        The function arguments passed follow Octave calling convention, not
        Python. That is, all values must be passed as a comma separated list,
        not using `x=foo` assignment.

        Examples
        --------
        >>> from oct2py import octave
        >>> cell = octave.feval('cell', 10, 10, 10)
        >>> cell.shape
        (10, 10, 10)

        >>> from oct2py import octave
        >>> x = octave.feval('linspace', 0, octave.pi() / 2)
        >>> x.shape
        (1, 100)

        >>> from oct2py import octave
        >>> x = octave.feval('svd', octave.hilb(3))
        >>> x
        array([[1.40831893],
               [0.12232707],
               [0.00268734]])
        >>> # specify three return values
        >>> (u, v, d) = octave.feval('svd', octave.hilb(3), nout=3)
        >>> u.shape
        (3, 3)

        Returns
        -------
        The Python value(s) returned by the Octave function call.
        """
        if not self._engine:
            msg = "Session is not open"
            raise LtfatError(msg)

        # nout handler
        nout = kwargs.get("nout", None)
        if nout is None:
            nout = 1
        elif nout == "max_nout":
            nout = self._get_max_nout(func_path)

        plot_dir = kwargs.get("plot_dir")
        
        # Choose appropriate plot backend.
        #default_backend = "inline" if plot_dir else self.backend
        #backend = kwargs.get("plot_backend", default_backend)

        #settings = dict(
        #    backend=backend,
        #    format=kwargs.get("plot_format"),
        #    name=kwargs.get("plot_name"),
        #    width=kwargs.get("plot_width"),
        #    height=kwargs.get("plot_height"),
        #    resolution=kwargs.get("plot_res"),
        #)
        #self._engine.plot_settings = settings

        dname = osp.dirname(func_path)
        fname = osp.basename(func_path)
        func_name, ext = osp.splitext(fname)
        if ext and ext != ".m":
            msg = "Need to give path to .m file"
            raise TypeError(msg)

        if func_name == "clear":
            msg = 'Cannot use `clear` command directly, use eval("clear(var1, var2)")'
            raise LtfatError(msg)

        stream_handler = kwargs.get("stream_handler")
        verbose = kwargs.get("verbose", True)
        store_as = kwargs.get("store_as", "")
        timeout = kwargs.get("timeout", self.timeout)
        if not stream_handler:
            stream_handler = self.logger.info if verbose else self.logger.debug
        
        #print(inargs)
        #print(func_name)
        #print(func_args)

        return self._feval(
            func_name,
            func_args,
            dname=dname,
            nout=nout,
            timeout=timeout,
            stream_handler=stream_handler,
            store_as=store_as,
            plot_dir=plot_dir,
        )

    def eval(  # noqa
        self, 
        cmds,
        verbose=True,
        timeout=None,
        stream_handler=None,
        temp_dir=None,
        plot_dir=None,
        plot_name="plot",
        plot_format="svg",
        plot_backend=None,
        plot_width=None,
        plot_height=None,
        plot_res=None,
        nout=0,
        **kwargs,
    ):
        """
        Evaluate an Octave command or commands.

        Parameters
        ----------
        cmds : str or list
            Commands(s) to pass to Octave.
        verbose : bool, optional
             Log Octave output at INFO level.  If False, log at DEBUG level.
        stream_handler: callable, optional
            A function that is called for each line of output from the
            evaluation.
        timeout : float, optional
            Time to wait for response from Octave (per line).  If not given,
            the instance `timeout` is used.
        nout : int or str, optional.
            The desired number of returned values, defaults to 0.  If nout
            is 0, the `ans` will be returned as the return value. If nout
            value is 'max_nout', _get_max_nout() will be used.
        temp_dir: str, optional
            If specified, the session's MAT files will be created in the
            directory, otherwise a the instance `temp_dir` is used.
            a shared memory (tmpfs) path.
        plot_dir: str, optional
            If specified, save the session's plot figures to the plot
            directory instead of displaying the plot window.
        plot_name : str, optional
            Saved plots will start with `plot_name` and
            end with "_%%.xxx' where %% is the plot number and
            xxx is the `plot_format`.
        plot_format: str, optional
            The format in which to save the plot (PNG by default).
        plot_width: int, optional
            The plot with in pixels.
        plot_height: int, optional
            The plot height in pixels.
        plot_backend: str, optional
            The plot backend to use.
        plot_res: int, optional
            The plot resolution in pixels per inch.
        **kwargs Deprecated kwargs.

        Examples
        --------
        >>> from oct2py import octave
        >>> octave.eval('disp("hello")') # doctest: +SKIP
        hello
        >>> x = octave.eval('round(quad(@sin, 0, pi/2));')
        >>> x
        1.0

        >>> a = octave.eval('disp("hello");1;')  # doctest: +SKIP
        hello
        >>> a = octave.eval('disp("hello");1;', verbose=False)
        >>> a
        1.0

        >>> from oct2py import octave
        >>> lines = []
        >>> octave.eval('for i = 1:3; disp(i);end', \
                        stream_handler=lines.append)
        >>> lines  # doctest: +SKIP
        [' 1', ' 2', ' 3']

        Returns
        -------
        out : object
            Octave "ans" variable, or None.

        Notes
        -----
        The deprecated `log` kwarg will temporarily set the `logger` level to
        `WARN`.  Using the `logger` settings directly is preferred.
        The deprecated `return_both` kwarg will still work, but the preferred
        method is to use the `stream_handler`.  If `stream_handler` is given,
        the `return_both` kwarg will be honored but will give an empty string
        as the response.

        Raises
        ------
        LtfatError
            If the command(s) fail.
        """
        if isinstance(cmds, str):
            cmds = [cmds]

        prev_temp_dir = self.temp_dir
        self.temp_dir = temp_dir or self.temp_dir
        prev_log_level = self.logger.level

        if kwargs.get("log") is False:
            self.logger.setLevel(logging.WARN)

        for name in ["log", "return_both"]:
            if name not in kwargs:
                continue
            msg = "Using deprecated `%s` kwarg, see docs on `Oct2Py.eval()`"
            warnings.warn(msg % name, stacklevel=2)

        return_both = kwargs.pop("return_both", False)
        lines: list[str] = []
        if return_both and not stream_handler:
            stream_handler = lines.append

        ans = None
        #inargs = []
        for cmd in cmds:
            resp = self.feval(
                "evalin",
                "base",
                cmd,
                nout=nout,
                timeout=timeout,
                stream_handler=stream_handler,
                verbose=verbose,
                plot_dir=plot_dir,
                plot_name=plot_name,
                plot_format=plot_format,
                plot_backend=plot_backend,
                plot_width=plot_width,
                plot_height=plot_height,
                plot_res=plot_res,
            )
            if resp is not None:
                ans = resp

        self.temp_dir = prev_temp_dir
        self.logger.setLevel(prev_log_level)

        if return_both:
            return "\n".join(lines), ans
        return ans

    def _feval(  # noqa
        self,
        func_name,
        func_args=(),
        dname="",
        nout=0,
        timeout=None,
        stream_handler=None,
        store_as="",
        plot_dir=None,
    ):
        """Run the given function with the given args."""
        engine = self._engine
        if engine is None:
            msg = "Session is closed"
            raise LtfatError(msg)

        # Set up our mat file paths.
        out_file = osp.join(self.temp_dir, "writer.mat")
        out_file = out_file.replace(osp.sep, "/")
        in_file = osp.join(self.temp_dir, "reader.mat")
        in_file = in_file.replace(osp.sep, "/")

        func_args = list(func_args)
        #HERE
        #print(*func_args)
        #print(any(isinstance(val, str) for val in tuple(func_args)))

        ref_indices = []
        for i, value in enumerate(func_args):
            if isinstance(value, OctavePtr):
                ref_indices.append(i + 1)
                func_args[i] = value.address
        ref_arr = np.array(ref_indices)

        # Save the request data to the output file.
        req = dict(
            func_name=func_name,
            func_args=tuple(func_args),
            dname=dname or "",
            nout=nout,
            store_as=store_as or "",
            ref_indices=ref_arr,
            #inargs = inargs[1:len(inargs)-1],
        )

        write_file(req, out_file, oned_as=self._oned_as, convert_to_float=self.convert_to_float)

        # Set up the engine and evaluate the `_pyeval()` function.
        #engine.line_handler = stream_handler.any() or self.logger.info
        engine.line_handler = stream_handler or self.logger.info
        if timeout is None:
            timeout = self.timeout

        try:
            engine.eval(f'_ltfatpyeval("{out_file}", "{in_file}");', timeout=timeout)
        except KeyboardInterrupt:
            stream_handler(engine.repl.interrupt())
            raise
        except TIMEOUT:
            stream_handler(engine.repl.interrupt())
            msg = "Timed out, interrupting"
            raise LtfatError(msg) from None
        except EOF:
            if not self._engine:
                return
            stream_handler(engine.repl.child.before)
            self.restart()
            msg = "Session died, restarting"
            raise LtfatError(msg) from None

        # Read in the output.
        resp = read_file(in_file, self)
        if resp["err"]:
            msg = self._parse_error(resp["err"])
            raise LtfatError(msg)

        result = resp["result"].ravel().tolist()
        if isinstance(result, list) and len(result) == 1:
            result = result[0]

        # Check for sentinel value.
        if (
            isinstance(result, Cell)
            and result.size == 1
            and isinstance(result[0], str)
            and result[0] == "__no_value__"
        ):
            result = None

        if plot_dir:
            engine.make_figures(plot_dir)

        return result

    def _parse_error(self, err):
        """Create a traceback for an Octave evaluation error."""
        self.logger.debug(err)
        stack = err.get("stack", [])
        if not err["message"].startswith("parse error:"):
            err["message"] = "error: " + err["message"]
        errmsg = "Octave evaluation error:\n%s" % err["message"]

        if not isinstance(stack, StructArray):
            return errmsg

        errmsg += "\nerror: called from:"
        for item in stack[:-1]:
            errmsg += "\n    %(name)s at line %(line)d" % item
            try:  # noqa
                errmsg += ", column %(column)d" % item
            except Exception:  # noqa
                pass
        return errmsg

        #override help from oct2py because of formatting
    def help(self, str):
        self.eval('help '+str)

    def push(self, name, var, timeout=None, verbose=True):
        if isinstance(name, str):
            name = [name]
            var = [var]

        for n, v in zip(name, var):
            self.feval('assignin', 'base', n, v, nout=0)

        
    def pull(self, var):
        #if isinstance(var, (OctaveVariablePtr)):
        #    raise LtfatError("LTFATPY Error: You can not evaluate an Octave pointer in Python.")
            

        if isinstance(var, str):
            var = [var]
        outputs = []
        for name in var:
            #exist = self._exist(name)
            exist = 1
            if exist == 1:
                outputs.append(self.feval("evalin", "base", name))
            else:
                outputs.append(self.get_pointer(name, timeout=timeout))

        if len(outputs) == 1:
            return outputs[0]
        return outputs

    def _exist(self, name):
        """Test whether a name exists and return the name code.

        Raises an error when the name does not exist.
        """
        cmd = 'exist("%s")' % name
        if not self._engine:
            msg = "Session is not open"
            raise LtfatError(msg)
        resp = self._engine.eval(cmd, silent=True).strip()
        exist = int(resp.split()[-1])
        if exist == 0:
            cmd = "class(%s)" % name
            resp = self._engine.eval(cmd, silent=True).strip()
            if "error:" in resp:
                msg = 'Value "%s" does not exist in Octave workspace'
                raise LtfatError(msg % name)
            else:
                exist = 2
        return exist

    def get_pointer(self, name, timeout=None):
        """Get a pointer to a named object in the Octave workspace.

        Parameters
        ----------
        name: str
            The name of the object in the Octave workspace.
        timeout: float, optional.
            Time to wait for response from Octave (per line).

        Examples
        --------
        >>> from oct2py import octave
        >>> octave.eval('foo = [1, 2];')
        >>> ptr = octave.get_pointer('foo')
        >>> ptr.value
        array([[1., 2.]])
        >>> ptr.address
        'foo'
        >>> # Can be passed as an argument
        >>> octave.disp(ptr)  # doctest: +SKIP
        1  2

        >>> from oct2py import octave
        >>> sin = octave.get_pointer('sin')  # equivalent to `octave.sin`
        >>> sin.address
        '@sin'
        >>> x = octave.quad(sin, 0, octave.pi())
        >>> x
        2.0

        Notes
        -----
        Pointers can be passed to `feval` or dynamic functions as function
        arguments.  A pointer passed as a nested value will be passed by value
        instead.

        Raises
        ------
        Oct2PyError
            If the variable does not exist in the Octave session or is of
            unknown type.

        Returns
        -------
        A variable, object, user class, or function pointer as appropriate.
        """
        #exist = self._exist(name)
        #isobject = self._isobject(name, exist)

        #if exist == 0:
        #    raise Oct2PyError('"%s" is undefined' % name)

        #elif exist == 1:
        return _make_variable_ptr_instance(self, name)

        #elif isobject:
        #    return self._get_user_class(name)

        #elif exist in [2, 3, 5]:
        #    return self._get_function_ptr(name)

        #raise Oct2PyError('Unknown type for object "%s"' % name)


def get_log(name=None):
    """Return a console logger.

    Output may be sent to the logger using the `debug`, `info`, `warning`,
    `error` and `critical` methods.

    Parameters
    ----------
    name : str
        Name of the log.
    """
    name = "oct2py" if name is None else "oct2py." + name

    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    return log


class LtfatError(Exception):
    """Called when we can't open Octave or Octave throws an error"""
    #sys.tracebacklimit = 0 #TODO: find a neater solution here
    pass


__all__ = [
    "ltfat"
]


try:
    ltfat = Ltfat()
#    ltfat.get_functions()
#throw an error if we can not instantiate ltfat
except LtfatError as e:
    print(e)  # noqa


#if __name__ == "__main__":
