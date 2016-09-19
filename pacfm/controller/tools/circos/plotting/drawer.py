from itertools import combinations

import matplotlib as mpl
mpl.use('WXAgg')

from matplotlib.patches import Rectangle,Polygon

import matplotlib.pyplot as plt
import svgutils.transform as sg
from PIL import Image

from pacfm.model import file_provider


colormaps= {
'BrBG':	'brbg-11-div',
'PiYG':	'piyg-11-div',
'PRGn':	'prgn-11-div',
'PuOr':	'puor-11-div',
'RdBu':	'rdbu-11-div',
'RdGy':	'rdgy-11-div',
'RdYlBu':	'rdylbu-11-div',
'RdYlGn':	'rdylgn-11-div',
'Spectral':	'spectral-11-div',
'Accent':	'accent-8-qual',
'Dark2':	'dark2-8-qual',
'Paired':	'paired-12-qual',
'Pastel1':	'pastel1-9-qual',
'Pastel2':	'pastel2-8-qual',
'Set1':	'set1-9-qual',
'Set2':	'set2-8-qual',
'Set3':	'set3-12-qual',
'Blues':	'blues-9-seq',
'BuGn':	'bugn-9-seq',
'BuPu':	'bupu-9-seq',
'GnBu':	'gnbu-9-seq',
'Greens':	'greens-9-seq',
'Greys':	'greys-9-seq',
'Oranges':	'oranges-9-seq',
'OrRd':	'orrd-9-seq',
'PuBu':	'pubu-9-seq',
'PuBuGn':	'pubugn-9-seq',
'PuRd':	'purd-9-seq',
'Purples':	'purples-9-seq',
'RdPu':	'rdpu-9-seq',
'Reds':	'reds-9-seq',
'YlGn':	'ylgn-9-seq',
'YlGnBu':	'ylgnbu-9-seq',
'YlOrBr':	'ylorbr-9-seq',
'YlOrRd':	'ylorrd-9-seq'
}

class Drawer(object):
    
    def __init__(self, links, plots, title="Relative abundance"):
        
        self.legendFile= file_provider['output']['legend_png']
        self.colorbarFile= file_provider['output']['colorbar_png']
        self.circosFile= file_provider['output']['circos_png']

        self.fantomCircosSVG= file_provider['output']['pacfm_svg']
        self.fantomCircosPNG= file_provider['output']['pacfm_png']
        self.config= file_provider['circos_config']['conf']
        
        self.title= title

        self.output_image= self.run(links, plots)


    def get_output_image(self):
        return self.output_image

    def run(self, links, plots):

        self.drawLegend(links)
        self.drawColorbars(plots)
        return self.mergePngFiles()
        #self.mergeSvgFiles mergePngFiles()
        

    def mergePngFiles(self):
        output_base= file_provider['output']    
        files= (output_base['circos_png'], output_base['legend_png'], output_base['colorbar_png'])
        #background = Image.open("test1.png")
        #foreground = Image.open("test2.png")

        #background.paste(foreground, (0, 0), foreground)
        #background.show()
        files= [Image.open(f) for f in files]
        half = 1
        files[2] = files[2].resize( [int(half * s) for s in files[2].size] )
        #print files[1].size
        w1 = int((files[0].size[0] / 2) - (files[1].size[0]/2))
        h1 = int((files[0].size[1] / 2) - (files[1].size[1]/2))
      
        w2= int(files[0].size[0] - files[2].size[0]* 5/4)
        h2= int(files[0].size[1] - files[2].size[1] - files[2].size[0] /4)


        files[0].paste(files[1], (w1,h1), files[1])
        files[0].paste(files[2], (w2,h2), files[2])
        
        return files[0]
        #pdb.set_trace()
        
        #files[0].show()



    
    def mergeSvgFiles(self):
        
        files= (self.circosFile, self.colorbarFile, self.legendFile)
        fOutSVG= self.fantomCircosSVG
        fOutPNG = self.fantomCircosPNG
        #create new SVG figure
        width, height= "18cm","18cm"
        fig = sg.SVGFigure(width, height)

        # load matpotlib-generated figures
        fig1 = sg.fromfile(files[0])
        fig2 = sg.fromfile(files[1])
        fig3 = sg.fromfile(files[2])

        # get the plot objects
        plot1 = fig1.getroot()
        plot2 = fig2.getroot()
        plot3 = fig3.getroot()

        plot1.moveto(0, 5, scale=0.21)
        plot2.moveto(490, 550, scale=0.25)
        plot3.moveto(180, 280, scale=0.6)

        # add text labels
        #txt1 = sg.TextElement(25,20, "A", size=12, weight="bold")
        #txt2 = sg.TextElement(305,20, "B", size=12, weight="bold")

        # append plots and labels to figure
        fig.append([plot1, plot2, plot3])
        #fig.append([txt1, txt2])

        # save generated SVG files
        fig.save(fOutSVG)
        
        ### none of the converter tools worked fine 
        ### for vector graphics in python
        ### we will try merging png files instead.



    def drawLegend(self, links):
        height= len(links)/3
        if len(links) >=2:
            a= max([len(''.join(com)) for com in combinations(links.names, 2)])
        elif len(links)  == 1:
            a= len(links.names[0])

        width= a/4 
        
        fig= plt.figure(figsize=(width,height), frameon=False)
        ax = fig.add_subplot(111)
        plt.axis('off')

        names= links.names
        colors= [l.color for l in links]

        P=[]
        i=0
        skipped_index=[]
        for item in colors:
            item_norm= [c / 255.0 for c in item]
            if item_norm[:3] == [1.0,1.0,1.0]: 
                skipped_index.append(i)
                i+=1
                continue
            p = Rectangle((5, 5), 100, 100, fc=item_norm)
            P.append(p)
            i+=1

        names= [names[i] for i in range(len(names)) if i not in skipped_index]
        
        leg=ax.legend(P, names, ncol=2,fancybox=True, loc='center')
        for t in leg.get_texts():
            t.set_fontsize(25) 
        ax.axis('off')

        plt.savefig(self.legendFile, transparent=True)
        


    def drawColorbars(self, plots):
        fig = plt.figure(figsize=(5,3), frameon=False)
        i=0
        for plot in plots:
            if plot.plot_type == 'heatmap': 
                ax= fig.add_axes([0.05, (i* 0.4)+0.15, 0.9 ,0.3])
                if i == 1:
                    ax.set_title(self.title, {'fontsize':20})
            
                color_scheme= [k for k,v in colormaps.iteritems() if plot.color_scheme == v][0]
                cmap = mpl.cm.get_cmap(color_scheme)
                norm = mpl.colors.Normalize(vmin=plot.min_value, vmax= plot.max_value)

                cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                                   norm=norm,
                                                   orientation='horizontal')


                cb1.ax.set_ylabel('Level %s' % plot.level, {'fontsize':15})
                i+=1

        plt.savefig(self.colorbarFile)

    def drawColorbars2(self, *intervals):
        fig = plt.figure(figsize=(5,3), frameon=False)
        
        for i in range(len(intervals)):
            ax= fig.add_axes([0.05, (i* 0.4)+0.15, 0.9 ,0.3])
            if i == 1:
                ax.set_title('Relative abundance', {'fontsize':20})
            
            cmap = mpl.cm.get_cmap('Oranges')
            norm = mpl.colors.Normalize(vmin=intervals[i][0], vmax=intervals[i][1])

            cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                               norm=norm,
                                               orientation='horizontal')

            cb1.ax.set_ylabel('Level %s' %(i+1), {'fontsize':15})


