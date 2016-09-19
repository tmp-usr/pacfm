import wx
import  wx.lib.colourselect as cSelect

ID=wx.ID_ANY
#### check the overlapping palettes with the matplotlib library
#### more on brewer palettes: http://mkweb.bcgsc.ca/brewer/

colormaps= {

'BrBG':	'brbg-11-div',
'PiYG':	'piyg-11-div',
'PRGn':	'prgn-11-div',
'PuOr':	'puor-11-div',
'RdBu':	'rdbu-11-div',
'RdGy':	'rdgy-11-div',
'RdYlBu':	'rdylbu-11-div',
'RdYlGn':	'rdylgn-11-div',
'Spectral':	'spectral-11-div',
'Accent':	'accent-8-qual',
'Dark2':	'dark2-8-qual',
'Paired':	'paired-12-qual',
'Pastel1':	'pastel1-9-qual',
'Pastel2':	'pastel2-8-qual',
'Set1':	'set1-9-qual',
'Set2':	'set2-8-qual',
'Set3':	'set3-12-qual',
'Blues':	'blues-9-seq',
'BuGn':	'bugn-9-seq',
'BuPu':	'bupu-9-seq',
'GnBu':	'gnbu-9-seq',
'Greens':	'greens-9-seq',
'Greys':	'greys-9-seq',
'Oranges':	'oranges-9-seq',
'OrRd':	'orrd-9-seq',
'PuBu':	'pubu-9-seq',
'PuBuGn':	'pubugn-9-seq',
'PuRd':	'purd-9-seq',
'Purples':	'purples-9-seq',
'RdPu':	'rdpu-9-seq',
'Reds':	'reds-9-seq',
'YlGn':	'ylgn-9-seq',
'YlGnBu':	'ylgnbu-9-seq',
'YlOrBr':	'ylorbr-9-seq',
'YlOrRd':	'ylorrd-9-seq'

}

plot_types=  ['histogram','heatmap']# if you change histogram to bars, don't forget to change it in the config file too!!!
locations=  ['center','right-top','left-top', 'right-bottom', 'left-bottom']


### added in version 0.0.6
pathway_abundance_calculation_types= ["sum","average"]
### Count and relative abundance data will be summed up during the calculation of 
### pathway level values. Fold change and such data inputs are better represented
### at pathway level with taking the average since summing up fold changes is not
### so meaningful.
input_types=["Abundance (Count)","Relative abundance (Proportional)","Fold change"]

# colorbar_title= "Relative abundance"
# negative values are automatically represented in the histogram
## however it would be even nicer to represent them by diverging 
## colors in the heatmaps.

class PlotsPanel(wx.Panel):
    def __init__(self, parent, biodb, plots= None ):
        wx.Panel.__init__(self,parent)

        self.initVariables(biodb, plots)
######## init controls #########
        
        self.txtLevel = wx.StaticText(id=ID,
              label=u'Level', parent=self)
        self.cbLevel = wx.Choice(choices=[],
                id=ID, name=u'cbLevel',
                parent=self)
        self.txtType = wx.StaticText(id=ID,
              label=u'Plot type', parent=self)
        self.cbType = wx.Choice(choices=plot_types,
                id=ID, name=u'cbType',
                parent=self)
        self.txtColor = wx.StaticText(id=ID,
              label=u'Color', parent=self)
        self.cPicker=  cSelect.ColourSelect(self, -1, "", (55, 55, 255), size=(60, 20))
        self.txtColorscheme = wx.StaticText(id=ID,
              label=u'Color scheme', parent=self)
        self.cbColorscheme = wx.ComboBox(choices= colormaps.keys(),
                value='Oranges',id=ID, 
                name=u'cbType', parent=self,
                style= wx.ALIGN_CENTER_VERTICAL )


        self.rbRaw = wx.RadioButton(self, -1, 'Raw', style =  wx.RB_GROUP )
        self.rbNorm = wx.RadioButton(self, -1, 'Normalized')
       
        lblDataContent = wx.StaticText(self, id=ID, label= "Data content")
        line2 = wx.StaticLine(self,style=wx.HORIZONTAL)
        
        sData= wx.BoxSizer(wx.VERTICAL)
        sData.Add(lblDataContent)
        sData.Add(line2, 1, wx.EXPAND | wx.RIGHT, border= 10 )
       
        sDataType= wx.BoxSizer(wx.HORIZONTAL)
        sDataType.Add(self.rbRaw)
        sDataType.Add(self.rbNorm,0, wx.LEFT, border= 10)

        sData.Add(sDataType, 0, wx.TOP, border= 10)

        #self.txtLegendLoc = wx.StaticText(id=ID,
        #      label=u'Legend location', parent=self)
        #self.cbLegendLoc = wx.Choice(choices= locations,
        #        id=ID, name=u'cbLegendLoc',
        #         parent=self)
        #self.txtColorbarLoc = wx.StaticText(id=ID,
        #      label=u'Colorbar location', parent=self)
        #self.cbColorbarLoc = wx.Choice(choices=locations,
        #        id=ID, name=u'cbColorbarLoc',
        #        parent=self)

########## bind events #######

        self.cPicker.Bind(cSelect.EVT_COLOURSELECT, self.onColorChanged)
        self.cbLevel.Bind(wx.EVT_CHOICE, self.onLevelChanged) 
        self.cbType.Bind(wx.EVT_CHOICE, self.onTypeChanged)
        self.cbColorscheme.Bind(wx.EVT_COMBOBOX, self.onColorschemeChanged)

########## set sizers ##########
        
        self.sizerContent = wx.FlexGridSizer(cols=2) 
        self.sizerContent.AddMany([
            (self.txtLevel, 0, wx.ALIGN_CENTER_VERTICAL), (self.cbLevel, 0, wx.ALL, 3),
            (self.txtType, 0,  wx.ALIGN_CENTER_VERTICAL), (self.cbType, 0, wx.ALL, 3),
            (self.txtColor, 0, wx.ALIGN_CENTER_VERTICAL), (self.cPicker, 0, wx.ALL, 3), 
            (self.txtColorscheme, 0, wx.ALIGN_CENTER_VERTICAL), (self.cbColorscheme, 0, wx.ALL , 3) ,
             
            ])
            
            #(sData, 1,  wx.EXPAND | wx.TOP, 30), (wx.StaticLine(self, style= wx.HORIZONTAL),1)
            # , 
            # (self.rbRaw, 0,  wx.ALIGN_CENTER | wx.TOP, 5), (self.rbNorm, 0, wx.TOP, 5), 
            #(self.txtColorbarLoc, 0,  wx.ALIGN_CENTER_VERTICAL |wx.TOP, 3), (self.cbColorbarLoc, 0, wx.ALL , 3),           
            #])
        
        sizerMain = wx.BoxSizer(wx.VERTICAL)
        sizerMain.Add(self.sizerContent, 0,  wx.TOP | wx.LEFT, border= 10)
        sizerMain.Add((0,30))
        sizerMain.Add(sData, 0 , wx.EXPAND |wx.LEFT, border= 10)
    
        self.initControls()
        
        self.SetSizerAndFit(sizerMain)

    def loadPlot(self, plot):

        self.cbLevel.SetSelection(plot.level -1)
        self.cbType.SetStringSelection(plot.plot_type)
        
        if plot.plot_type == "histogram":
            self.cPicker.Enable()
            self.cbColorscheme.Disable()
            self.cPicker.SetColour(plot.color)
        
        elif plot.plot_type == "heatmap":
            self.cbColorscheme.Enable()
            self.cPicker.Disable()
            color_scheme= [k for k,v in colormaps.iteritems() if v == plot.color_scheme][0]
            self.cbColorscheme.SetStringSelection(color_scheme)


    #on  plot_type changed event should be updated!

    #def onInputTypeChanged(self, e):
    #    self.input_type= e.GetSelection() + 1  


    def onColorschemeChanged(self, e):
        plot= self.plots.get_current()
        plot.color_scheme= colormaps[e.GetString()]
        plot.color= None

    def onTypeChanged(self,e):
        plot= self.plots.get_current()
        plot_type= e.GetString()
        plot.plot_type= plot_type
        
        if plot_type == "histogram":
            self.cPicker.Enable()
            self.cbColorscheme.Disable()
            self.cPicker.SetColour(plot.color)
        
        elif plot_type == "heatmap":
            self.cbColorscheme.Enable()
            self.cPicker.Disable()
            color_scheme= [k for k,v in colormaps.iteritems() if v == plot.color_scheme][0]
            self.cbColorscheme.SetStringSelection(color_scheme)


    def onLevelChanged(self,e):
        level = e.GetSelection() + 1
        plot= self.plots[level]
        self.loadPlot(plot)


    def initVariables(self, biodb, plots, input_type= 2):
        self.biodb= biodb
        self.plots= plots
        self.input_type= input_type

    def initControls(self, plot_types=None, colorschemes=None):

        dbLevelCount= self.biodb.getLevelCount()
        levels= ["Level %s" %i for i in range(1, dbLevelCount)]
        self.cbLevel.SetItems(levels)

        if plot_types:
            self.cbType.SetItems(plot_types)
        if colorschemes:    
            self.cbColorscheme.SetItems(colorschemes)
####################################
       

        plot= self.plots.get_current()
        self.loadPlot(plot)

    
    
    def onColorChanged(self, e):
        plot= self.plots.get_current()
        plot.color= list(e.GetValue().Get(True))

class TestFrame(wx.Frame):
    def __init__(self, parent, biodb, plots):
        wx.Frame.__init__(self, parent, -1, "Simple Grid Demo", size=(640,480))
        self.grid = PlotsPanel(self, biodb, plots)
        #---------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    from wx.lib.mixins.inspection import InspectableApp
    from pacfm import PlotContainer
    from biodb.sqling.selector import Selector
    
    biodb= Selector('kegg_orthology')
    p= PlotContainer()
    p.load()
    
    
    app = InspectableApp(False)
    frame = TestFrame(None, biodb, p)
    frame.Show(True)
    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()

        
        #self.txtColorscheme = wx.StaticText(id=ID,
        #      label=u'Color scheme', parent=self)


        
  
