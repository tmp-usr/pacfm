import pickle

class PacfmObjectBase(object):
    def __init__(self, name, color= None, level= None):
        self.name = name
        self.color= color
        self.level= level

    def __repr__(self): return self.name
    def __str__(self): return self.name


class PacfmContainerBase(object):
    def __init__(self, items=[]):
        self.items= items
        self.current= self.items[0] if items != [] else None
        self.dmp_file = ""


    def __getitem__(self, name): 
        item= [item for item in self.items if item.name.lower() == name.lower()][0] 
        self.set_current(item)
        return item

    def __iter__(self):
        return  (item for item in list.__iter__(self.items))


    def __repr__(self):
        return '; '.join(self.names)

    def __len__(self):
        return len(self.items)

   
    def __add__(self, item):
        self.items.append(item)
        return self

    def get_by_index(self, index):
        if len(self) > 0:
            return self.items[index]
        return None

    @property
    def names(self):
        return [i.name for i in self.items]

    def set_current(self, item):
        self.current= item
    
    def get_current(self):
        return self.current

    def add(self, *args):
        pass

    def add_items(self, items):
        self.items+=items
        self.set_current(items[-1])

    def edit(self, **kwargs) :
        
        item= self.get_current()
    
        for k,v in kwargs.iteritems():
            item.__dict__[k]= v


    def remove(self, name):
        self.items.remove(self[name])

    def dump(self):
        pickle.dump(self.items, open(self.dmp_file,'w'))
    
    def load(self):
        self.items= pickle.load(open(self.dmp_file))
        if len(self.items) > 0:
            self.set_current(self.items[0])
