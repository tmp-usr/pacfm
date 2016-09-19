from itertools import combinations

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon

from pacfm import file_provider


def drawLegend(links):
    
    height= len(links)/3
    a= max([len(''.join(com)) for com in combinations(links.keys(), 2)])
    width= (a/7) + 1
    fig= plt.figure(figsize=(width,height), frameon=False)
    ax = fig.add_subplot(111)
    plt.axis('off')

    names= links.keys()
    colors= links.values()

    P=[]
    i=0
    for item in colors:
        print item
        p = Rectangle((0, 0), 5, 5, fc=item )
        P.append(p)
        i+=1


    leg=ax.legend(P, names, ncol=2,fancybox=True, loc='center')
    for t in leg.get_texts():
        t.set_fontsize(10) 
    ax.axis('off')

    plt.savefig(file_provider["output"]["legend_svg"], transparent=True)
    plt.show()
