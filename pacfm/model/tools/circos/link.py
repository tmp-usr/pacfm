from pacfm.model.helper import file_provider
from base import PacfmObjectBase, PacfmContainerBase

class Link(PacfmObjectBase):
    def __init__(self, name=None, z_index=None, color=None, level=None):
        PacfmObjectBase.__init__(self, name= name, color= color, level = level)
        self.z_index= z_index
    

class LinkContainer(PacfmContainerBase):
    def __init__(self, links=[]):
        PacfmContainerBase.__init__(self, items= links)
        self.dmp_file= file_provider["launching"]["links"] 

    @property
    def level(self):
        return self.items[0].level

    def set_links_by_names(self, names):
        for name in names:
            if name not in self.names:
                self.add(name)
        self.items= [l for l in self.items if l.name in names]        

    def edit(self, name, z_index=1,color=(127,127,127), level=2) :
        link= self[name]
        link.z_index= z_index
        link.color= color
        link.level= level

    def add(self, name, z_index=1, color=(127,127,127), level=2):
        l=Link(name=name, z_index=z_index, color=color, level=level )
        self.items.append(l)    
