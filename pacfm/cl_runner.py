import subprocess
import glob, os, sys

calculation_types= ["sum","average"]
db_names= ["kegg_orthology_metabolism", "kegg_orthology"]


for cal_type in calculation_types:
    #calculation_type= "average"
    path= "/Users/kemal/Desktop/postdoc/data_cheng/data_28_07/ko/%s/log/*.txt" %cal_type 
    figures_dir = os.path.join(os.path.dirname(path), "figures") 
    tables_dir = os.path.join(os.path.dirname(path), "tables") 

    if not os.path.exists(figures_dir):
        os.makedirs(figures_dir)


    if not os.path.exists(tables_dir):
        os.makedirs(tables_dir)


    f_names= glob.glob(path)

    for f_name in f_names:
        input_file= f_name
        
        command_line= ["python","pacfmd.py", "2"]
        command_line.append("-i=%s" % input_file )

        for db_name in db_names:
            
            command_line.append("-d=%s" %db_name)
            out_f_name= os.path.basename(f_name).rstrip('.txt')
            if "metabolism" in db_name:
                out_f_name+= "_metabolism"
            out_f_figure = out_f_name+ ".png"
            out_f_table= out_f_name+ ".xls"
            output_figure_path= os.path.join(figures_dir, out_f_figure)
            output_table_path= os.path.join(tables_dir, out_f_table)
            command_line.append("-f=%s" % output_figure_path)
            command_line.append("-t=%s" % output_table_path)

            if "FC" in f_name:
                command_line.append("-r=(log) Fold change")
                command_line.append("-c=average")

            else:
                command_line.append("-r=Expression")
                command_line.append("-c=sum")
           
            command_line.append("-o=2")

            print "Running... %s " %" ".join(command_line)

            p = subprocess.Popen(command_line,stderr=subprocess.STDOUT)
            out, err = p.communicate()
            print out

