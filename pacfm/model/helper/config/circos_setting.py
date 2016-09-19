class CircosSetting(object):
    def __init__(self, confFile, data, item_tag ):
        self.confFile = confFile
        self.data= data
        self.item_tag = item_tag
        self.settingList=[]

    def __repr__(self):
        return "Content of %s file and %s/%s !"
