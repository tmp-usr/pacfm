import wx
import os

ID= wx.ID_ANY

input_types=["Abundance (Count)","Relative abundance (Proportional)","Fold change"]
db_names= ["kegg_orthology", "kegg_orthology_metabolism"]

class NewProjectDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, id=ID, name='', parent=parent,  title=u'Import Data')
        
        #### TOOLS ####

        ### Project
        lblProjectName = wx.StaticText(id=ID,
              label=u'Project name', name='lblProjectName', parent=self)

        self.txtProjectName = wx.TextCtrl(id=ID, name=u'txtProjectName',
              parent=self, value=u'New Project')

        ### File Browser
        lblBrowse = wx.StaticText(id=ID,
              label=u'Input file', name='lblBrowse', parent=self)

        self.txtBrowse = wx.TextCtrl(id=ID, name=u'txtBrowse',
              parent=self, value=u'Select input file ...')
        
        self.btnBrowse = wx.Button(id=ID, label=u'Browse...',
              name=u'btnBrowse', parent=self)
        
      
        ### Database
        lblDB = wx.StaticText(id=ID,
              label=u'Database', name='lblDB', parent=self)
        self.cbDB= self.cbProject = wx.Choice(choices= db_names,
              id=ID, name=u'cbDatabase', parent=self)    
        self.cbDB.SetSelection(0)


        #######

        ### OK/Cancel Buttons
        self.btnCancel = wx.Button(id=wx.ID_CANCEL, label=u'Cancel',
              name=u'btnCancel', parent=self)

        self.btnOk = wx.Button(id=wx.ID_OK,parent=self, label=u'OK', name=u'btnOk')
        
        ### Input type radio buttons
        lblInputType = wx.StaticText(self, id=ID, label=u'Input type')
        self.rbAbundance = wx.RadioButton(self, -1, input_types[0], style =  wx.RB_GROUP )
        self.rbRelative = wx.RadioButton(self, -1, input_types[1])
        self.rbFoldChange = wx.RadioButton(self, -1, input_types[2])
        
        self.rbAbundance.SetValue(1)
        self.input_type= self.rbAbundance.GetLabel()  
        
        #### SIZERS ####

        ### OK/Cancel
        
        sBtm=wx.BoxSizer(wx.HORIZONTAL)
        sBtm.Add(self.btnCancel)
        sBtm.Add((10,0))
        sBtm.Add(self.btnOk)

        ### Project
        sProjectName= wx.BoxSizer(wx.HORIZONTAL)
        sProjectName.Add(lblProjectName, 0)
        sProjectName.Add(self.txtProjectName, 1, wx.EXPAND| wx.RIGHT, border= 30)

        ### Input types

        sInputType= wx.BoxSizer(wx.VERTICAL)
        
        sInputTypeRb= wx.BoxSizer(wx.HORIZONTAL)
        sInputTypeRb.Add(self.rbAbundance)
        sInputTypeRb.Add(self.rbRelative,0, wx.LEFT, border= 10)
        sInputTypeRb.Add(self.rbFoldChange,0, wx.LEFT, border= 10)

        sInputType.Add(lblInputType)
        line1 = wx.StaticLine(self,style=wx.HORIZONTAL)
        sInputType.Add(line1, 1, wx.EXPAND | wx.RIGHT, border= 10 )
        sInputType.Add((0,10)) 
        sInputType.Add(sInputTypeRb, 0, wx.RIGHT, border= 10)

        ### File browser

        sBrowse=wx.BoxSizer(wx.HORIZONTAL)
        
        sBrowse.Add(lblBrowse)
        sBrowse.Add(self.txtBrowse, 1, flag=wx.LEFT|wx.EXPAND, border=25)
        sBrowse.Add(self.btnBrowse, flag=wx.RIGHT, border=25)
        
        ### Database

        sDB = wx.BoxSizer(wx.HORIZONTAL)
        sDB.Add(lblDB)
        sDB.Add(self.cbDB, 1, wx.LEFT, border=25)

        ### main sizer
        sizer= wx.BoxSizer(wx.VERTICAL)
        sizer.Add((0,20))
        sizer.Add(sProjectName, 0, wx.EXPAND|  wx.LEFT | wx.TOP, border= 10)
        sizer.Add((0,5))
        sizer.Add(sBrowse, 0, wx.EXPAND| wx.LEFT,  border=10)
        sizer.Add((0,5))
        sizer.Add(sDB, 0, wx.LEFT,  border=10)
        sizer.Add((0,5))
        sizer.Add(sInputType, 1, wx.LEFT, border= 10)
        sizer.Add((0,10))
        sizer.Add(sBtm,0, wx.ALIGN_RIGHT | wx.RIGHT, border= 10)
        sizer.Add((0,20))

        #### Final Layout
        self.SetSizerAndFit(sizer)


        ###### Bind Events
        self.btnBrowse.Bind(wx.EVT_BUTTON, self.onFileBrowse)
        self.Bind(wx.EVT_RADIOBUTTON, self.onInputTypeSelected)

    def onInputTypeSelected(self, e):
        rb= e.GetEventObject()
        self.input_type= rb.GetLabel()  

    def onFileBrowse(self, e):
        dialog = wx.FileDialog(None, style= wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            file_path = dialog.GetPath()
            self.txtBrowse.SetValue(file_path)


class TestFrame(wx.Frame):
    def __init__(self, parent, log):
        wx.Frame.__init__(self, parent, -1, "Huge (virtual) Table Demo", size=(640,480))
        grid = NewProjectDialog(None)
        a= grid.ShowModal()
       #grid.SetReadOnly(5,5, True)
#---------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    app = wx.App()
    frame = TestFrame(None, sys.stdout)
    app.MainLoop()
