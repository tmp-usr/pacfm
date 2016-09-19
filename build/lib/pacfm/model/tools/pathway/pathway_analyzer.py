import pickle
import os
import subprocess

from pandas import DataFrame
from pacfm.model import file_provider

class PathwayAnalyzer(object):
   
    def __init__(self, biodb_selector, input_builder): # hierarchical_abundance_data,
        self.biodb_selector= biodb_selector
        self.input_builder= input_builder
        
        ### ideograms should be copied
        self.ideograms= input_builder.assembler.ideograms
        
        #self.hier_df_fantom= hierarchical_abundance_data
        self.update_dataframe()

    #def filter_pathways_by_level(self, pathway_list, level):
    #    self.fam_hier[level]

    def update_dataframe(self):
        self.data_frame= self.input_builder.assembler.to_data_frame()

    def get_dataframe(self):
        return self.data_frame

    def filter_pathways_by_key_leaf_features(self, key_type,  nPathways=1000, pathway_key_ids= None, remove_feature= False):
        """
            ideograms
            
            0: any
            1: all
            2: manual (key enzyme selection)
            3: association


            pathway_keys: dictionary of pathways as keys and coordinate_lists as values
            nPathways: the number of maximum number of association that a key enzyme is
            restricted by.
        """
        ide= self.ideograms[-1]
        
        for pathway in ide.chromosomes:
            
            key_feature_ids= None
            if pathway_key_ids is not None:
                if pathway.name in pathway_key_ids:
                    key_feature_ids= pathway_key_ids[pathway.name]
                
            pathway.filter_coordinates_by_key_features(key_type, nPathways, key_feature_ids, remove_feature)
            
            if remove_feature:
                filtered_link_features= pathway.get_filtered()
            else:
                filtered_link_features= pathway.get_null_features()

            
            for feature in filtered_link_features:
                ide.filter_links_by_feature(feature)
        
        
        #remove the link coordinates from the ide
        
        self.update_dataframe()


        
    ### pathway object should have an attribute called 
    #   db_features: including total sequence length and total number of proteins
    #   pathway_container object should potentially keep the dump


    def set_pathway_info(self):
        for ide in self.ideograms:
            ide.load_db_data()
        
        self.update_dataframe()
       
    def update_ideograms_by_dataframe(self, dataframe):
        for ide in self.ideograms:
            ide.update_by_dataframe(dataframe)

    def update_ideograms_by_pathways(self, pathways):
        for ide in self.ideograms:
            ide.update_by_pathways(pathways)


    def normalize_by_pathway(self, pathway_feature, level=3): 
        """
            pathway_feature can be n_protein or sequence_lenght
        """
        self.set_pathway_info()

        pathway_factor= {c.name: c.db_data[pathway_feature] for c in self.ideograms[level-1].chromosomes}
        nLevels= self.biodb_selector.getLevelCount()
        
        df_lengths= DataFrame(pathway_factor.items(), index= range(len(pathway_factor)), columns=["Level %s" % level,"Length"])
        #return df_lengths
        ## by merging acording to the lengths dataframe, we also 
        ## filter the main dataframe in the meanwhile
        
        df_merged= df_lengths.merge(self.data_frame, on= "Level %s" % level)
        ### columns have one extra level for accession and one more
        ### for the lengths in df_merged
        
        df_merged[self.data_frame.columns[nLevels+1:]]=  df_merged[self.data_frame.columns[nLevels+1:]].divide(df_merged['Length'].values, axis= 0)
        
        df_normalized= df_merged[self.data_frame.columns]       
        self.update_ideograms_by_dataframe(df_normalized)
        self.update_dataframe()

    def normalize_by_algorithm(self, algorithm):
        """
            fam
        """

        if algorithm == 'minpath':
            
            if not self.biodb_selector.db_name.lower().startswith('kegg'):
                raise Exception('MinPath algorithm is only designed for the KEGG database!')
       
            minpath_file= file_provider['minpath']['input']
            with open(minpath_file, 'w') as fIn:
                accessions= set(self.data_frame['Accession'])
                for k,v in zip(range(len(accessions)), accessions):
                    fIn.write('%s\t%s\n'%(k,v))
                
            
            
            
            minpath_program= file_provider['minpath']['bin']
            minpath_output= file_provider['minpath']['output']
            
            
            cmd= 'python %s -ko %s -report %s' % (minpath_program, minpath_file, minpath_output)
            run_cmd(cmd)
            
            Pathways={}
            Discarded= {}
            with open(minpath_output) as minOut:
                for line in minOut:
                    cols= line.rstrip('\n').split()
                    
                    minp= cols[6]
                    test= int(cols[7])
                    
                    name= ' '.join(cols[13:]).lower()
                    accession= cols[1].strip() 
                    try:
                        pathway_id= self.biodb_selector.getFeatureByAccession(unicode(accession)).id
                    except:
                        print accession, "not found" 
                        continue

                    if test:
                        Pathways[pathway_id]=1
                    else:
                        Discarded[pathway_id]=1
            
            pathways= Pathways.keys()
            discarded= Discarded.keys()
            self.update_ideograms_by_pathways(pathways)
            self.update_dataframe()

def run_cmd(cmd):
    p = subprocess.Popen(cmd, shell= True, stdout=subprocess.PIPE)
    #ret_code = p.wait()
    output = p.communicate()[0]
    #print output
    return output
                    


#write ide updater functions for the normalization functions


trash= """



    def normalize_by_orthologous_sequence_length(self, Orth_sequence_lengths): 
        '''
            
           !!! skip this!!!
           !!! - instead of dividing by the enzyme length of each ko
           !!! get the total sequence length of enzymes required in a
           !!! pathway!!!

        '''
        nLevels= self.biodb_selector.getLevelCount()
        df_lengths= DataFrame(Orth_sequence_lengths.items(), index= range(len(Orth_sequence_lengths)), columns=["Accession","Length"])
        ## by merging acording to the lengths dataframe, we also 
        ## filter the main dataframe in the meanwhile
        df_merged= df_lengths.merge(self.data_frame, on= "Accession")
        ### columns have one extra level for accession and one more
        ### for the lengths in df_merged
        df_merged[self.data_frame.columns[nLevels+1:]]=  df_merged[self.data_frame.columns[nLevels+1:]].divide(df_merged['Length'].values, axis= 0)
        return df_merged[self.data_frame.columns]

             




"""
