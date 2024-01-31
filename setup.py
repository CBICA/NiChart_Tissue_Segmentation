from setuptools import setup, find_packages
import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='NiChart_Tissue_Segmentation',
      version='0.1.7',
      description='Run NiChart_Tissue_Segmentation on your data(currently only structural pipeline is supported).',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Ashish Singh, Guray Erus, George Aidinis',
      author_email='software@cbica.upenn.edu',
      license='MIT',
      url="https://github.com/CBICA/NiChart_Tissue_Segmentation",
	  install_requires=[
        'torch<2.1',
        'nnunet==1.7.1'
    ],
    entry_points={
        'console_scripts': [
            'NiChart_Tissue_Segmentation = NiChart_Tissue_Segmentation.__main__:main'
        ]        
    },    
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Operating System :: Unix',
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,	
      )
