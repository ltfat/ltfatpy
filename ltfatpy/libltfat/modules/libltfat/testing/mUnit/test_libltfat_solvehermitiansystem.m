function test_failed = test_libltfat_solvehermitiansystem(varargin)
test_failed = 0;

fprintf(' ===============  %s ================ \n',upper(mfilename));

definput.flags.complexity={'double','single'};
[flags]=ltfatarghelper({},definput,varargin);
dataPtr = [flags.complexity, 'Ptr'];

Larr =    [301, 9,11,110, 9, 8, 11, 10, 301];


    complexstring = 'complex'; 
    funname_init = makelibraryname('hermsystemsolver_init',flags.complexity,1);
    funname_execute = makelibraryname('hermsystemsolver_execute',flags.complexity,1);
    funname_done = makelibraryname('hermsystemsolver_done',flags.complexity,1);
   
    p = libpointer();
    calllib('libltfat',funname_init,max(Larr),p); 
    
for Lidx = 1:numel(Larr)
    L = Larr(Lidx);
    

    
     

    D = randn(L,flags.complexity)+1i*randn(L,flags.complexity);
   % D(:,1) = D(:,end);
    A = D*D';
    Amessedup = A;
    for n=2:size(A,2)
        for m=1:n-1
              Amessedup(m,n) = randn(1);
        end
    end
    Aint = complex2interleaved(Amessedup);
    APtr = libpointer(dataPtr,Aint);

    b = randn(L,1,flags.complexity)+ 1i*randn(L,1,flags.complexity);
    bint = complex2interleaved(b);
    bPtr = libpointer(dataPtr,bint);
    
    tic
    trueres = A\b;
    toc
           
    tic
    status = calllib('libltfat',funname_execute,p,APtr,L,bPtr);
    toc

    
    res = norm(trueres - interleaved2complex(bPtr.Value));

    [test_failed,fail]=ltfatdiditfail(res+status,test_failed,1e-8);
    fprintf(['SOLVEHERM L:%3i, %s %s %s %s\n'],L,flags.complexity,complexstring,ltfatstatusstring(status),fail);

end

    calllib('libltfat',funname_done,p);

