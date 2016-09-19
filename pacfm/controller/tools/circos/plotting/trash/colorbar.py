'''
Make a colorbar as a separate figure.
'''
from pacfm.model import file_provider

from matplotlib import pyplot
import matplotlib as mpl





def drawColorbars(*intervals):
    #(nrows, ncols, plot_number)
    fig = pyplot.figure(figsize=(7,3), frameon=False)
    for i in range(len(intervals)):
        #ax1 = fig.add_axes([0.05, 0.80, 0.9, 0.15])
        #ax2 = fig.add_axes([0.05, 0.475, 0.9, 0.15])
        ax= fig.add_subplot(len(intervals),1,i+1)

        cmap = mpl.cm.YlOrRd
        norm = mpl.colors.Normalize(vmin=intervals[i][0], vmax=intervals[i][1])

        cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                           norm=norm,
                                           orientation='horizontal')


        #norm = mpl.colors.Normalize(vmin=5, vmax=10)
        #cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,
        #                                     norm=norm,
        #                                     spacing='proportional',
        #                                     orientation='horizontal')
        #cb2.set_label('Discrete intervals, some other units')


    cb1.set_label('Some Units')
    #pyplot.show()
    pyplot.savefig(file_provider["output"]["colorbar_svg"])


intervals= [(1,10),(5,20)]
drawColorbars(*intervals)
