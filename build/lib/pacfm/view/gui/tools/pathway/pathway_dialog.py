import wx
import sys

from pacfm.view.gui import ItemsPickerPanel
from pacfm.view.gui import CheckListCtrl 

ID= wx.ID_ANY



class PathwayPanel(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, id=ID,  parent=parent ) 
        #wx.Dialog.__init__(self, parent=parent)
        #self.leftpanel = wx.ScrolledWindow(splitter, -1, style=wx.SUNKEN_BORDER)
        self.SetScrollRate(20,20)
        ### controls
        self.chLevel = wx.Choice(self, id= ID)
        #self.comboPw= wx.ComboBox(self, 501, "default value", wx.DefaultPosition,
        #                        (350, -1), [], wx.CB_DROPDOWN)
        #self.checkOthers= wx.CheckBox(self, ID, "Select all (others)")
        
        # Here we dynamically add our values to the second combobox.
        #for item in sampleList:
        #    cb.Append(item, item.upper())
        
        
        #self.cPaneManual= wx.CollapsiblePane(self, label="",
        #                  style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)
        
        self.clcPw = CheckListCtrl(self)


        ### we are replacing itemspicker with a check list box
        ### becasue items picker inherits from panel, however checklistbox inherits
        ### from itemcontainer which allows us to Append objects instead of
        ### only strings as items picker forces us to represen a list as.
        
        self.clcKeyEnzymes = wx.CheckListBox(self, ID) #ItemsPickerPanel(self, [])  
        
        self.spinPanel= wx.Panel(self, -1)
        lblAss = wx.StaticText(self.spinPanel, id=ID, label= "Number of pathways")
        self.spinAss = wx.SpinCtrl(self.spinPanel, -1, "100", size= (50, 25),
                                  min= 0, max= 1000, initial=100, style= wx.ALIGN_RIGHT)


        self.cPaneAss= ""
        
        keyMethodList= ["Any (default)", "All", "Manual", "Pathway association"]
        

        self.rbs= []
        sRb= wx.BoxSizer(wx.HORIZONTAL)
        i=0
        for m in keyMethodList:
            if i == 0:
                rb = wx.RadioButton(self, -1, m, style =  wx.RB_GROUP )
                rb.SetValue(1)
            else:
                rb = wx.RadioButton(self, -1, m )
            self.rbs.append(rb)
            sRb.Add(rb, 0 , wx.LEFT, border= 10)
            i+=1
        #self.rbKeyMethod = wx.RadioBox(
        #        self, -1, "Select key enzymes", wx.DefaultPosition, wx.DefaultSize,
        #        keyMethodList, 4, wx.RA_SPECIFY_COLS
        #        )


        self.cbPwLength = wx.CheckBox(self, id=ID, label=u'Number of proteins/enzymes')
        self.cbPwSeq = wx.CheckBox(self, id=ID, label=u'Total amino acid sequence length')
        self.cbMinPath = wx.CheckBox(self, id=ID, label=u'MinPath')


        lblKeyEnzymes = wx.StaticText(self, id=ID, label= "Key enzyme selection")
        line1 = wx.StaticLine(self,style=wx.HORIZONTAL)
        
        
        lblNorm = wx.StaticText(self, id=ID, label= "Normalize by")
        line2 = wx.StaticLine(self,style=wx.HORIZONTAL)


        self.clcKeyEnzymes.Hide()
        self.spinPanel.Hide()



        #self.popControls(1, level_names)


        ### events

        #self.rbKeyMethod.Bind(wx.EVT_RADIOBOX, self.onRbKeyMethodSelected)
        

        ### sizers
        self.sizerMain= wx.BoxSizer(wx.VERTICAL)
        #sPW= wx.BoxSizer(wx.HORIZONTAL)
        #sPW.Add(self.comboPw)
        #sPW.Add(self.checkOthers)
        
        sAss= wx.BoxSizer(wx.HORIZONTAL)
        sAss.Add(lblAss)    
        sAss.Add(self.spinAss)
        
        self.spinPanel.SetSizer(sAss)
    

        self.sizerMain.Add(self.chLevel, 0, wx.TOP | wx.LEFT  , border= 10 )
        #self.sizerMain.Add(sPW, 0, wx.LEFT|wx.EXPAND  , border= 17 )
        self.sizerMain.Add((0,10))
        self.sizerMain.Add(self.clcPw,0, wx.LEFT|wx.EXPAND | wx.RIGHT  , border= 10 )

        self.sizerMain.Add((0,20))
        #self.sizerMain.Add(self.rbKeyMethod, 0, wx.LEFT| wx.TOP  , border= 15 )
        self.sizerMain.Add(lblKeyEnzymes, 0, wx.TOP | wx.LEFT | wx.RIGHT, border= 10)
        self.sizerMain.Add(line1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border= 5)
        self.sizerMain.Add(sRb, 0, wx.LEFT| wx.TOP  , border= 10 )

        self.sizerMain.Add(self.clcKeyEnzymes, 1, wx.TOP|wx.RIGHT | wx.LEFT| wx.EXPAND, border=10)
        self.sizerMain.Add(self.spinPanel, 0, wx.LEFT | wx.TOP , border= 10 )
        
        self.sizerMain.Add((0,10))
        self.sizerMain.Add(lblNorm, 0, wx.TOP | wx.LEFT | wx.RIGHT, border= 10)
        self.sizerMain.Add(line2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border= 5)
        self.sizerMain.Add(self.cbPwLength, 0, wx.TOP | wx.LEFT, border= 10)
        self.sizerMain.Add(self.cbPwSeq, 0, wx.TOP | wx.LEFT , border= 10)
        self.sizerMain.Add(self.cbMinPath, 0, wx.TOP | wx.LEFT , border= 10)

        self.sizerMain.Add((0,10))



        self.SetSizerAndFit(self.sizerMain)


class PathwayDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, "Pathway Analysis", size=(800,700))
        self.pnl = PathwayPanel(self)
        s=wx.BoxSizer(wx.VERTICAL)
        s.Add(self.pnl, 1, wx.EXPAND)

        line = wx.StaticLine(self,style=wx.HORIZONTAL)
        s.Add(line, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, border= 5)

        self.btnOK = wx.Button(self, wx.ID_OK, "OK")
        self.btnCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        sBtns= wx.BoxSizer(wx.HORIZONTAL)
        sBtns.Add(self.btnCancel)
        sBtns.Add(self.btnOK, 0, wx.LEFT, border= 10)
        s.Add(sBtns, 0, wx.ALIGN_RIGHT| wx.ALIGN_BOTTOM | wx.NORTH| wx.RIGHT| wx.TOP | wx.BOTTOM ,border=20)

        self.SetSizer(s)
        self.Layout()
        self.Centre()
#grid.SetReadOnly(5,5, True)


if __name__ == '__main__' and __package__ is None:
    import sys
    from wx.lib.mixins.inspection import InspectableApp
    app = InspectableApp(False)
    frame = PathwayDialog(None)
    frame.Show(True)
    
    
    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()


trash= """
        feature_type= "Enzymes"
        feature_list= map(str, range(50))
        level_names= ["Level %s"%i for i in range(1,5)]
        if method == "":
            self.pnlX= self.populateItemsPicker(feature_type, feature_list, level_names)
        elif method == "":
            self.pnlX= self.populateItemsPicker(feature_type, feature_list, level_names)
        elif method == "":
            self.pnlX= self.populateItemsPicker(feature_type, feature_list, level_names)



"""

