import wx

class HelpDialog( wx.Dialog ) :

    """Create a very simple app frame.
    This will be completely filled with the DrawWindow().
    """
    def __init__( self, parent, help_info, title) :
       
        wx.Dialog.__init__(self, parent= parent, size= (600,500), 
                            title= title )

        self.text = wx.TextCtrl(self, -1,"",size=(200, 100), style=wx.TE_MULTILINE )
        self.setText(help_info)

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        sBtns= wx.BoxSizer(wx.HORIZONTAL)
        sBtns.Add(self.btnCancel)
        sBtns.Add(self.btnOK, 0, wx.LEFT, border= 10)

        sizer= wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text, 1, wx.EXPAND)
        sizer.Add(sBtns, 0, wx.ALIGN_RIGHT| wx.ALIGN_BOTTOM | wx.NORTH| wx.RIGHT| wx.TOP | wx.BOTTOM ,border=20)
        
        self.text.DiscardEdits() 
        self.SetSizer(sizer)
        self.Layout()

    
    def setText(self, help_info):
        lines=""
        for name, assoc_list in help_info.iteritems():
            lines += "%s: %s\n" %(name, "; ".join(assoc_list))
            lines += "--------------------------------------------\n"

        self.text.SetValue(lines)


class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Simple Grid Demo", size=(1000,900))
        a={"dfsf":["sgdf","gfg","sfgsg"], "sdf":["gfag","l","kf"],"ajga":["jgla","dkfl"]}
        b={"a":"sgdfgfgsfgsg", "b":"gfaglkfajgajgladkfl"}
        l={"1":a, "2":b}
        dlg = HelpDialog(self,a , "hamza")
        dlg.ShowModal()

if __name__ == "__main__":
    app= wx.App(None)
    frame= MyFrame(None)
    app.MainLoop()



