import wx

import  wx.lib.filebrowsebutton as filebrowse


ID= wx.ID_ANY

class NewFileDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, id=ID, name='', parent=parent, size=wx.Size(600, 250), title=u'Import Abundance File')
        
        self.rbFam = wx.RadioBox(self, id=ID, choices=['Abundance file','Blast output'], style= wx.RA_SPECIFY_COLS)
        self.blast= BlastPanel(self)
        self.fam= FamPanel(self)

        self.rbFam.Bind(wx.EVT_RADIOBUTTON,self.onRbFam) 
        
        
        self.sizer= wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.rbFam, flag= wx.TOP|wx.LEFT, border= 10)    
        self.sizer.Add(self.fam, flag= wx.ALL , border= 10 )    
        self.sizer.Add(self.blast, flag= wx.ALL , border= 10)    
    
        self.blast.Hide()

        self.btnCancel = wx.Button(id=wx.ID_CANCEL, label=u'Cancel', name=u'btnCancel', parent=self)

        self.btnOk = wx.Button(id=wx.ID_OK,parent=self, label=u'OK', name=u'btnOk')

        sizerBtm=wx.BoxSizer(wx.HORIZONTAL)
        sizerBtm.Add(self.btnCancel)
        sizerBtm.Add((10,0))
        sizerBtm.Add(self.btnOk, flag= wx.RIGHT|wx.BOTTOM, border= 10)

        self.sizer.Add(sizerBtm, 1, flag= wx.ALIGN_RIGHT| wx.RIGHT|wx.BOTTOM, border=10)

        self.SetSizerAndFit(self.sizer)

    def onRbFam(self,e):
        famType= self.rbFam.GetSelection()
        
        if famType == 1:
            self.fam.Hide()
            self.blast.Show()
            self.SetSizerAndFit(self.sizer)
        else:
            self.blast.Hide()
            self.fam.Show()
            self.SetSizerAndFit(self.sizer)


listBlastFields= ["query","subject","% id","alignment length","mistmatches","gap openings","q.start","q.end","s.start","s.end","e-value","bit score"]


class BlastPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, id=ID, name='', parent=parent) #,size=wx.Size(600, 250), title=u'Import Data')
        
        self.fbbBout = filebrowse.FileBrowseButtonWithHistory(  self, -1, size=(450, -1),  changeCallback = self.onFbbBoutBrowse, labelText= "Blast tabular output file"
            )

        self.fbbBout.callCallback = False
        #self.fbbBout.SetHistory(['You', 'can', 'put', 'some', 'filenames', 'here'], 4)

        lblPerc= wx.StaticText( id=ID,parent=self, label=u'% identity')
        self.txtPerc = wx.TextCtrl(id=ID,
              name=u'txtPerc', parent=self,value="60")
        
        lblAlignmentLength =  wx.StaticText( id=ID,parent=self, label=u'Alignment length')
        self.txtAlignmentLength = wx.TextCtrl(id=ID,
              name=u'txtAlignmentLength', parent=self,value="10")


        lblEvalue= wx.StaticText( id=ID,parent=self, label=u'e-value')
        self.txtEvalue = wx.TextCtrl(id=ID,
              name=u'txtEvalue', parent=self,value="1e-5")

        lblBitScore =  wx.StaticText( id=ID,parent=self, label=u'Bit score')
        self.txtBitScore = wx.TextCtrl(id=ID,
              name=u'txtBitScore', parent=self,value="")


        sizerFilter = wx.FlexGridSizer(4, 2, 5, 2) # 5 columns, 2 rows, vertical gap 5, horizontal gap 5
    
        sizerFilter.AddMany([
                (lblPerc),(self.txtPerc),
                (lblAlignmentLength),(self.txtAlignmentLength),
                (lblEvalue),(self.txtEvalue),
                (lblBitScore),(self.txtBitScore),
            
            ])

        sizerMain=wx.BoxSizer(wx.VERTICAL)
        sizerMain.Add(self.fbbBout)
        sizerMain.Add(sizerFilter)
        self.SetSizer(sizerMain)

    def onFbbBoutBrowse(self, e):
        if hasattr(self, 'fbbBout'):
            value = e.GetString()
            if not value:
                return
            history = self.fbbh.GetHistory()
            if value not in history:
                history.append(value)
                self.fbbh.SetHistory(history)
                self.fbbh.GetHistoryControl().SetStringSelection(value)





class FamPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, id=ID, name='', parent=parent)
        self.fbbAbundance = filebrowse.FileBrowseButtonWithHistory(  self, -1, size=(450, -1),  changeCallback = self.onAbundanceBrowse, labelText= "Abundance file")

        self.fbbAbundance.callCallback = False
        #self.fbbAbundance.SetHistory(['You', 'can', 'put', 'some', 'filenames', 'here'], 4)
        
    def onAbundanceBrowse(self, e):
        if hasattr(self, 'fbbAbundance'):
            value = e.GetString()
            if not value:
                return
            history = self.fbbAbundance.GetHistory()
            if value not in history:
                history.append(value)
                self.fbbAbundance.SetHistory(history)
                self.fbbAbundance.GetHistoryControl().SetStringSelection(value)



a="""    def onAddBlastFilter(self,e):
        cbID= wx.NewId()
        cbBoutFilter = wx.Choice(choices=listBlastFields, size=wx.Size(135, 23), id=cbID, name=u'cbBout', parent=self, value="Blast field")
"""



if __name__ == '__main__':
    import sys
    from wx.lib.mixins.inspection import InspectableApp
    app = InspectableApp(False)
    frame = NewFileDialog(None)
    frame.Show(True)
    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
