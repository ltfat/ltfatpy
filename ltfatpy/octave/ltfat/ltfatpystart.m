function ret = ltfatpystart(varargin)

%ret = 0;
bp = ltfatpybasepath;

persistent workpath
workpath = genpath(bp);

banner = sprintf(['This is LTFATPY version 0.1. ']);
  
disp(banner);

addpath(workpath);