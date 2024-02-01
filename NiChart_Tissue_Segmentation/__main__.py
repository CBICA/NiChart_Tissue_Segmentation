# This Python file uses the following encoding: utf-8
"""
contact: software@cbica.upenn.edu
Copyright (c) 2018 University of Pennsylvania. All rights reserved.
Use of this source code is governed by license located in license file: https://github.com/CBICA/NiChart_Tissue_Segmentation/LICENSE
"""

import argparse
import sys
import tempfile
import shutil
from pathlib import Path
import pkg_resources  # part of setuptools
from DLICV.compute_icv import compute_volume

VERSION = pkg_resources.require("NiChart_Tissue_Segmentation")[0].version

def validate_path(parser, arg):
    """Ensure the provided path exists."""
    if not Path(arg).exists():
        parser.error(f"The path {arg} does not exist.")
        sys.exit(1)
    return arg

def copy_and_rename_inputs(input_path, destination_dir):
    """Copy and rename input files according to nnUNet convention."""
    input_path = Path(input_path)
    destination_dir = Path(destination_dir)
    
    if input_path.is_dir():
        for filepath in input_path.glob('*.nii.gz'):
            new_filename = filepath.stem.split('.')[0] + '_0000.nii.gz'
            shutil.copy(filepath, destination_dir / new_filename)
    else:
        new_filename = input_path.stem + '_0000.nii.gz'
        shutil.copy(input_path, destination_dir / new_filename)

def main():
    prog = "NiChart_Tissue_Segmentation"
    description = "NiChart Brain Tissue Segmentation Pipeline"
    usage = """
    NiChart_Tissue_Segmentation v{VERSION}
    ICV calculation, tossie segmentation for structural MRI data.

    required arguments:
        [INPUT]         The filepath of the directory containing the input. The 
        [-i, --input]   input can be a single .nii.gz (or .nii) file or a  
                        directory containing .nii.gz files (or .nii files). 

        [OUTPUT]        The filepath of the directory where the output will be
        [-o, --output]  saved.
    
        [MODEL]         The filepath of the nNUnet model to be used for ICV 
        [-m, --model]   extraction.

        [KWARGS]        The keyword arguments for the nNUnet model arch. Please
        [-k, --kwargs]  visit the DLICV package for more documentation.
    
        
        [-h, --help]    Show this help message and exit.
        
        [-V, --version] Show program's version number and exit.

        EXAMPLE USAGE:
        
        NiChart_Tissue_Segmentation  --input  /path/to/input     \
                                     --output /path/to/output
    """.format(VERSION=VERSION)

    parser = argparse.ArgumentParser(prog=prog,
                                     usage=usage,
                                     description=description,
                                     add_help=False)
    
    ################# Required Arguments #################
    # INPUT argument
    parser.add_argument('-i',
                        '--input_path', 
                        '--input',
                        type=str, 
                        help='Input T1 image file path.', 
                        default=None, 
                        required=True)
    
    # OUTPUT argument
    parser.add_argument('-o',
                        '--output_path', 
                        '--output',
                        type=str,
                        help='Output file name with extension.', 
                        default=None, required=True)
    
    # MODEL argument
    parser.add_argument("-m",
                        "--model_path",
                        "--model",
                        type=lambda x: validate_path(parser, x), 
                        help="Model path.",
                        default=None, required=True)
    
    # KWARGS
    parser.add_argument("-k",
                        "--kwargs", 
                        nargs=argparse.REMAINDER, 
                        help="Additional keyword arguments to pass to compute_icv.py",
                        default=None, required=False)
    
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
    
    input_path = args.input_path
    output_path = args.output_path
    model_path = args.model_path
    kwargs = {}
    
    if args.kwargs:
        for kwarg in args.kwargs:
            key, value = kwarg.split('=', 1)
            kwargs[key] = value

    # Create cross-platform temp dir, and child dirs that nnUNet needs
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_input_dir = Path(temp_dir) / "nnUNet_raw_data"
        temp_preprocessed_dir = Path(temp_dir) / "nnUNet_preprocessed"
        temp_output_dir = Path(temp_dir) / "nnUNet_out"
        temp_input_dir.mkdir()
        temp_output_dir.mkdir()

        copy_and_rename_inputs(input_path, temp_input_dir)
        compute_volume(
            str(temp_input_dir),
            str(temp_output_dir),
            model_path,
            **kwargs
        )

        # Move results to the specified output location, including only .nii.gz files
        dlicv_mask_dir = Path(output_path) / "DLICV_mask"
        dlicv_mask_dir.mkdir(exist_ok=True)
        for file in temp_output_dir.iterdir():
            if file.suffixes == ['.nii', '.gz']:
                shutil.move(str(file), dlicv_mask_dir)
        print()
        print()
        print()
        print(f"Prediction complete. Results saved to {output_path}")


if __name__ == '__main__':
    main()
