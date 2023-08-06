import os
import SimpleITK as sitk
from .utils import read_dcm_series


def load_image(path):
    """
    Load CT image volume
    Args:
        path: Str. Path to the .nii(.gz) file or dicom series directory
    Returns:
        image: Numpy array. The 3D CT volume.
    """
    if os.path.isdir(path):
        sitk_image = read_dcm_series(path)
    else:
        sitk_image = sitk.ReadImage(path)
    image = sitk.GetArrayFromImage(sitk_image)

    return image


def load_seg(path):
    """
    Load segmentation mask
    Args:
        path: Str. Path to the .nii or .dcm mask.
    Returns:
        seg: Numpy array. The mask of ROI with the same shape of image.
    """
    if path.endswith(".dcm"):
        # RTStruct dcm file sometimes cannot be loaded by SimpleITK
        ds = dicom.read_file(path)
        seg = ds.pixel_array
    else:
        sitk_seg = sitk.ReadImage(path)
        seg = sitk.GetArrayFromImage(sitk_seg)

    return seg