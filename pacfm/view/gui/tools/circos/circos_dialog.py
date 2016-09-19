import wx

from plots_panel import PlotsPanel
from links_panel import LinksPanel
from highlights_panel import HighlightsPanel


ID= wx.ID_ANY




class CircosDialog(wx.Dialog):
    def __init__(self, parent, biodb= None, plots=None, links=None, highlights= None):
        
        wx.Dialog.__init__(self, parent, ID, size= (800,700), title= "PACFM Options")

        self.nb= wx.Notebook(self,-1,  style= wx.BK_DEFAULT)
                                 #wx.BK_TOP 
                                 #wx.BK_BOTTOM
                                 #wx.BK_LEFT
                                 #wx.BK_RIGHT
                                 # | wx.NB_MULTILINE
        
        self.plotType= PlotsPanel(self.nb, biodb, plots)     
        self.links= LinksPanel(self.nb, biodb, links)
        self.highlights= HighlightsPanel(self.nb, biodb, highlights)
        

        self.nb.AddPage(self.plotType, 'Plots')
        self.nb.AddPage(self.links, 'Links')
        self.nb.AddPage(self.highlights,'Highlights')
   

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        sBtns= wx.BoxSizer(wx.HORIZONTAL)
        sBtns.Add(self.btnCancel)
        sBtns.Add(self.btnOK, 0, wx.LEFT, border= 10)

        #self.SetSizer(s)


        #self.btnCancel = wx.Button(id=wx.ID_CANCEL, label=u'Cancel', name=u'btnCancel', parent=self)


        #self.btnOk = wx.Button(id=wx.ID_OK,parent=self, label=u'OK', name=u'btnOk')

        #sizerBtm=wx.BoxSizer(wx.HORIZONTAL)
        
        
        #sizerBtm.Add(self.btnCancel)
        #sizerBtm.Add((10,0))
        #sizerBtm.Add(self.btnOk)



        sizerMain=wx.BoxSizer(wx.VERTICAL)
        sizerMain.Add(self.nb, 1,  wx.EXPAND)
        #sizerMain.Add(sizerBtm, 0 ,wx.ALL| wx.ALIGN_RIGHT , border=5)
        sizerMain.Add(sBtns, 0, wx.ALIGN_RIGHT| wx.ALIGN_BOTTOM | wx.TOP| wx.RIGHT | wx.BOTTOM ,border=20)
    
        self.SetSizer(sizerMain)
        self.Layout()
        self.Centre()



                             
