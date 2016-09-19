import wx

from pacfm.view.gui import PathwayDialog
from pacfm.model import PathwayAnalyzer


#import pdb


#biodb_selector=Selector('kegg_orthology')
#ex_in= "/Users/kemal/phd/projects/pack_fm/src/circos/pp_kegg_short.tsv" 

#input_builder= InputBuilder(biodb_selector, ex_in)

#! Assembler conversion to fantom hier file is lacking
#! Check if the pathway analyzer data frame and fantom s hierarchy files have the 
#same format!!!


#### change clcKeyEnzymes to a more reasonable name. clcKeys

class PathwayController(object):
    def __init__(self, biodb_selector, input_builder):
        self.view= PathwayDialog(None)
        
        self.input_builder= input_builder
        self.biodb_selector= biodb_selector
        self.ideograms= self.input_builder.assembler.ideograms
        
        level_names = ["Level %s" %l for l in range(1,len(self.ideograms)+1)]

        self.popPathwayContainer(1)
        self.key_enzyme_type= 0

        ### events
        self.pnl= self.view.pnl
        for rb in self.pnl.rbs:
            rb.Bind(wx.EVT_RADIOBUTTON, self.OnRbSelected)
    
        self.pnl.clcPw.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.pnl.chLevel.Bind(wx.EVT_CHOICE, self.OnLevelChanged)
        self.pnl.clcKeyEnzymes.Bind(wx.EVT_KILL_FOCUS, self.onFocusLostClcKeyEnzymes)
        #self.pnl.clcPw.Bind(wx.EVT_KILL_FOCUS, self.onFocusLostClcPw)
        
        #self.view.Bind(wx.EVT_WINDOW_DESTROY, self.onClose)
        #self.view.btnOK.Bind(wx.EVT_BUTTON, self.onClose)
        #self.view.btnCancel.Bind(wx.EVT_BUTTON, self.onClose)
        #####
        self.initLevels(level_names)
        self.initPathways(self.pathway_container)
        
        #self.view.ShowModal()
      
      # gettables:
        # check list ctrl: get checked (list) +
        # checkboxes: getChecked -
        # in checklistctrl selecttionchanged:  clcKeyEnzymes getSelected +
        # pathway assoication text: getstring 
        # rbs: get selected
        # 


    #def onFocusLostClcPw(self, e):
    #    unchecked_items= self.pnl.clcPw.unchecked_items
    #    level_index = self.pnl.chLevel.GetSelection()
    #    level_name= self.pnl.chLevel.GetString(level_index)
    #    import pdb
    #    #pw_index= self.pnl.clcPw.GetFirstSelected()
    #    for unchecked_index in unchecked_items:
    #        pw= self.pathway_container[unchecked_index+1][0]
    #        
    #        pdb.set_trace()

    def onFocusLostClcKeyEnzymes(self, e):
        #print dir(self.pnl.clcKeyEnzymes)
        checked_items= self.pnl.clcKeyEnzymes.GetChecked() #GetCheckedItems() #Selections()
        key_enzymes= [self.pnl.clcKeyEnzymes.GetClientData(i) for i in checked_items]
        
        pw_index= self.pnl.clcPw.GetFirstSelected()
        pw= self.pathway_container[pw_index+1][0]

        pw.set_key_leaf_features(key_enzymes)

        self.popPathwayContainer(pw.level)
        self.initPathways(self.pathway_container)
        self.pnl.clcPw.Select(pw_index)
        self.pnl.clcKeyEnzymes.SetChecked(checked_items)

        #self.pathway_container[]
        #print self.pnl.clcKeyEnzymes.GetCheckedStrings() #Selections()
        
        #print [f.accession for f in items]

      
    def OnItemSelected(self, e):
        index= e.GetData()
        pw= self.pathway_container[index][0]
        
        #print self.pnl.clcKeyEnzymes.ip.GetSelections()
        self.pnl.clcKeyEnzymes.Clear()
        i= 0
        checked_indexes=[]
        for f in pw.get_leaf_features(): 
            self.pnl.clcKeyEnzymes.Append(f.name, f)
            if f in pw.get_key_leaf_features():
                checked_indexes.append(i)
            i+=1
            
        self.pnl.clcKeyEnzymes.SetChecked(checked_indexes)
        self.pnl.clcKeyEnzymes.SetFirstItem(0)
        #self.pnl.clcKeyEnzymes.ip.SetItems([(f.name, f) for f in pw.get_leaf_features()])
        #self.pnl.clcKeyEnzymes.ip.SetSelections([])
    

    def initLevels(self, levels):
        self.pnl.chLevel.SetItems(levels)
    

    def initPathways(self, pathways): 
        self.initClcPw()
        self.insertClcPwItems(pathways)
        self.pnl.SetSizer(self.pnl.sizerMain)


    def initClcPw(self):
        self.pnl.clcPw.ClearAll()
        self.pnl.clcPw.InsertColumn(0, "")
        self.pnl.clcPw.InsertColumn(1, "Pathway") #wx.LIST_FORMAT_RIGHT)
        self.pnl.clcPw.InsertColumn(2, "# orthologous proteins")
        self.pnl.clcPw.InsertColumn(3, "# key proteins")

        self.pnl.clcPw.SetColumnWidth(0, 70)
        self.pnl.clcPw.SetColumnWidth(1, 300)
        self.pnl.clcPw.SetColumnWidth(2, 150)
        self.pnl.clcPw.SetColumnWidth(3, 150)


    def insertClcPwItems(self, pathway_container):
        i=1
        for key, data in pathway_container.iteritems():
            index = self.pnl.clcPw.InsertStringItem(len(pathway_container), str(i))
            self.pnl.clcPw.SetStringItem(index, 1, data[2])
            self.pnl.clcPw.SetStringItem(index, 2, data[3])
            self.pnl.clcPw.SetStringItem(index, 3, data[4])
            self.pnl.clcPw.SetItemData(index, key)
            
            if data[1]:
                self.pnl.clcPw.CheckItem(index)

            i+=1


    def popPathwayContainer(self, level):
        self.ide= self.ideograms[level-1]
        self.pathway_container= dict.fromkeys(range(1, len(self.ide.chromosomes)), None)
        i=1
        for pathway in self.ide.chromosomes:
            key_enzymes= pathway.get_key_leaf_features()
            try:
                n_proteins= pathway.get_db_data()['n_protein']
            except:
                n_proteins= 0
            self.pathway_container[i] = (pathway, pathway.get_included(), pathway.name, "%s" % n_proteins, "%s" %len(key_enzymes))
            i+=1

    
    def OnLevelChanged(self,e):
        unchecked_items= self.pnl.clcPw.unchecked_items[self.pnl.clcPw.current_level]
        checked_items= self.pnl.clcPw.checked_items[self.pnl.clcPw.current_level]
        
        for unchecked_index in unchecked_items:
            
            pw= self.pathway_container[unchecked_index+1][0]
            pw.set_included(False)

        for checked_index in checked_items:
            pw= self.pathway_container[checked_index+1][0]
            pw.set_included(True)

        level = self.current_level= e.GetSelection()+1
        self.pnl.clcPw.SetLevel(level)
        self.popPathwayContainer(level)
        self.initPathways(self.pathway_container)
        self.pnl.clcKeyEnzymes.Clear()

    #    level_index = self.pnl.chLevel.GetSelection()
    #    level_name= self.pnl.chLevel.GetString(level_index)
    #    import pdb
    #    #pw_index= self.pnl.clcPw.GetFirstSelected()
    #    for unchecked_index in unchecked_items:
    #        pw= self.pathway_container[unchecked_index+1][0]
    #        
    #        pdb.set_trace()

    def OnRbSelected(self, e):
        rb= e.GetEventObject()
        selection= rb.GetLabel()
        if selection == "Any (default)":
            self.pnl.clcKeyEnzymes.Hide()
            self.pnl.spinPanel.Hide()
            self.pnl.SetSizer(self.pnl.sizerMain)
            self.pnl.Layout()
            self.key_enzyme_type= 0

        elif selection == "All":
            self.pnl.clcKeyEnzymes.Hide()
            self.pnl.spinPanel.Hide()
            self.pnl.SetSizer(self.pnl.sizerMain)
            self.pnl.Layout()
            self.key_enzyme_type= 1

        elif selection == "Manual":
            self.pnl.clcKeyEnzymes.Show()
            self.pnl.spinPanel.Hide()
            self.pnl.SetSizer(self.pnl.sizerMain)
            self.pnl.Layout()
            self.key_enzyme_type= 2
            
        else:
            self.pnl.spinPanel.Show()
            self.pnl.clcKeyEnzymes.Hide()
            self.pnl.SetSizer(self.pnl.sizerMain)
            self.pnl.Layout()
            self.key_enzyme_type= 3


if __name__ == '__main__' and __package__ is None:
    from wx.lib.mixins.inspection import InspectableApp
    app = InspectableApp(False)
    c = PathwayController(None)
    frame= c.view
    frame.ShowModal()
    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()
    app.MainLoop()
