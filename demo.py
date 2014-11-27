from src import *

lap = 'First'
saveMC = False
while (True):
	if (lap == 'First'):
		info = init.window_config(lap)
		lap = 'Second'
	else: info = init.window_config(lap, info=info)
	stimulus = init.create_stimulus(info)
	pagyme.show_stimulus(stimulus, 'MotionClouds-demo')
	if (lap == 'Second'):
		info2, saveMC = save.window_save(lap)
		if (saveMC): lap = 'end_init'
	else: info2, saveMC = save.window_save(lap, info=info2)
	if (saveMC):
		save.movie(info, info2)
