from base import PacfmObjectBase, PacfmContainerBase
from pacfm.model import file_provider

class Highlight(PacfmObjectBase):
    def __init__(self, name, pathways, level, color, checked=True):
        PacfmObjectBase.__init__(self, name= name, level=level, color=color) 
        self.pathways= pathways
        self.checked= checked
   
    
    def add_pathway(self, pathway):
        if pathway not in self.pathways:
            self.pathways.append(pathway)

    def remove_pathway(self, pathway):
        if pathway in self.pathways:
            self.pathways.remove(pathway)


class HighlightContainer(PacfmContainerBase):
    def __init__(self, highlights=[]): 
        PacfmContainerBase.__init__(self, items= highlights)
        self.dmp_file= file_provider["launching"]["highlights"]

    
    def add(self, name= "New highlight", names=[], level=2, color=(127,127,127), checked= True):
        i=1
        base= name
        while name in self.names:
            i+=1
            name= base+' %s' %i
        
        h= Highlight(name, names, level, color, checked)
        self.items.append(h)
        self.set_current(h)
        return h

    def add_pathway(self, pathway):
        hl= self.get_current().add_pathway(pathway)
    
    def remove_pathway(self, pathway):
        self.get_current().remove(pathway)

