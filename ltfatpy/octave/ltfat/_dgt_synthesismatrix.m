function G = _dgt_synthesismatrix(g, a, M, L)

    Ncoef = a/M*L;
    lt = [0 1];
    do_timeinv = 0;

    G = [];
    tmpf = zeros(Ncoef,1); tmpf(1) = 1;    
    for n = 1:Ncoef
        coef = reshape(tmpf, [a, size(tmpf,1)/a,size(tmpf,2)]);
        G(:,n) = comp_idgt(coef,g,M, lt, do_timeinv, 0); 
        tmpf = circshift(tmpf,1);
    end