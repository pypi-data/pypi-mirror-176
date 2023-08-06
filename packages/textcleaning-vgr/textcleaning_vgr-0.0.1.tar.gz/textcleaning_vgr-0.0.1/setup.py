from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'text cleaning'
LONG_DESCRIPTION = 'text clean before feeding to a sequence to sequence model'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="textcleaning_vgr", 
        version=VERSION,
        author="Gangadhara Reddy Velagala",
        author_email="<gv2310@columbia.edu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['nltk','spacy','pandas', 'wordninja','nltk',
        'spacy','en_core_web_lg'],
        
        keywords=['python'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)

