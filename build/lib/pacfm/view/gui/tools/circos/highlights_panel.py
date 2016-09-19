
import  wx
import  wx.lib.colourselect as csel

from wx.lib.itemspicker import ItemsPicker,  IP_REMOVE_FROM_CHOICES, IP_SORT_CHOICES,EVT_IP_SELECTION_CHANGED

#from helper.itemspicker import ItemsPickerPanel
import pdb
#----------------------------------------------------------------------
ID=wx.ID_ANY

class HighlightsPanel(wx.Panel):
    def __init__(self, parent, biodb, highlights= None):
        
        wx.Panel.__init__(self, parent, -1)
        
        self.initVariables(biodb, highlights)
##### init controls #####
        
        self.lblAddHighlight = wx.StaticText(id=ID, label=u'Highlights', parent=self)
        self.clAddHighlight = wx.CheckListBox(self, ID, style= wx.CB_DROPDOWN)
       
        self.btnAddHighlight = wx.Button(id=ID, label=u'Add', name=u'btnAddHiglight', parent=self)
        self.btnRemoveHighlight = wx.Button(id=ID, label=u'Remove', name=u'btnAddHiglight', parent=self)

        self.lblCategory = wx.StaticText(id=ID, label=u'Name', parent=self)
        self.txtCategory = wx.TextCtrl(id=ID, parent=self)
        self.txtLevel = wx.StaticText(id=ID,
              label=u'Level', parent=self)
        self.cbLevel = wx.Choice(choices=[],
                id=ID, name=u'cbLevel',
                parent=self)
        self.txtColor = wx.StaticText(id=ID,
              label=u'Color', parent=self)
        self.cPicker=  csel.ColourSelect(self, -1, "", size=(60, 20))
        self.ip= ItemsPicker(self, size= wx.Size(500,200), ipStyle=  IP_REMOVE_FROM_CHOICES | IP_SORT_CHOICES)
        
##### bind events #######        
        self.btnAddHighlight.Bind(wx.EVT_BUTTON, self.onAddHighlight)
        self.cbLevel.Bind(wx.EVT_CHOICE, self.onLevelChanged)
        self.clAddHighlight.Bind(wx.EVT_LISTBOX, self.onHighlightSelected)
        self.ip.Bind(EVT_IP_SELECTION_CHANGED, self.onSelectionChanged)
        
        self.cPicker.Bind(csel.EVT_COLOURSELECT, self.onColorSelected)
        self.btnRemoveHighlight.Bind(wx.EVT_BUTTON, self.onRemoveHighlight) 
        self.Bind(wx.EVT_CLOSE, self.onClose)
               
               
##### set sizers #######

        sizerAddCategory= wx.BoxSizer(wx.HORIZONTAL)
        sizerAddCategory.Add(self.lblAddHighlight)
        sizerAddCategory.Add((3,0))
        sizerAddCategory.Add(self.clAddHighlight, 1, wx.EXPAND)
        sizerAddCategory.Add((20,0))
        sizerAddCategory.Add(self.btnAddHighlight)
        sizerAddCategory.Add((5,0))
        sizerAddCategory.Add(self.btnRemoveHighlight)


        sizerEditCategory= wx.BoxSizer(wx.HORIZONTAL)
        sizerEditCategory.Add(self.lblCategory)
        sizerEditCategory.Add(self.txtCategory,1, wx.EXPAND)
        sizerEditCategory.Add((20,0))
        sizerEditCategory.Add(self.txtLevel)
        sizerEditCategory.Add(self.cbLevel)
        sizerEditCategory.Add((30,0))
        sizerEditCategory.Add(self.txtColor)
        sizerEditCategory.Add(self.cPicker)

        self.sizerMain=wx.BoxSizer(wx.VERTICAL)

        self.sizerMain.Add(sizerAddCategory, 1, wx.EXPAND )
        self.sizerMain.Add(sizerEditCategory, flag= wx.EXPAND| wx.TOP, border=10)
        self.sizerMain.Add(self.ip, 2, flag= wx.TOP| wx.EXPAND, border= 5)
            
        
        #pos = lb.GetPosition().x + lb.GetSize().width + 25
        #btn = wx.Button(self, -1, "Test SetString", (pos, 50))
        #self.Bind(wx.EVT_BUTTON, self.OnTestButton, btn)
        self.initControls()    

    def initControls(self):
        dbLevelCount= self.biodb.getLevelCount()
        levels= ["Level %s" %i for i in range(1, dbLevelCount+1)]
        self.cbLevel.SetItems(levels)

        if len(self.highlights) > 0:
            self.clAddHighlight.SetItems([h.name for h in self.highlights.items])
            self.clAddHighlight.SetSelection(0)
            highlight= self.highlights.items[0]
            self.loadHighlight(highlight)

        else:
            self.clAddHighlight.Clear()
#####################################
        self.SetSizer(self.sizerMain) 
        self.Layout()
    

    def initVariables(self, biodb, highlights):
        self.biodb=biodb 
        self.highlights= highlights
    
    def updateHighlights(self, highlights):
        self.highlights= highlights  

    
    def onLevelChanged(self, e):
        dlg = wx.MessageDialog(self, 'You will lose selections from the previous level. Will you still proceed?',
                               'WASTED TIME ALERT!',
                               wx.OK | wx.CANCEL | wx.ICON_EXCLAMATION)
        
        if len(self.ip.GetSelections()) > 0:
            resp= dlg.ShowModal() 
        
            if resp == wx.ID_OK:
                names= [i.name for i in self.biodb.getFeaturesByLevel(e.GetSelection()+1)]
                self.ip.SetItems(names)
                self.ip.SetSelections([])
               
            else:
                h=self.highlights.get_by_index(self.clAddHighlight.GetSelection())
                self.cbLevel.SetSelection(h.level-1)
        else:
            
            names= [i.name for i in self.biodb.getFeaturesByLevel(e.GetSelection()+1)]
            self.ip.SetItems(names)
            self.ip.SetSelections([])


    def onSelectionChanged(self, e):
        e.Skip()
        #names= e.GetItems()
        #for name in names:self.highlights.add_pathway(name) 
    
    def onAddHighlight(self, e):
        h=self.highlights.add()
        
        self.clAddHighlight.InsertItems([h.name],len(self.highlights)-1 )
        self.clAddHighlight.SetSelection(len(self.highlights)-1)

        self.txtCategory.SetValue(h.name)
        
        self.cbLevel.SetSelection(h.level-1)

        self.cPicker.SetColour(h.color)
        
        names= [i.name for i in self.biodb.getFeaturesByLevel(h.level)]
        
        self.ip.SetItems(names)
        self.ip.SetSelections([])


    def onRemoveHighlight(self, e):
        selected_highlight= self.highlights.get_by_index(self.clAddHighlight.GetSelection())
        if selected_highlight:
            self.highlights.remove(selected_highlight.name)
            self.initControls()
        #self.initVariables(highlights= self.)
        

    def saveHighlight(self):
        name= self.txtCategory.GetValue()
        names= self.ip.GetSelections()
        color= self.cPicker.GetColour()
        level= self.cbLevel.GetSelection()+1
        index= self.highlights.items.index(self.highlights.get_current())
        checked= self.clAddHighlight.IsChecked(index)

        self.highlights.edit(name= name, pathways= names, color=color, level= level, checked= checked)


    def onHighlightSelected(self, e):
        #cur_highlight= self.highlights.get_current()
        self.saveHighlight()        
        
        
        #self.clAddHighlight.SetItems([i.name for i in self.highlights.highlights])
        #self.clAddHighlight.SetSelection(e.GetSelection())
        
        highlight= self.highlights.get_by_index(e.GetSelection())
        self.loadHighlight(highlight)
        self.highlights.set_current(highlight)


    def loadHighlight(self, highlight):
        self.txtCategory.SetValue(highlight.name)
        self.cbLevel.SetSelection(highlight.level-1)
        self.cPicker.SetColour(highlight.color)
        
        
        checked_indexes= [self.highlights.items.index(item) for item in self.highlights.items if item.checked]
        
        self.clAddHighlight.SetChecked(checked_indexes)
        
        names= [i.name for i in self.biodb.getFeaturesByLevel(highlight.level)]
        
        names= [name for name in names if name not in highlight.pathways]
        
        self.ip.SetItems(names)
        self.ip.SetSelections(highlight.pathways)

    def onColorSelected(self, e):
        self.highlights.edit(color= e.GetValue())

    def onClose(self, e):
        pdb.set_trace()
        self.saveHighlight()        
        self.highlights.dump()

    #def EvtListBox(self, e):
    #    e.Skip()
    #   #self.log.WriteText('EvtListBox: %s\n' % event.GetString())

    #def EvtCheckListBox(self, e):
        #index = e.GetSelection()
        #label = self.cbFunctions.GetString(index)
        #status = 'un'
        #if self.cbFunctions.IsChecked(index):
        #    status = ''
        #self.cbFunctions.SetSelection(index)    # so that (un)checking also selects (moves the highlight)
        #hl= self.highlights.getCurrenHighlight()
        #print hl.names
        #self.ip.SetSelections(hl.names)

    #def OnTestButton(self, evt):
    #    self.lb.SetString(4, "FUBAR")

    #def OnDoHitTest(self, evt):
    #    item = self.lb.HitTest(evt.GetPosition())
    #    #self.log.write("HitTest: %d\n" % item)
 
 
class TestFrame(wx.Frame):
    def __init__(self, parent, biodb= None, highlights= None):
        wx.Frame.__init__(self, parent, -1, "Simple Grid Demo", size=(640,480))
        self.hl = HighlightsPanel(self, biodb, highlights)
#---------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    from wx.lib.mixins.inspection import InspectableApp
    app = InspectableApp(False)
    from pacfm import HighlightContainer, Highlight
    from biodb.sqling.selector import Selector
    
    biodb= Selector('kegg_orthology')
    h= HighlightContainer()
    h.load()
    
    frame = TestFrame(None, biodb, h)
    frame.Show(True)

    #frame.hl.initControls(biodb, h)
    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
