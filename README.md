# NiChart_Tissue_Segmentation

Brain tissue segmentation using FSL FAST and DLICV

## Overview

NiChart_Tissue_Segmentation offers easy brain tissue segmantation.

This is achieved through the [DLICV](https://github.com/CBICA/DLICV) and [FAST](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FAST) methods. Intermediate step results are saved for easy access to the user.

Given an input (sMRI) scan, NiChart_Tissue_Segmentation extracts the following:

1. ICV mask
2. ICV image
3. Tissue segmentation

This package uses [nnUNet](https://github.com/MIC-DKFZ/nnUNet/tree/nnunetv1) (version 1) as a basis model architecture for the deep learning parts, [nipype](https://nipy.org/packages/nipype/index.html) for the workflow management and various other [libraries](requirements.txt).

It is available both as an installable package, as well as a [docker container](https://hub.docker.com/repository/docker/aidinisg/nichart_tissue_segmentation/general). Please see [Installation](#installation) and [Usage](#usage) for more information on how to use it.

## Installation

1. Create a new conda env

    ```bash
    conda create --name NCTS python=3.8
    conda activate NCTS
    ```

    In one command:

    ```bash
    conda create --name NCTS -y python=3.8 && conda activate NCTS
    ```

2. Clone and install NiChart_Tissue_Segmentation

    ```bash
    git clone  https://github.com/CBICA/NiChart_Tissue_Segmentation.git
    cd NiChart_Tissue_Segmentation
    pip install .
    ```

3. Run NiChart_Tissue_Segmentation. Example usage below

    ```bash
    NiChart_Tissue_Segmentation --indir                     /path/to/input     \
                                --outdir                    /path/to/output
    ```

## Docker/Singularity/Apptainer-based build and installation

The package comes already pre-built as a [docker container](https://hub.docker.com/repository/docker/aidinisg/nichart_tissue_segmentation/general), for convenience. Please see [Usage](#usage) for more information on how to use it. Alternatively, you can build the docker image locally, like so:

```bash
docker build -t nichart_tissue_segmentation .
```

Singularity and Apptainer images can be built for NiChart_Tissue_Segmentation, allowing for frozen versions of the pipeline and easier installation for end-users.
Note that the Singularity project recently underwent a rename to "Apptainer", with a commercial fork still existing under the name "Singularity" (confusing!).
Please note that while for now these two versions are largely identical, future versions may diverge. It is recommended to use the AppTainer distribution. For now, these instructions apply to either.

First install [the container engine](https://apptainer.org/admin-docs/3.8/installation.html).
Then, from the cloned project repository, run:

```bash
singularity build nichart_tissue_segmentation.sif singularity.def
```

This will take some time, but will build a containerized version of your current repo. Be aware that this includes any local changes!
The nichart_tissue_segmentation.sif file can be distributed via direct download, or pushed to a container registry that accepts SIF images.

## Usage

Pre-trained nnUNet models for the skull-stripping and segmentation tasks can be found in the [NiChart_Tissue_Segmentation - 0.0.0](https://github.com/CBICA/NiChart_Tissue_Segmentation/releases/tag/0.0.0) release as an [artifact](https://github.com/CBICA/NiChart_Tissue_Segmentation/releases/download/0.0.0/nnUNet_model.zip). Feel free to use it under the package's [license](LICENSE).

Due to the [nnunetv1](https://github.com/MIC-DKFZ/nnUNet/tree/nnunetv1) dependency, the package follows nnUNet's requirements for folder structure and naming conventions. It is recommended that you follow this guide's structure and logic, so that the issues arising from the requirements of the nnUNet dependency are minimized.

The model provided as an artifact is already in the file structure that's needed for the package to work, so make sure to include it as downloaded.
The `nnUNet_preprocessed`, `nnUNet_raw_database` directories are needed for the nnUNet library to store (if needed) temporary files. It is highly suggested that you keep these in the same directory as the model and the data, as to avoid any confusion with using the library. This will be fixed in upcoming releases.

Therefore assuming the following folder structure:

```bash
temp
├── nnUNet_model            // As provided from the release
│   └── nnUNet
├── nnUNet_out              // Output destination
├── nnUNet_preprocessed     // Empty
└── nnUNet_raw_database     // Empty
    └── nnUNet_raw_data     // Input folder. Image names are irrelevant.
        ├── image1.nii.gz
        ├── image2.nii.gz
        └── image3.nii.gz
```

### As a locally installed package

A complete command would be (run from the directory of the package):

```bash
NiChart_Tissue_Segmentation -i /path/to/input/ \
                            -o /path/to/output/ \
                            -m /path/to/model/
```

For further explanation please refer to the complete documentation:

```bash
NiChart_Tissue_Segmentation -h
```

### Using the docker container

An example command using the [docker container](https://hub.docker.com/repository/docker/aidinisg/nichart_tissue_segmentation/general) is the following:

```bash
docker run -it --rm --gpus all -v ./:/workspace/ aidinisg/nichart_tissue_segmentation:0.0.0 NiChart_Tissue_Segmentation -i path/to/input -o path/to/output
```