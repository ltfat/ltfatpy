function [g,scal] = filterbankscale(g,varargin)
%FILTERBANKSCALE Scale filters in filterbank
%   Usage:  g=filterbankscale(g,scal)
%           g=filterbankscale(g,'flag')
%           g=filterbankscale(g,L,'flag')
%           [g,scal]=filterbankscale(...)
%
%   `g=filterbankscale(g,scal)` scales each filter in *g* by multiplying it
%   with *scal*. *scal* can be either scalar or a vector of the same length
%   as *g*. The function only works with filterbanks already instantiated
%   (returned from a function with a `filter` (of `filters`) suffix or run
%   trough |filterbankwin|) such that the elements of *g* must be either structs
%   with .h or .H fields or be plain numeric vectors.
%
%   `g=filterbankscale(g,'flag')` instead normalizes each filter to have
%   unit norm defined by 'flag'. It can be any of the flags recognized by
%   |setnorm|. The  normalization is done in the time domain by default.
%   The normalization can be done in frequency by passing extra flag 'freq'.
%
%   `g=filterbankscale(g,L,'flag')` works as before, but some filters require
%   knowing *L* to be instantialized to obtain their norm. The normalization
%   will be valid for the lengh *L* only.
%
%   `[g,scal]=filterbankscale(g,...)` additionally returns a vector *scal* 
%   which contains scaling factors used.
%
%   In any case, the returned filters will be in exactly the same format as
%   the input filters.
%

%AUTHOR: Zdenek Prusa

complainif_notenoughargs(nargin,2,'FILTERBANKSCALE');

definput.import={'setnorm'};
definput.importdefaults={'norm_notset'};
definput.flags.normfreq = {'nofreq','freq'};
definput.keyvals.arg1 = [];
[flags,kv,arg1]=ltfatarghelper({'arg1'},definput,varargin);

% Try running filterbankwin without L. This should fail
% for any strange filter definitions like 'gauss','hann',{'dual',...}
try
    filterbankwin(g,1,'normal');
catch
    err = lasterror;
    if strcmp(err.identifier,'L:undefined')
        % If it blotched because of the undefined L, explain that.
        % This should capture only formats like {'dual',...} and {'gauss'}
        error(['%s: Function cannot handle g in such format. ',...
        'Consider pre-formatting the filterbank by ',...
        'calling g = FILTERBANKWIN(g,a) or ',...
        'g = FILTERBANKWIN(g,a,L) first.'],upper(mfilename));
   else
       % Otherwise just rethrow the error
       error(err.message);
   end
end


% At this point, elements of g can only be:
% struct with numeric field .h,
% struct with numeric field .H
% struct with function handle in .H
% numeric vectors

if flags.do_norm_notset
    % No flag from setnorm was set
    scal = scalardistribute(arg1,ones(size(g)));

    for ii=1:numel(g)
        if isstruct(g{ii})
            % Only work with .h or .H, any other struct field is not
            % relevant
            if isfield(g{ii},'h')
                if ~isnumeric(g{ii}.h)
                    error('%s: g{ii}.h must be numeric',upper(mfilename));
               end
               g{ii}.h = scal(ii)*g{ii}.h;
           elseif isfield(g{ii},'H')
               if isa(g{ii}.H,'function_handle')
                   g{ii}.H = @(L) scal(ii)*g{ii}.H(L);
               elseif isnumeric(g{ii}.H)
                   g{ii}.H = scal(ii)*g{ii}.H;
               else
                   error(['%s: g{ii}.H must be either numeric or a ',...
                   ' function handle'],upper(mfilename));
               end
           else
               error('%s: SENTINEL. Unrecognized filter struct format',...
               upper(mfilename));
           end
       elseif isnumeric(g{ii})
           % This is easy
           g{ii} = scal(ii)*g{ii};
       else
           error('%s: SENTINEL. Unrecognized filter format',...
           upper(mfilename));
       end
   end
else
    scal = zeros(numel(g),1);
    % setnorm flag was set
    
    L = arg1; % can be still empty
    % Run again with L specified
    [g2,~,info] = filterbankwin(g,1,L,'normal');
    
    if ~isempty(L) && L < max(info.gl)
         error('%s: One of the windows is longer than the transform length.',upper(mfilename));
    end;
    
    for ii=1:numel(g)
        if isstruct(g{ii})
            if isfield(g{ii},'h')
                if ~isnumeric(g{ii}.h)
                    error('%s: g{ii}.h must be numeric',upper(mfilename));
                end
                % Normalize either in time or in the frequency domain

                if flags.do_freq
                    complain_L(L);
                    % Get frequency response and it's norm
                    H = comp_transferfunction(g2{ii},L);
                    [~,scal(ii)] = setnorm(H,flags.norm);
                    if scal(ii) == 0, scal(ii) = 1; end
                    g{ii}.h = g{ii}.h/scal(ii);
                else
                    if isfield(g{ii},'fc') && g{ii}.fc~=0
                        complain_L(L); % L is required to do a proper modulation
                    else
                        L = numel(g2{ii}.h);
                    end
                    % Get impulse response with all the fields applied
                    tmpg = comp_filterbank_pre(g2(ii),1,L,inf);
                    [~,scal(ii)] = setnorm(tmpg{1}.h,flags.norm);
                    if scal(ii) == 0, scal(ii) = 1; end
                     g{ii}.h = g{ii}.h/scal(ii);
                end
            elseif isfield(g{ii},'H')
                if isa(g{ii}.H,'function_handle')
                    complain_L(L);
                    H = comp_transferfunction(g2{ii},L);
                    if flags.do_freq
                        [~,scal(ii)] = setnorm(H,flags.norm);
                        if scal(ii) == 0, scal(ii) = 1; end
                        g{ii}.H = @(L) g{ii}.H(L)/scal(ii);
                    else
                        [~,scal(ii)] = setnorm(ifft(H),flags.norm);
                        if scal(ii) == 0, scal(ii) = 1; end
                        g{ii}.H = @(L) g{ii}.H(L)/scal(ii);
                    end
                elseif isnumeric(g{ii}.H)
                    if ~isfield(g{ii},'L')
                        error('%s: g.H is numeric, but .L field is missing',...
                        upper(mfilename));
                    end
                    if isempty(L)
                        L = g{ii}.L;
                    else
                        if L ~= g{ii}.L
                            error('%s: L and g.L are not equal',...
                            upper(mfilename));
                        end
                    end

                    H = comp_transferfunction(g2{ii},L);
                    if flags.do_freq
                        [~,scal(ii)] = setnorm(H,flags.norm);
                        if scal(ii) == 0, scal(ii) = 1; end
                        g{ii}.H = g{ii}.H/scal(ii);
                    else
                        [~,scal(ii)] = setnorm(ifft(H),flags.norm);
                        if scal(ii) == 0, scal(ii) = 1; end
                        g{ii}.H = g{ii}.H/scal(ii);
                    end
                end
            else
                  error('%s: SENTINEL. Unrecognized filter struct format',...
                  upper(mfilename));
            end
        elseif isnumeric(g{ii})
            % This one is not so easy
            if flags.do_freq
                complain_L(L);
                % We must use g2 here
                [~, scal(ii)] = setnorm(fft(g2{ii}.h,L),flags.norm);
                if scal(ii) == 0, scal(ii) = 1; end
                g{ii} = g{ii}/scal(ii);
            else
                [g{ii}, scal(ii)] = setnorm(g{ii},flags.norm);
            end
        else
            error('%s: SENTINEL. Unrecognized filter format',...
            upper(mfilename));
        end
    end
    % Convert to a scaling factor
    scal = 1./scal;
end

function complain_L(L)

if isempty(L)
     error('%s: L must be specified',upper(mfilename));
end

complainif_notposint(L,'L',mfilename)
