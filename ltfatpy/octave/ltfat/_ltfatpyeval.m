function _ltfatpyeval(output_file, input_file)
% _PYEVAL: Load a request from an input file, execute the request, and save
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

load("writer.mat")

in_args = strjoin(inargs, ',');
[result{1:nout}]=eval(strcat(func_name, '(', in_args, ')'));


% Save the output to a file.
try
  save('-v6', '-mat-binary', output_file, 'result', 'err');
catch ME
  result = { sentinel };
  err = ME;
  save('-v6', '-mat-binary', output_file, 'result', 'err');
end

end  % function
