from biodb.sqling.selector import Selector

class PacfmBase(object):
    def __init__(self, *args, **kwargs):
        self.init_attributes()
        self.init_variables(**kwargs)

    def init_attributes(self):
        self.pw_controller = None 
        self.pw_analyzer= None
        self.input_builder= None
        self.circos_controller= None
        
        self.level_abbreviations= {} 
        self.key_enzymes= {}
        self.enzyme_pathway_link= {}

    def init_variables(self, **kwargs):
        """
            Should be overridden.
        """
        pass
