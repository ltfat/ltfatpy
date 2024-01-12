function cout=ref_col2diag(cin);
%-*- texinfo -*-
%@deftypefn {Function} ref_col2diag
%@verbatim
%REF_COL2DIAG  Compute matrix represenation from spreading symbol
%
%  This function is its own inverse.
%@end verbatim
%@strong{Url}: @url{http://ltfat.github.io/doc/reference/ref_col2diag.html}
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
  
L=size(cin,1);
cout=zeros(L);

for ii=0:L-1
  for jj=0:L-1
    cout(ii+1,jj+1)=cin(ii+1,mod(ii-jj,L)+1);
  end;
end;



