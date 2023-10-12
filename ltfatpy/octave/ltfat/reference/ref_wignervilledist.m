function W=ref_wignervilledist(f,g)
%REF_WIGNERVILLEDIST Reference wigner-Ville distribution
%   Usage:  W=ref_wignervilledist(f)
%
%   REF_WIGNERVILLEDIST(f,g) computes the Wigner-Ville distribution of f and g.

% AUTHOR: Jordy van Velthoven

if ~all(length(f)==length(g))
  error('%s: f and g must have the same length.', upper(mfilename));
end;

L = length(f);
H = floor(L/2);
R = zeros(L,L);
W = zeros(L,L);

% Compute the analytic representation of f
if (nargin == 1)
  if isreal(f)
   z = fft(f);
   z(2:L-H) = 2*z(2:L-H);
   z(H+2:L) = 0;
   z1 = ifft(z);
   z2 = z1;
  else
   z1 = f;
   z2 = z1;
  end
elseif (nargin == 2)
  if isreal(f) || isreal(g)
   z1 = fft(f);
   z1(2:L-H) = 2*z1(2:L-H);
   z1(H+2:L) = 0;
   z1 = ifft(z1);
   z2 = fft(g);
   z2(2:L-H) = 2*z2(2:L-H);
   z2(H+2:L) = 0;
   z2 = ifft(z2);
  else
    z1 = f;
    z2 = g;
  end
end

% Compute instantaneous autocorrelation matrix R
for l = 0 : L-1;
  for m = -min([L-l, l, round(L/2)-1]) : min([L-l, l, round(L/2)-1]);
    R(mod(L+m,L)+1, l+1) =  z1(mod(l+m, L)+1).*conj(z2(mod(l-m, L)+1));
  end
end

% Compute the Wigner-Ville distribution
for hh=0:L-1
  for ii=0:L-1
    for jj = 0:L-1
      W(hh+1, ii+1) = W(hh+1, ii+1) + R(jj+1, ii+1) .* exp(-2*pi*i*hh*jj/L);
    end
  end
end
