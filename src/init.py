### init.py ###

import classdlg
import MotionClouds as mc

height = 0
width = 1
frame = 2
color = 3
alpha = 4
ft_0 = 5
orientation = 6
theta = 7
B_theta = 8
radial = 9
sf_0 = 10
B_sf = 11
ft_0b = 12
loggabor = 13
speed = 14
V_X = 15
V_Y = 16
B_V = 17
random_cloud = 18
seed = 19
impulse = 20
do_amp = 21
isoluminance = 22

def window_config(lap, info=None):
	if (lap == 'First'):
		height, width, frame = 256, 256, 32
		color, alpha, ft_0 = True, mc.alpha, True
		orientation, theta, B_theta = True, mc.theta, mc.B_theta
		radial, sf_0, B_sf, ft_0b, loggabor = True, mc.sf_0, mc.B_sf, True, mc.loggabor
		speed, V_X, V_Y, B_V = True, mc.V_X, mc.V_Y, mc.B_V
		random_cloud, seed, impulse, do_amp= True, None, False, False
		isoluminance, reset = False, False
	else:
		height, width, frame = info[0], info[1], info[2]
		color, alpha, ft_0 = info[3], info[4], info[5]
		orientation, theta, B_theta = info[6], info[7], info[8]
		radial, sf_0, B_sf, ft_0b, loggabor = info[9], info[10], info[11], info[12], info[13]
		speed, V_X, V_Y, B_V = info[14], info[15], info[16], info[17]
		random_cloud, seed, impulse, do_amp = info[18], info[19], info[20], info[21]
		isoluminance, reset = info[22], False
	myDlg = classdlg.Dlg(title="MotionClouds-demo")
	myDlg.addText('esc to quit the programm')
	myDlg.addText('height, width and frame need to be pair and > 2')
	myDlg.addField('height', height)
	myDlg.addField('width', width)
	myDlg.addField('frame', frame)
	myDlg.addField('envelope_color', color)
	myDlg.addField('alpha (0 = white, 1 = pink, 2 = red)', alpha)
	myDlg.addField('ft_0 (spatiotemporal scaling factor)', ft_0)
	myDlg.addField('envelope_orientation (von-Mises distribution)', orientation)
	myDlg.addField('theta (orientation of the Gabor kernel)', theta)
	myDlg.addField('B_theta (orientation bandwidth)', B_theta)
	myDlg.addField('envelope_radial (sf = spacial frequency)', radial)
	myDlg.addField('sf_0 (sf relative to the sampling frequency)', sf_0)
	myDlg.addField('B_sf (sf bandwidth)', B_sf)
	myDlg.addField('ft_0', ft_0b)
	myDlg.addField('loggabor (log-Gabor kernel or traditional gabor)', loggabor)
	myDlg.addField('envelope_speed (V_X=1 == displacement of 1/height)', speed)
	myDlg.addField('V_X (> 0 is downward)', V_X)
	myDlg.addField('V_Y (> 0 is rightward)', V_Y)
	myDlg.addField('B_V (speed bandwidth)', B_V)
	myDlg.addField('random_cloud (create a random phase spectrum)', random_cloud)
	myDlg.addField('use a specific seed to specify the RNG\'s seed', seed)
	myDlg.addField('test the impulse response of the kernel', impulse)
	myDlg.addField('test the effect of randomizing amplitudes', do_amp)
	myDlg.addField('isoluminance', isoluminance)
	myDlg.addText('')
	myDlg.addField('reset parameters?', reset)
	myDlg.show()
	if (myDlg.OK):
		info = myDlg.data
	else:
		import sys
		print 'user cancelled'
		sys.exit()
	if (info[23]): info = window_config('First')
	return(info)


def control(info):
	ok = True
	if (info[color] + info[orientation] + info[radial] + info[speed] == 0):
		ok = False
	if (info[height] < 2 or info[width] < 2 or info[frame] < 2):
		ok = False
	if (info[height] % 2 != 0 or info[width] % 2 != 0 or info[frame] % 2 != 0):
		ok = False
	if (ok != True):
		import sys
		print 'very funny...'
		sys.exit()


def create_stimulus(info, return_env=False):
	control(info)

	import numpy as np

	fx, fy, ft = mc.get_grids(info[height], info[width], info[frame])

	env_color = 1
	env_orientation = 1
	env_radial = 1
	env_speed = 1
	if (info[color] == True):
		if (info[ft_0] == True): ft_0_color = np.inf
		else: ft_0_color = 1
		env_color = mc.envelope_color(fx, fy, ft, alpha=info[alpha], ft_0=ft_0_color)
	if (info[orientation] == True):
		env_orientation = mc.envelope_orientation(fx, fy, ft, theta=info[theta], B_theta=info[B_theta])
	if (info[radial] == True):
		if (info[ft_0b] == True): ft_0_radial = np.inf
		else: ft_0_radial = 1
		env_radial = mc.envelope_radial(fx, fy, ft, sf_0=info[sf_0], B_sf=info[B_sf], ft_0=ft_0_radial, loggabor=info[loggabor])
	if (info[speed] == True):
		env_speed = mc.envelope_speed(fx, fy, ft, V_X=info[V_X], V_Y=info[V_Y], B_V=info[B_V])

	env = env_color * env_orientation * env_radial * env_speed
	if (info[random_cloud] == True):
		if (info[seed] == 'None'): seed_t = None
		else: seed_t = int(info[seed])
		env = mc.random_cloud(env, seed=seed_t, impulse=info[impulse], do_amp=info[do_amp])
	env = mc.rectif(env, contrast=1.)
	env = env * 255
	if (return_env == True):
		return (env)
	stimulus = np.zeros([info[height], info[width], info[frame], 3]).astype(int)

	if (info[isoluminance] == True):
		stimulus[:, :, :, 0] = env
		stimulus[:, :, :, 1] = 255 - env
		stimulus[:, :, :, 2] = 127
	else:
		for i in range(3):
			stimulus[:, :, :, i] = env[:, :, :]

	return(stimulus)
