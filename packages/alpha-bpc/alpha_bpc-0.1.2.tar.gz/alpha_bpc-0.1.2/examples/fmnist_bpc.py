"""Example of using BPC for feature extraction on MNIST dataset.
ImageSelectionMethod = 1: C-KS
ImageSelectionMethod = 2: CRS
ImageSelectionMethod = 3: RS
"""

# Remember to set PythonPath = ".." in the Run/Debug Configuration

from alpha_bpc.BPC import BPC
from alpha_bpc.utils.load_fmnist import load_fmnist as lf


def main():
    x_train, y_train = lf("../data/fmnist", kind="train")

    y_train = (
        y_train.copy() + 1
    )  # Since our framework operates on 1-10, and not 0-9
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
    