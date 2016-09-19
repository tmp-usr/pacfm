#import os
#import sys

from biodb.sqling.selector import Selector

from pacfm_base import PacfmBase

from pacfm.model import LinkContainer, HighlightContainer, PlotContainer
from pacfm.model import PathwayAnalyzer
from pacfm.model import file_provider  

from pacfm.controller import InputBuilder, CircosController, Drawer
from pacfm.controller import PathwayController
from pacfm.controller import PilImageToWxImage

class PacfmCL(PacfmBase):
    """
        Commandline interface for PACFM.
    """
    def __init__(self, pw_length=False, pw_sequence=False, pw_minpath=False, pw_key_enzyme=-1, n_association=1000, input_file_path="", output_figure_path="pacfm.png", output_table_path="pacfm.tsv", output_type=0, info_types=[],  abbreviations_path= "abbreviations.txt", links_path= "links.txt", key_enzymes_path="key_enzymes.txt", calculation_type= "sum", db_name="kegg_orthology", colorbar_title= "Relative abundance"):
        PacfmBase.__init__(self, normalized= False, pw_length= pw_length, pw_sequence= pw_sequence, pw_minpath= pw_minpath, pw_key_enzyme= pw_key_enzyme, n_association= n_association, input_file_path= input_file_path, output_figure_path= output_figure_path, output_table_path= output_table_path, output_type= output_type, info_types= info_types,  abbreviations_path= abbreviations_path, links_path= links_path, key_enzymes_path=key_enzymes_path, calculation_type= calculation_type, db_name= db_name, colorbar_title= colorbar_title )

        


    def init_variables(self, **kwargs):
        """
            overriden method
        """
        ###
        self.pw_length= kwargs['pw_length'] 
        self.pw_sequence= kwargs['pw_sequence'] 
        self.pw_minpath= kwargs['pw_minpath']
        self.pw_key_enzyme= kwargs['pw_key_enzyme']
        ###
        self.n_association= kwargs['n_association']
        ###
        self.input_file_path= kwargs['input_file_path']
        self.output_figure_path= kwargs['output_figure_path']
        self.output_table_path= kwargs['output_table_path']
        ###
        self.output_type= kwargs['output_type']
        ###
        self.info_types= kwargs['info_types']
        self.abbreviations_path= kwargs['abbreviations_path']
        self.links_path= kwargs['links_path']
        self.key_enzymes_path= kwargs['key_enzymes_path']
        ###
        self.calculation_type= kwargs['calculation_type']
        self.db_name= kwargs['db_name'] 
        self.colorbar_title= kwargs['colorbar_title']


### COMMANDLINE SPECIFIC ###
    
    def init_project(self):

        self.biodb_selector= Selector(self.db_name)
        self.input_builder= InputBuilder(biodb_selector= self.biodb_selector, fam_path= self.input_file_path, calculation_type= self.calculation_type)
    
    
    def normalize_pathways(self):
        """
            Runs the pathway analysis options.
        """
        
        if self.input_builder:
            self.pw_analyzer= PathwayAnalyzer(self.biodb_selector, self.input_builder)
            #####
            if self.pw_length:
                print "normalizing by sequence length"
                self.pw_analyzer.normalize_by_pathway('sequence_length')
            
            if self.pw_sequence:
                print "normalizing by the number of proteins/enzymes in the pathway"
                self.pw_analyzer.normalize_by_pathway('n_protein')
            
            if self.pw_minpath:
                print "normalizing by the minpath algorithm"
                self.pw_analyzer.normalize_by_algorithm('minpath')
            
            if self.pw_key_enzyme >= 0:
                key_enzyme_type= self.pw_key_enzyme
                if key_enzyme_type == 0 or key_enzyme_type == 1:
                    self.pw_analyzer.filter_pathways_by_key_leaf_features(key_enzyme_type)
            
                ### key_enzyme_type 2 is disabled in the commandline version. 
                elif key_enzyme_type == 3:
                    assert self.n_association >= 0, "You have not set the criteria for the numnber of pathway associations."
                    print "Running the pathway association check. Please wait..."
                    self.pw_analyzer.filter_pathways_by_key_leaf_features(3, self.n_association)
            
            self.data_frame= self.input_builder.assembler.to_data_frame()
            
            ######################################### 
            print "OK"
            
        else:
            print "Select an input file first"

    
    def plot_circos(self):
        """
            Draws the final plot!
        """
        if self.output_type == 0 or self.output_type == 2: 
            h= HighlightContainer()
            h.load()
            
            l=LinkContainer()
            l.load()

            p=PlotContainer()
            p.load()

            for ide in self.input_builder.assembler.ideograms:
                p.get_by_index(ide.level-1).min_value= ide.get_min_value()
                p.get_by_index(ide.level-1).max_value= ide.get_max_value()
            
            self.input_builder.build_circos_inputs_and_run(plots= p, links= l, highlights= h)
            
            d= Drawer(l, p, self.colorbar_title) 
            self.result_image= d.get_output_image()


### info ###
    def save_abbreviations(self):
        if not self.normalized:
            ideograms= self.input_builder.assembler.ideograms
        else:
            ideograms= self.pw_analyzer.ideograms

        for ide in ideograms:
            if ide.level not in self.level_abbreviations:
                self.level_abbreviations[str(ide.level)]= ide.abbreviations
        
        with open(self.abbreviations_path, 'w') as outfile:
            for level in xrange(1,4):
                line1= "##### LEVEL %s #####\n" %level
                outfile.write(line1)
                for k, v in self.level_abbreviations[str(level)].iteritems():
                    line2= "%s: %s\n" %(k,v) 
                    outfile.write(line2)

    def save_key_enzyme_info(self):
        """
            Saves the key enzymes into a file."
        """
        if not self.normalized:
            ide= self.input_builder.assembler.ideograms[-1]
        else:
            ide= self.pw_analyzer.ideograms[-1]
        
        for chrom in ide.chromosomes:
            self.key_enzymes[chrom.name]= [f.name for f in chrom.get_non_null_features()]  
        
        
        with open(self.key_enzymes_path, 'w') as outfile:
            for k, v in self.key_enzymes.iteritems():
                line= "%s: %s\n" %(k, ', '.join(v)) 
                outfile.write(line)

    def save_link_info(self): 
        """
            Saves the pathway assoication info into a file.
        """
        if not self.normalized:
            ide= self.input_builder.assembler.ideograms[-1]
        else:
            ide= self.pw_analyzer.ideograms[-1]
        
        for id, link_coordinate in ide.link_coordinates.iteritems():
            feature= self.biodb_selector.getFeatureByID(id) 
            pws= [coor.get_name_by_level(ide.level) for coor in link_coordinate.coordinates]
            self.enzyme_pathway_link[feature.name] = pws
        
        with open(self.links_path, 'w') as outfile:
            for k, v in self.enzyme_pathway_link.iteritems():
                line= "%s: %s\n" %(k, ', '.join(v)) 
                outfile.write(line)
 
    def save_info(self):
        """
            Saves selected info types into files.
        """
        if "abbreviations" in self.info_types:
            self.save_abbreviations()
        if "links" in self.info_types:
            self.save_link_info()
        if "key_enzymes" in self.info_types:
            self.save_key_enzyme_info()
### info ###       

### output ###
    def save_data(self):
        self.data_frame.to_csv(self.output_table_path, sep= "\t", index_label="Index")
        
    def save_plot(self):
        self.result_image.save(self.output_figure_path)
        self.result_image.close()
   
    def save_output(self):
        if self.output_type == 0:
            self.save_plot()
        elif self.output_type == 1:
            self.save_data()
        elif self.output_type == 2: 
            self.save_plot()
            self.save_data()
### output ###
