function gd=ref_gabtight(g,a,M)
%-*- texinfo -*-
%@deftypefn {Function} ref_gabtight
%@verbatim
%REF_GABTIGHT   Reference GABTIGHT
%   Usage:  gd=ref_gabtight(g,a,M);
%
%   Calculate the canonical tight window by simple linear algebra
%@end verbatim
%@strong{Url}: @url{http://ltfat.github.io/doc/reference/ref_gabtight.html}
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
g = double(g);

G=frsynmatrix(frame('dgt',g,a,M),length(g));

gd=(G*G')^(-1/2)*g;


