import monai
import torch
import torch.nn as nn
import pickle


class Model(nn.Module):
    def __init__(self, net, embed_dim=32):
        super(Model, self).__init__()
        self.net = net
        self.flatten = nn.Flatten(start_dim=1, end_dim=-1)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
        self.fc1 = nn.Linear(2048, 128, bias=True)
        self.fc2 = nn.Linear(129, embed_dim, bias=True)
        
    def forward(self, x, add_variable):
        x = self.net(x)
        x = self.flatten(x)
        x = torch.cat((self.dropout(self.relu(self.fc1(x))), add_variable.unsqueeze(1)),1)
        x = self.fc2(x)
        return x


def get_model(wpath="./data/cnn_proj_weights.pkl"):
    """
    Args:
        wpath (str): path to the saved model weights file.
    Returns:
        model: a CNN model with pre-trained weights loaded. (In CPU)
    """
    temp_model = monai.networks.nets.Classifier(in_shape=(1,64,64,64), classes=5, channels=(8,8,4), strides=(2,2,2))
    net = temp_model.net
    model = Model(net)

    weights = torch.load(wpath)
    model.load_state_dict(weights)

    return model


def get_pca(ppath="./data/pca_trans.sav"):
    """
    Args:
        ppath (str): path to the saved PCA transform function.
    Returns:
        pca_trans: a pre-trained PCA transform function
    """
    return pickle.load(open(ppath, 'rb'))

