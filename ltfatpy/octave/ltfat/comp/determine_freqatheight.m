function freq = determine_freqatheight(fun,peakpos,height,direction)
%FREQATHEIGHT the position at which the function fun [f(x = freq)] decreases 
%below the specified height 'height';
%
%   Usage: freq = determine_freqatheight(fun,peakpos,height,direction)
%
%   Input parameters:
%         fun  : Function handle
%         peakpos  : peak position on the abscissa
%         height : threshold (ordinate value); designates the ordinate value
%                   below which the algorithm terminates 
%         direction : the direction in which the search is performed; *0* 
%                     specifies a search in the direction of decreasing indices, 
%                     starting from `peakpos`. *1* specifies a search towards 
%                     increasing indices.
%
%   Output parameters:
%         freq     : the value on the abscissa where fun decreases below height
%
% For a function `fun` monotonously decreasing around a unique peak `peakpos` or 
% plateau, this function determines the position at which `fun` decreases below 
% the specified height `height`. The search is performed in the direction indicated
% by `direction`: *0* specifies a search in the direction of decreasing indices, 
% starting from `peakpos`. *1* specifies a search towards increasing indices.
%
%
% AUTHORS: Zdenek Prusa, Nicki Holighaus, Guenther Koliander, Clara Hollomey
 
freq = peakpos;
height_current = fun(peakpos);
if height_current <= height
    return;
end

if direction 
    freq_right = freq;
    while height_current > height
        freq_right = freq_right + 1/4;
        height_current = fun(freq_right);
    end
    freq_current = freq_right;
    kk = 3;
    while abs(height_current - height) > 1e-6 && kk < 100
        freq_current = freq_right - 2^(-kk);
        height_current = fun(freq_current);
        if height_current < height
            freq_right = freq_current;
        end
        kk = kk+1;
    end
else
    freq_left = freq;
    while height_current > height
        freq_left = freq_left - 1/4;
        height_current = fun(freq_left);
    end
    freq_current = freq_left;
    kk = 3;
    while abs(height_current - height) > 1e-6 && kk < 100
        freq_current = freq_left + 2^(-kk);
        height_current = fun(freq_current);
        if height_current < height
            freq_left = freq_current;
        end
        kk = kk+1;
    end
end

freq = freq_current;
