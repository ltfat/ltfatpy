import numpy as numpy
#import oct2py as oct
import os, sys

bp = os.path.dirname(__file__)
target_path = os.path.join(bp, '..')
print(target_path)
sys.path.insert(0,target_path)
from ltfatpy import ltfat

Lr=[24,16,144,108,144,24,135,35,77,20]
ar=[ 4, 4,  9,  9, 12, 6,  9, 5, 7, 1]
Mr=[ 6, 8, 16, 12, 24, 8,  9, 7,11,20]

LTFAT_TEST_TYPE = 'double'

for rtype in range(2):
      
    if rtype==1:
      rname='REAL'	
      g=ltfat.tester_rand(Lr,1)
    else:
      rname='CMPLX'
      g=ltfat.tester_crand(Lr,1)
 
 #   global LTFAT_TEST_TYPE;
    if ltfat.strcmpi(LTFAT_TEST_TYPE,'single'):
        C = ltfat.gabframebounds(g,ar,Mr)
        while C>1e3:
           #  oct.warning(oct.sprintf(['The frame is too badly conditioned '...
           #                   'for single precision. Cond. num. %d. '...
           #                   ' Trying again.'],C));
                         
                         if rtype==1:
                             rname='REAL '
                             g=ltfat.tester_rand(Lr,1)
                         else:
                             rname='CMPLX'
                             g=ltfat.tester_crand(Lr,1)

                         C = ltfat.gabframebounds(g,ar,M)
                         print(C)