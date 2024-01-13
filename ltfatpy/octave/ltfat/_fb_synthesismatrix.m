function G = _fb_synthesismatrix(g, a, L)

  M = length(a);
  F = frame('filterbank',g,a, M);
  G=frsynmatrix(F,L);

 end
