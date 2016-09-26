from collections import OrderedDict
from itertools import permutations,combinations
from copy import deepcopy

import wx
import numpy as np
from pandas import DataFrame

from feature import Feature, Pathway, PathwayContainer
from pacfm.model.helper import Abbrator

import pdb

class Coordinate(Feature):
    '''
     basic class of the lowest hierachy level in biological databases
     typically referring to enzymes or proteins.
     levels: (start, end) pair of coordinates at each level 


     !!! a drastic change: the name hier is replaced by parent_hier
    '''
    def __init__(self, biodb, step_size=5, levels=[], name_hier=[], parent_hier=[]):
        Feature.__init__(self, biodb= biodb)
        self.step_size= step_size
        
        if parent_hier == []:
            parent_hier=[None]*3
        self.parent_hier= parent_hier
        
        if levels == []:
            levels=[None]*3
        
        self.levels= levels
        self.links=[]

    def get_coordinate(self):
        return self.levels[0]

    def get_coordinate_by_level(self,level):
        if level > 0:        
            return self.levels[level-1]
    
    def set_coordinate_by_level(self, level, start):
        if level > 0:
            self.levels[level-1]= (start, start+self.step_size)        
    
    def get_name_by_level(self, level):
        return self.get_parent_by_level(level).name

    def set_parent_by_level(self, level, parent):
        if level > 0:    
            self.parent_hier[level-1]=parent
    
    def get_parent_by_level(self, level):
        if level > 0:
            return self.parent_hier[level-1]
    
    def add_link(self, coordinate):
        self.links.append(coordinate)

class Chromosome(Pathway):
    '''
     functional group representing a pathway or a higher level category. ideograms are composed of an ordered list of chromosomes.
    '''
    def __init__(self, biodb, biodb_selector, end= 0):
        '''
        children attribute of the pathway class and coordinate_list are different attributes. children are basically pathways and coordinate_list elelments are coordinates.

        '''
        Pathway.__init__(self, biodb= biodb, biodb_selector= biodb_selector ) 
        self.included= True
        self.end=end
    
    def _init_coordinate_list(self):
        for feature in self.leaf_features:
            self.append(Coordinate(feature))

    def get_included(self):
        if self.level > 1:
            if self.parents[0].get_included():
                return self.included
            else:
                return self.parents[0].get_included()
        else:
            return self.included

        
    def set_included(self, included):
        if self.level > 1:
            if self.parents[0].get_included(): 
                self.included = included
            else:
                self.included= False
        else:
            self.included= included

    def filter_coordinate(self, feature):
        self.filtered.append(feature)
        self.leaf_features.remove(feature)
   

    def filter_coordinate_by_id(self, feature_id):
        for feature in self.leaf_features:
            if feature.id == feature_id:
                self.filter(feature)


    def append_coordinates(self, coordinates):
        """
        overridden function

        """
        for feature in coordinates:
            self.append(feature)    

    def append(self, coordinate):
        """
        overridden function       
        previously known as append_coordinate
        """
        coordinate.set_coordinate_by_level(self.level, self.end)
        coordinate.set_parent_by_level(self.level, self)
    
        self.set_end(self.end + coordinate.step_size) 
        self.leaf_features.append(coordinate)


    def filter_coordinates_by_key_features(self, key_type, nPathways=1000, key_feature_ids= None, remove_feature= False):
        """
            ideograms
            
            0: any
            1: all
            2: manual (key enzyme selection)
            3: association


            key_biodbs: dictionary of pathways as keys and coordinate_lists as values
            nPathways: the number of maximum number of association that a key enzyme is
            restricted by.
        """
        if key_type is 0:
            self.filtered= []
        
        elif key_type is 1:
            # get all leaf features. check if they are equal to the present features!
            self.leaf_features+= self.filtered
            self.filtered= []

            all_leaf_features= self.biodb_selector.getChildrenByParentID(self.id, self.level)
            all_leaf_feature_ids= sorted([f.id for f in all_leaf_features])
            leaf_feature_ids= sorted([f.id for f in self.leaf_features])
            if all_leaf_feature_ids != leaf_feature_ids:
                for feature_id in leaf_feature_ids:
                    self.filter_by_id(feature_id, remove_feature)
        
        elif key_type is 2:
            ## even though it says key leaf feature, we are dealing with coordinates
            ## in this context; so we gotta initiate coordinates.
            self.leaf_features+= self.filtered
            self.filtered= []

            present_feature_ids= [f.id for f in self.leaf_features]
            filtered_present_feature_ids= list(set(present_feature_ids).difference(set(key_feature_ids)))
            
            for feature_id in filtered_present_feature_ids:
                self.filter_by_id(feature_id, remove_feature)
            
            
        elif key_type is 3:
            self.leaf_features+= self.filtered
            self.filtered= []
            key_feature_ids= [f.id for f in self.biodb_selector.getUniqueEnzymesByPathwayLimit(self, nPathways)]
            present_feature_ids= [f.id for f in self.leaf_features]
            
            filtered_present_feature_ids= list(set(present_feature_ids).difference(set(key_feature_ids)))

            for feature_id in filtered_present_feature_ids:
                self.filter_by_id(feature_id, remove_feature)
   
    def append_child(self,chromosome):
        coors =  chromosome.get_all_coordinates()
        for coor in coors:
            start = self.get_end()
            coor.set_coordinate_by_level(self.level, start)
            coor.set_parent_by_level(self.level, self)
            self.append_coordinate(coor)
    
    def get_coordinates(self):return self.leaf_features

    
    def get_end(self):return self.end
    def set_end(self, end):self.end= end

    def get_coordinate_on_karyotype(self):
        firstCoor= self.leaf_features[0]
        start= firstCoor.get_coordinate_by_level(1)[0]
        lastCoor= self.leaf_features[-1]
        end= lastCoor.get_coordinate_by_level(1)[1]
        return  start, end

    def get_karyotype_name(self):
        firstCoor= self.leaf_features[0]
        return firstCoor.get_name_by_level(1)


    def setCoordinatesFromChildren(self):
        pass


    def getCoordinateByLeafFeature(self):
        pass
  
    def getCoordinateByLeafFeature(self, leafFeature):
        pass
    



class Ideogram(PathwayContainer):
    '''

    object covering all functional groups at a level of a biological database, refering to the circular plots in a circos plot.
        
    data file generation should be performed over one level of the ideograms since the coordinates and names are kept in all hier level ideograms.
    
    
    '''
    def __init__(self, level, calculation_type= "sum"):
    
        PathwayContainer.__init__(self, level= level, calculation_type= calculation_type)

        self.level=level
        self.link_coordinates= {}
        self.filtered_links={}
        self.abbreviations= {}
         

    @property
    def chromosomes(self): 
        return self.get_all()

    def get_all_coordinates(self):
        all_coors=[]
        for chrom in self.pathways:
            all_coors+=chrom.get_coordinates()
        return all_coors
   

    def test_continuity(self):
        coors= self.get_all_coordinates()
        for coor in coors:
            if all(coor.levels):
                pass
   
    def set_link_coordinates(self, link_coordinates):
        assert self.level == 3, "Set only for the base ideogram!"
        self.link_coordinates= link_coordinates


    def filter_links_by_feature(self, feature):
        if feature.id in self.link_coordinates:
            self.filtered_links[feature]= self.link_coordinates[feature.id]
            del self.link_coordinates[feature.id]


    def to_dataframe(self):
        coors= self.get_all_coordinates()
        
        n_levels= self.chromosomes[0].biodb_selector.getLevelCount()
        
        assert self.level == n_levels -1, "This function is intended for the pathway level only!"
        
        frame= []
        index= []
        columns= ['Level %s' % (i+1) for i in range(n_levels-1)]
        columns+= ['Protein/enzyme','Accession', 'Value']
        
        j=0
        for coor in  coors:
            j+=1
            index.append(j)
            cols= [coor.get_name_by_level(k) for k in range(1,4)]
            cols+= [coor.name, coor.accession, coor.get_value()]
            frame.append(cols)
        
        return DataFrame(data= frame, index= index, columns= columns)
    

    def update_by_dataframe(self, dataframe):
        coors = self.get_all_coordinates()
        for coor in coors:
            if coor.accession in dataframe['Accession'].tolist() :
                subset= dataframe[dataframe['Accession'] == coor.accession]
                for i in subset.index:
                    if subset.ix[i]['Level 3'] == coor.get_parent_by_level(3).name:
                        coor.set_value(subset.ix[i]['Value'])
            
            else:
                coor.set_value(0)



    def update_by_pathways(self, pathway_ids, level= 3):
        """
            ids can be biodb_ids, accessions or names 
        """
        coors= self.get_all_coordinates()
        discarded= {}
        kept= {}
        
        for coor in coors:
            pathway_id= coor.get_parent_by_level(level).id
            
            if not pathway_id in pathway_ids:
                coor.set_value(0)
                discarded[pathway_id] = 1
                if coor.id in self.link_coordinates:
                    self.link_coordinates[coor.id].remove(coor)
            else:
                kept[pathway_id] = 1


    def yield_data(self, karyotype):
        """
            self.karyotype
        """
        for chrom in self.chromosomes:
            start, end= chrom.get_coordinate_on_karyotype()
            karyotype_name= chrom.get_karyotype_name()
            
            if self.calculation_type == "sum":
                value= chrom.get_unique_total_value()
            elif self.calculation_type == "average":
                value= chrom.get_unique_average_value()
            
            line= [karyotype[karyotype_name], str(start), str(end), "%.2g" %value ] 
            
            if value < 0:
                line.append("fill_color=lblue")

            yield "\t".join(line)+"\n"

        
        if len(self.chromosomes) == 1:
            line= ["h", str(0), str(2), "0"]
            yield "\t".join(line) + "\n" 


    def yield_text(self, karyotype, coors_between_letters=100):
        """
            self.karyotype
            Abbrator
        """
        ### below parameters are related to the karyotype size!!1
        ### TODO adjust them accordingly!!!!

            ### factors: directionality, color
            ### 
            #" current problems: 
            #    1 highlights and text coordinates do not match with the heatmap coordinates. check it out
            #    2 spaces between words should not take 3 times the siz of an empty character.
            #    3 ....
        coor_step_size= 5
        
        total_coordinate_len= len(self.get_all_coordinates())
        total_ideogram_len= total_coordinate_len * coor_step_size
        ### broadest level will fit more letters.
        if self.level == 1:
            total_letters= 190
        elif self.level == 2:
            total_letters= 180
        
        ### total number of letters that an ideogram (circle) can fit
        #total_letters= 180
        
        ### length of a character in coordinate units
        char_len=  total_ideogram_len / total_letters  


        
        if self.calculation_type == "sum":
            values= sorted([chrom.get_unique_total_value() for chrom in self.chromosomes])
            #global_total_value= self.get_total_value()
       
        elif self.calculation_type == "average":
            values= sorted([chrom.get_unique_average_value() for chrom in self.chromosomes])
            #global_total_value = self.get_average_value()

        heat_stop_1= int(0.8* len(self.chromosomes))
        heat_stop_2= int(0.5* len(self.chromosomes))
        threshold1= values[heat_stop_1]
        threshold2= values[heat_stop_2]
        ### avg does not work in our case. check what are the light
        ### colors and what are the dark colors in the circos coloring
        ### scheme. in worst case, color dark if the abundance level s
        ### lower than 2/3 instead of averadge. 


        for chrom in self.chromosomes:
            
            name= chrom.name
            
            coordinate_len= len(chrom.get_coordinates())
            chromosome_len= coordinate_len * coor_step_size

            allowed_char_n = int(chromosome_len / char_len) 
            
            abbr_pathway= Abbrator(name, allowed_char_n).abbr
            karyotype_name= chrom.get_coordinates()[0].get_name_by_level(1).strip()
            ### there is enough space after the abbreviation for sure
            self.abbreviations[name] = abbr_pathway

            ### center the label in the ideogram


            ### update the pathway abbreviation according to blank penalty rules
            abbr_pathway= abbr_pathway.replace('.', '')

            free_space= chromosome_len - (len(abbr_pathway) * char_len)
            free_coors= free_space / coor_step_size 
            init_coor= free_coors / 2 
            
            if init_coor < 0 : init_coor= 0
            
            options= ""
           

            
            if self.calculation_type == "sum":
                total= chrom.get_unique_total_value()

            elif self.calculation_type == "average":
                total= chrom.get_unique_average_value()
                
            
            if total < threshold2:
                color = "vdgrey"
           
            elif total >= threshold2 and total < threshold1:
                color= "vvdgrey"

            else:
                color = "white"

            option1= "color=%s" %color
            ## below options did not work
            
            #option2= "label_snuggle=yes" 
            #option3= "label_parallel=no"
            #options= ",".join([option1, option2, option3])
            options= option1


            blank_penalty= 0

            for i in range(len(abbr_pathway)):
                #coor_index= int(init_coor) + int(i * char_len / coor_step_size)
                coor_index= int(init_coor) + (int(init_coor) + int(i * char_len)) / coor_step_size
               
                #if self.level == 2:

                #    pdb.set_trace()
                
                coor= chrom.get_coordinates()[coor_index] 
            
                letter= abbr_pathway[i] 
                
                if letter == " ":
                    blank_penalty+=1
                    
                    #line = [karyotype[karyotype_name], str(startCoor), 
                    #        str(startCoor + int(char_len)), letter, options]

                    #yield "\t".join(line)+'\n'


                else:
                    
                    #if letter == ".":
                    #    blank_penalty += 1
                    #    continue
                    penalty= blank_penalty * int(char_len) / 3
                    crs= coor.get_coordinate()
                    ### we have to also update the init_coor accordingly
                    startCoor= crs[0] - int(penalty) 
                    
                    
                    line = [karyotype[karyotype_name], str(startCoor), 
                            str(startCoor + int(char_len)), letter, options]

                    yield "\t".join(line)+'\n'



    def yield_highlights2(self, karyotype, highlight):
        highlighted_pathway_names= map(unicode.lower, highlight.pathways)
        for chrom in self.chromosomes:
            crs= (chrom.get_coordinates()[0],chrom.get_coordinates()[-1])
            if chrom.name.lower() in highlighted_pathway_names:
                karyotype_name= crs[0].get_name_by_level(1)
                coor= (crs[0].get_coordinate()[0], crs[1].get_coordinate()[1])
                
                option="fill_color=" 

                if type(highlight.color) is str:
                    option+= "%s" % highlight.color
                
                elif type(highlight.color) is wx.Colour:
                    color= list(highlight.color.Get(True))
                    color[3] = 1- (color[3] / 255.0)
                    option+= "%s" % ','.join(map(str, color))
                elif type(highlight.color) is tuple or type(highlight.color) is list:
                    if len(highlight.color) == 4 and highlight.color[3] > 1:
                        color= list(highlight.color)
                        color[3] = 1- (color[3] / 255.0)
                    
                    option+="%s" % ','.join(map(str, color))
                

                line= map(str, [karyotype[karyotype_name], coor[0], coor[1], option])
                
                yield '\t'.join(line) + "\n"   



    def yield_highlights(self, karyotype):
        for coor in self.get_all_coordinates():
            karyotype_name= coor.get_name_by_level(1)
            option="fill_color=" 
            
            if coor.value > 0:
                option += "255,0,0,0.6"

            else:
                option+= "0,0,255,0.6"
            
            
            line= map(str, [karyotype[karyotype_name], coor.get_coordinate()[0], coor.get_coordinate()[1], option])
            
            yield '\t'.join(line) + "\n"   



    def yield_karyotype(self, karyotype):
        assert self.level == 1, "Karyotype file can only be built for the top level." 
        line = ['chr','-','c_c','Cell_Communication','0','725', 'spectral-5-div-1']
        
        ### if there s only one chromosome create a hypothetical one
        ##### very unpythonic but it's too late to quench the root of the circular import evil.    
        from pacfm.controller import CircosConfigParser
        ccp= CircosConfigParser("conf")
        ccp.parse()
        chromosomes= []

        for chromosome in self.chromosomes:
            name= chromosome.name
            line[2] = karyotype[name]
            line[3] = name.replace(' ','_')
            line[5] = str(chromosome.get_end())
            chromosomes.append(karyotype[name])
            yield "\t".join(line)+ "\n"
       
        if len(self.chromosomes) == 1:
            name= "Hypothetical"
            abbr= "h"
            end= "2"
            line[2]= abbr
            line[3]= name
            line[5]= end
            chromosomes.append(abbr)
            yield "\t".join(line) +"\n"
   
        
        ccp.set("chromosomes", ";".join(chromosomes))
        ccp.write() 

    def yield_pathway_names(self, karyotype):
        for chromosome in self.chromosomes:
            name= Abbrator(chromosome.name, 15, upper= False, pathway=True).abbr
            name= name.capitalize()
            self.abbreviations[chromosome.name] = name 
            coors= chromosome.get_coordinates()
            first= coors[0].get_coordinate()[1]
            karyotype_name= coors[0].get_name_by_level(1)
            last=  coors[-1].get_coordinate()[1]
            coor= (first + last)/2
            line= map(str, [karyotype[karyotype_name], coor, coor, name])              
            yield "\t".join(line)+"\n"
        

    def yield_links(self, karyotype, links, nPathways):
        
        biodb_selector= self.get_by_index(0).biodb_selector
        level= links.level
        link_names= map(unicode.lower, links.names) 
        for feature_id, link_coordinate in self.link_coordinates.iteritems():
            
            for i,j in permutations(link_coordinate.coordinates, 2):
                if nPathways: 
                    if not biodb_selector.isUniqueFeature(i.feature, nPathways):
                        continue
                    
                name= i.get_name_by_level(level)
                if name.lower() in link_names:    
                    c1= i.get_coordinate_by_level(1)
                    c2= j.get_coordinate_by_level(1) 
                    
                    ide1= i.get_name_by_level(1)
                    ide2= j.get_name_by_level(1)
                    
                    n1= karyotype[ide1]
                    n2= karyotype[ide2]

                    link= links[name]
                   
                    option= ""
                    if type(link.color) is str:
                        option+= "color=%s" % link.color
                    
                    elif type(link.color) is wx.Colour:
                        color= list(link.color.Get(True))
                        color[3] = 1- (color[3] / 255.0)
                        option+= "color=%s" % ','.join(map(str, color))
                    
                    elif type(link.color) is tuple or type(link.color) is list:
                        color= link.color 
                        if len(link.color) == 4 and link.color[3] > 1:
                            color= list(link.color)
                            color[3] = 1- (float(color[3]) / 255.0)

                        option+= "color=%s" % ','.join(map(str, color))

                    
                    option+= ",z=%i" %link.z_index
                    
                    line= map(str, [ n1, c1[0] , c1[1], n2, c2[0], c2[1], option]  )
                    yield "\t".join(line)+'\n'




    def getCoordinatesByChromosomeName(self, cName):
        pass

    def setChromosomeDict(self, cDict):
        pass


class LinkCoordinate(object):
    def __init__(self, feature, coordinates=None):
        self.feature = feature
        if not coordinates:
            self.coordinates=[] 
    
    def add(self, coordinate):
        self.coordinates.append(coordinate)

    def remove(self, coordinate):
        self.coordinates.remove(coordinate)


