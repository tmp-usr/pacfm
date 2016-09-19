import argparse
license= ""    
    
class MainView(object):

    def __init__(self, main_controller):
        
        self.parser= argparse.ArgumentParser(description=license, formatter_class=argparse.ArgumentDefaultsHelpFormatter, prefix_chars="-")
        
        self.parser.add_argument('-i','--input', dest='input_file_path', required=True, help='Input file containing KO counts in one or more samples.')

        self.parser.add_argument('-s','--sequence', dest='pw_sequence', help='Normalization of pathways by sequence length', action= "store_true")

        self.parser.add_argument('-l','--length', dest='pw_length', help='Normalization of pathways by protein length.', action= "store_true")

        self.parser.add_argument('-m','--minpath', dest='pw_minpath', help='Normalization of pathways by the minpath algorithm.', action="store_true")
        
        self.parser.add_argument('-n','--n_association', dest='n_association', default= 1000, help='Number of pathway associations.', type= int)

        self.parser.add_argument('-k','--key_enzymes', dest='pw_key_enzyme', default=0, choices=[0,1,3], help= "Pathway normalization based on key enzymes: [0: any, 1: all, 2: manual selection (disabled in the command line version), 3: pathway associations]", type= int)

        self.parser.add_argument('-o','--output', dest='output_type', default= 0, choices=[0,1,2], help="Output type: [0: plot, 1: table, 2: both]", type=int)
        
        self.parser.add_argument('-f','--output_figure', dest='output_figure_path', help='Figure output file')
        
        self.parser.add_argument('-t','--output_table', dest='output_table_path',  help='Table output file')

        self.parser.add_argument('-e', '--addditional_information', dest="info_types", action="append", default= [], help="Selects the typ(s) of additional info including links, abbreviations, key_enzymes")

        self.parser.add_argument('-g','--get_key_enzymes', dest='key_enzymes_path', help='Outputs the list of key enzymes of each pathway in a text file.')

        self.parser.add_argument('-a','--abbreviations', dest='abbreviations_path', help='Outputs the list of pathway abbreviations with their long names.')

        self.parser.add_argument('-x', '--links', dest= "links_path" , help='Pathway associations of individual enzymes (links).')
        
        
        self.parser.add_argument('-d', '--db_name', dest= "db_name" , help='Database name.')
        self.parser.add_argument('-c', '--calculation_type', dest= "calculation_type" , help='Calculation method of pathway values.')
        self.parser.add_argument('-r', '--colorbar_title', dest= "colorbar_title" , help='Colorbar title (default: Relative abundance).')


        args, unknown= self.parser.parse_known_args(namespace= main_controller)
        #self.parser.parse_args(namespace= main_controller)
      
        main_controller.init_project()
        main_controller.normalize_pathways()
        main_controller.plot_circos()
        main_controller.save_output()
        main_controller.save_info()
    
