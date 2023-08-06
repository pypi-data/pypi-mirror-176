import numpy as np
import pickle
from rpy2.robjects import r
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

def calPPS(infer_data, reference_data_path="./data/ref_data.json", traj_obj_path="./data/traj_obj.rds"):
    """
    Calculate the Pseudo-Progression Score (PPS) for the inference data.
    Args:
        infer_data (Numpy array): The PCA embedding(s) of inference data, should be in shape (N, 2)
        reference_data_path (str, optional): Path to the reference data. Defaults to "./data/ref_data.json".
        traj_obj_path (str, optional): Path to the trajecory object. . Defaults to "./data/traj_obj.rds".

    Returns:
        infer_pred_ps: The inferenced PPS which quantifies the progression status of early-stage LUAD.
    """
    pandas2ri.numpy2ri.activate()
    slingshot = importr("slingshot")

    with open(reference_data_path, 'rb') as f:
        ref_data = pickle.load(f)
    train_data = ref_data["pca_embed"]
    traj_obj = r.readRDS(traj_obj_path)

    infer_len = infer_data.shape[0]
    infer_data_aug = r.rbind(infer_data, train_data)
    infer_pred_aug = slingshot.predict(slingshot.as_SlingshotDataSet(traj_obj), infer_data_aug)
    infer_pred_ps_aug = slingshot.slingPseudotime(infer_pred_aug).flatten()
    infer_pred_ps = infer_pred_ps_aug[:infer_len]

    return infer_pred_ps
