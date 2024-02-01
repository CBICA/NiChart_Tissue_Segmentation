# Use aidinisg/dlicv:0.0.0 as the base image
FROM aidinisg/dlicv:0.0.0

 

# Install dependencies and FSL using Neurodebian
# First, add the Neurodebian repository
RUN apt-get update && apt-get install -y software-properties-common gnupg && wget -O- http://neuro.debian.net/lists/focal.us-nh.full | tee /etc/apt/sources.list.d/neurodebian.sources.list && wget -qO - http://neuro.debian.net/_static/neuro.debian.net.asc | apt-key add -
 

# Update apt-get and install FSL
RUN apt-get update && \
    apt-get install -y fsl-complete && \
    apt-get install -y --no-install-recommends unzip && \
    mkdir /NiChart_Tissue_Segmentation/ && \
    cd /NiChart_Tissue_Segmentation/ && \
    git clone https://github.com/georgeaidinis/NiChart_Tissue_Segmentation/

RUN mkdir /NiChart_Tissue_Segmentation/model
COPY ./temp/model/* /NiChart_Tissue_Segmentation/model/

# ADD https://github.com/CBICA/DLICV/releases/download/v0.0.0/model.zip /NiChart_Tissue_Segmentation/
# RUN unzip /NiChart_Tissue_Segmentation/model.zip /NiChart_Tissue_Segmentation/ && \
#     rm -rf /NiChart_Tissue_Segmentation/model.zip && \
#     echo "FSL installation:" && which fsl

# Set the default command or entrypoint (optional, depending on your package needs)
ENTRYPOINT ["NiChart_Tissue_Segmentation", "--model", "/NiChart_Tissue_Segmentation/model/"]
CMD ["--help"]