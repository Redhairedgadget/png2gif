import os
from os import path
from png2gif_script import Gif
SCRIPT_FOLDER = path.dirname(path.realpath(__file__))
import sys
import numpy as np
sys.path.append(SCRIPT_FOLDER)


import wx
import imageio
import PIL

# TODO: make 100% by default for scale


class png2gifMainWindow(wx.Frame):
    def __init__(self, parent, title):

        self.DEBUG = False

        self.dirname = ''
        wx.Frame.__init__(self, parent, title="Welcome to png2gif!", size=(600, 500))
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        #wx.TextCtrl(self, pos=(150, 0), size=(140,-1))

        self.editNameField = wx.TextCtrl(self, pos=(200, 10), size=(140,-1))
        self.editFactorField = wx.TextCtrl(self, pos=(200, 40), size=(140,-1))
        self.editFpsField = wx.TextCtrl(self,   pos=(200, 70), size=(140,-1))
        self.editLoopField = wx.TextCtrl(self, pos=(200, 100), size=(140,-1))

        self.Bind(wx.EVT_TEXT, self.NameFieldListener, self.editNameField)
        self.Bind(wx.EVT_TEXT, self.FactorListener, self.editFactorField)
        self.Bind(wx.EVT_TEXT, self.editFpsFieldListener, self.editFpsField)
        self.Bind(wx.EVT_TEXT, self.editLoopFieldListener, self.editLoopField)

        # Setting up the menu.
        fileMenu= wx.Menu()

        wx.StaticText(self, label="Amount of loops(default is 0) :", pos=(20,100))
        wx.StaticText(self, label="FPS (default is 25):", pos=(20,70))
        wx.StaticText(self, label="Scale % (default is 100):", pos=(20,40))
        wx.StaticText(self, label="Name (default is a folder name) :", pos=(20,10))
        wx.StaticText(self, label="Choose the folder :", pos=(20,190))


        # Stuff for text bar(Browse)
        self.logger = wx.TextCtrl(self, pos=(200,230), size=(310,40), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = fileMenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = fileMenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu,"&File") # Adding the "fileMenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Checkbox
        self.insure = wx.CheckBox(self, label="Do you want an inverse gif?", pos=(20,280))
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.insure)

        # Create button
        self.btnBrowse = wx.Button(self, label="Browse...", pos =(20, 230))
        self.creatGifBtn = wx.Button(self, label="Create Gif", pos =(200, 320), size =(190, 80))

        # Set events.
        self.Bind(wx.EVT_BUTTON, self.createGif, self.creatGifBtn)
        self.Bind(wx.EVT_BUTTON, self.Browse, self.btnBrowse)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Show(True)

        self.p2g = Gif()
        if (self.DEBUG):
            self.p2g.editName = "dojn"
            self.p2g.editFactor = "100"
            self.p2g.editFps = "25"
            self.p2g.editLoop = "0"

    def NameFieldListener(self, event):
        self.p2g.editName = event.GetString()

    def FactorListener(self, event):
        self.p2g.editFactor = event.GetString()

    def editFpsFieldListener(self, event):
        self.p2g.editFps = event.GetString()

    def editLoopFieldListener(self, event):
        self.p2g.editLoop = event.GetString()

    def OnAbout(self, event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "Make your gif from a png sequence in just a couple of clicks! 2017", "About Png2Gif", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self, event):
        self.Close(True)  # Close the frame.

    def Browse(self, event):
        dialog = wx.DirDialog(None, "Choose a directory :", style=1 )
        if dialog.ShowModal() == wx.ID_OK:
            self.p2g.imagesDir = dialog.GetPath()
            self.BrowseSave(self.p2g.imagesDir)
            dialog.Destroy()

    def BrowseSave(self, chosepath):
        self.logger.Clear()
        self.logger.AppendText(" %s\n" %chosepath)

    def EvtCheckBox(self, event):
        self.p2g.isReversed = False if self.p2g.isReversed else True
        print(self.p2g.isReversed)

    def GifComplete(self):
        dial = wx.MessageDialog(self, "The gif was created!", "Congratulations!", wx.OK | wx.ICON_INFORMATION)
        dial.ShowModal()

        # Exception messages

    def ErrorNoDirectory(self):
        dlg = wx.MessageBox("Please, choose the folder!", "Error", wx.OK | wx.ICON_ERROR)


    def createGif(self, event):

        if (self.p2g.imagesDir == None):
            self.ErrorNoDirectory()

        if (self.p2g.generateGifFile()):
            self.GifComplete()


app = wx.App(False)
frame = png2gifMainWindow(None, title="Welcome to png2gif!")
app.MainLoop()
