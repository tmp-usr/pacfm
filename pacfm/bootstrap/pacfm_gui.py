import os, sys
#----
import wx
from biodb.sqling.selector import Selector
#----
from pacfm_base import PacfmBase
from pacfm.model import LinkContainer, HighlightContainer, PlotContainer
from pacfm.model import PathwayAnalyzer
from pacfm.model import file_provider  

from pacfm.controller import InputBuilder, CircosController, Drawer
from pacfm.controller import PathwayController
from pacfm.controller import PilImageToWxImage

from pacfm.view.gui import MainView, CircosPanel
from pacfm.view.gui import AbbrDialog, HelpDialog
from pacfm.view.gui import GridPanel      
from pacfm.view.gui import NewProjectDialog



class PacfmGUI(PacfmBase):
    """
        GUI class
    """
    
    def __init__(self, wx_app= None, normalized=False, db_name="kegg_orthology", calculation_type= "sum", colorbar_title= "Relative abundance"):
       
        PacfmBase.__init__(self, wx_app= wx_app, normalized= normalized, db_name= db_name, calculation_type= calculation_type, colorbar_title= colorbar_title)

        self.view= MainView(None)
        self.init_controls()

        ### events
        self.bind_events()

        ### final
        self.view.Show()

    def init_variables(self, **kwargs):
        """
            overriden method
        """
        self.app = kwargs['wx_app'] 
        self.normalized= kwargs['normalized']
        self.calculation_type= kwargs["calculation_type"]
        self.db_name= kwargs['db_name']
        self.colorbar_title= kwargs['colorbar_title']
        self.biodb_selector= None 
### GUI ###
    def bind_events(self):
        """
            GUI: Binds events to be triggered in gui.
        """
        self.view.Bind(wx.EVT_TOOL, self.onNewProject, id= self.view.newID)
        self.view.Bind(wx.EVT_TOOL, self.onPathwayAnalysis, id= self.view.pathwayID)
        self.view.Bind(wx.EVT_TOOL, self.onCircosPlot, id=self.view.circosID)
        self.view.Bind(wx.EVT_TOOL, self.onRestart, id=self.view.homeID)
        self.view.Bind(wx.EVT_CLOSE, self.onExit)
        
        ## menubar events
        self.view.Bind(wx.EVT_MENU, self.onNewProject, self.view.fItemNew )
        self.view.Bind(wx.EVT_MENU, self.onSaveRawData, self.view.sRawData)
        self.view.Bind(wx.EVT_MENU, self.onSaveRawPlot, self.view.sRawPlot)
        self.view.Bind(wx.EVT_MENU, self.onSaveNormData, self.view.sNormData)
        self.view.Bind(wx.EVT_MENU, self.onSaveNormPlot, self.view.sNormPlot)

        self.view.Bind(wx.EVT_MENU, self.onPathwayAbbreviations, self.view.pItemAbbr)
        self.view.Bind(wx.EVT_MENU, self.onEnzymeAssociations, self.view.pItemAss)
        self.view.Bind(wx.EVT_MENU, self.onKeyEnzymes, self.view.pItemKey)



    def enable_toolbar_controls(self, enabled=True):
        #---- TOOLBAR ----#
        self.view.tb.EnableTool(self.view.pathwayID, enabled) 
        self.view.tb.EnableTool(self.view.homeID, enabled) 
        self.view.tb.EnableTool(self.view.circosID, enabled)

    def enable_menubar_controls(self, enabled= True):
        #---- File Menu ----#
        self.view.fItemSave.Enable(enabled)
        self.view.pItemAbbr.Enable(enabled)
        self.view.pItemAss.Enable(enabled)
        self.view.pItemKey.Enable(enabled)
    
    def enable_controls(self, enabled= True):
        self.enable_toolbar_controls(enabled)
        self.enable_menubar_controls(enabled)

    def enable_normalized_controls(self, enabled= True):
        self.view.sNormData.Enable(enabled)
        self.view.sNormPlot.Enable(enabled)

    def init_controls(self):
        self.enable_controls(False)


    def onExit(self, e):
        """
            GUI:Forcefully closes the gui.
        """
        self.view.Destroy()
        self.app.ExitMainLoop()    
        wx.WakeUpMainThread()

    def onRestart(self, e):
        """
            Restarts the default settings.
        """
        self.loadNewProject()

    def onPathwayAbbreviations(self, e):
        """
            Shows the long and abbreviated forms of pathway names as shown in the figure.
        """
        dlg= AbbrDialog(self.view, self.get_abbreviations())
        dlg.ShowModal()
        e.Skip()
    
    def onEnzymeAssociations(self, e):
        """
            Shows the pathways which each enzyme is associated with.
        """
        dlg= HelpDialog(self.view, self.get_link_info(), "Enzyme Associations")
        dlg.ShowModal()

    def onKeyEnzymes(self, e):
        """
            Shows the key enzymes of each pathway. 
        """
        dlg= HelpDialog(self.view, self.get_key_enzyme_info(), "Key enzymes of pathways")
        dlg.ShowModal()
    
    def get_abbreviations(self):
        """
           Returns the abbreviations attribute of the ideograms \
                   placed at individiual hierarchy level.
        """
        if not self.normalized:
            ideograms= self.input_builder.assembler.ideograms
        else:
            ideograms= self.pw_analyzer.ideograms

        for ide in ideograms:
            if ide.level not in self.level_abbreviations:
                self.level_abbreviations[str(ide.level)]= ide.abbreviations
        return self.level_abbreviations

    def get_key_enzyme_info(self):
        """
            Returns the key enzymes of individual pathways as defined by the users.
        """
        if not self.normalized:
            ide= self.input_builder.assembler.ideograms[-1]
        else:
            ide= self.pw_analyzer.ideograms[-1]
        
        for chrom in ide.chromosomes:
            self.key_enzymes[chrom.name]= [f.name for f in chrom.get_non_null_features()]  
        return self.key_enzymes

    def get_link_info(self): 
        """
            Returns the pathway pairs that individual enzyme is linked by.
        """
        if not self.normalized:
            ide= self.input_builder.assembler.ideograms[-1]
        else:
            ide= self.pw_analyzer.ideograms[-1]
        
        for id, link_coordinate in ide.link_coordinates.iteritems():
            feature= self.biodb_selector.getFeatureByID(id) 
            pws= [coor.get_name_by_level(ide.level) for coor in link_coordinate.coordinates]
            self.enzyme_pathway_link[feature.name] = pws
        return self.enzyme_pathway_link

    def save_table(self, table, file_path):
        """
            GUI: Saves the data inside a wx table.
        """
        fOut= open(file_path,"w")

        n_cols= table.GetColsCount()
        n_rows= table.GetRowsCount()

        col_names= [table.GetColLabelValue(i) for i in range(n_cols)]
        header= "\t".join(col_names) + "\n"
        fOut.write(header)

        for j in range(n_rows):
            row= [] 
            for i in range(n_cols):
                value= table.GetValue(j, i)
                row.append("%s" %value)
            row_line= "\t".join(row) +"\n"
            fOut.write(row_line)
    
    def get_save_plot_dialog(self):
        """
            GUI: Displays a dialog window to save figures in an appropriate image format.
        """
        wildcard = "PNG (*.png)|*.png|"    \
                   "JPG (*.jpeg)|*.jpeg" 

        dlg = wx.FileDialog(
            self.view, message="Save file as ...", defaultDir=os.getcwd(), 
            defaultFile="my_plot", wildcard=wildcard, style=wx.SAVE
            )
        return dlg

    def get_save_data_dialog(self):
        """
            GUI: Displays a dialog window to save data in an appropriate image format.
        """
        wildcard = "Tab separated text file (*.tsv)|*.tsv"  
        dlg = wx.FileDialog(
            self.view, message="Save file as ...", defaultDir=os.getcwd(), 
            defaultFile="my_data", wildcard=wildcard, style=wx.SAVE
            )
        return dlg

    def onSaveRawData(self, e):
        """
            GUI: Saves the raw data to a file.
        """
        dlg= self.get_save_data_dialog()
        if dlg.ShowModal() == wx.ID_OK:
            file_path= dlg.GetPath()
            table= self.pnlRawData.grid.GetTable()
            self.save_table(table, file_path)
    
    def onSaveNormData(self, e):
        """
            Saves the normalized data to a file.
        """
        dlg= self.get_save_data_dialog()
        if dlg.ShowModal() == wx.ID_OK:
            file_path= dlg.GetPath()
            table= self.pnlNormData.grid.GetTable()
            self.save_table(table, file_path)

    def save_plot(self, plot_panel):
        """
            GUI: Saves the PACFM plot inside a wx panel.
        """
        dlg= self.get_save_plot_dialog()
        if dlg.ShowModal() == wx.ID_OK:
            file_path= dlg.GetPath()
            if file_path.lower().endswith(".png"):
                plot_panel.wxImage.SaveFile(file_path, wx.BITMAP_TYPE_PNG)
            elif file_path.lower().endswith(".jpg") or file_path.lower().endswith(".jpeg"):
                plot_panel.wxImage.SaveFile(file_path, wx.BITMAP_TYPE_JPEG)
            else:
                print file_path

    def onSaveRawPlot(self, e):
        """
            Saves the raw data plot to a file.
        """
        self.save_plot(self.pltRawData)

    def onSaveNormPlot(self, e):
        """
            Saves the raw data plot to a file.
        """
        self.save_plot(self.pltNormData)
    
    def onNewProject(self, e):
        """
            GUI: Displays a dialog window to start a new project.
        """
        dlg= NewProjectDialog(None)
        
        if dlg.ShowModal() == wx.ID_OK:
            self.file_path= dlg.txtBrowse.GetValue()
            
            if dlg.rbAbundance or dlg.rbRelative:
                self.calculation_type = "sum"
                self.colorbar_title= dlg.input_type
            
            elif dlg.rbFoldChange:
                self.calculation_type= "average"

            self.project_name= dlg.txtProjectName.GetValue()

            self.view.statusBar.SetStatusText("PACFM: Loading a new project... \
Please wait!")
            self.db_name= dlg.cbDB.GetStringSelection()
            self.loadNewProject() 
            self.view.statusBar.SetStatusText("PACFM: A new project \
has been successfully loaded!")
        
        else:
            pass


            #   self.view.statusBar.SetStatusText("PACFM: Start a new project!")
        #wildcard = "Tab-separated text file (*.tsv)|*.tsv|" \
        #           "(*.txt)|*.txt"
        #dlg= wx.FileDialog(self.view, message="Choose a tab-separated text \
        #        file (*.tsv |*.txt)",
        #                    defaultFile="",
        #                    wildcard= wildcard,
        #                    style=wx.FD_OPEN | wx.FD_CHANGE_DIR
        #                  )


    def onOpenProject(self, e):
        """
            GUI: Displays a dialog window to start an existing pacfm \
project with the .pac extension.
        """
        
        wildcard = "PACFM files (*.pac)|*.pac"  
        dlg= wx.FileDialog(self.view, message="Choose a file",
                            defaultFile="",
                            wildcard=wildcard,
                            style=wx.OPEN | wx.CHANGE_DIR
                          )
        
        e.Skip()

    def loadNewProject(self):
        """
            Resets the variables to default settings and loads the new project into PACFM.
        """
        if self.biodb_selector:
            # check if this is enough to switch from a database to another.
            del self.biodb_selector
        
        self.biodb_selector= Selector(self.db_name)
        self.input_builder= InputBuilder(self.biodb_selector, self.file_path, calculation_type= self.calculation_type)
        
        self.pnlRawData= GridPanel(self.view.nb.pnlRawData, -1)
        data_frame= self.input_builder.assembler.to_data_frame()
        self.pnlRawData.grid.UpdateTable(data_frame)

        #### find replacement for the below lines
        # There should be a simpler pnl.Refresh() method!
        sizer= wx.BoxSizer()
        sizer.Add(self.pnlRawData, 1, wx.EXPAND)
        self.view.nb.pnlRawData.SetSizer(sizer)
        self.view.nb.pnlRawData.Layout()
        ######################################### 
        self.view.nb.ChangeSelection(0)
        self.view.nb.analysisBook.ChangeSelection(0)

        self.normalized= False
        
        self.enable_controls(True)
        self.enable_normalized_controls(False)


    def onPathwayAnalysis(self, e):
        """
            GUI: Displays a dialog window to adjust pathway analysis settings.
        """
        if self.input_builder:
            self.pw_controller= PathwayController(self.biodb_selector, self.input_builder)

            pw_panel= self.pw_controller.view.pnl
            pw_length_query= pw_panel.cbPwLength.IsChecked()
            pw_sequence_query= pw_panel.cbPwSeq.IsChecked()
            pw_minpath_query= pw_panel.cbMinPath.IsChecked()

            status_text = ""
            if pw_length_query:
                status_text+= "Normalizing pathway data by sequence length! "
            if pw_sequence_query:
                status_text+= "Normalizing pathway data by the total number \
of proteins/enzymes in the pathways! "
            if pw_minpath_query:
                status_text+= "Normalizing pathway data by the minpath algorithm! "
            status_text+= "Running the pathway association check! Please wait..."
            self.view.statusBar.SetStatusText("PACFM: %s"%status_text)
            response= self.pw_controller.view.ShowModal() 
            
            if response == wx.ID_OK:

                self.pw_analyzer= PathwayAnalyzer(self.biodb_selector, self.input_builder)
                if pw_length_query:

                    self.pw_analyzer.normalize_by_pathway('sequence_length')
                if pw_sequence_query:
                    self.pw_analyzer.normalize_by_pathway('n_protein')
                if pw_minpath_query:
                    self.pw_analyzer.normalize_by_algorithm('minpath')
              
                key_enzyme_type= self.pw_controller.key_enzyme_type
                if key_enzyme_type == 0 or key_enzyme_type == 1:
                    self.pw_analyzer.filter_pathways_by_key_leaf_features(key_enzyme_type)
                elif key_enzyme_type == 3:
                    n_association= pw_panel.spinAss.GetValue() 
                    self.pw_analyzer.filter_pathways_by_key_leaf_features(3, n_association)
        
                self.normalized= True
                self.pnlNormData= GridPanel(self.view.nb.pnlNormData, -1)
                
                data_frame= self.input_builder.assembler.to_data_frame()
                self.pnlNormData.grid.UpdateTable(data_frame)
                
                self.normalized= True
                self.view.nb.ChangeSelection(0)
                self.view.nb.analysisBook.ChangeSelection(1)
                
                
                #### find replacement for the below lines
                # There should be a simpler pnl.Refresh() method!
                sizer= wx.BoxSizer()
                sizer.Add(self.pnlNormData, 1, wx.EXPAND)
                self.view.nb.pnlNormData.SetSizer(sizer)
                self.view.nb.pnlNormData.Layout()
                ######################################### 
                self.enable_normalized_controls(True)
                print "OK"
                status_text= "Pathway analyses have been successfully performed!"
                
                self.view.statusBar.SetStatusText("PACFM: %s"%status_text)
            
            
            else:
                print "Cancel"
                
            ## included pathways are handled in the pathway_controller module
        else:
            print "Select a file first"

    def onCircosPlot(self, e):
        """
            GUI: Runs CIRCOS and displays a modified version of the plot in PACFM.
        """
        hc= HighlightContainer()
        hc.load()
        
        l=LinkContainer()
        l.load()

        p=PlotContainer()
        p.load()

        for ide in self.input_builder.assembler.ideograms:
            p.get_by_index(ide.level-1).min_value= ide.get_min_value()
            p.get_by_index(ide.level-1).max_value= ide.get_max_value()

        
        self.circos_controller = CircosController(self.biodb_selector, p, l, hc)
        if self.normalized:
            self.circos_controller.view.plotType.rbNorm.SetValue(1)
        else:
            self.circos_controller.view.plotType.rbRaw.SetValue(1)
       
        
        
        status_text= "Drawing the plot. Please wait..."
        self.view.statusBar.SetStatusText("PACFM: %s"%status_text)

        response= self.circos_controller.view.ShowModal()
    
        if response ==  wx.ID_OK:   
            plots = self.circos_controller.view.plotType.plots
            links= self.circos_controller.view.links.links
            ### filter links that are not found in the dataset
            #print self.input_builder.assembler.ideograms[l.level-1].names
            for name in links.names:
                if name not in self.input_builder.assembler.ideograms[l.level-1].names:
                    links.remove(name)
            
            highlights= self.circos_controller.view.highlights.highlights
            
            
            self.input_builder.build_circos_inputs_and_run(plots= plots,
                    links= links, highlights= highlights)
            
            d= Drawer(links, plots, self.colorbar_title) 
            result_image= d.get_output_image()
            wx_image= PilImageToWxImage(result_image)
           
            self.view.nb.ChangeSelection(1)
            
            if not self.normalized:
                self.pltRawData= CircosPanel(self.view.nb.pltRawData, wx_image)
                # There should be a simpler pnl.Refresh() method!
                
                self.view.nb.circosBook.ChangeSelection(0)
                
                sizer= wx.BoxSizer()
                sizer.Add(self.pltRawData, 1, wx.EXPAND)
                # 
                self.view.nb.pltRawData.SetSizer(sizer)
                self.view.nb.pltRawData.Layout()
            else:
                
                self.pltNormData= CircosPanel(self.view.nb.pltNormData, wx_image)
                # There should be a simpler pnl.Refresh() method!
                
                self.view.nb.circosBook.ChangeSelection(1)
                
                sizer= wx.BoxSizer()
                sizer.Add(self.pltNormData, 1, wx.EXPAND)
                self.view.nb.pltNormData.SetSizer(sizer)
                self.view.nb.pltNormData.Layout()

            self.circos_controller.view.Destroy()
            
            self.normalized= self.circos_controller.view.plotType.rbNorm.GetValue()     
            status_text= "The PACFM plot has been successfully drawn!"
            self.view.statusBar.SetStatusText("PACFM: %s"%status_text)

### GUI ###





