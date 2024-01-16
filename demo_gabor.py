#difference between the LTFAT syntax in Octave and Python: cells
#example:
#calculate tight gabor window in Octave:
# gd=gabwin({'tight','gauss'},a,M,L)

#calculate tight gabor window in Python:
gd = ltfat.gabwin(('tight', 'gauss'), 10, 20, 100)

#note that there are many different ways cell arrays are
#used in LTFAT. Therefore, for the alpha version, it is entirely
#possible that not every combination of input parameters works.