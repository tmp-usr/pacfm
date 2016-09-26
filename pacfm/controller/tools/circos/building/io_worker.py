import os

from pacfm.model import Karyotype, Abbrator, file_provider
from pacfm.controller import CircosConfigParser

import pdb

class IOWorker(object):
    '''
        ib: ideogrambuilder object instance
        builds circos input files including
        data, text, links, highlights etc.
    '''

    def __init__(self, assembler):
        self.assembler= assembler
        
        karyotype= Karyotype(self.assembler.biodb_selector)
        
        if not os.path.exists(karyotype.output):
            self.karyotype= karyotype.set_karyotype()

        else:
            self.karyotype= karyotype.get_karyotype()


    def build_karyotype(self):
        """
            line = ['chr','-','c_c','Cell Communication','0','725', 'spectral-5-div-1']
        """
        ide= self.assembler.ideograms[0]
        with open(file_provider['circos_config']['karyotype'],'w') as fKaryo:    
            for line in ide.yield_karyotype(self.karyotype):fKaryo.write(line)

    def edit_plots_config(self, plots):
        configParser= CircosConfigParser('plots')
        configParser.parse()
        
        for plot in plots:
            index= "abundance_%s" %plot.level
            prop_values= {}
            if plot.plot_type == "histogram":
                prop_color = "fill_color"
                color = plot.color
                if len(plot.color) == 4 and plot.color[3] > 1:
                    color= list(plot.color)
                    color[3] = 1- (float(color[3]) / 255.0)
                value= ','.join(map(str, color))
                
                prop_values[prop_color] = value
                
                ide = self.assembler.ideograms[plot.level - 1] 
                prop_min_value= "min"
                prop_max_value= "max"

                min_value= ide.get_min_value()
                max_value= ide.get_max_value()
                
                prop_values[prop_min_value]= min_value
                prop_values[prop_max_value]= max_value

            elif plot.plot_type == "heatmap":
                prop_color = "color"
                value= plot.color_scheme
                
                prop_values[prop_color] = value

            
            for prop, value in prop_values.iteritems():
                configParser.set(prop, value, 'plot', 'index', index )


    def build_data(self):
        """
            line = ["c_p", "0", "875","0.0446476272322"]
        """
        for i in range(3):        
            with open(file_provider.abundance(i+1), 'w') as fData:        
                for line in self.assembler.ideograms[i].yield_data(self.karyotype): fData.write(line)


    def build_text(self):
        """

            building the abbreviations. params
            name length
            coordinate length
            font size
            coordinate length that a character occupies.    
            empty space to be left from each side

        """
        #total_units=0
        ### params for ~5000 lines
        coors_between_letters= 50 
        #adjustment_factor= 50
    
        ### params for ~1000 lines
        #total_units=0
        #coors_between_letters= 20 
        #adjustment_factor= 10
        #adjustment_factor= 1
        for i in range(2):
            ide= self.assembler.ideograms[i]
            with open(file_provider.labels(i+1), 'w') as fLabel:    
                for line in ide.yield_text(self.karyotype, coors_between_letters):
                    fLabel.write(line)
    
    
    
    def build_links(self, links, nPathways=None):
        """
            to be updated with the conditionally colored links for different levels

        """

        with open(file_provider.links(links.level),'w') as fOut:
            biodb_selector= self.assembler.biodb_selector
            ide= self.assembler.ideograms[biodb_selector.getLevelCount() - 2 ]
            lines= ide.yield_links(self.karyotype, links, nPathways)
            for line in lines:fOut.write(line)


    def build_pathway_names(self):
        """
        add a pathway abbreviator function to the abbrator. current version
        is not giving coherent names for the pathways!
        """
        ide= self.assembler.ideograms[2]
        with open(file_provider.labels(3), "w") as fPW:
            for line in ide.yield_pathway_names(self.karyotype):fPW.write(line)



    def build_highlights(self, highlights):
        #### assert highlight color is set!
        ide= self.assembler.ideograms[2]

        with open(file_provider['circos_data']['highlights'], 'w') as fHL:     
            for line in ide.yield_highlights(self.karyotype):fHL.write(line)
            trash="""
            
            for i in range(len(highlights)):
                highlight= highlights.get_by_index(i)
                level= highlight.level
                """
