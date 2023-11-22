import sys, os
#this path is for my debugging and depends on the virtual environment used (can be uncommented)
sys.path.append("/home/clara/Documents/clara/lib/python3.11/site-packages/")
#--------------------------------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
#this is messy, but reasonably stable and more versatile as long as there is no full package installation
os.chdir('..')
sys.path.append("/home/clara/Documents/ltfat_development_code/ltfatpy")
from ltfatpy.modules import Gabor
import numpy as np


import unittest

class TestWindows(unittest.TestCase):


    #def test_framebounds(self):
    #    g=gabor.tester_rand(Lr,1)
    #    self.assertEqual(gabor.framebounds(g, self.ar[i], self.M[i]), 'FOO')

    def test_windows(self):
        Lr=[24,16,144,108,144,24,135,35,77,20]
        ar=[ 4, 4,  9,  9, 12, 6,  9, 5, 7, 1]
        Mr=[ 6, 8, 16, 12, 24, 8,  9, 7,11,20]
        tolerance = 10e-10
        for i,L in enumerate(Lr):
            with self.subTest(i):
      
                #for j in ar:
                #    for k in Mr:
                            #g=gabor.tester_rand(L,1) 
                            g=np.random.rand(L,1)
                            gabor = Gabor(ar[i], Mr[i], g) 
                            gd=gabor.window("dual")
                            gt=gabor.window("tight")

                            ref_gd=gabor.ref_gabdual(g,ar[i],Mr[i])
                            res=gabor.norm(ref_gd-gd)
                            print(res)
                            self.assertLess(res, tolerance)

                            #self.assertAlmostEqual(first, second, decimalPlace, message)


    #def test_split(self):
    #    s = 'hello world'
    #    self.assertEqual(s.split(), ['hello', 'world'])
    #    # check that s.split fails when the separator is not a string
    #    with self.assertRaises(TypeError):
    #        s.split(2)

if __name__ == '__main__':
    unittest.main()