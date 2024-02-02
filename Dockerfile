# Use aidinisg/dlicv:0.0.0 as the base image
FROM scitran/fsl-fast:latest as fsl-fast
FROM aidinisg/dlicv:0.0.0

COPY --from=fsl-fast /usr/local/fsl /usr/local/fsl
ENV FSLDIR=/usr/local/fsl
ENV PATH=$FSLDIR/bin:$PATH
ENV FSLOUTPUTTYPE=NIFTI_GZ

RUN mkdir /NiChart_Tissue_Segmentation/ && \
    cd /NiChart_Tissue_Segmentation/ && \ 
    git clone https://github.com/georgeaidinis/NiChart_Tissue_Segmentation/ && \ 
    cp /DLICV/model /NiChart_Tissue_Segmentation/ && \
    pip install .

# Set the default command or entrypoint (optional, depending on your package needs)
ENTRYPOINT ["NiChart_Tissue_Segmentation", "--model", "/NiChart_Tissue_Segmentation/model/"]
CMD ["--help"]