from pacfm.model import file_provider
from my_xml_parser import MyXMLParser
from setting_parser import SettingParser

class CircosConfigParser:
    '''
    circos implemented the apache config format which has no builtin parser in python. this class is intended to parse and manipulate the circos configuration files.
    '''
    
    def __init__(self, configType):
        self.configType = configType
        self.xmlParser=None
        self.txtParser=None
        self.conf_file= file_provider['circos_config'][configType]
        self.parse()

    def parse(self):
        '''
            returns a tuple with the first item as a dictionary of attributes outside xml blocks AND the second item as a list of xml blocks. the first item is straight forward. Second item should be further parsed iteratively by using the iPaseXML function
        '''
        with open(self.conf_file) as f:
            text=f.read()
            self.xmlParser= MyXMLParser(text)
            xml_text= self.xmlParser.tostring()
            non_xml_text= text.replace(xml_text, "")
            self.txtParser= SettingParser(non_xml_text)
            
    
    def set(self, prop, value, item_tag="", refProp="index", refValue= ""):
        if item_tag != "": ## means coming from the xml part
            self.xmlParser.set(item_tag, prop, value, refProp, refValue)
        else: ### means coming from the text part
            self.txtParser.set(prop, value)
       
        self.write()

    def write(self):
        ### !!! TODO: this part should be rewritten
        ### There is still a problem with the xmlparser. 
        
        with open(self.conf_file,'w') as f:
            f.write(self.tostring())

    def tostring(self):
        if self.configType == 'plots': 
            self.doc= self.xmlParser.tostring()
        else:
            self.doc= self.txtParser.tostring() + self.xmlParser.tostring()
        return self.doc





