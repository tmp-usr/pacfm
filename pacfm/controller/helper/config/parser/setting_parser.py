import re

from collections import OrderedDict

class SettingParser:
    def __init__(self, text):
        self.text= text.replace('>>','))').replace('<<','#((')
        self.props=OrderedDict()
        self.commentLines=[]
        self.parse()
    
    def parse(self):
        re_text=r'(^[^#]\w+)\s*=\s*(.*)'
        re_comment= r'^#.*'
        exp_text = re.compile(re_text, re.M)
        exp_comment= re.compile(re_comment, re.M)
        for i,j in re.findall(exp_text, self.text ):
            self.props[i.strip()] = j.strip()
        
        for line in re.findall(exp_comment, self.text ):
            self.commentLines.append(line.strip())

        return self.props
    
    def tostring(self):
        text="\n"
        for prop,value in self.props.iteritems():
            text+= "%s = %s\n" % (prop, value)
        for line in self.commentLines:
            text+= line+'\n'
        
        text= text.replace('))','>>').replace('#((','<<')
        return text

    def get(self, prop=""):
        if prop == "": return self.props
        else: return self.props[prop]

    def set(self, prop, value):
        self.props[prop]=value



