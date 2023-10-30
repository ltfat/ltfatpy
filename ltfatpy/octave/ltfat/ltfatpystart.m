function ret = ltfatpystart(varargin)

ret = 0;
bp = ltfatpybasepath;

persistent workpath
workpath = genpath(bp);

addpath(workpath);