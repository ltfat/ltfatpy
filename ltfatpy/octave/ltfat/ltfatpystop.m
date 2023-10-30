function ret = ltfatpystop(varargin)

ret = 0;
bp = ltfatpybasepath;

persistent workpath
workpath = genpath(bp);

rmpath(workpath);