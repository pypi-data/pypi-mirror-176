"""Example of using BPC for feature extraction on MNIST dataset.
ImageSelectionMethod = 1: C-KS
ImageSelectionMethod = 2: CRS
ImageSelectionMethod = 3: RS
"""

# Remember to set PythonPath = ".." in the Run/Debug Configuration

from alpha_bpc.BPC import BPC
import scipy.io as sio
import numpy as np


def main():
    data = sio.loadmat("../data/mnist/mnistdata.mat")

    x_train = data["training"]
    x_train = x_train.reshape(x_train.shape[0], -1)
    y_train = np.concatenate(data["Gtrain"])
    num_clusters = 5
    num_imgs = 4

    BPC_extractor = BPC(
        x_train,
        y_train,
        num_clusters=num_clusters,
        verbose=True,
        image_selection_method=1,
    )

    x_train_convolved = BPC_extractor.fit_transform(num_imgs)
    print(x_train_convolved.shape)


if __name__ == "__main__":
    main()
