import subprocess
import os
import nibabel as nib

def apply_mask_to_image(image_path, mask_path, output_path):
    """Apply the given mask to the image and save the result."""
    image = nib.load(str(image_path))
    mask = nib.load(str(mask_path))
    masked_image = nib.Nifti1Image(image.get_fdata() * mask.get_fdata(), image.affine)
    nib.save(masked_image, str(output_path))


def perform_tissue_segmentation(input_path, output_path):
    """Perform tissue segmentation using FSL's FAST."""
    fast_command = ["fast", "-o", str(output_path), str(input_path)]
    subprocess.run(fast_command)