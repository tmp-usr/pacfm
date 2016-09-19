import pickle
from pacfm.model import file_provider
from base import PacfmObjectBase, PacfmContainerBase

class PlotSetting(PacfmObjectBase):
    def __init__(self, level, plot_type, color=None, color_scheme=None, min_value=0, max_value= 1000):
        name= "Level %s" % level
        PacfmObjectBase.__init__(self, name= name, color= color, level= level) 
        self.plot_type= plot_type
        self.color_scheme= color_scheme
        self.min_value= min_value
        self.max_value= max_value


class PlotContainer(PacfmContainerBase):
    def __init__(self, plots=[]):
        PacfmContainerBase.__init__(self, items= plots)
        self.dmp_file= file_provider["launching"]["plots"]

    def __getitem__(self, level): 
        plot= [p for p in self.items if p.level == level][0] 
        self.set_current(plot)
        return plot
        
    def add(self, level, plot_type, color=(127,127,127,255), color_scheme= "oranges-seq-6"):
        p= PlotSettings(level, plot_type, color, colors_cheme)
        self.items.append(p)
        self.set_current(p)
        return p

    def dump(self):
        ### very unpythonic
        from pacfm.controller import CircosConfigParser
        
        pickle.dump(self.items, open(self.dmp_file,'w'))
        parser= CircosConfigParser('plots')
        parser.parse()
        for plot in self.items:    
            parser.set('type', plot.plot_type, 'plot', 'index', 'plot_%s'%plot.level)
            parser.set('color', plot.color_scheme, 'plot', 'index', 'plot_%s'%plot.level)
            color=plot.color
            if color is not None:
                color= list(color)
                if len(color) == 4:
                    color= list(color)
                    color[3] = 1- (color[3] / 255.0)
        
                color= ','.join(map(str, color))
        
            parser.set('fill_color',color, 'plot', 'index', 'plot_%s'%plot.level)
            parser.set('min', plot.min_value, 'plot', 'index', 'plot_%s'%plot.level)
            parser.set('max', plot.max_value, 'plot', 'index', 'plot_%s'%plot.level)

