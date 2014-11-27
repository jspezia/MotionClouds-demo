### classdlg.py ###

# Part of the PsychoPy library
# Copyright (C) 2014 Jonathan Peirce
# Distributed under the terms of the GNU General Public License (GPL).

import wx
import numpy
import string, os

class Dlg(wx.Dialog):
    """A simple dialogue box. You can add text or input boxes
    (sequentially) and then retrieve the values.
    """
    def __init__(self,title='PsychoPy dialogue',
            pos=None, size=wx.DefaultSize,
            style=wx.DEFAULT_DIALOG_STYLE|wx.DIALOG_NO_PARENT,
            labelButtonOK = " OK ",
            labelButtonCancel = " Cancel "):
        style=style|wx.RESIZE_BORDER
        try:
            wx.Dialog.__init__(self, None, -1, title, pos, size, style)
        except:
            global app
            app = wx.App(False)
            wx.Dialog.__init__(self, None, -1, title, pos, size, style)
        self.inputFields = []
        self.inputFieldTypes= []
        self.inputFieldNames= []
        self.data = []
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.pos = pos
        self.labelButtonOK = labelButtonOK
        self.labelButtonCancel = labelButtonCancel
    def addText(self, text, color=''):
        textLength = wx.Size(8*len(text)+16, 25)
        myTxt = wx.StaticText(self, -1, label=text,
                                style=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL,
                                size=textLength)
        if len(color): myTxt.SetForegroundColour(color)
        self.sizer.Add(myTxt,1,wx.ALIGN_CENTER)

    def addField(self, label='', initial='', color='', tip=''):
        self.inputFieldNames.append(label)
        self.inputFieldTypes.append(type(initial))
        if type(initial)==numpy.ndarray:
            initial=initial.tolist()
        container=wx.GridSizer(cols=2, hgap=10)
        labelLength = wx.Size(9*len(label)+16, 25)
        inputLabel = wx.StaticText(self, -1, label,
                                        size=labelLength,
                                        style=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        if len(color): inputLabel.SetForegroundColour(color)
        container.Add(inputLabel, 1, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        if type(initial)==bool:
            inputBox = wx.CheckBox(self, -1)
            inputBox.SetValue(initial)
        else:
            inputLength = wx.Size(max(50, 5*len(unicode(initial))+16), 25)
            inputBox = wx.TextCtrl(self, -1, unicode(initial), size=inputLength)
        if len(color): inputBox.SetForegroundColour(color)
        if len(tip): inputBox.SetToolTip(wx.ToolTip(tip))

        container.Add(inputBox,1, wx.ALIGN_CENTER_VERTICAL)
        self.sizer.Add(container, 1, wx.ALIGN_CENTER)

        self.inputFields.append(inputBox)
        return inputBox

    def addFixedField(self,label='',value='',tip=''):
        thisField = self.addField(label,value,color='Gray',tip=tip)
        thisField.Disable()
        return thisField

    def show(self):
        buttons = wx.BoxSizer(wx.HORIZONTAL)
        OK = wx.Button(self, wx.ID_OK, self.labelButtonOK)
        OK.SetDefault()

        buttons.Add(OK)
        CANCEL = wx.Button(self, wx.ID_CANCEL, self.labelButtonCancel)
        buttons.Add(CANCEL)
        self.sizer.Add(buttons,1,flag=wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM,border=5)

        self.SetSizerAndFit(self.sizer)
        if self.pos == None:
            self.Center()
        if self.ShowModal() == wx.ID_OK:
            self.data=[]
            for n in range(len(self.inputFields)):
                thisName = self.inputFieldNames[n]
                thisVal = self.inputFields[n].GetValue()
                thisType= self.inputFieldTypes[n]
                if thisType in [tuple,list,float,int]:
                    exec("self.data.append("+thisVal+")")
                elif thisType==numpy.ndarray:
                    exec("self.data.append(numpy.array("+thisVal+"))")
                elif thisType in [str,unicode,bool]:
                    self.data.append(thisVal)
                else:
                    self.data.append(thisVal)
            self.OK=True
        else:
            self.OK=False
        self.Destroy()
