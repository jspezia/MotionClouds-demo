### save.py ###

import classdlg
import init
import os
import pygame
from pygame.locals import *
from pygame import surfarray

def remove_frames(tmpdir, files):
    for fname in files: os.remove(fname)
    if not(tmpdir == None): os.rmdir(tmpdir)

def saveSurface(pixels, filename):
    try:
        surf = pygame.surfarray.make_surface(pixels)
    except IndexError:
        (width, height, colours) = pixels.shape
        surf = pygame.display.set_mode((width, height))
        pygame.surfarray.blit_array(surf, pixels)
    pygame.image.save(surf, filename)

def saveFrame(stimulus, filename='exemple', figpath='movie_frame'):
    if not(os.path.isdir(figpath)): os.mkdir(figpath)
    for i in range(stimulus.shape[2]):
        filename = figpath + 'frame' + str(i) + '.jpg'
        saveSurface(stimulus[:, :, i, :], filename)

def saveMovie(stimulus, filename, vext='.webm', fps=50, verbose=False):
    import tempfile

    if verbose: verb_ = ''
    else: verb_ = ' 2>/dev/null'
    if (vext != '.webm' and vext != '.gif'):
        print 'format ' + str(vext) + ' not found'
        return
    tmpdir = tempfile.mkdtemp()
    files = []
    f = stimulus.shape[2]
    frame = 0
    for frame in range(f):
        fname = os.path.join(tmpdir, 'frame%03d.png' % frame)
        files.append(fname)
        saveSurface(stimulus[:, :, frame, :], fname)
    if (vext == '.webm'):
        options = '-f webm -pix_fmt yuv420p -vcodec libvpx -qmax 12 -g ' + str(fps) + ' -r ' + str(fps) + ' -y '
        cmd = 'ffmpeg -i '  + tmpdir + '/frame%03d.png ' + options + filename + '.webm' + verb_
    if (vext == '.gif'):
        options = '-delay 1 -loop 0 '
        cmd = 'convert '  + tmpdir + '/frame*.png  ' + options + filename + vext + verb_
    os.system(cmd)
    remove_frames(tmpdir, files)

def fileSaveDlg(initFilePath="", initFileName="",
                prompt="Select file to save",
                allowed=None):
    """
        display a interactiv window and return the path
    """

# Part of the PsychoPy library
# Copyright (C) 2014 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).

    import wx
    import os
    OK = wx.ID_OK
    if allowed==None:
        allowed = "All files (*.*)|*.*"
    try:
        dlg = wx.FileDialog(None,prompt,
                          initFilePath, initFileName, allowed, wx.SAVE)
    except:
        tmpApp = wx.PySimpleApp()
        dlg = wx.FileDialog(None,prompt,
                          initFilePath, initFileName, allowed, wx.SAVE)
    if dlg.ShowModal() == OK:
        outName = dlg.GetFilename()
        outPath = dlg.GetDirectory()
        dlg.Destroy()
        fullPath = os.path.join(outPath, outName)
    else: fullPath = None
    return fullPath

def movie(info, info2):
	info[0], info[1], info[2] = info2[0], info2[1], info2[2]
	stimulus = init.create_stimulus(info)
	filename = fileSaveDlg()
	if (filename == None): return
	if (info2[3] == True): saveMovie(stimulus, filename, vext='.webm')
	if (info2[4] == True): saveMovie(stimulus, filename, vext='.gif')
	if (info2[5] == True):
		import numpy as np
		np.save(filename, stimulus)
	if (info2[6] == True):
		from scipy.io import savemat
		savemat((filename + '.mat'), {'stimulus':stimulus})

def control2(info):
	ok = True
	if (info[0] < 2 or info[1] < 2 or info[2] < 2):
		ok = False
	if (info[0] % 2 != 0 or info[1] % 2 != 0 or info[2] % 2 != 0):
		ok = False
	if (ok != True):
		import sys
		print 'very funny...'
		sys.exit()

def window_save(lap, info=None):
	saveMC = False
	if (lap == 'Second'):
		height, width, frame = 512, 512, 128
		webm, gif, npy, mat = True, False, False, False
		not_save = False
	else:
		height, width, frame = info[0], info[1], info[2]
		webm, gif, npy, mat = info[3], info[4], info[5], info[6]
		not_save = info[7]
	myDlg = classdlg.Dlg(title="Would you like to save the last MotionCloud?")
	myDlg.addText('escap to cancel')
	myDlg.addText('new parameters')
	myDlg.addField('height', height)
	myDlg.addField('width', width)
	myDlg.addField('frame', frame)
	myDlg.addText('format video:')
	myDlg.addField('.webm', webm)
	myDlg.addField('.gif', gif)
	myDlg.addField('.npy', npy)
	myDlg.addField('.mat', mat)
	myDlg.addText('')
	myDlg.addText('')
	myDlg.addText('Do you want to use only the viewer?')
	myDlg.addField('don\'t show backup window again:', not_save)
	myDlg.show()
	if (myDlg.OK):
		info = myDlg.data
		saveMC = True
		control2(info)
	return(info, saveMC)
