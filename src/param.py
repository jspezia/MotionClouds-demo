import numpy as np

DEBUG = False
if DEBUG:
    size = 5
    size_T = 5
    figsize = (400, 400)
else:
    size = 7
    size_T = 7
    figsize = (600, 600)

N_X = 2**size
N_Y = N_X
N_frame = 2**size_T

alpha = 0.0
ft_0 = np.inf
sf_0 = 0.15
B_sf = 0.1
V_X = 1.
V_Y = 0.
B_V = .2
theta = 0.
B_theta = np.pi/32.
loggabor = True
