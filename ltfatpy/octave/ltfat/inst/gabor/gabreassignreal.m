function sr=gabreassignreal(s,tgrad,fgrad,a,M)
%-*- texinfo -*-
%@deftypefn {Function} gabreassignreal
%@verbatim
%GABREASSIGNREAL  Reassign time-frequency distribution for real signals
%   Usage:  sr = gabreassignreal(s,tgrad,fgrad,a,M);
%
%   GABREASSIGNREAL(s,tgrad,fgrad,a,M) reassigns the values of the positive
%   time-frequency distribution s using the phase gradient given by fgrad*
%   and tgrad. The lattice is determined by the time shift a and the 
%   number of channels M.
%
%   fgrad and tgrad can be obtained by the routine GABPHASEGRADREAL.
%
%   Examples:
%   ---------
%
%   The following example demonstrates how to manually create a
%   reassigned spectrogram. An easier way is to just call RESGRAM:
%
%     % Create reassigned vector field of the bat signal.
%     a=4; M=100;
%     [phased,c] = gabphasederivreal({'t','f'},'dgt',bat,'gauss',a,M,'relative');
%     [tgrad, fgrad] = deal(phased{:});
%
%     % Perform the actual reassignment
%     sr = gabreassignreal(abs(c).^2,tgrad,fgrad,a,M);
%
%     % Display it using plotdgt
%     plotdgt(sr,a,143000,50);
%  
%
%   References:
%     F. Auger and P. Flandrin. Improving the readability of time-frequency
%     and time-scale representations by the reassignment method. IEEE Trans.
%     Signal Process., 43(5):1068--1089, 1995.
%     
%@end verbatim
%@strong{Url}: @url{http://ltfat.github.io/doc/gabor/gabreassignreal.html}
%@seealso{resgram, gabphasederivreal, gabreassign}
%@end deftypefn

% Copyright (C) 2005-2023 Peter L. Soendergaard <peter@sonderport.dk> and others.
% This file is part of LTFAT version 2.6.0
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>.

% AUTHOR: Peter L. Soendergaard, 2008.
%         Nicki Holighaus, 2023.

thisname = upper(mfilename);
complainif_notenoughargs(nargin,5,thisname);
complainif_notposint(a,'a',thisname);
complainif_notposint(M,'M',thisname);


% Basic checks
if any(cellfun(@(el) isempty(el) || ~isnumeric(el),{s,tgrad,fgrad}))
    error('%s: s, tgrad, fgrad must be non-empty and numeric.',...
          upper(mfilename));
end

% Check if argument sizes are consistent
if ~isequal(size(s),size(tgrad),size(fgrad))
   error('%s: s, tgrad, fgrad must all have the same size.',...
          upper(mfilename));
end

% Check if any argument is not real
if any(cellfun(@(el) ~isreal(el),{tgrad,fgrad}))
   error('%s: tgrad, fgrad must be real.',...
          upper(mfilename));
end

% if any(s<0)
%     error('%s: s must contain positive numbers only.',...
%         upper(mfilename));
% end

sr=comp_gabreassignreal(s,tgrad,fgrad,a,M);
