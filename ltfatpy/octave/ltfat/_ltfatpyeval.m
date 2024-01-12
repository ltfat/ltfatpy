function _ltfatpyeval(output_file, input_file)
% _LTFATPYEVAL: Load a request from an input file, execute the request, and save
%         the response to the output file.
%
%   This allows you to run any Octave code. req should be a struct with the
%   following fields:
%       dname: The name of a directory to add to the runtime path before attempting to run the code.
%       func_name: The name of a function to invoke.
%       func_args: An array of arguments to send to the function.
%       nout: An int specifying how many output arguments are expected.
%       ref_indices: The indices of in the func_args that should
%         be replaced by the value represented by their name.
%       store_as: Optional name to store the return value in the base
%         workspace, instead of returning a value.
%
%   Should save a file containing the result object.
%
% Based on Max Jaderberg's web_feval and oct2pys _pyeval


sentinel = { '__no_value__' };
result = { sentinel };
err = '';


load("writer.mat");

%check if there are any strings that should be interpreted as cell arrays
variables = whos;

%pderiv = pderivs;
%disp(size(pderivs))
%clear pderivs;
%pderivs{1} = pderiv;
%pderivs{2} = pderiv;
%pderivs{3} = pderiv;
%pderivs{4} = pderiv;
%pderivs{5} = pderiv;

%pderivs = num2cell(pderivs);
for ii = 1:numel(variables)
    if ischar(variables(ii).class)
        %evaluate each char in the workspace
        variables(ii).name = eval(variables(ii).name);
        if ~isempty(variables(ii).name) && strcmp(variables(ii).name(1), '{')
            %and if it has braces at the beginning, convert it to a cell
            %array
            variables(ii).name = cellstr(variables(ii).name);
            variables(ii).name = variables(ii).name{1};
            class(variables(ii).name)
        end

    end
end

%nout
%func_name
%inargs
%fs
%variables.name

if ~exist('func_args', 'var')
  in_args = strjoin(inargs, ',');
  %strcat(func_name, '(', in_args, ')')
  [result{1:nout}]=eval(strcat(func_name, '(', in_args, ')'));
else
  %assignin('base', 'ans', sentinel);
  %for ii = 1:numel(inargs)
  %  eval(inargs{ii});
  %end
  [result{1:nout}]=eval(strcat(func_name, func_args{1}));
  %feval(func_name, func_args{1}, c=func_args{2});
end


% Save the output to a file.
try
  save('-v6', '-mat-binary', output_file, 'result', 'err');
catch ME
  %result = { sentinel };
  %err = ME;
  %result
  for ii = 1:nout
    result{ii} = "dummy";
    end
  save('-v6', '-mat-binary', output_file, 'result', 'err');
end


end  % function
