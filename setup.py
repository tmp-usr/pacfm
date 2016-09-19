from setuptools import setup

setup(
      name             = 'pacfm',
      version          = '0.1.0',
      description      = 'pathway analysis with circos for functional metagenomics',
      long_description = open('readme.txt').read(),
      license          = 'MIT',
      url              = 'http://github.com/ecotox/pacfm/',
      author           = 'Kemal Sanil',
      author_email     = 'kemalsanli1@gmail.com',
      classifiers      = ['Topic :: Scientific/Engineering :: Bio-Informatics'],
      packages         = [
         
"pacfm",
"pacfm/controller",
"pacfm/controller/helper",
"pacfm/controller/helper/config",
"pacfm/controller/helper/config/parser",
"pacfm/controller/tools",
"pacfm/controller/tools/circos",
"pacfm/controller/tools/circos/building",
"pacfm/controller/tools/circos/plotting",
"pacfm/controller/tools/pathway",
"pacfm/model",
"pacfm/model/helper",
"pacfm/model/helper/config",
"pacfm/model/tools",
"pacfm/model/tools/circos",
"pacfm/model/tools/pathway",
"pacfm/view",
"pacfm/view/commandline",
"pacfm/view/gui",
"pacfm/view/gui/helper",
"pacfm/view/gui/helper/config",
"pacfm/view/gui/helper/custom_control",
"pacfm/view/gui/helper/data",
"pacfm/view/gui/helper/dialog",
"pacfm/view/gui/main",
"pacfm/view/gui/main/display",
"pacfm/view/gui/tools",
"pacfm/view/gui/tools/circos",
"pacfm/view/gui/tools/pathway",
"pacfm/bootstrap"                    
          ],



      install_requires = ['matplotlib', 'pandas', 'svgutils', 'biodb'],

      dependency_links= ["https://github.com/ecotox/biodb/tarball/master#egg=biodb-0.0.1"]
      )




