import  sys
import  wx


class PacNB(wx.Notebook):
    def __init__(self, parent, id):
        wx.Notebook.__init__(self, parent, id, size=(21,21), style=
                             wx.BK_DEFAULT
                             |wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             # | wx.NB_MULTILINE
                             )
        
        win2=wx.Panel(self)
        self.AddPage(win2, 'Data')

        #win = self.makeColorPanel(wx.GREEN)
        
        self.analysisBook=wx.Notebook(win2, style= wx.NB_LEFT)#not supported on windows 
        self.pnlRawData=wx.Panel(self.analysisBook)
        self.analysisBook.AddPage(self.pnlRawData, "Raw")
                
        self.pnlNormData=wx.Panel(self.analysisBook)
        self.analysisBook.AddPage(self.pnlNormData, "Normalized")
       
        
        win=wx.Panel(self)
        self.AddPage(win, "Plot")

        self.circosBook=wx.Notebook(win, style= wx.NB_LEFT)#not supported on windows 
        self.pltRawData=wx.Panel(self.circosBook)
        self.circosBook.AddPage(self.pltRawData, "Raw")
       
        
        self.pltNormData=wx.Panel(self.circosBook)
        self.circosBook.AddPage(self.pltNormData, "Normalized")


        sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.analysisBook, 1, wx.EXPAND, 0)
        win2.SetSizer(sizer)


        sizer=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.circosBook, 1, wx.EXPAND, 0)
        win.SetSizer(sizer)



        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
        
        self.Layout()


    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        event.Skip()

    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        event.Skip()


class TestFrame(wx.Frame):
    def __init__(self, parent, log):
        wx.Frame.__init__(self, parent, -1, "Huge (virtual) Table Demo", size=(640,480))
        grid = FantomNB(self,-1)
        #grid.SetReadOnly(5,5, True)
#---------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    app = wx.App()
    frame = TestFrame(None, sys.stdout)
    frame.Show(True)
    app.MainLoop()


overview = """\

"""

