# radiotrace

**radiotrace** is a Python package to quantify and visualize the progression status of early-stage lung adenocarcinoma (esLUAD) from CT images. It is designed and developed by Jiaqi Li from [XGlab](http://bioinfo.au.tsinghua.edu.cn/member/xuegonglab/), Tsinghua University. The work is collaborated with Prof. Wenzhao Zhong's group from Guangdong Provincial People's Hospital and Prof. Lin Yang's group from Shenzhen People's Hospital.

**radiotrace** package is **free for academic use**. Please contact the authors for commercial usage.

## Install
The **radiotrace** package integrates the use of Python and R. Don't worry, we have wrapped the R functions in the Python code and users only need to install some packages and then write Python code only.  

BTW, consider the potential conflicts of packages, we strongly suggest you to install the packages in a new [anaconda](https://www.anaconda.com/products/distribution) environment :)  

First let's install the python packages. Please pay special attention to PyTorch if you want to use GPU. It is easy to download the proper version of GPU version PyTorch from the official webpage (https://pytorch.org/get-started/locally/). In this case, make sure that you install the GPU version PyTorch before install **radiotrace**.  

After that, or if you only need CPU version PyTorch, install **radiotrace** packages.
```
pip install radiotrace
```  

Next, let's install the R packages. We also install the R using anaconda:  
```
conda install -c conda-forge r-base
```  

Then enter the R programming software by one character of code:
```
R
```

The R package we need is the slingshot (Street et al., BMC Genomics, 2018), which can be installed from [Bioconductor](https://www.bioconductor.org/packages/release/bioc/html/slingshot.html). Here we use two lines of code to install these two packages:  
```R
install.packages("BiocManager")  
BiocManager::install("slingshot")
```

Now we have finished package installation. It's time to explore the use of **radiotrace**.  



## Tutorial

By running **radiotrace** package users are walking through several steps: Load image and segmentation, Locate and extract tumor, Load projection functions, Inference the emebedding vector(s) and coordinate(s) in PCA space, Visualization and Quantify progression status. Here we did clustering on the pixel-wise radiomic features.   

### 0. Load packages

```python
import os
import numpy as np
import matplotlib.pyplot as plt

from radiotrace.load import load_image, load_seg
from radiotrace.locate import locate_tumor
from radiotrace.get_projection import get_model, get_pca
from radiotrace.inference import model_inference, pca_trans
from radiotrace.visualize import visualize_reference, visualize
from radiotrace.calPPS import calPPS
from radiotrace.utils import cal_tumor_size, get_largest_slice
```

### 1. Load image and segmentation

Here we use public NSCLC-RadioGenomics data as an example. This is a public dataset available on The Cancer Imaging Archive ([TCIA](https://www.cancerimagingarchive.net/)). Here the image and segmentation are stored in the NIFTI (.nii.gz) format.  


```python
dicom_path = "./RadioGenomics/R01-001_img.nii.gz"
seg_path = "./RadioGenomics/R01-001_seg.nii.gz"
image = load_image(dicom_path)
seg = load_seg(seg_path)
print(image.shape, seg.shape)
```

```
(304, 512, 512) (304, 512, 512)
```


### 2. Locate and extract tumor

Next, we locate the tumor using segmentation mask, and extract the tumor image with bounding box.   
```python
tumor_image, tumor_mask = locate_tumor(image, seg)
```

We can visualize a slice of the extracted tumor corresponding mask.
```python
img2d, mask2d = get_largest_slice(tumor_image, tumor_mask)
plt.subplot(121)
plt.imshow(img2d, cmap="bone")
plt.title("Tumor")
plt.subplot(122)
plt.imshow(img2d, cmap="bone")
plt.imshow(mask2d, alpha=0.5)
plt.title("Stack mask")
```

![p1](https://github.com/LiJiaqi96/radiotrace/blob/main/figures/p1.png)


### 3. Prepare data and load projection functions

We use a deep learning model and a PCA transform function to project the tumor image to the PCA space of training set. Here we prepare the tumor image data for model input and then load the projection functions.  

If you want to use GPU to do the inference, remember to specify the environment variable before loading the model.  

```python
size = [cal_tumor_size(tumor_mask)]
tumor_image = [tumor_image]

## Optional: specify GPU device
# os.environ['CUDA_VISIBLE_DEVICES'] = '1'

model = get_model("./data/cnn_proj_weights.pkl")
pca_func = get_pca("./data/pca_trans.sav")
```

Note that the input image should be in shape (N Z H W), and tumor size should be a list. Here we show the example of inference one tumor. Just append more samples to the list if you want to inference multiple samples.  


### 4. Project the tumor image to vectors

In this step, we will project the tumor image to the embedding vectors, then to the PCA spacce of training set. It will not take a long time when using CPU and it is very easy to switch between CPU and GPU mode using the argument "use_GPU".  

```python
pred_embed = model_inference(tumor_image, size, model, use_GPU=False)
pca_embed = pca_trans(pred_embed, pca_func)
```


### 5. Visualize the progression status of the inference tumor  

We provide two visualization functions for users to visualize the reference trajectory and samples in the training set, as well as the relative position of the inference tumors.  

```python
## Visualize the reference only
fig = visualize_reference(reference_data_path="./data/ref_data.json", curve_data_path="./data/curve_data.npy")
```
![p2](https://github.com/LiJiaqi96/radiotrace/blob/main/figures/p2.png)

```python
## Visualize the reference and inference tumors. Use "transparency" argument to adjust the color of training samples.
fig = visualize(reference_data_path="./data/ref_data.json", curve_data_path="./data/curve_data.npy", transparency=0.2)
```
![p3](https://github.com/LiJiaqi96/radiotrace/blob/main/figures/p3.png)


### 6. Calculate pseudo-progression score (PPS)

Finally, we quantify the progression status of the inference tumor(s). The PPS=0 indicates the earliest progression status. This step will return a list of PPS values.  

```python
pps = calPPS(pca_embed, reference_data_path="./data/ref_data.json", traj_obj_path="./data/traj_obj.rds")
```

```
[2.56895608]
```
