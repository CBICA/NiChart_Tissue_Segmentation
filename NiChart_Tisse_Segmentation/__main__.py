# This Python file uses the following encoding: utf-8
"""
contact: software@cbica.upenn.edu
Copyright (c) 2018 University of Pennsylvania. All rights reserved.
Use of this source code is governed by license located in license file: https://github.com/CBICA/NiChart_Tissue_Segmentation/LICENSE
"""

import argparse
import sys

import pkg_resources  # part of setuptools
from NiChart_Tissue_Segmentation import Segmentation

VERSION = pkg_resources.require("NiChart_DLMUSE")[0].version

def main():
    prog = "NiChart_Tissue_Segmentation"
    description = "NiChart Brain Tissue Segmentation Pipeline"
    usage = """
    NiChart_Tissue_Segmentation v{VERSION}
    ICV calculation, tossie segmentation for structural MRI data.

    required arguments:
        [INDIR]         The filepath of the directory containing the input. The 
        [-i, --indir]   input can be a single .nii.gz (or .nii) file or a  
                        directory containing .nii.gz files (or .nii files). 

        [OUTDIR]        The filepath of the directory where the output will be
        [-o, --outdir]  saved.
    
        [-h, --help]    Show this help message and exit.
        
        [-V, --version] Show program's version number and exit.

        EXAMPLE USAGE:
        
        NiChart_Tissue_Segmentation  --indir  /path/to/input     \
                                     --outdir /path/to/output
    """.format(VERSION=VERSION)

    parser = argparse.ArgumentParser(prog=prog,
                                     usage=usage,
                                     description=description,
                                     add_help=False)
    
    ################# Required Arguments #################
    # INDIR argument
    parser.add_argument('-i',
                        '--indir', 
                        '--inDir',
                        '--input',
                        type=str, 
                        help='Input T1 image file path.', 
                        default=None, 
                        required=True)
    
    # OUTDIR argument
    parser.add_argument('-o',
                        '--outdir', 
                        '--outDir',
                        '--output',
                        type=str,
                        help='Output file name with extension.', 
                        default=None, required=True)
    
    # VERSION argument
    help = "Show the version and exit"
    parser.add_argument("-V", 
                        "--version", 
                        action='version',
                        version=prog+ ": v{VERSION}.".format(VERSION=VERSION),
                        help=help)

    # HELP argument
    help = 'Show this message and exit'
    parser.add_argument('-h', 
                        '--help',
                        action='store_true', 
                        help=help)
    
        
    args = parser.parse_args()

    indir = args.indir
    outdir = args.outdir
    
    print()
    print("Arguments:")
    print(args)
    print()


if __name__ == '__main__':
    main()
