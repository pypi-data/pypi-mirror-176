import numpy as np
import SimpleITK as sitk
import six
from radiomics import featureextractor

def read_dcm_series(dcm_dir):
    """
    Args:
        dcm_dir: Str. Path to dicom series directory
    Returns:
        sitk_image: SimpleITK object of 3D CT volume.
    """
    reader = sitk.ImageSeriesReader()
    series_file_names = reader.GetGDCMSeriesFileNames(dcm_dir)
    reader.SetFileNames(series_file_names)
    sitk_image = reader.Execute()

    return sitk_image


def get_largest_slice(img3d, mask3d):
    """
    Get the slice with largest tumor area
    Args:
        img3d: Numpy array. The whole CT volume (3D)
        mask3d: Numpy array. Same size as img3d, binary mask with tumor area set as 1, background as 0
    Returns:
        img: Numpy array. The 2D image slice with largest tumor area
        mask: Numpy array. The subset of mask in the same position of sub_img
    """
    area = np.sum(mask3d == 1, axis=(1, 2))
    area_index = np.argsort(area)[-1]
    img = img3d[area_index, :, :]
    mask = mask3d[area_index, :, :]

    return img, mask


def cal_tumor_size(mask):
    """
    Args:
        mask: Numpy array. The mask of tumor with the same shape of image. Can be either the single mask or a list of masks.
    Returns:
        t_size: Int. The size of tumor.
    """
    mask = np.array(mask)
    if len(mask.shape)==4:
        return np.sum(mask, axis=(1,2,3))
    elif len(mask.shape)==3:
        return np.sum(mask)
    else:
        raise Exception("Mask size should be either single mask or a list of masks")
