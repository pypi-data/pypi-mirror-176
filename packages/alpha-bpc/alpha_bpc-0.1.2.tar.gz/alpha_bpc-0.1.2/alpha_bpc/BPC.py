"""Main module."""
import logging as log
import numpy as np
from utils.cks import ks_variant
from utils.crs import crs
from utils.rs import rs
from utils.convolve_filts import convolve_filts
from utils.extract_filters import extract_filters_np


class BPC:
    """
    Class for Binay Patch Convolution Framework
    """

    sample_algorithms = {
        1: ks_variant,
        2: crs,
        3: rs,
    }

    def __init__(
        self,
        x_train,
        y_train,
        num_clusters=None,
        image_selection_method=1,
        precomputed_filters=None,
        threshold=95,
        orig_img_size=(28, 28),
        patch_size=(14, 14),
        center_patch=True,
        bsize=64,
        verbose=False,
    ) -> None:

        """Initialize the BPC class.

        :param x_train: Training data
        :param y_train: Training labels
        :param num_clusters: Number of clusters to be used if using clustering based sampling
        :param image_selection_method: Method to be used for sampling, 1 for C-KS, 2 for C-RS, 3 for RS
        :param precomputed_filters: Precomputed filters to be used for convolution
        :param threshold: Threshold for binarizing patches
        :param orig_img_size: Original image size, used for for reshaping selected images
        :param patch_size: Size of the patches to be extracted
        :param center_patch: Whether to include the center patch or not
        :param bsize: Batch size for convolution operation (default: 64)
        :param verbose: Whether to print progress or not (default: False)

        Raises
        ------
        ValueError
            If the image selection method is not 1, 2 or 3
        ValueError
            If the image selection method is 1 or 2 and the number of clusters is not provided
        ValueError
            If x_train and y_train are not of the same length
        ValueError
            If x_train is 3D
        """

        if verbose:

            def _v_print(text):
                print(text)

        else:
            _v_print = lambda text: None

        global v_print
        v_print = _v_print

        if image_selection_method not in self.sample_algorithms.keys():
            raise ValueError("Image selection method should be 1, 2 or 3")
        if x_train.shape[0] != y_train.shape[0]:
            raise ValueError("x_train and y_train must have the same length")
        # If x_train is 3D , raise value error tellling them to flatten it
        if x_train.ndim > 2:
            raise ValueError("x_train must be 2D (please flatten it)")
        if y_train is None or x_train is None:
            raise ValueError("y_train and x_train must not be None")

        self.x_train = x_train
        self.y_train = y_train

        self.threshold = threshold
        self.orig_img_size = orig_img_size
        self.patch_size = patch_size
        self.center_patch = center_patch
        self.bsize = bsize

        if image_selection_method != 3 and num_clusters is None:
            raise ValueError(
                "Num_clusters must be specified for random supervised image selection method"
            )

        self.num_clusters = num_clusters

        self.image_selection_method = image_selection_method

        if precomputed_filters is not None:
            self.filters = precomputed_filters
        else:
            self.filters = None

    def fit(self, img_per_cluster):
        """
        Fit the model
        :param img_per_cluster: Number of images to be selected per cluster, or number of images to be selected per group if using random sampling
        """

        if self.filters is not None:

            self.x_convolved = convolve_filts(
                self.x_train,
                self.filters,
            )

            self.x_convolved_extended = np.hstack(
                (self.x_train, self.x_convolved)
            )

            v_print("Convolution done")

            return self.x_convolved_extended

        if self.image_selection_method == 3:

            self.selected_images = self.sample_algorithms[
                self.image_selection_method
            ](self.x_train, self.y_train, img_per_cluster)
        else:

            self.selected_images = self.sample_algorithms[
                self.image_selection_method
            ](
                self.x_train,
                self.y_train,
                self.num_clusters,
                img_per_cluster,
            )

        if self.image_selection_method == 1:
            self.selected_images = np.concatenate(self.selected_images)
        else:
            self.selected_images = np.asarray(self.selected_images)

        self.selected_images = self.selected_images.reshape(
            self.selected_images.shape[0],
            self.orig_img_size[0],
            self.orig_img_size[1],
        )
        v_print("Image selection done")

        self.filters = extract_filters_np(
            self.selected_images,
            threshold=self.threshold,
            kernel_size=self.patch_size,
            center=self.center_patch,
        )
        self.filters = self.filters.reshape(
            self.filters.shape[0] * self.filters.shape[1],
            self.patch_size[0],
            self.patch_size[1],
        )
        v_print("Filter extraction done")

        v_print("Completed fitting")

        return self

    def transform(self, x_test):
        """
        Transform the test data
        :param x_test: Test data
        :return: Transformed test data
        """

        if self.filters is None:
            raise ValueError("Model must be fitted before transforming")

        x_test_convolved = convolve_filts(
            x_test.reshape(x_test.shape[0], *self.orig_img_size),
            None,
            self.filters,
            bsize=self.bsize,
        )

        x_test_convolved_extended = np.hstack((x_test, x_test_convolved))

        return x_test_convolved_extended

    def fit_transform(self, img_per_cluster):
        """
        Fit the model and transform the training data
        :param img_per_cluster: Number of images to be selected per cluster, or number of images to be selected per group if using random sampling
        """

        self.fit(img_per_cluster)

        x_convolved = convolve_filts(
            self.x_train.reshape(self.x_train.shape[0], *self.orig_img_size),
            None,
            self.filters,
            bsize=self.bsize,
        )

        x_convolved_extended = np.hstack((self.x_train, x_convolved))

        v_print("Convolution done")

        return x_convolved_extended


if __name__ == "__main__":
    print(__package__)
