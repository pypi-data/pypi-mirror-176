import numpy as np


def locate_tumor(image, mask, label=1, padding=2):
    """
    Locate and extract tumor from CT image using mask
    Args:
        img: Numpy array. The whole image.
        mask: Numpy array. Same size as img, background is 0.
        label: Int. The value of mask foreground.
        padding: Int. Number of pixels padded on each side after extracting tumor.
    Returns:
        sub_img: Numpy array. The tumor area defined by mask.
        sub_mask: Numpy array. The subset of mask in the same position of sub_img.
    """
    top_margin = min(np.where(mask == label)[0])
    bottom_margin = max(np.where(mask == label)[0])
    front_margin = min(np.where(mask == label)[1])
    back_margin = max(np.where(mask == label)[1])
    left_margin = min(np.where(mask == label)[2])
    right_margin = max(np.where(mask == label)[2])
    sub_img = image[max(0, top_margin - padding):min(bottom_margin + padding + 1, image.shape[0]-1), 
                max(0, front_margin - padding):min(back_margin + padding + 1, image.shape[1]-1),
                max(0, left_margin - padding):min(right_margin + padding + 1, image.shape[2]-1)]
    sub_mask = mask[max(0, top_margin - padding):min(bottom_margin + padding + 1, mask.shape[0]-1), 
                max(0, front_margin - padding):min(back_margin + padding + 1, mask.shape[1]-1),
                max(0, left_margin - padding):min(right_margin + padding + 1, mask.shape[2]-1)]
    return sub_img, sub_mask

