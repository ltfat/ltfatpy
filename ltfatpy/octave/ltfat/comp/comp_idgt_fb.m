function [f]=comp_idgt_fb(coef,g,L,a,M)
%COMP_IDGT_FB  Filter bank IDGT.
%   Usage:  f=comp_idgt_fb(c,g,L,a,M);
%       
%   This is a computational routine. Do not call it directly.
%
%   Input must be in the M x N*W format, so the N and W dimension is
%   combined.
%
%   See also: idgt

%   AUTHOR : Peter L. Søndergaard.
%   TESTING: OK
%   REFERENCE: OK

% Calculate the parameters that was not specified.
N=L/a;
b=L/M;

%W=prod(size(coef))/(M*N);
W = size(coef,3);

N=L/a;
b=L/M;

gl=length(g);
glh=floor(gl/2);  % gl-half

%if ndims(coef)>2
%  error('Reshape to M x N*W');
%end;

% Apply ifft to the coefficients.
coef=ifft(coef)*sqrt(M);

%coef=reshape(coef,M,N,W);

% The fftshift actually makes some things easier.
g=fftshift(g);

f=zeros(L,W,assert_classname(coef,g));

ff=zeros(gl,1,assert_classname(coef,g));

% Rotate the coefficients, duplicate them until they have same
% length as g, and multiply by g.
% FIXME Kill the loop over w by bsxfun
for w=1:W
  
    
  % ----- Handle the first boundary using periodic boundary conditions. ---
  for n=0:ceil(glh/a)-1
    delay=mod(-n*a+glh,M);
    for ii=0:gl/M-1
      for m=0:delay-1
        ff(m+ii*M+1)=coef(M-delay+m+1,n+1,w)*g(m+ii*M+1);
      end;
      for m=0:M-delay-1
        ff(m+ii*M+delay+1)=coef(m+1,n+1,w)*g(m+delay+ii*M+1);
      end;
    end;
    
    sp=mod(n*a-glh,L);
    ep=mod(n*a-glh+gl-1,L);
    
    % Add the ff vector to f at position sp.
    for ii=0:L-sp-1
      f(sp+ii+1,w)=f(sp+ii+1,w)+ff(1+ii);
    end;
    for ii=0:ep
      f(1+ii,w)=f(1+ii,w)+ff(L-sp+1+ii); 
    end;
  end;

  % ----- Handle the middle case. ---------------------
  for n=ceil(glh/a):floor((L-ceil(gl/2))/a)
    delay=mod(-n*a+glh,M);    
    for ii=0:gl/M-1
      for m=0:delay-1
        ff(m+ii*M+1)=coef(M-delay+m+1,n+1,w)*g(m+ii*M+1);
      end;
      for m=0:M-delay-1
        ff(m+ii*M+delay+1)=coef(m+1,n+1,w)*g(m+delay+ii*M+1);
      end;
    end;

    sp=mod(n*a-glh,L);
    ep=mod(n*a-glh+gl-1,L);
  
    % Add the ff vector to f at position sp.
    for ii=0:ep-sp
      f(ii+sp+1,w)=f(ii+sp+1,w)+ff(ii+1);
    end;
  end;

  % ----- Handle the last boundary using periodic boundary conditions. ---
  % This n is one-indexed, to avoid to many +1
  for n=floor((L-ceil(gl/2))/a)+1:N-1
    delay=mod(-n*a+glh,M);
    for ii=0:gl/M-1
      for m=0:delay-1
        ff(m+ii*M+1)=coef(M-delay+m+1,n+1,w)*g(m+ii*M+1);
      end;
      for m=0:M-delay-1
        ff(m+ii*M+delay+1)=coef(m+1,n+1,w)*g(m+delay+ii*M+1);
      end;
    end;
    
    sp=mod(n*a-glh,L);
    ep=mod(n*a-glh+gl-1,L);
    
    % Add the ff vector to f at position sp.
    for ii=0:L-sp-1
      f(sp+ii+1,w)=f(sp+ii+1,w)+ff(1+ii);
    end;
    for ii=0:ep
      f(1+ii,w)=f(1+ii,w)+ff(L-sp+1+ii); 
    end;
  end;
end;

% Scale correctly.
f=sqrt(M)*f;






