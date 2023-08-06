import matplotlib.pyplot as plt
import numpy as np
import pickle


def visualize_reference(show_curve=True, reference_data_path="./data/ref_data.json", curve_data_path="./data/curve_data.npy", transparency=1.0):
    """
    Visualize the distribution of reference data. Users can choose whether to show the radiomic trajectory.
    Args:
        show_curve (bool, optional): Whether to show the trajectory together with data points. Defaults to True.
        reference_data_path (str, optional): Path to the reference data. Defaults to "./data/ref_data.npy".
        curve_data_path (str, optional): Path to the curve points data. Defaults to "./data/curve_data.npy".
        transparency (float, optional): The degree of transparency of reference data points. Defaults to 1.0.
    Returns:
        fig: Generated figure.
    """
    with open(reference_data_path, 'rb') as f:
        ref_data = pickle.load(f)
    pca_embed = ref_data["pca_embed"]
    labels = ref_data["labels"]

    fig = plt.figure(figsize=(10,3))
    c0 = plt.scatter(pca_embed[labels==0,0], pca_embed[labels==0,1], c='blue', label='AIS', s=10, alpha=transparency)
    c1 = plt.scatter(pca_embed[labels==1,0], pca_embed[labels==1,1], c='lime', label='MIA', s=10, alpha=transparency)
    c2 = plt.scatter(pca_embed[labels==2,0], pca_embed[labels==2,1], c='olive', label='AIC-I', s=10, alpha=transparency)
    c3 = plt.scatter(pca_embed[labels==3,0], pca_embed[labels==3,1], c='orange', label='IAC-II', s=10, alpha=transparency)
    c4 = plt.scatter(pca_embed[labels==4,0], pca_embed[labels==4,1], c='red', label='IAC-III', s=10, alpha=transparency)
    plt.legend()
    plt.xlabel("PCA_1")
    plt.ylabel("PCA_2")
    plt.xlim([-1.6,2])
    plt.ylim([-0.6, 0.6])

    if show_curve:
        curve = np.load(curve_data_path)
        plt.plot(curve[:,0], curve[:,1], c='black', linewidth=0.8)
    
    return fig


def visualize(pca_embed, show_reference=True, reference_data_path="./data/ref_data.json", curve_data_path="./data/curve_data.npy", transparency=0.2):
    """
    Visualize the distribution of query tumor. Users can choose whether to show the refernce data.
    Args:
        pca_embed (_type_): The PCA embedding of inference data, should be in shape (N, 2)
        show_reference (bool, optional): Whether to show reference data and trajectory. Defaults to True.
        transparency (float, optional): The degree of transparency of reference data points. Defaults to 0.2.
    Returns:
        fig: Generated figure.
    """
    if show_reference:
        fig = visualize_reference(reference_data_path=reference_data_path, curve_data_path=curve_data_path, transparency=transparency)
        plt.scatter(pca_embed[:,0], pca_embed[:,1], s=10, c='purple')
    else:
        fig = plt.figure(figsize=(10,3))
        plt.scatter(pca_embed[:,0], pca_embed[:,1], s=10, c='purple')
        plt.xlim([-1.6,2])
        plt.ylim([-0.6, 0.6])
        plt.xlabel("PCA_1")
        plt.ylabel("PCA_2")
    
    return fig



