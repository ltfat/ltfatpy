function [o1,o2]=gabdualnorm(g,gamma,a,M,varargin);
%GABDUALNORM  Measure of how close a window is to being a dual window
%   Usage:  dn=gabdualnorm(g,gamma,a,M);
%           dn=gabdualnorm(g,gamma,a,M,L);
%           dn=gabdualnorm(g,gamma,a,M,'lt',lt);
%           [scal,res]=gabdualnorm(...);
%
%   Input parameters:
%         gamma  : input window..
%         g      : window function.
%         a      : Length of time shift.
%         M      : Number of modulations.
%         L      : Length of transform to consider
%   Output parameters:
%         dn     : dual norm.
%         scal   : Scaling factor
%         res    : Residual
%
%   `gabdualnorm(g,gamma,a,M)` calculates how close *gamma* is to being a
%   dual window of the Gabor frame with window *g* and parameters *a* and *M*.
%
%   The windows *g* and *gamma* may be vectors of numerical values, text strings
%   or cell arrays. See the help of |gabwin| for more details.
%
%   `[scal,res]=gabdualnorm(...)` computes two entities: *scal* determines
%   if the windows are scaled correctly, it must be 1 for the windows to be
%   dual. Note that the scaling factor *scal* is expected to be real for 
%   real-valued window pairs *g* and *gamma*, but may be complex for general 
%   windows. *res* is close to zero if the windows (scaled correctly) are dual
%   windows.
%
%   `gabdualnorm(g,gamma,a,M,L)` does the same, but considers a transform
%   length of *L*.
%
%   `gabdualnorm(g,gamma,a,M,'lt',lt)` does the same for a non-separable
%   lattice specified by *lt*. Please see the help of |matrix2latticetype|
%   for a precise description of the parameter *lt*.
%
%   `gabdualnorm` can be used to get the maximum relative reconstruction
%   error when using the two specified windows. Consider the following code
%   for some signal *f*, windows *g*, *gamma*, parameters *a* and *M* and 
%   transform-length *L* (See help on |dgt| on how to obtain *L*)::
%
%     fr=idgt(dgt(f,g,a,M),gamma,a); 
%     er=norm(f-fr)/norm(f);
%     eest=gabdualnorm(g,gamma,a,M,L);
%
%   Then  $er<eest$ for all possible input signals *f*.
%
%   To get a similar estimate for an almost tight window *gt*, simply use ::
%  
%     eest=gabdualnorm(gt,gt,a,M,L);
%
%   See also:  gabframebounds, dgt

  
%% ---------- Assert correct input.

if nargin<4
  error('%s: Too few input parameters.',upper(mfilename));
end;

definput.keyvals.L=[];
definput.keyvals.lt=[0 1];
[flags,kv,L]=ltfatarghelper({'L'},definput,varargin);

%% ------ step 2: Verify a, M and L
if isempty(L)
    % Minimum transform length by default.
    Ls=1;
    
    % Use the window lengths, if any of them are numerical
    if isnumeric(g)
        Ls=max(length(g),Ls);
    end;

    if isnumeric(gamma)
        Ls=max(length(gamma),Ls);
    end;

    % ----- step 2b : Verify a, M and get L from the window length ----------
    L=dgtlength(Ls,a,M,kv.lt);

else

    % ----- step 2a : Verify a, M and get L

    Luser=dgtlength(L,a,M,kv.lt);
    if Luser~=L
        error(['%s: Incorrect transform length L=%i specified. Next valid length ' ...
               'is L=%i. See the help of DGTLENGTH for the requirements.'],...
              upper(mfilename),L,Luser)
    end;

end;

[g,    info_g]     = gabwin(g,    a,M,L,kv.lt,'callfun',upper(mfilename));
[gamma,info_gamma] = gabwin(gamma,a,M,L,kv.lt,'callfun',upper(mfilename));
 
% gamma must have the correct length, otherwise dgt will zero-extend it
% incorrectly using postpad instead of fir2long
gamma=fir2long(gamma,L);
g    =fir2long(g,L);

% Handle the Riesz basis (dual lattice) case.
if a>M

  % Calculate the right-hand side of the Wexler-Raz equations.
  rhs=dgt(gamma,g,a,M,L,'lt',kv.lt);
  scalconst=1;
  
else
  
  % Calculate the right-hand side of the Wexler-Raz equations.
  rhs=dgt(gamma,g,M,a,L,'lt',kv.lt);
  
  scalconst=a/M;
  
end;

if nargout<2
  % Subtract from the first element to make it zero, if the windows are
  % dual.
  rhs(1)=rhs(1)-scalconst;

  o1=norm(rhs(:),1);
else
  % Scale the first element to make it one, if the windows are dual.
  o1=rhs(1)/scalconst;
  if ( norm(imag(g)) + norm(imag(gamma)) )== 0
     o1 = real(o1); 
  end 
  o2=norm(rhs(2:end),1);
end;
