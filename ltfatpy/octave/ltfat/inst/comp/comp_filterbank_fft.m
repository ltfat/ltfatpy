function c=comp_filterbank_fft(F,G,a)
%-*- texinfo -*-
%@deftypefn {Function} comp_filterbank_fft
%@verbatim
%COMP_FILTERBANK_FFT  Compute filtering in FD
%
%   does the same as comp_filterbank_fftbl, but for
%   filters that are not bandlimited in the frequency domain
%@end verbatim
%@strong{Url}: @url{http://ltfat.github.io/doc/comp/comp_filterbank_fft.html}
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

M = numel(G);
[L,W] = size(F);
c = cell(M,1);
N = L./a;

for m=1:M
    c{m}=zeros(N(m),W,assert_classname(F,G{m}));
    for w=1:W
        c{m}(:,w)=ifft(sum(reshape(F(:,w).*G{m},N(m),a(m)),2))/a(m);
    end;
end

