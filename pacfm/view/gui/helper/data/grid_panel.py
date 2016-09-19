import wx
import  wx.grid 

import numpy as N

ID=wx.ID_ANY


class TableBase(wx.grid.PyGridTableBase): 
    '''
        #data is the abundance input of type OrderedDict. 
        # data: is a dataframe. columns are the level names and the 
                                value rows are the database hierarhcies.       
    
    '''
    def __init__(self, data_frame): 
        wx.grid.PyGridTableBase.__init__(self) 
        self.data_frame = data_frame 

    def GetNumberRows(self): 
        return len(self.data_frame.index)

    def GetNumberCols(self): 
        return len(self.data_frame.columns)

    def GetValue(self, row, col):
        index= self.data_frame.index[row]
        col= self.data_frame.columns[col]
        return self.data_frame[col][index]

    def GetColLabelValue(self, col):
        return self.data_frame.columns[col]



class Grid(wx.grid.Grid): 
    def __init__(self, parent, data_frame): 
        wx.grid.Grid.__init__(self, parent, -1) 
        #table = TableBase(data_frame) 
        #self.SetTable(table, True)


    """New method added"""
    def UpdateTable(self,data_frame):
        table = TableBase(data_frame) 
        self.SetTable(table, True)
        self.SetDefaultColSize(150, True)
        self.AutoSizeColumn(4)
        self.AutoSizeColumn(5)
        self.SetColFormatFloat(5, precision= 3)
        #self.AutoSizeColumns(2)

class GridPanel(wx.Panel):
    '''
        panel to import input abundance files. 
    '''
    def __init__(self, parent, ID):
        wx.Panel.__init__(self, parent, ID)
        
        #self.staticText1 = wx.StaticText(id=ID,
        #      label=u'Input', name='staticText1', parent=self)
        
        #self.txtInput = wx.TextCtrl(id=ID, name=u'txtMeta',
        #      parent=self,

        #      value=u'Select input metadata file ...')

        #self.btnInput = wx.Button(id=ID, label=u'Browse...',
        #      name=u'btnInput', parent=self)

       
        #sizerTop= wx.BoxSizer(wx.HORIZONTAL)
        #sizerTop.Add(self.staticText1)
        #sizerTop.Add(self.txtInput, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, border=10)
        #sizerTop.Add(self.btnInput)

        #line = wx.StaticLine(parent=self,style=wx.HORIZONTAL)
        
        #self.data=OrderedDict({'kemal':5,'hamza':3, 'mehmet':2})
        #print self.data
        self.grid = Grid(self, None)

        #button_1 = wx.Button(self, -1, "Update Grid")
        #grid_sizer_1 = wx.FlexGridSizer(2, 1, 0, 0)
        sizerMain = wx.BoxSizer(wx.VERTICAL)
        #sizerMain.Add(sizerTop, 0,  wx.TOP| wx.LEFT, border=10)
        #sizerMain.Add(line)
        sizerMain.Add(self.grid, 1, wx.EXPAND)
        #pan.SetSizer(sizer_1)
        #grid_sizer_1.Add(pan, 1, wx.EXPAND, 0)
        #grid_sizer_1.Add(button_1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 0)
        self.SetSizer(sizerMain)
        #grid_sizer_1.AddGrowableRow(0)
        #grid_sizer_1.AddGrowableCol(0)
        self.Layout()


        #self.Bind(wx.EVT_BUTTON, self.UpdateGrid,button_1)





