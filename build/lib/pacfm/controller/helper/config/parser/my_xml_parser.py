import re
import xml.etree.ElementTree as ET

from setting_parser import SettingParser

class MyXMLParser:
    
    def __init__(self, text):
        self.xmlBlocks = []
        self.text= text.replace('>>','))').replace('<<','#((')
        self.parse()



    def parse(self):
        re_xml=r'^<(\w+)(>.*)</(\1)>'
        exp_xml= re.compile(re_xml, re.M | re.S)
        self.xmlBlocks = [item.group(0) for item in list(re.finditer(exp_xml, self.text ))]

    
    def get(self, item_tag, prop="", child=None):
        for in_text in self.xmlBlocks:
            # this step is done to avoid confusion due to the "<<" and ">>" signs
            root= ET.fromstring(in_text)
            if root.tag == root_tag:
                ### we use XPath features of the xml.etree library here
                root.findall('.%s' % child)
                propSet= SettingParser(child.text)
                if propSet.get(refProp) == refValue:
                   propSet.set(prop, value) 
                   child.text= propText.tostring()



    def set(self, item_tag, prop, value, refProp, refValue):
        for i in range(len(self.xmlBlocks)):
            # this step is done to avoid confusion due to the "<<" and ">>" signs
            in_text= self.xmlBlocks[i]
            root= ET.fromstring(in_text)
            #print root.text
             
            for item in root.iter():
                #print item.tag
                if item.tag == item_tag:
                    parser=SettingParser(item.text)
                    if refValue != "":
                        try:
                            if parser.get(refProp) == refValue:
                                parser.set(prop,value)
                        
                        except:
                            pass
                    
                    else:
                        parser.set(prop, value)
                    
                    item.text= parser.tostring()

            out_text = ET.tostring(root)
            self.xmlBlocks[i]= out_text
            



    def tostring(self):
        text=""
        for in_text in self.xmlBlocks:
            root= ET.fromstring(in_text)
            text+= ET.tostring(root)+'\n'

        text= text.replace('))','>>').replace('#((','<<')
        return text

        
