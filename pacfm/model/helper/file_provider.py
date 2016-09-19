import os, sys

### the _MEIPASS file path sign should only be used with the
### application version. for the local run, use the version below

### below function is used for the pyinstaller deployment step
#def resource_path(relative_path):
#    """ Get absolute path to resource, works for dev and for PyInstaller """
#    try:
#        # PyInstaller creates a temp folder and stores path in _MEIPASS
#        base_path = sys._MEIPASS
#    except Exception:
#        base_path = os.path.abspath(".")

#    return os.path.join(base_path, relative_path)


#def resource_path(relative):
#    if getattr(sys, 'frozen', False):
#        return  os.path.join(getattr(sys, "_MEIPASS"), os.path.dirname(os.path.abspath(__file__)), relative)
 #   return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative)


#def resource_path(relative):
#    if getattr(sys, '_MEIPASS2', False):
#        return os.path.join(os.environ.get("_MEIPASS2", os.path.abspath(".")),relative)
#    else:
#        return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative)


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


base_dir= resource_path(os.getcwd()) 
data_dir= os.path.join(base_dir, '.data')
tools_dir= os.path.join(base_dir, 'tools')
circos_base_dir= os.path.join(data_dir, "circos")
circos_config_dir= os.path.join(circos_base_dir, "config")
circos_data_dir= os.path.join(circos_base_dir, "data")

tmp_output_dir= os.path.join(base_dir, "outputs",".tmp")
output_dir= os.path.join(base_dir, "outputs")

launching_dir= os.path.join(data_dir, "launching")

example_dir= os.path.join(data_dir, "example")


class FileProvider(dict):
    
    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)
        self._dict= dict()
        self._dict['circos_config'] = {
                'conf': os.path.join(circos_base_dir, 'my_circos.conf'),   
                'plots': os.path.join(circos_config_dir, 'my_plots.conf' ),                                    'ideogram': os.path.join(circos_config_dir, 'ideogram.conf' ), 
                'karyotype': os.path.join(circos_config_dir, 'karyotype.conf' ),  
                'ticks': os.path.join(circos_config_dir, 'ticks.conf' ), }
        
        self._dict['circos_data'] = {
            # since hierarchy levels will differ from db to db, we should find an expandable solution
            # for the file names. for now, lets keep the config type as a dir and get the file from a function
            # below
            'abundance_dir' : os.path.join(circos_data_dir, "abundance"),  
            'labels_dir': os.path.join(circos_data_dir, "labels"), 
            'links_dir': os.path.join(circos_data_dir, "links"),
            'highlights': os.path.join(circos_data_dir, "highlights.txt"),  }
        
        
        self._dict['output']= {
            'circos_png': os.path.join( tmp_output_dir, "circos.png"), 
            'circos_svg': os.path.join( tmp_output_dir, "circos.svg"), 
            #'plot_svg': 'circos.svg',#,os.path.join(circos_base_dir, circos_output_dir, "circos.svg"), 
            'legend_png': os.path.join(tmp_output_dir, "legend.png") ,
            'legend_svg': os.path.join(tmp_output_dir, "legend.svg") ,
            'colorbar_png': os.path.join(tmp_output_dir, "colorbar.png") ,
            'colorbar_svg': os.path.join(tmp_output_dir, "colorbar.svg") ,
            
            'pacfm_svg': os.path.join(output_dir, "pacfm.svg"),
            'pacfm_png': os.path.join(output_dir, "pacfm.png") }
        
        self._dict['launching']= {
            
            "links": os.path.join(launching_dir, "links.dmp"),
            "highlights": os.path.join(launching_dir, "highlights.dmp"),
            "plots": os.path.join(launching_dir, "plots.dmp"),
            "abbr":os.path.join(launching_dir, "abbreviations.dmp"), 
            "icons": os.path.join(launching_dir, "icons")
            
        } 
        self._dict['example']=  {
            'kegg': os.path.join(example_dir, "kegg.tsv")
            
            }


        self._dict['circos']= { 
            'bin': os.path.join(tools_dir, 'circos-0.67-7', 'bin','circos'),
            }

        self._dict['minpath']= {
            'bin':  os.path.join(tools_dir, 'minpath-1.2', 'Minpath1.2.py'),
            'output': os.path.join(tools_dir, 'minpath-1.2', 'files', '.minpath.report'),
            'input': os.path.join(tools_dir, 'minpath-1.2', 'files','.minpath.input'),
                
            }

        self.makedirs()

    def __getitem__(self, item):
        return self._dict.__getitem__(item)

    def abundance(self, level):
        self._dict['circos_data']['abundance_%s' % level]= os.path.join(self._dict['circos_data']['abundance_dir'], '%s.txt' % level)
        return self._dict['circos_data']['abundance_%s' % level]
    
    def links(self, level):
        self._dict['circos_data']['links_%s' % level]= os.path.join(self._dict['circos_data']['links_dir'], '%s.txt' % level)
        return self._dict['circos_data']['links_%s' % level]
    
    def labels(self, level):
        self._dict['circos_data']['labels_%s' % level]= os.path.join(self._dict['circos_data']['labels_dir'], '%s.txt' % level)
        return self._dict['circos_data']['labels_%s' % level]

    
    def makedirs(self):
        for cat, label_path in self._dict.iteritems():
            for label, path in label_path.iteritems(): 
                if os.path.isfile(path):
                    path = os.path.dirname(path)

                if not os.path.exists(path):
                    if os.path.basename(os.path.dirname(path)) == "pacfm":        
                        os.makedirs(path)

file_provider= FileProvider()

