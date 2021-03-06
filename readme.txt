PACFM: Pathway Analysis with Circos for Functional Metagenomics
----------------------------------------------------------------

PACFM is a software tool developed for the analysis of
biological pathways in metagenomics projects. It provides 
the users with an improved way of visualizing pathway 
abundance data in addition to presenting a wide array of 
methods for filtering and normalization. 

Download 
--------
PACFM is available from the links below as compressed 
directories for Mac OS X (10.11), Windows 10 and
the souce code can be accessed from the github page. 

1. Mac OS X: https://github.com/ecotox/pacfm/raw/master/install/pacfm-0.0.1.macosx-10.11-intel.tar.gz
2. Windows: https://github.com/ecotox/pacfm/raw/master/install/pacfm-0.0.1.win-10-x64.zip
3. Source: https://github.com/ecotox/pacfm/tree/master/src/

Installation
------------

- Mac OSX:
  
  1. Download the tarball from the link above. 
 
  2. Open a terminal window and type:
    >> tar -xzvf pacfm-0.0.1.macosx-10.11.tar.gz

- Windows:
  
  1. Download the zip file and extract the source files.

- Source:
  
  1. Install python 2.7
  
  2. Install perl (>= 5.8) 
  
  3. Install the latest wxpython release compatible with 
    your OS, from the following website 
    http://www.wxpython.org/download.php
  
  4. (Required for Circos) Install the perl modules by 
    typing the following in a terminal window :
    >> cpan X::Y::Z
      The module name X::Y::Z is replaced by the folllowing: 
      Config::General, Font::TTF::Font, Math::Bezier, 
      Math::VecStat, Readonly, Text::Format, Statistics::Basic, 
      Set::IntSpan, Regexp::Common, SVG  
  
  5. Clone into the pacfm project on github by typing:
    
    >> git clone https://github.com/ecotox/pacfm/src
    >> cd pacfm
    >> python setup.py install

Running
---------

-- The GUI

- Mac OSX

  1. From the terminal window change your directory into
     the path which you extracted the content of the tarball.
     >> cd path/to/pacfm

  2. Run pacfm from the command line.
     >> ./pacfm
      
- Windows

  1. Change your directory into the path which you extracted 
    the content of the .zip file. 

  2. Double click on the executable file "pacfm.exe".

- Source

    >> cd pacfm/pacfm/  
    >> python pacfmd.py


-- The Commandline Interface

- * nix

  1. Type the following command in a terminal window.
    >> python pacfmd.py [-h] -i INPUT_FILE_PATH [-s] [-l] 
                        [-m] [-n N_ASSOCIATION] [-k {0,1,3}] 
                        [-o {0,1,2}] [-f OUTPUT_FIGURE_PATH]
                        [-t OUTPUT_TABLE_PATH] [-e INFO_TYPES] 
                        [-g KEY_ENZYMES_PATH] [-a ABBREVIATIONS_PATH] 
                        [-x LINKS_PATH]

Usage
-------
Please see the user manual!


Reference
---------
If you use PACFM in your research please cite the following paper:

-- Sanli, K., Sinclair, L., Nilsson, R. H., Mardinoglu, A., and 
Eiler, A. (2016). PACFM: Pathway Analysis with Circos in Functional 
Metagenomics. Manuscript.

