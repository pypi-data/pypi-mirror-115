import os
from typing import Callable
from typing import Optional as O
from typing import Sequence
from typing import Union as U

import numpy as np

from ..base import data_readers, df_creators, df_manipulators
from ..base.histo_dataset import HistoDataset


def midog_classification_patches(
    root: str,  # '/data/ldap/histopathologic/original_read_only/MIDOG'
    patch_size: int,
    transformation: O[U[Callable, Sequence[Callable]]] = None,
    pre_transformation: O[U[Callable, Sequence[Callable]]] = None,
    subset: str = "all",
    splitting_seed: int = 1,
    scanner_to_use: O[U[int, list]] = None,
    seed: O[int] = None,
    convert_rgb2hed: O[bool] = False,
) -> HistoDataset:
    """
    Creates the MIDOG classification dataset and returns it as type HistoDataset, which inherits from torch.utils.data.Dataset.

    Data and further information can be found at the README.md of the git repository (TODO).

    Arguments:
        root: Absolute or relative path to the dataset files.
        transformation: A callable or a list of callable transformations.
        pre_transformation: A callable or a list of
                       callable transformations. "pre_transformation"
                       is called before "transformation". The transformation
                       is called with a seed and will give always the same
                       result.
        subset: Which part of the dataset should be used.
                One of {"train", "validation", "test", "all"}; size of subsets: train 3414,val 505,test 516
        splitting_seed: Seed used for splitting the data set
        scanner_to_use: The midog classification dataset includes three scanners.
                        This is a list or a integer that describes which scanner
                        is used. Allowed values are 0,1 or 2.
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
        patch_size: The images get cropped from the original image. Here you can
                decide which size arround the mitosis get cropped.

    Returns:
        HistoDataset:
            The dataset that loads the bach patches. You can use this
            as normal pytorch dataset. If you call it, the data will
            be returned as dictionary in form
            dict['images': torch.Tensor, 'feature': torch.Tensor].
            And the label is between 0 and 1.
            The feature 0 stands for Mitosis, the label 1 stands for
            non-mitotic.
    """
    manipulators_to_use = []

    # handle training, validation and test cases
    if subset:
        subset = subset.lower()
    if subset.startswith("tr"):
        folds_to_use = [0, 1]
    elif subset.startswith("val"):
        folds_to_use = [2]
    elif subset.startswith("te"):
        folds_to_use = [3]
    elif subset == "all":
        folds_to_use = [0, 1, 2, 3]
    else:
        raise NotImplementedError(
            'The parameter "subset" needs to be one of ["train", "validation", "test", "all"].'
        )

    """
    # If this is used instead of the following, then each large original image, will be
    # set to one of the subsets with all the datapoints in it.
    manipulators_to_use.append(
        df_manipulators.RandomDataSetSplitFilterByColumnValue(
            "image_id", num_of_folds=4, folds_to_use=folds_to_use, seed=splitting_seed
        )
    )
    """
    manipulators_to_use.append(
        df_manipulators.RandomDataSetSplitFilter(
            num_of_folds=4, folds_to_use=folds_to_use, seed=splitting_seed
        )
    )

    # handle scanner values
    if scanner_to_use:
        if isinstance(scanner_to_use, int):
            allowed_values = np.arange(50) + 1 + 50 * scanner_to_use
        elif isinstance(scanner_to_use, list):
            allowed_values = []
            for s in scanner_to_use:
                allowed_values.extend(np.arange(50) + 1 + 50 * s)
        else:
            raise NotImplementedError(
                'The parameter "scanner_to_use" needs to be None, an integer or a list.'
            )
        manipulators_to_use.append(df_manipulators.ColumnFilter("image_id", allowed_values))

    manipulators_to_use.append(df_manipulators.BoundingBoxToCenterCoordinates("bbox"))

    data_reader = data_readers.ReadFromImageFile(
        "images/{image_id:03d}.tiff", return_image_size=patch_size, convert_rgb2hed=convert_rgb2hed
    )

    # create HistoDataset object and pass relevant attributes
    ds = HistoDataset(
        df_creators.CreateDFFromJSON("MIDOG.json", "annotations"),
        root,
        df_manipulators=manipulators_to_use,
        data_readers=data_reader,
        feature_readers=data_readers.ReadValueFromCSV(r"{category_id}", encoded_values=["1", "2"]),
        seed=seed,
        pre_transfs=pre_transformation,
        da_transfs=transformation,
    )
    return ds


""" TODO: how the offline dataset was generated
# MIDOG
from histodata.datasets import midog

from torchvision import transforms

transform = transforms.Compose([
    transforms.ToTensor(),
])
for patch_size in [423, 200]:
    ds = midog.midog_classification_patches(
        '/data/ldap/histopathologic/original_read_only/MIDOG',
        transformation=transform,
        subset='all',
        splitting_seed=1,
        patch_size=patch_size,
    )
    ds.save('/data/ldap/histopathologic/original_read_only/MIDOG_classification_' + str(patch_size))
"""


def midog_classification_patches_preprocessed(
    root: str,  # '/data/ldap/histopathologic/original_read_only/MIDOG2/'
    transformation: O[U[Callable, Sequence[Callable]]] = None,
    pre_transformation: O[U[Callable, Sequence[Callable]]] = None,
    subset: O[str] = "train",
    seed: O[int] = None,
) -> HistoDataset:
    """
    Creates the midog dataset and returns it as type HistoDataset, which inherits from torch.utils.data.Dataset.

    Data and further information can be found at TODO

    Arguments:
        root: absolute or relative path to the dataset files.
        transformation (Callable): A callable or a list of
                       callable transformations.
        pre_transformation (Callable): A callable or a list of
                       callable transformations. "pre_transformation"
                       is called before "transformation". The transformation
                       is called with a seed and will give always the same
                       result.
        subset: Which part of the dataset should be used.
                One of {"train", "valid", "test"}; size of subsets: train 3414,val 505,test 516
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
            be returned as dictionary in form
            dict['images': torch.Tensor, 'feature': torch.Tensor].
            And the label is between 0 and 1.
            The feature 0 stands for Mitosis, the label 1 stands for
            non-mitotic.
    """
    if subset:
        subset = subset.lower()
    if subset.startswith("tr"):
        df_manipulator = df_manipulators.ColumnFilter(
            name_of_column="__folds__", allowed_values=[0, 1]
        )
    elif subset.startswith("val"):
        df_manipulator = df_manipulators.ColumnFilter(
            name_of_column="__folds__", allowed_values=[2]
        )
    elif subset.startswith("te"):
        df_manipulator = df_manipulators.ColumnFilter(
            name_of_column="__folds__", allowed_values=[3]
        )
    elif subset.startswith("all"):
        df_manipulator = None
    else:
        raise NotImplementedError(
            'The parameter "subset" needs to be one of ["train", "valid", "test"].'
        )

    # create HistoDataset object and pass relevant attributes
    ds = HistoDataset(
        df_creators.CreateDFFromCSV("features.csv"),
        root,
        df_manipulators=df_manipulator,
        data_readers="data/{id}.tiff",
        feature_readers=data_readers.ReadValueFromCSV(r"{feature}", encoded_values=["0", "1"]),
        seed=seed,
        pre_transfs=pre_transformation,
        da_transfs=transformation,
    )
    return ds
