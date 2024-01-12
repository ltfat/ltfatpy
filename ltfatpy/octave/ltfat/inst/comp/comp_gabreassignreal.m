function sr=comp_gabreassignreal(s,tgrad,fgrad,a,M);
%-*- texinfo -*-
%@deftypefn {Function} comp_gabreassignreal
%@verbatim
%COMP_GABREASSIGNREAL  Reassign time-frequency distribution.
%   Usage:  sr = comp_gabreassign(s,tgrad,fgrad,a);
%
%   COMP_GABREASSIGNREAL(s,tgrad,fgrad,a,M) will reassign the values of the 
%   positive time-frequency distribution s using the instantaneous time and 
%   frequency fgrad and tgrad. The lattice is determined by the time shift 
%   a and the number of channels M.
%
%
%   References:
%     F. Auger and P. Flandrin. Improving the readability of time-frequency
%     and time-scale representations by the reassignment method. IEEE Trans.
%     Signal Process., 43(5):1068--1089, 1995.
%     
%@end verbatim
%@strong{Url}: @url{http://ltfat.github.io/doc/comp/comp_gabreassignreal.html}
%@seealso{gabreassignreal}
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

%   AUTHOR : Peter L. Soendergaard.
%   TESTING: OK
%   REFERENCE: OK

[M2,N,W]=size(s);
L=N*a;
b=L/M;

freqpos=(0:M2-1).';
tgrad=bsxfun(@plus,tgrad/b,freqpos);

timepos=fftindex(N);
fgrad=bsxfun(@plus,fgrad/a,timepos.');

tgrad=round(tgrad);
fgrad=round(fgrad);

tgrad=mod(tgrad,M);
fgrad=mod(fgrad,N);  
  
sr=zeros(M2,N,W,assert_classname(s,tgrad,fgrad));

fgrad=fgrad+1;
tgrad=tgrad+1;

% In theory, this should not be necessary, but we make sure that fgrad is
% in the range 1 to M2
zeroIdxs = (tgrad > floor(3/4*M)+1);
tgrad(zeroIdxs) = 1;
tgrad(tgrad > M2 & ~ zeroIdxs) = M2;

for w=1:W
    for ii=1:M2
        for jj=1:N      
            sr(tgrad(ii,jj),fgrad(ii,jj),w) = sr(tgrad(ii,jj),fgrad(ii,jj),w)+s(ii,jj,w);
        end;
    end;  
end;




