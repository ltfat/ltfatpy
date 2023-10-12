function YCbCr = rgb2jpeg(RGB)
%RGB2JPEG  Coverts from RGB format to the YCbCr format used by JPEG 
%   Usage:  YCbCr = rgb2jpeg(RGB);
% 
%   Input parameters:
%         RGB   : 3d data-cube, containing RGB information of the image
% 
%   Output parameters:
%         YCbCr : 3d data-cube, containing the YCbCr information of the
%                 image
% 
%   'rgb2jpeg(RGB)' performs a transformation of the 3d data-cube *RGB* with
%   dimensions $N \times M \times 3$, which contains information of the
%   colours "red", "green" and "blue". The output variable *YCbCr* is a 3d
%   data-cube of the same size containing information about "luminance",
%   "chrominance blue" and "chrominance red". The output will be of
%   the `uint8` type.
%
%   See `<http://en.wikipedia.org/wiki/YCbCr>`_ and
%   `<http://de.wikipedia.org/wiki/JPEG>`_.
%
%   Examples:
%   ---------
%
%   In the following example, the Lichtenstein test image is split into
%   its three components. The very first subplot is the original image:::
%
%    f=lichtenstein;
% 
%    f_jpeg=rgb2jpeg(f);
% 
%    subplot(2,2,1);
%    image(f);axis('image');
% 
%    Ymono=zeros(512,512,3,'uint8');
%    Ymono(:,:,1)=f_jpeg(:,:,1);
%    Ymono(:,:,2:3)=128;
%    fmono=jpeg2rgb(Ymono);
%    subplot(2,2,2);
%    image(fmono);axis('image');
% 
%    Cbmono=zeros(512,512,3,'uint8');
%    Cbmono(:,:,2)=f_jpeg(:,:,2);
%    Cbmono(:,:,3)=128;
%    fmono=jpeg2rgb(Cbmono);
%    subplot(2,2,3);
%    image(fmono);axis('image');
% 
%    Crmono=zeros(512,512,3,'uint8');
%    Crmono(:,:,3)=f_jpeg(:,:,3);
%    Crmono(:,:,2)=128;
%    fmono=jpeg2rgb(Crmono);
%    subplot(2,2,4);
%    image(fmono);axis('image');
%
%   See also:   jpeg2rgb
 

% AUTHOR:   Markus Faulhuber, February 2013

[s1,s2,s3] = size(RGB);
RGB = double(RGB);

if s3 ~= 3
    disp('Sorry, this routine is for RGB of dimension NxMx3 only')
    return;
end

YCbCr(:,:,1) = 0.299*RGB(:,:,1)+0.587*RGB(:,:,2)+0.114*RGB(:,:,3);
YCbCr(:,:,2) = 128-0.168736*RGB(:,:,1)-0.331264*RGB(:,:,2)+0.5*RGB(:,:,3);
YCbCr(:,:,3) = 128+0.5*RGB(:,:,1)-0.418688*RGB(:,:,2)-0.081312*RGB(:,:,3);

YCbCr = uint8(YCbCr);
