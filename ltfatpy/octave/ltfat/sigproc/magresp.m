function magresp(g,varargin);
%MAGRESP   Magnitude response plot of window
%   Usage:   magresp(g,...);
%            magresp(g,fs,...);
%            magresp(g,fs,dynrange,....);
%
%   `magresp(g)` will display the magnitude response of the window on a log
%   scale (dB);
%
%   `magresp(g,fs)` does the same for windows that are intended to be used
%   with signals with sampling rate *fs*. The x-axis will display Hz.
%
%   `magresp(g,fs,dynrange)` will limit the dynamic range (see below).
%   
%   `magresp` takes the following parameters at the end of the line of
%   input arguments.
%
%     'dynrange',r  Limit the dynamic range of the plot to r dB.
%
%     'fir'         Indicate that the input is an FIR window. |magresp| will
%                   zero-extend the window to display a smooth magnitude
%                   response.
%
%     'L',L         Zero-extend the window to length L.
%
%     'posfreq'     Show only positive frequencies.
%
%     'nf'          Show also negative frequencies
%
%     'autoposfreq'  Show positive frequencies for real-valued signals,
%                    otherwise show also the negative frequencies. This is
%                    the default.
%
%     'opts',op     Pass options onto the plot command. The extra options
%                   *op* are specified as a cell array
%
%   In addition to these flags, it is possible to speficy any of the
%   normalization flags from |setnorm| to normalize the input before
%   calculation of the magnitude response. Specifying `'1'` or `'area'` will
%   display a magnitude response which peaks at 0 dB.
%
%   Examples:
%   ---------
%
%   The following will display the magnitude response of a Hann window
%   of length 20 normalized to a peak of 0 dB:::
%
%     magresp({'hann',20},'1');
%
%   The following will display the magnitude response of a Gaussian window
%   of length 100:::
%
%     magresp('gauss','L',100)
%
%   The following passes additional options to the plot command to draw
%   in red:::
%
%     magresp({'nuttall11',30},'opts',{'r'});
%
%   Demos: demo_gabfir     

%   AUTHOR : Peter L. Søndergaard.
%   TESTING: NA
%   REFERENCE: NA

if nargin<1
  error('Too few input arguments.');
end;

L=[];
fs=[];
donf=0;

% Define initial value for flags and key/value pairs.

definput.flags.posfreq={'autoposfreq','posfreq','nf'};

definput.import={'setnorm'};
definput.importdefaults={'null'};
definput.keyvals.fs=[];
definput.keyvals.opts={};
definput.keyvals.L=[];
definput.flags.wintype={'notype','fir','long'};
definput.keyvals.dynrange=[];

[flags,kv,fs]=ltfatarghelper({'fs','dynrange'},definput,varargin);

[g,info] = comp_fourierwindow(g,kv.L,'MAGRESP');

do_real=flags.do_posfreq;
if flags.do_autoposfreq
  do_real=info.wasreal;
end;

if flags.do_fir
  info.isfir=1;
end;

if isempty(kv.L) 
  if info.isfir
    % Choose a strange length, such that we don't accidentically hit all
    % the zeros in the response.
    kv.L=info.gl*13+47;
  else
      if isempty(info.gl)
          % Default value
          kv.L=4177;
      else          
          kv.L=info.gl;
      end;
  end;
end;

if (isstruct(g)) && isfield(g,'fs') && (~isempty(g.fs)) && (isempty(fs))
    fs=g.fs;
end;

g=pfilt([1;zeros(kv.L-1,1)],g);

g=setnorm(g,flags.norm);
if do_real

  % Compute spectrum and normalize
  FF=abs(fftreal(real(g)));
    
  % Convert to dB. Add eps to avoid log of zero.
  FF=20*log10(FF+realmin);

  xmin=0;

else

  % Compute spectrum and normalize. fftshift to center correctly for plotting.
  FF=fftshift(abs(fft(g)));
  
  % Convert to dB. Add eps to avoid log of zero.
  FF=20*log10(FF+realmin);

  xmin=-1;
end;

ymax=max(FF);
if ~isempty(kv.dynrange)
  ymin=ymax-kv.dynrange;
else
  ymin=min(FF);
end;

Lplot=length(FF);

% Only plot positive frequencies for real-valued signals.
if isempty(fs)
  xrange=linspace(xmin,1,Lplot).';
  axisvec=[xmin 1 ymin ymax];
else
  xrange=linspace(xmin*floor(fs/2),floor(fs/2),Lplot).';
  axisvec=[xmin*fs/2 fs/2 ymin ymax];
end;

plot(xrange,FF,kv.opts{:});
set(gca,'yscale','linear');
if ymax-ymin~=0
    axis(axisvec);
end
ylabel('Magnitude response (dB)');

if isempty(fs)
  xlabel('Frequency (normalized) ');
else
  xlabel('Frequency (Hz)');
end;

legend('off');

