import os
from typing import Callable
from typing import Optional as O
from typing import Sequence
from typing import Union as U

import torch
from h5py import File
from torch.utils.data import Dataset
from torchvision.transforms import Compose

from ..base import data_readers, df_creators, df_manipulators
from ..base.histo_dataset import HistoDataset
from ..helper import helper

# TODO change to HistoDataset API


def pcam_patches(
    root: str,  # '/data/ldap/histopathologic/original_read_only/PCAM_extracted'
    transformation: O[U[Callable, Sequence[Callable]]] = None,
    #   pre_transformation: O[U[Callable, Sequence[Callable]]] = None, # pretrans not possible yet
    subset: O[str] = "train",
    seed: int = None,
) -> Dataset:
    """
    Creates the PCAM dataset and returns it as type torch.utils.data.Dataset.

    Data and further information can be found at https://humanunsupervised.github.io/humanunsupervised.com/pcam/pcam-cancer-detection.html

    Arguments:
        root: Absolute or relative path to the dataset files.
        transformation: A callable or a list of callable transformations.
        subset: Which part of the dataset should be used.
                One of {"train", "validation", "test"}
        seed: The seed that is used for the
                "transformation". If the seed is
                set, the "transformation" will use always the same seed
                depending on the call position.

    Returns:
        torch.utils.data.Dataset:
            The dataset that loads the pcam patches. You can use this
            as normal pytorch dataset. If you call it, the data will
            be returned as dictionary with structure:
            dict['images': torch.Tensor, 'feature': torch.Tensor].
            The feature 0 stands for Normal-Tissue, the label 1 stands for
            Metastase-Tissue.
    """
    root = os.path.expanduser(root)

    if subset:
        subset = subset.lower()
    if subset.startswith("tr"):
        imgs_hdf5_filepath = os.path.join(root, "camelyonpatch_level_2_split_train_x.h5")
        labels_hdf5_filepath = os.path.join(root, "camelyonpatch_level_2_split_train_y.h5")
    elif subset.startswith("val"):
        imgs_hdf5_filepath = os.path.join(root, "camelyonpatch_level_2_split_valid_x.h5")
        labels_hdf5_filepath = os.path.join(root, "camelyonpatch_level_2_split_valid_y.h5")
    elif subset.startswith("te"):
        imgs_hdf5_filepath = os.path.join(root, "camelyonpatch_level_2_split_test_x.h5")
        labels_hdf5_filepath = os.path.join(root, "camelyonpatch_level_2_split_test_y.h5")
    # TODO use case not possible yet
    # elif subset == 'all':
    #     pass
    else:
        raise NotImplementedError(
            'The parameter "subset" needs to be one of ["train", "validation", "test"].'
        )

    return PCAM(
        imgs_hdf5_filepath=imgs_hdf5_filepath,
        labels_hdf5_filepath=labels_hdf5_filepath,
        transform=transformation,
        seed=seed,
    )

class PCAM(Dataset):
    """
    Creates the PCAM dataset and returns it as type HistoDataset, which inherits from torch.utils.data.Dataset.

    Data and further information can be found at https://humanunsupervised.github.io/humanunsupervised.com/pcam/pcam-cancer-detection.html
    """

    def __init__(
        self,
        imgs_hdf5_filepath: str,
        labels_hdf5_filepath: str,
        imgs_key: str = "x",
        labels_key: str = "y",
        transform: O[Compose] = None,
        seed: int = None,
    ):
        """
        Initializes dataset.
        
        Arguments:
            imgs_hdf5_filepath: The path to the HDF5 file that contains the images.
            labels_hdf5_filepath: The path to the HDF5 file that contains the labels.
            imgs_key: The key that is used in the HDF5 file to get the images.
            labels_key: The key that is used in the HDF5 file to get the labels.
            transform: The transformation that is used on the image data.
            seed: The seed that is used for the
                    "transformation". If the seed is
                    set, the "transformation" will use always the same seed
                    depending on the call position.
        """

        self.imgs_hdf5_filepath = imgs_hdf5_filepath
        self.labels_hdf5_filepath = labels_hdf5_filepath
        self.imgs_key = imgs_key
        self.labels_key = labels_key

        self.transform = transform
        self.loaded_images = None
        self.loaded_labels = None
        
        self.seed = seed
        self.seed_increment = 0

    def __len__(self):
        """
        Returns length of dataset
        """
        with File(self.labels_hdf5_filepath, "r") as db:
            lens = len(db[self.labels_key])

        return lens

    def preload(self):
        """
        Load the image and the label into the RAM.
        """
        with File(self.imgs_hdf5_filepath, "r") as db:
            self.loaded_images = db[self.imgs_key][::]
        with File(self.labels_hdf5_filepath, "r") as db:
            self.loaded_labels = db[self.labels_key][::]

    def get_feature_for_all_rows(self):
        """
        Returns:
            Returns a dictionary with the key 'feature' that includes all labels of the dataset.
        """
        labels = []
        with File(self.labels_hdf5_filepath, "r") as db:
            for idx in range(len(self)):
                label = db[self.labels_key][idx][0][0][0]  # TODO make it nice
                labels.append(label)
        return {"feature": labels}

    def __getitem__(self, idx: int) -> dict:
        """
        Return a datapoint at a special position.
        
        Arguments:
            idx: The id to return. The value must be between 0 <= idx < len(Dataset)
            
        Returns:
            A dictionary with the keys 'data' and 'feature'. Under the key 'data' you can find the image.
            Under the key 'feature' you can find the label.
        """
        if self.seed:
            # save random state to reactivate this state after the call
            saved_seed_state = helper.get_random_seed()
            # set seets
            worker_info = torch.utils.data.get_worker_info()
            if worker_info is None:
                worker_id = 0
                num_workers = 1
            else:
                worker_id = worker_info.id
                num_workers = worker_info.num_workers
            seed_to_set = (1 + self.seed_increment + worker_id) * int(1e7) + self.seed

            helper.set_random_seed_with_int(seed_to_set)
            # increase seed increment to use a new random seed at next call
            self.seed_increment += num_workers

        if self.loaded_images is None:
            # get images
            with File(self.imgs_hdf5_filepath, "r") as db:
                image = db[self.imgs_key][idx]
            # get labels
            with File(self.labels_hdf5_filepath, "r") as db:
                label = db[self.labels_key][idx][0][0][0]  # TODO make it nice
        else:
            image = self.loaded_images[idx]
            label = self.loaded_labels[idx][0][0][0]

        # transform data
        if self.transform:
            image = self.transform(image)
            
        if self.seed:
            # reactivate random state
            helper.set_random_seed(*saved_seed_state)

        return {"data": image, "feature": torch.as_tensor(label).type(torch.LongTensor)}


def pcam_patches_preprocessed(
    root: str,  # '/data/ldap/histopathologic/original_read_only/PCAM_extracted_images'
    transformation: O[U[Callable, Sequence[Callable]]] = None,
    pre_transformation: O[U[Callable, Sequence[Callable]]] = None,
    subset: O[str] = "train",
    seed: O[int] = None,
) -> HistoDataset:
    """
    Creates the PCAM dataset and returns it as type HistoDataset, which inherits from torch.utils.data.Dataset.

    Data and further information can be found at TODO

    Arguments:
        root: absolute path to the dataset files.
        transformation (Callable): A callable or a list of
                       callable transformations.
        pre_transformation (Callable): A callable or a list of
                       callable transformations. "pre_transformation"
                       is called before "transformation". The transformation
                       is called with a seed and will give always the same
                       result.
        subset: Which part of the dataset should be used.
                One of {"train", "valid", "test"}
        seed:   The seed that is used for the "pre_transformation" and the
                "transformation". If the seed is set, the "pre_transformation"
                will always use the same seed for a data row. If the seed is
                set, the "transformation" will use always the same seed
                depending on the call position. For example:
                    Call-Index,     Seed f.              Seed f.
                                pre_transformation,  transformation
                        0     ,     100           ,    124
                        1     ,     100           ,    512
                        2     ,     100           ,    810
                        3     ,     100           ,    612
                    If we create the exact same dataset the transformation seeds
                    will be the same:
                    Call-Index,     Seed f.              Seed f.
                                pre_transformation,  transformation
                        0     ,     100           ,    124
                        1     ,     100           ,    512
                        2     ,     100           ,    810
                        3     ,     100           ,    612

    Returns:
        HistoDataset:
            The dataset that loads the bach patches. You can use this
            as normal pytorch dataset. If you call it, the data will
            be returned as dictionary.
    """
    if subset:
        subset = subset.lower()
    if subset.startswith("tr"):
        path_to_dataset = os.path.join(root, "train")
    elif subset.startswith("val"):
        path_to_dataset = os.path.join(root, "valid")
    elif subset.startswith("te"):
        path_to_dataset = os.path.join(root, "test")
    else:
        raise NotImplementedError(
            'The parameter "subset" needs to be one of ["train", "valid", "test"].'
        )

    path_to_csv = os.path.join(path_to_dataset, "features.csv")
    # create HistoDataset object and pass relevant attributes
    ds = HistoDataset(
        df_creators.CreateDFFromCSV(path_to_csv),
        path_to_dataset,
        data_readers="data/{id}.tiff",
        feature_readers=data_readers.ReadValueFromCSV(r"{feature}", encoded_values=["0", "1"]),
        seed=seed,
        pre_transfs=pre_transformation,
        da_transfs=transformation,
    )
    return ds
