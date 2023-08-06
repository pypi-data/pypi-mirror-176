import torch
from torch.utils.data import Dataset, DataLoader
import monai
from monai.transforms import AddChannel, Resize, ScaleIntensity, EnsureType, Compose
from sklearn.decomposition import PCA


class earlyLUADDataset(Dataset):
    def __init__(self, tumors, sizes, transform):
        self.tumors = tumors
        self.sizes = sizes
        self.transform = transform
    
    def __len__(self):
        return len(self.sizes)
    
    def __getitem__(self, index):
        tumor = self.tumors[index]
        size = torch.scalar_tensor(self.sizes[index]/16000.)
        trans_tumor = self.transform(tumor)
        # tumor_tensor = torch.tensor(trans_tumor, dtype=torch.float)
        return trans_tumor, size


def model_inference(images, sizes, model, batch_size=1, unisize=(64,64,64), use_GPU=False):
    """
    Args:
        images (Numpy array or Torch tensor): The input tumor(s), should be in shape (N C Z H W).
        sizes (List of int): The corresponding tumor sizes, should be in shape (N 1).
        model (nn.Module): The loaded pre-trained CNN model.
        batch_size (Int): Batch size for model inference. Defaults to 1.
        unisize (tuple, optional): The uniformed size of input image. Defaults to (64,64,64).
    Returns:
        outputs (Numpy array): The embedding vector of the tumor, should be in shape (B 32)
    """
    trans_func = Compose([AddChannel(), Resize(spatial_size=unisize), ScaleIntensity(), EnsureType()])
    infer_data = earlyLUADDataset(images, sizes, trans_func)
    infer_loader = DataLoader(infer_data, batch_size=batch_size, num_workers=0)

    if use_GPU:
        model = model.cuda()
        model.eval()
        with torch.no_grad():
            preds = []
            for inputs, sizes in infer_loader:
                inputs = inputs.cuda()
                sizes = sizes.cuda()
                output = model(inputs, sizes)
                preds.append(output)
            preds = torch.concat(preds).cpu().data.numpy()
    else:
        model.eval()
        with torch.no_grad():
            preds = []
            for inputs, sizes in infer_loader:
                output = model(inputs, sizes)
                preds.append(output)
            preds = torch.concat(preds).numpy()
    
    return preds


def pca_trans(embed, pca):
    """
    Args:
        embed (Numpy array): The embedding vectors of tumors, should in shape (N, 32), N is the inference sample size and 32 is the embedding dimension.
    Returns:
        pca_embed (Numpy array): The coordinates of embedding vectors on the PCA space.
    """
    return pca.transform(embed)

