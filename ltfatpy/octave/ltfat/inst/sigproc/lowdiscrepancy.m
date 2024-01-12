function delays = lowdiscrepancy(name, varargin)
%-*- texinfo -*-
%@deftypefn {Function} lowdiscrepancy
%@verbatim
%LOWDISCREPANCY  Returns a low discrepancy sequence
%   Usage: delays=lowdiscrepancy(name)
%
%   Input parameters:
%         name  : Name of the low discrepancy sequence
%   Output parameters:
%         delays     : Anonymous function specifying the sequence
%
%   LOWDISCREPANCY(name) returns a low discrepancy sequence for the usage
%   as a delay generating function in conjunction with waveletfilters.
%   Currently, a kronecker sequence and a digital net are implemented.
%
%
%   Authors: Nicki Holighaus, Clara Hollomey, Guenther Koliander
%@end verbatim
%@strong{Url}: @url{http://ltfat.github.io/doc/sigproc/lowdiscrepancy.html}
%@seealso{waveletfilters}
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

definput.keyvals.s = ceil(log2(4096));

[~, kv] = ltfatarghelper({}, definput, varargin);


switch name
    case 'digital'
        input = (0:2^kv.s-1);
        bin_vecs = [fliplr(dec2binary(input))';zeros(1,2^kv.s)];

        temp = tril(ones(kv.s+1));
        temp(3:end,1:end-2) = temp(3:end,1:end-2) - temp(1:end-2,1:end-2);
        C1 = temp;

        out = mod(C1*bin_vecs,2);
        ord = zeros(1,size(out,2));
        for kk = 1:size(out,1)
            ord = ord + out(kk,:).*2^(-kk);
        end    
        delays = @(n,a) a*(mod(ord(n+1)+.5,1)-.5);
    
    case 'kronecker'
        alpha = 1-2/(1+sqrt(5)); % 1-1/(goldenratio) delay sequence
        delays = @(n,a) a*(mod(n*alpha+.5,1)-.5);
    otherwise
        disp('Sequence not yet implemented.');
end
end

function out = dec2binary(int)
    ll = floor(log2(max(int)))+1;
    out = rem(floor(int(:)*pow2(1-ll:0)),2);
end
