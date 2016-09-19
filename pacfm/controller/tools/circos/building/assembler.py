from collections import OrderedDict

from pandas import DataFrame 

from pacfm.model import Coordinate, Chromosome, Ideogram
from pacfm.model import LinkCoordinate

import pdb


class Assembler(object):
    """
        assembles the circos abundance map structure.
        biodb_selector: biodb.Selector instance
        abundance: dictionary of keys= accessions, values= abundances 
    """


    def __init__(self, biodb_selector, abundance, calculation_type):
        self.biodb_selector= biodb_selector
        self.abundance= abundance

        self.n_levels= self.biodb_selector.getLevelCount()
        n_of_ideograms= self.n_levels - 1
        
        self.assembly= self.ideograms= [None] * n_of_ideograms 
        
        self.calculation_type= calculation_type
        self._init_ideograms()
        
        

    def _init_ideograms(self):

        for i in range(len(self.ideograms)):
            self.ideograms[i] = Ideogram(i+1, calculation_type= self.calculation_type) 


    def construct_base_ideogram(self):
        
        enzymes= self.abundance.keys()
        
        ide= self.ideograms[self.biodb_selector.getLevelCount()-2]
        
        link_coordinates= {}
        
        for e in enzymes:
            biodb = self.biodb_selector.getFeatureByAccession(unicode(e))
            if not biodb:
                continue
           
            parents= self.biodb_selector.getParentsByChildID(biodb.id)
            lc= LinkCoordinate(biodb)
            for parent in parents:
                c= Coordinate(biodb)
                c.set_value(self.abundance[e])
                if parent.name not in ide.names:
                    ide.append(Chromosome(parent, self.biodb_selector))
                lc.add(c)
                
                chromosome= ide[parent.name]
                chromosome.append(c)
            
            link_coordinates[biodb.id]= lc
        
        ide.set_link_coordinates(link_coordinates)
        
        return ide



    def assemble_ideograms(self):
        
        base_ide=self.construct_base_ideogram()
        self.ideograms[base_ide.level-1]= base_ide
        
        for i in range(len(self.ideograms)-1, 0, -1):

            ide= self.ideograms[i] 
            
            chromosomes= ide.get_all()
            
            for chrom in chromosomes:
                parents= [self.biodb_selector.getParentsByChildID(chrom.id)[0]]
                
                for parent in parents:
                    curIde= self.ideograms[parent.level -1]
                    
                    if parent.name not in curIde.names:
                        newChrom= Chromosome( parent, self.biodb_selector )
                        newChrom.append_coordinates( chrom.get_coordinates() )
                        curIde.append( newChrom  )
                        chrom.append_parent(newChrom)
                    
                    else:
                        myChrom= curIde[parent.name]
                        myChrom.append_coordinates( chrom.get_coordinates() )
                        chrom.append_parent(myChrom)
                    
        


    def proof_read_coordinates(self):
        for ide in self.ideograms:
            coors= ide.get_all_coordinates()
            print ide.level, len(coors)
    
    def to_data_frame(self):
        ideogram= self.ideograms[-1]
        return ideogram.to_dataframe()
        

