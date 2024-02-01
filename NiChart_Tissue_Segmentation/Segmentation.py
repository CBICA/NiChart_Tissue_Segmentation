import subprocess
import os
import nibabel as nib
from nibabel.orientations import axcodes2ornt, inv_ornt_aff, ornt_transform
import numpy as np
from scipy import ndimage
from scipy.ndimage.measurements import label

## Find bounding box for the foreground values in img, with a given padding percentage
def calc_bbox_with_padding(img, perc_pad = 10):
    
    img = img.astype('uint8')
    
    ## Output is the coordinates of the bounding box
    bcoors = np.zeros([3,2], dtype=int)
    
    ## Find the largest connected component 
    ## INFO: In images with very large FOV DLICV may have small isolated regions in
    ##       boundaries; so we calculate the bounding box based on the brain, not all
    ##       foreground voxels
    str_3D = np.array([[[0, 0, 0], [0, 1, 0], [0, 0, 0]],
                       [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
                       [[0, 0, 0], [0, 1, 0], [0, 0, 0]]], dtype='uint8')
    labeled, ncomp = label(img, str_3D)
    sizes = ndimage.sum(img, labeled, range(ncomp + 1))
    img_largest_cc = (labeled == np.argmax(sizes)).astype(int)

    ## Find coors in each axis
    for sel_axis in [0, 1, 2]:
    
        ## Get axes other than the selected
        other_axes = [0, 1, 2]
        other_axes.remove(sel_axis)
        
        ## Get img dim in selected axis
        dim = img_largest_cc.shape[sel_axis]
        
        ## Find bounding box (index of first and last non-zero slices)
        nonzero = np.any(img_largest_cc, axis = tuple(other_axes))
        bbox= np.where(nonzero)[0][[0,-1]]    
        
        ## Add padding
        size_pad = int(np.round((bbox[1] - bbox[0]) * perc_pad / 100))
        b_min = int(np.max([0, bbox[0] - size_pad]))
        b_max = int(np.min([dim, bbox[1] + size_pad]))
        
        bcoors[sel_axis, :] = [b_min, b_max]
    
    return bcoors

def apply_reorient(in_img_name, out_img_name, ref_img_name = None):
    '''Reorient input image
       - If provided, to ref img orientation
       - If not, to LPS
    '''
    ## Read input img
    nii_in = nib.load(in_img_name)

    ## Detect target orient
    if ref_img_name is None:
        ref_orient = 'LPS'
    else:
        nii_ref = nib.load(ref_img_name)
        ref_orient = nib.aff2axcodes(nii_ref.affine)
        ref_orient = ''.join(ref_orient)

    # Find transform from current (approximate) orientation to
    # target, in nibabel orientation matrix and affine forms
    orient_in = nib.io_orientation(nii_in.affine)
    orient_out = axcodes2ornt(ref_orient)
    transform = ornt_transform(orient_in, orient_out)
    affine_xfm = inv_ornt_aff(transform, nii_in.shape)

    # Apply transform
    reoriented = nii_in.as_reoriented(transform)
    
    # Write to out file
    reoriented.to_filename(out_img_name)


def apply_mask_to_image(in_img_name, mask_img_name, out_img_name):
    ## Read input image and mask
    nii_in = nib.load(in_img_name)
    nii_mask = nib.load(mask_img_name)

    img_in = nii_in.get_fdata()
    img_mask = nii_mask.get_fdata()

    ## Mask image
    img_in[img_mask == 0] = 0

    # ################################
    # ## INFO: nnunet hallucinated on images with large FOV. To solve this problem
    # ##       we added pre/post processing steps to crop initial image around ICV 
    # ##       mask before sending to DLMUSE
    # ##
    # ## Crop image
    # bcoors = calc_bbox_with_padding(img_mask)
    # img_in_crop = img_in[bcoors[0,0]:bcoors[0,1], bcoors[1,0]:bcoors[1,1], bcoors[2,0]:bcoors[2,1]]    

    ## Save out image
    # nii_out = nib.Nifti1Image(img_in_crop, nii_in.affine, nii_in.header)    
    nii_out = nib.Nifti1Image(img_in, nii_in.affine, nii_in.header)    
    nii_out.to_filename(out_img_name)

def perform_tissue_segmentation(input_path, output_path):
    """Perform tissue segmentation using FSL's FAST."""
    fast_command = ["fast", "-o", str(output_path), str(input_path)]
    subprocess.run(fast_command)