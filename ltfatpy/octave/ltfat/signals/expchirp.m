function [outsig]=expchirp(L,fstart,fend,varargin)
%EXPCHIRP  Exponential chirp
%   Usage: outsig=expchirp(L,fstart,fend)
%
%   `expchirp(L,fstart,fend)` computes an exponential chirp of length *L*
%   starting at frequency *fstart* and ending at frequency *fend*. The
%   freqencies are assumed to be normalized to the Nyquist frequency.
%
%   `expchirp` takes the following parameters at the end of the line of input
%   arguments:
%
%     'fs',fs    Use a sampling frequency of *fs* Hz. If this option is
%                specified, *fstart* and *fend* will be measured in Hz.
%
%     'phi',phi  Starting phase of the chirp. Default value is 0.
%
%     'fc',fc    Shift the chirp by *fc* in frequency. Default values is 0.
%
%     'ramp',r   Apply fade-in and fade out ramps on the first and last *r* samples.
%
%   See also: pchirp

% AUTHORS:  Piotr Majdak, Peter L. Søndergaard.

if nargin<3
  error('%s: Too few input parameters.',upper(mfilename));
end;

thismfilename = upper(mfilename);
complainif_notposint(L,'L',thismfilename);

if ~all(cellfun(@isscalar,{fstart,fend})) || ...
    any(cellfun(@(el) el<=0,{fstart,fend}))
    error('%s: fstart and fend must be scalars strictly greater than 0.',...
          thismfilename);
end

definput.keyvals.phi=0;
definput.keyvals.fs=[];
definput.keyvals.fc=0;
definput.keyvals.ramp=0;

[~,kv]=ltfatarghelper({},definput,varargin);

if ~isempty(kv.fs)
  fstart=fstart/kv.fs*2;
  fend  =  fend/kv.fs*2;
  kv.fc = kv.fc/kv.fs*2;
end;

if kv.ramp > L || kv.ramp < 0 || rem(kv.ramp,1) ~= 0
    error('%s: Ramp length must be a positive integer number less than L.',thismfilename);
end

w1=pi*fstart*L;
w2=pi*fend*L;

ratio = w2/w1;

A=w1/log(ratio);
tau=1/log(ratio);

l = 0:L-1; l = l(:);
t= l./L;
outsig=exp(1i*A*(exp(t/tau)-1)+kv.phi + 1i*pi*l*kv.fc);

if kv.ramp > 0
    outsig(end:-1:end-kv.ramp+1) = outsig(end:-1:end-kv.ramp+1).*rampup(kv.ramp);
    outsig(1:kv.ramp) = outsig(1:kv.ramp).*rampup(kv.ramp);
end

