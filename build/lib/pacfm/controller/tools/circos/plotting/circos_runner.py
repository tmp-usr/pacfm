import subprocess
from pacfm.model import file_provider

### This class is not used any longer. Check input_builder class. ###

class CircosRunner:
    
    def __init__(self):
        
        self.circos_file= file_provider['output']['circos_png']
        self.config= self.fp['circos_config']['conf']

        self.run()


    def run(self):
       
        self.cmd= ['/Users/kemal/phd/projects/circos-0.67-7/bin/circos','--conf', self.config,'-outputfile', self.circos_file]
        cmd= ' '.join(self.cmd)
        print "Running...", cmd
        p= subprocess.Popen(cmd, shell= True, stdout=subprocess.PIPE)
        output= p.communicate()[0]
        print output
        return output



