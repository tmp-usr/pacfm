from run import *
import os
import glob

input_files= []
project= "twin"
#data_base= "/Users/kemal/repos/pacfm_project/manuscript_data/alex_lucas/pacfm_eval/"

#data_dir= os.path.join(data_base, project, "data_reformated" )
data_dir= "/Users/kemal/Downloads/twin_study/pacfm_input/abs"
#data_dir= "/Users/kemal/Downloads/twin_study/pacfm_input"
input_files= glob.glob(os.path.join(data_dir, '*.tsv'))


for input_file in input_files: 

    base_dir= ""

    input_base= os.path.basename(input_file)

    base_dir_name= input_base.split('.')[0]
    data_dir= os.path.dirname(input_file)

    base_dir= os.path.join(data_dir, base_dir_name)
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    pacfm= MainController()
    pacfm.load_project(input_file)

    raw_data_frame= pacfm.input_builder.assembler.to_data_frame()
    raw_output_file= os.path.join(base_dir, "all.tsv")
    raw_data_frame.to_csv(raw_output_file, sep='\t', index_label="index")

    n_associations= [1,2,3,100]

    for n_association in n_associations:
        pacfm.load_project(input_file)
        norm_data_frame= pacfm.normalize_pathways(3, n_association)
        output_file = os.path.join(base_dir, "%i.tsv" %n_association)
        print "writing %s" %output_file
        norm_data_frame.to_csv(output_file, sep="\t", index_label="index")
        

