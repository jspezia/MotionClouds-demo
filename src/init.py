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
ft_0b = 11
loggabor = 12
speed = 13
V_X = 14
V_Y = 15
B_V = 16
random_cloud = 17
seed = 18
impulse = 19
do_amp = 20
threshold = 21
isoluminance = 22

def window_config(lap, info=None):
	if (lap == 'First'):
		height, width, frame = 256, 256, 32
		color, alpha, ft_0 = True, mc.alpha, True
		orientation, theta, B_theta = True, mc.theta, mc.B_theta
		radial, sf_0, ft_0b, loggabor = True, mc.sf_0, True, mc.loggabor
		speed, V_X, V_Y, B_V = True, mc.V_X, mc.V_Y, mc.B_V
		random_cloud, seed, impulse, do_amp, threshold = True, None, False, False, 1.e-3
		isoluminance, reset = False, False
	else:
		height, width, frame = info[0], info[1], info[2]
		color, alpha, ft_0 = info[3], info[4], info[5]
		orientation, theta, B_theta = info[6], info[7], info[8]
		radial, sf_0, ft_0b, loggabor = info[9], info[10], info[11], info[12]
		speed, V_X, V_Y, B_V = info[13], info[14], info[15], info[16]
		random_cloud, seed, impulse, do_amp, threshold = info[17], info[18], info[19], info[20], info[21]
		isoluminance, reset = info[22], False
	myDlg = classdlg.Dlg(title="MotionClouds-demo")
	myDlg.addText('esc to quit the programm')
	myDlg.addText('height, width and frame need to be pair and > 2')
	myDlg.addField('height', height)
	myDlg.addField('width', width)
	myDlg.addField('frame', frame)
	myDlg.addField('envelope_color', color)
	myDlg.addField('alpha', alpha)
	myDlg.addField('ft_0', ft_0)
	myDlg.addField('envelope_orientation', orientation)
	myDlg.addField('theta', theta)
	myDlg.addField('B_theta', B_theta)
	myDlg.addField('envelope_radial', radial)
	myDlg.addField('sf_0', sf_0)
	myDlg.addField('ft_0b', ft_0b)
	myDlg.addField('loggabor', loggabor)
	myDlg.addField('envelope_speed', speed)
	myDlg.addField('V_X', V_X)
	myDlg.addField('V_Y', V_Y)
	myDlg.addField('B_V', B_V)
	myDlg.addField('random_cloud', random_cloud)
	myDlg.addField('seed', seed)
	myDlg.addField('impulse', impulse)
	myDlg.addField('do_amp', do_amp)
	myDlg.addField('threshold', threshold)
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
		env_radial = mc.envelope_radial(fx, fy, ft, sf_0=info[sf_0], ft_0=ft_0_radial, loggabor=info[loggabor])
	if (info[speed] == True):
		env_speed = mc.envelope_speed(fx, fy, ft, V_X=info[V_X], V_Y=info[V_Y], B_V=info[B_V])

	env = env_color * env_orientation * env_radial * env_speed

	if (info[random_cloud] == True):
		if (info[seed] == 'None'): seed_t = None
		else: seed_t = int(info[seed])
		env = mc.random_cloud(env, seed=seed_t, impulse=info[impulse], do_amp=info[do_amp], threshold=info[threshold])

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
