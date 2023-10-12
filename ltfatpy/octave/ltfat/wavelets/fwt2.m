function c = fwt2(f,w,J,varargin)
%FWT2   Fast Wavelet Transform 2D
%   Usage:  c = fwt2(f,w,J);
%           c = fwt2(f,w,J,...);
%
%   Input parameters:
%         f     : Input data.
%         w     : Wavelet filter bank definition.
%         J     : Number of filter bank iterations.
%
%   Output parameters:
%         c      : Coefficients stored in a matrix.
%
%   `c=fwt2(f,w,J)` returns wavelet coefficients *c* of the input matrix *f*
%   using *J* iterations of the basic wavelet filter bank defined by *w*.
%   Please see |fwt| for description of *w* and *J*.
%
%   `fwt2` supports just the non-expansive boundary condition 'per' and
%   critically subsampled filter banks in order to be able to pack the
%   coefficients in a matrix. Also the *J* is limited to some maximum value
%   for the same reason.
%
%   Additional flags make it possible to specify how the algorithm
%   should subdivide the matrix:
%
%      'standard'  
%         Standard behaviour of the JPEG 2000 standard.
%         This is the default.
%
%      'tensor'
%         This corresponds to doing a full |fwt| along each dimension of
%         the matrix.
%
%   Examples:
%   ---------
%
%   Some simple example of calling the |fwt2| function, compare with the
%   |cameraman| image. Only the 70 dB largest coefficients are shown, to
%   make the structures more visible.
%
%   The first example uses the standard layout:::
%
%     c = fwt2(cameraman,'db8',4);
%     imagesc(dynlimit(20*log10(abs(c)),70));
%     axis('image'); colormap(gray);
%
%   The second example uses the tensor product layout:::
%
%     c = fwt2(cameraman,'db8',4,'tensor');
%     imagesc(dynlimit(20*log10(abs(c)),70));
%     axis('image'); colormap(gray);
%
%   See also: ifwt2, fwtinit
%
%   Demos: demo_imagecompression
%
%   References: ma98

% AUTHOR: Zdenek Prusa


if nargin<3
  error('%s: Too few input parameters.',upper(mfilename));
end;

complainif_notposint(J,'J');

[M,N]=size(f);
if(M==1||N==1)
   error('%s: The input data is vector.',upper(mfilename));
end

% Initialize the wavelet filters structure
w = fwtinit(w);

if(~all(w.a==length(w.h)))
   error('%s: Non-critically subsampled filter banks not supported.',...
         upper(mfilename));
end


%Do not allow single wavelet coefficient at two consecutive levels
if(any(w.a(1)^J>size(f)))
   error(['%s: %d-level decomposition of the input is not possible. ',...
          'Maximum J is %d.'],...
          upper(mfilename),J,floor(log(min(size(f)))/log(w.a(1))));
end

%% ----- step 0 : Check inputs -------
definput.import = {'fwt2'};
[flags,kv]=ltfatarghelper({},definput,varargin);
nFilts = numel(w.h);

Lcrows = fwtclength(size(f,1),w,J);
Lccols = fwtclength(size(f,2),w,J);

if(flags.do_standard)
   Jstep = 1;
   c = fwt(f,w,Jstep,'dim',1,'per');
   c = fwt(c,w,Jstep,'dim',2,'per');
   for jj=1:J-1
      colRange = 1:Lcrows(end-jj*(nFilts-1)+1);
      rowRange = 1:Lccols(end-jj*(nFilts-1)+1);
      c(colRange,rowRange) = fwt(c(colRange,rowRange),w,Jstep,'dim',1,'per');
      c(colRange,rowRange) = fwt(c(colRange,rowRange),w,Jstep,'dim',2,'per');
   end
elseif(flags.do_tensor)
   c = fwt(f,w,J,'dim',1,'per');
   c = fwt(c,w,J,'dim',2,'per');
else
    error('%s: Should not get here. Bug somewhere else.',upper(mfilename));
end

