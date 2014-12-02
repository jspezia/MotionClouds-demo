import libpy as lb
import numpy as np
import sys, os
import MotionClouds as mc

h = 128
w = 128
f = 32

fx, fy, ft = mc.get_grids(h, w, f)
#color = mc.envelope_color(fx, fy, ft)
#env = color * mc.envelope_speed(fx, fy, ft)
env = mc.envelope_gabor(fx, fy, ft, B_theta=2)
env = mc.random_cloud(env, seed=12)
env = mc.rectif(env, contrast=1.)
tomat = env
env = env * 255
stimulus = np.zeros([h, w, f, 3]).astype(int)

stimulus[:, :, :, 0] = env
stimulus[:, :, :, 1] = 255 - env
stimulus[:, :, :, 2] = 127

lb.show_stimulus(stimulus, 'stimulus', exit=False)
lb.saveMovie(stimulus, 'movietest', vext='.gif')
