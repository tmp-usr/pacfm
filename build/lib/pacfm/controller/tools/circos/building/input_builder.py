import os
import subprocess

from pandas import read_csv

from assembler import Assembler
from io_worker import IOWorker

from pacfm.model import file_provider


class InputBuilder(object):

    def __init__(self, biodb_selector, fam_path, index_col= "Name", calculation_type="sum"):
        self.biodb_selector= biodb_selector
        self.abundance_frame= read_csv(fam_path, sep= '\t', index_col=index_col)
        self.abundance= self.abundance_frame.T.mean()
        self.assembler= Assembler(biodb_selector, self.abundance, calculation_type)
        self.assembler.assemble_ideograms()
        self.io_worker= IOWorker(self.assembler)

    def build_circos_inputs_and_run(self, plots=None, links=None, highlights=None):
        """
            pathway names will be added
        """

        self.io_worker.build_links(links)
        self.io_worker.build_highlights(highlights)
        self.io_worker.edit_plots_config(plots)

        self.io_worker.build_karyotype()
        self.io_worker.build_text()
        self.io_worker.build_pathway_names()
        self.io_worker.build_data()
        
        self.save_settings(plots, links, highlights)
        self.run_circos()

    def save_settings(self, plots, links, highlights):
        plots.dump()
        links.dump()
        highlights.dump()

    def run_circos(self):
        circos_file= file_provider['output']['circos_png']
        config= file_provider['circos_config']['conf']
        out_dir = os.path.dirname(circos_file)
        out_file= os.path.basename(circos_file)

        circos_bin= file_provider['circos']['bin']
        cmd_args= ['perl', circos_bin,'--conf',  config,' --outputdir', out_dir,  '--outputfile', out_file]
        cmd= ' '.join(cmd_args)
        print "Running circos...", cmd
        p= subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr= subprocess.PIPE)
        #p= subprocess.Popen(cmd_args)
        output, err= p.communicate()
        print output
        print "#####"
        print err
        return output

    def build_optionals(self):
        pass


