import os, pickle
import math

from biodb.sqling.storm_objects import BioDB

import pdb


class Feature(BioDB):
    def __init__(self, biodb, value= 0, relative_abundance= 0.0):
        BioDB.__init__(self, biodb.id, biodb.accession, biodb.name, biodb.level)
        self.value= value
        self.relative_value= relative_abundance
        self.is_key= False

    def __repr__(self): return self.name
    def __str__(self): return self.name

    def get_value(self):return self.value
    def set_value(self, value):self.value= value

    def set_key(self, iskey): self.is_key= iskey


class Pathway(Feature):
    """
    Pathway model.
    leaf_features= feature list from the database
    present_leaf_features= leaf_features found in the sample
    for practical purposes, I decided to ommit assigning leaf
    features to chromosomes and assume leaf features and present
    leaf features refer to the same list.
    key_leaf_features= leaf_features set by the user


    children: Pathways
    parent: Pathway
    container: PathwayContainer equivalent of a level object
    """
    def __init__(self, biodb, biodb_selector, present_leaf_features=[], key_leaf_features=[], children= [], container= None):
        Feature.__init__(self, biodb= biodb)
        
        self.biodb_selector= biodb_selector
        
        self.leaf_features= []
        self.present_leaf_features= self.leaf_features
        
        if key_leaf_features == []:
            self.key_leaf_features= present_leaf_features
        else:
            self.key_leaf_features= key_leaf_features
       
        # remember to uncomment this line
        #self._init_pathway()

        
        self.children= children 
        self.parents= []
        self.container= container
        self.filtered= []
        self.db_data = {}
        

    def _init_pathway(self):
        biodb_features= self.biodb_selector.getLeafNodesByParent(self, self.biodb_selector.getLevelCount())
        self.leaf_features= [Feature(f) for f in biodb_features]

    #def __repr__(self):return ';'.join([f.name for f in self.leaf_features])
    def __repr__(self):return self.name
    def __str__(self):return self.name
    
    def __len__(self):return len(self.children)       
 
    def __getitem__(self, index):
        return self.leaf_features[index]

    def __iter__(self):
        return (feature for feature in list.__iter__(self.leaf_features))

    
    def filter(self, feature, remove=False):
        
        if remove:
            self.filtered.append(feature)
            self.leaf_features.remove(feature)
        else:
            feature.set_value(0)

    def filter_by_id(self, feature_id, remove=False):
        for feature in self.leaf_features:
            if feature.id == feature_id:
                self.filter(feature, remove)

    def get_filtered(self):return self.filtered
    def get_null_features(self):return [f for f in self.leaf_features if f.get_value() == 0]
    def get_non_null_features(self):return [f for f in self.leaf_features if f.get_value() != 0]
    
    def append(self, leaf_feature):
        self.leaf_features.append(leaf_feature)
        
    def append_leaf_features(self, leaf_features):
        self.leaf_features+= leaf_features

    def set_parents(self, parents):self.parents= parents
    def get_parents(self):return self.parents

    def append_parent(self, parent):self.parents.append(parent)
        
    def get_present_leaf_features(self):return self.present_leaf_features
    def set_present_leaf_features(self, present_leaf_features):
        self.present_leaf_features = present_leaf_features

    def get_children(self):return self.children
    def set_children(self, children):self.children = children
    
    def get_key_leaf_features(self):return self.key_leaf_features
    def set_key_leaf_features(self,key_leaf_features):self.key_leaf_features= key_leaf_features

    def get_level(self):return self.level
    def set_level(self, level):self.level = level


    def set_leaf_features(self, leaf_features):self.leaf_features = leaf_features
    def get_unique_leaf_features(self):return {f.id: f for f in self.leaf_features}.values()
    
    def get_total_value(self):
    ### consider adding a function for summing up the unique enzymes
        return math.fsum([c.value for c in self.leaf_features])
  
    def get_unique_total_value(self):
    ### consider adding a function for summing up the unique enzymes
        self.cumulative_features= {c.name:c.value for c in self.leaf_features}
        return math.fsum(self.cumulative_features.values())
   
    def get_unique_average_value(self):
        return self.get_unique_total_value()/len(self.cumulative_features)

    def get_unique_features(self):return set(self.key_leaf_features)

    def set_db_data(self, attribute, value):
        self.db_data[attribute] = value

    def get_db_data(self):return self.db_data



class PathwayContainer(object):
    """
        equivalent of a Level object

    """
    def __init__(self, level, calculation_type= "sum" ):
        self.pathways= []
        self.level= level
        self.dmp_file= "/Users/kemal/repos/pacfm/pacfm/.data/launching/kegg_orthology_lengths_%s.dmp" %level
        self.calculation_type= calculation_type

    def __add__(self, pathway):
        self.pathways.append(pathway)
        return self

    def __iter__(self):
        return (self[name] for name in list.__iter__(self.names))

    def __getitem__(self, name): 
        try:
            return [p for p in self.pathways if p.name == name][0]
        except:
            return self.get_by_index(name)
        
    def __repr__(self):
        return '; '.join([p.name for p in self.pathways])

    def __len__(self):
        return len(self.pathways)

    def get_by_index(self, index):
        return self.pathways[index]

    @property
    def names(self):
        return [i.name for i in self.pathways]

    def edit_pathway(self, **kwargs) :
        
        p= self.get_current_pathway()
    
        for k,v in kwargs.iteritems():
            p.__dict__[k]= v

    def get_all(self):return self.pathways


    def get_level(self):return self.level
    def set_level(self, level):self.level = level


    def append(self, pathway):
        self.add_pathway(pathway)

    def add_pathway(self, pathway):
        self.pathways.append(pathway)
        self.set_current_pathway(pathway)

    def add_pathways(self, pathways):
        self.pathways+= pathways
        self.set_current_pathway(pathways[-1])

    def remove_pathway(self, name):
        self.pathways.remove(self[name])

    def filter(self, names):
        for name in self.names:
            if name not in names:
                self.remove_pathway(name)

    def set_current_pathway(self, pathway):
        self.current_pathway= pathway

    def get_min_value(self):
        if self.calculation_type ==  "sum":
            return min([pathway.get_unique_total_value() for pathway in self.pathways])
        
        elif self.calculation_type ==  "average":
            return min([pathway.get_unique_average_value() for pathway in self.pathways])


    def get_max_value(self):
        if self.calculation_type ==  "sum":
            return max([pathway.get_unique_total_value() for pathway in self.pathways])
        
        elif self.calculation_type ==  "average":
            return max([pathway.get_unique_average_value() for pathway in self.pathways])

    
    def get_total_value(self):
        """ total value should be equal to the unique total where no enzyme is repeated
            however, to keep the seamless integration with fantom, we add features 
            in the naive fashion.
        """
        return math.fsum([pathway.get_total_value() for pathway in self.pathways])

    def get_average_value(self):
        return self.get_total_value / len(self.pathways)
    
    def get_level(self):
        return self.level
   
    def get_all_leaf_features(self):
        leaf_features= []
        for pathway in self.pathways:
            leaf_features+= pathway.get_leaf_features()
    
    def get_unique_features(self):
        features= self.get_all_leaf_features()
        return set(features)

    def dump_db_data(self):
        db_data= {pathway.name:pathway.get_db_data() for pathway in self.pathways}
        pickle.dump(db_data, open(self.dmp_file, "w"))

    def load_db_data(self):
        
        if self.pathways[0].get_db_data() == {}:

            if not os.path.exists(self.dmp_file):
                self.set_pathway_lengths()
                self.set_pathway_sequence_lengths()
                self.dump_db_data()

            db_data= pickle.load(open(self.dmp_file))
            for pathway in self.pathways:
                for k,v in db_data[pathway.name].iteritems():
                    pathway.set_db_data(k,v)


    def set_pathway_lengths(self):
        pathway_lengths = {}
        for pw in self.pathways:
            if pw.level == pw.biodb_selector.getLevelCount()  - 1:
                pw_length = len(pw.biodb_selector.getChildrenByParentID(pw.id, pw.level))
            else:
                pw_length = len(set(pw.biodb_selector.getLeafNodesByParent(pw, pw.biodb_selector.getLevelCount())))
            pw.set_db_data('n_protein', pw_length)

    def set_pathway_sequence_lengths(self):
        fKo= open("/Users/kemal/repos/pacfm/pacfm/src/pathway/norm_for_pack/ko_lenghts.dmp")
        ko_lengths= pickle.load(fKo)
        
        pathway_sequence_lengths = {}
        for pw in self.pathways:
            if pw.level == pw.biodb_selector.getLevelCount() -1:
                kos= pw.biodb_selector.getChildrenByParentID(pw.id, pw.level)
            else:
                kos = set(pw.biodb_selector.getLeafNodesByParent(pw, pw.biodb_selector.getLevelCount()))
            # we start by one in order not to divide by 0 
            # in case we dont retrieve the lengths from the 
            # database.
            pw_length=1
            for ko in kos:
                if ko.accession in ko_lengths:
                    pw_length+= ko_lengths[ko.accession]
            
            pw.set_db_data('sequence_length', pw_length)
