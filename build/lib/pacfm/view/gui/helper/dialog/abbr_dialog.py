import wx

class AbbrDialog( wx.Dialog ) :

    """Create a very simple app frame.
    This will be completely filled with the DrawWindow().
    """
    def __init__( self, parent, level_abbreviations) :
       
        wx.Dialog.__init__(self, parent= parent, size= (600,500), 
                            title= "Pathway Abbreviations" )

        level_names = ["Level %s" %l for l in range(1,len(level_abbreviations)+1)]
        self.level_abbreviations= level_abbreviations
        self.chLevel = wx.Choice(self, id= -1, choices= level_names)
        self.text = wx.TextCtrl(self, -1,"",size=(200, 100), style=wx.TE_MULTILINE )

        self.setText(level_abbreviations["1"])

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        ### events
        self.chLevel.Bind(wx.EVT_CHOICE, self.onLevelChanged)

        sBtns= wx.BoxSizer(wx.HORIZONTAL)
        sBtns.Add(self.btnCancel)
        sBtns.Add(self.btnOK, 0, wx.LEFT, border= 10)

        
        sizer= wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.chLevel,0, wx.ALL, border=10)
        sizer.Add(self.text, 1, wx.EXPAND)
        sizer.Add(sBtns, 0, wx.ALIGN_RIGHT| wx.ALIGN_BOTTOM | wx.NORTH| wx.RIGHT| wx.TOP | wx.BOTTOM ,border=20)
        
        self.text.DiscardEdits() 
        self.SetSizer(sizer)
        self.Layout()

    def setText(self, abbreviations):
        lines=""
        for abbr, pw_name in abbreviations.iteritems():
            lines += "%s: %s\n" %(abbr, pw_name)
        self.text.SetValue(lines)


    def onLevelChanged(self, e):
        level = e.GetSelection()+1
        abbreviations= self.level_abbreviations[str(level)]
        self.setText(abbreviations)

class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Simple Grid Demo", size=(1000,900))
        a={"dfsf":"sgdfgfgsfgsg", "sdf":"gfaglkfajgajgladkfl"}
        b={"a":"sgdfgfgsfgsg", "b":"gfaglkfajgajgladkfl"}
        l={"1":a, "2":b}
        dlg = AbbrDialog(self,l )
        dlg.ShowModal()

if __name__ == "__main__":
    app= wx.App(None)
    frame= MyFrame(None)
    app.MainLoop()



