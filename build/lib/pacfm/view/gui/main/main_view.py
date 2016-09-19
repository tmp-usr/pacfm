# -*- coding: utf-8 -*-
import os
import wx
from pacfm.view.gui import PacNB
from pacfm.model import file_provider


#1. fantomnb from helper


FRAMETB = False
TBFLAGS = ( wx.TB_HORIZONTAL
            #| wx.SP_BORDER
            | wx.TB_FLAT
            #| wx.TB_TEXT
            #| wx.TB_HORZ_LAYOUT
            )


title= "PACFM: Pathway Analysis with Circos for Functional Metagenomics"

def icon(name):
    
    path=  os.path.join(file_provider['launching']['icons'], "%s.png" %name.capitalize())
    #path=  "./icon_pack/png/24x24/%s.png" %name.capitalize()
    return wx.Bitmap(path, wx.BITMAP_TYPE_ANY)


class MainView(wx.Frame):
    def __init__(self, parent):
        
        wx.Frame.__init__(self, parent, -1, title, size=(1000, 800))

        self.client = wx.Panel(self, -1)
        
        self.nb= PacNB(self.client,-1)
        
        if FRAMETB:
            self.tb = tb= self.CreateToolBar( TBFLAGS )
        else:
            self.tb = tb= wx.ToolBar(self.client, style=TBFLAGS)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(self.tb, 0, wx.EXPAND)
            sizer.Add(self.nb, 1, wx.EXPAND)
            self.client.SetSizer(sizer)

        self.menubar = wx.MenuBar()
        fileMenu= wx.Menu()
        saveMenu = wx.Menu()
        dataMenu= wx.Menu()
        plotMenu= wx.Menu()
        
        self.sRawData= dataMenu.Append(wx.ID_ANY, "Raw")
        self.sNormData=  dataMenu.Append(wx.ID_ANY, "Normalized")
        self.sRawPlot =  plotMenu.Append(wx.ID_ANY, "Raw")
        self.sNormPlot =  plotMenu.Append(wx.ID_ANY, "Normalized")
        
        saveMenu.AppendMenu(wx.ID_ANY, "Data", dataMenu)
        saveMenu.AppendMenu(wx.ID_ANY, "Plot", plotMenu)
    
        self.fItemNew= fileMenu.Append(wx.ID_NEW, "&New\tCTRL-N")
        #self.fItemOpen= fileMenu.Append(wx.ID_OPEN, "&Open\tCTRL-O")
        fileMenu.AppendSeparator()
        self.fItemSave= fileMenu.AppendMenu(wx.ID_ANY, "&Save", saveMenu)
        self.fItemExit= fileMenu.Append(wx.ID_EXIT, "Quit", "Quit the application")
        #fItemExit2= fileMenu.Append(wx.ID_ANY, "&Quit")
        
        pathwayMenu= wx.Menu()
        
        self.pItemAbbr= pathwayMenu.Append(wx.ID_ANY, "Abbreviations")
        self.pItemAss= pathwayMenu.Append(wx.ID_ANY, "Enzyme associations")
        self.pItemKey= pathwayMenu.Append(wx.ID_ANY, "Key enzymes")

        helpMenu= wx.Menu()
        self.hItemAbout= helpMenu.Append(wx.ID_ANY, "About PACFM")
        
        self.menubar.Append(fileMenu, "&File")
        self.menubar.Append(pathwayMenu, "Pathway")
        self.menubar.Append(helpMenu, "&Help")

        self.statusBar= self.CreateStatusBar()
        self.statusBar.SetStatusText('PACFM')
        
        tsize = (24,24)
        new_bmp = icon('new')
        home_bmp = icon('home')
        pathway_bmp = icon('pathway')
        circos_bmp = icon('circos')

        
        self.tb.SetToolBitmapSize(tsize)

        #self.tb.AddSimpleTool(10, new_bmp, "New", "Long help for 'New'")
        newShort="New abundance file"
        self.newID= wx.NewId()
        self.tb.AddLabelTool(self.newID, newShort, new_bmp, shortHelp=newShort, longHelp="")

        homeShort="Restart analysis"
        self.homeID= wx.NewId()
        self.tb.AddLabelTool(self.homeID, homeShort, home_bmp, shortHelp=homeShort, longHelp="")

        self.tb.AddSeparator()
        
        pathwayShort="Pathway analysis"
        self.pathwayID= wx.NewId()
        self.tb.AddLabelTool(self.pathwayID, pathwayShort, pathway_bmp, shortHelp= pathwayShort, longHelp="")

        circosShort="Plot"
        self.circosID= wx.NewId()
        self.tb.AddLabelTool(self.circosID, circosShort, circos_bmp, shortHelp=circosShort, longHelp="")


        self.tb.AddSeparator()

        ### other stuffs 
        self.tb.Realize()
        

        ### sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.client, 1, wx.EXPAND)
        

        self.SetMenuBar(self.menubar)
        self.SetSizer(sizer)
        self.Layout()
        self.Centre()
        


if __name__ == '__main__':
    #import sys
    #from wx.lib.mixins.inspection import InspectableApp
    #app = InspectableApp(False)
    app= wx.App()
    frame = MainView(None)
    frame.Show()
    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()


