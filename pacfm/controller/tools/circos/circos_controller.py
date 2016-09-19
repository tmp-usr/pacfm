import wx
from pacfm.view.gui import CircosDialog 

class CircosController(object):

    def __init__(self, biodb=None, plots=None, links=None, highlights=None):
        dbLevelCount= biodb.getLevelCount()
        
        LinkLevel= 2
        LinkPathwayNames= [f.name for f in biodb.getFeaturesByLevel(LinkLevel)]
        
        self.links= links
        self.highlights= highlights


        self.view = CircosDialog(None, biodb= biodb, plots=plots, links= links, highlights= highlights)
        
         
