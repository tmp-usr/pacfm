import os
import pickle

from pacfm.model.helper import Abbrator, file_provider

karyotypeAbbr= lambda x: "_".join([i[0].lower() for i in x.split(' ')])

fOut= file_provider["launching"]["abbr"]

class Karyotype:
    
    def __init__(self, bl=None):
        self.bl= bl
        if self.bl is not None:
            self.names= [feature.name for feature in self.bl.getFeaturesByLevel(1)]
        
        
        self.output= fOut
        self.Abbr={}


    def get_karyotype(self):
        if os.path.exists(self.output):
            with open(self.output) as inF:
                self.Abbr= pickle.load(inF)
            return self.Abbr
        else:
            return self.set_karyotype()
            #print 'set the karyotype file first! cool down! get a glass of water!'

    def set_karyotype(self):
        """
            this can only be build for the highest hierarchy level
        """
        
        Trash= {}
       
        for name in self.names:
            abbr= karyotypeAbbr(name)
            
            if abbr not in Trash:
                Trash[abbr]=1
            else:
                rank= abbr.split('_')[-1]
                
                try:
                    rank= int(rank)
                    rank+= 1
                    abbr_l= abbr.split('_')
                    abbr_l[-1]= str(rank)
                except:
                    abbr_l=abbr.split('_')
                    abbr_l[-1]= "1"
                
                abbr= '_'.join(abbr_l)
                Trash[abbr]= 1
            self.Abbr[name] =abbr
       
        if len(self.names) == 1:
            self.Abbr["Hypothetical"] = "h"

        with open(self.output,'w') as outF:
            pickle.dump(self.Abbr, outF)
        
        return self.Abbr
                
    #karyotypeFile= '/Users/kemal/Downloads/circos/circos-course-0.61/workstation/2/data/other_inputs/karyotype_a_'+str(n)+'.txt'
    #fOut2=open(karyotypeFile,'w')
    # circos related - karyotype file
    #for i,v in cDict.iteritems():
    #    line= 'chr\t-\t'+PW_abr[v.name]+'\t'+'_'.join(v.name.split(' '))+'\t0\t'+ str(v.end)+'\tspectral-5-div-1'
   #     fOut2.write(line+'\n')
    

        


