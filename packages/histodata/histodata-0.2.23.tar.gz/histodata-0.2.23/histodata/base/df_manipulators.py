import math
import random

import matplotlib.pyplot as plt
import numpy as np
import openslide
import pandas as pd
from scipy.ndimage.measurements import center_of_mass
from skimage import morphology
from skimage.color import rgb2hed
from skimage.filters import threshold_otsu
from skimage.segmentation import slic


class DataFrameManipulator:
    """
    Parent class for all manipulators. Subclasses need to implement their call method.
    """

    def __init__(self):
        pass

    def __call__(self, df, path_to_image, reader):
        pass


class BoundingBoxToCenterCoordinates(DataFrameManipulator):
    """
    TODO
    """

    def __init__(
        self, column_of_bbox: str, name_of_x_column: str = "__x__", name_of_y_column: str = "__y__"
    ):
        self.column_of_bbox = column_of_bbox
        self.name_of_x_column = name_of_x_column
        self.name_of_y_column = name_of_y_column

    def __call__(self, df, path_to_image, reader):
        x = []
        y = []
        for _, row in df.iterrows():
            x.append((row[self.column_of_bbox][1] + row[self.column_of_bbox][3]) / 2)
            y.append((row[self.column_of_bbox][0] + row[self.column_of_bbox][2]) / 2)
        df[self.name_of_x_column] = x
        df[self.name_of_y_column] = y
        return df


class EditDFImageFilter(DataFrameManipulator):
    """
    TODO
    """
    def __init__(self, min_std):
        super().__init__()
        
        
    def __call__(self, df, path_to_image: str, reader):
        """
        TODO

        Arguments:
            df: TODO
            path_to_image: TODO
            reader: TODO

        Returns:
            TODO: TODO
        """
        import matplotlib.pyplot as plt
        for index, row in df.iterrows():
            img = reader(row, path_to_image)
            img = img[int(img.shape[0]*0.25):int(img.shape[0]*0.75),int(img.shape[1]*0.25):int(img.shape[1]*0.75)]
            img_max_red_blue = (np.array(img[:,:,0],dtype=float)<235) | (np.array(img[:,:,1],dtype=float)<150)
            max_red_blue = np.sum(img_max_red_blue) / (img.shape[0] * img.shape[1])
            if max_red_blue < 0.25:
                df.drop(index, inplace=True)
        return df
    
class EditDFImageGrid(DataFrameManipulator):
    """
    TODO
    """

    def __init__(self, return_image_size, perc_overlapping: float = 0.0, input_im_size=None):
        """
        TODO

        Arguments:
            return_image_size: TODO
            perc_overlapping: TODO
            input_im_size: TODO
        """

        super().__init__()
        self.return_image_size = return_image_size
        self.perc_overlapping = perc_overlapping
        self.input_im_size = input_im_size

    def get_points(self, im_size1d):
        """
        TODO

        Arguments:
            im_size1d: TODO

        """

        im_size_center = im_size1d - self.return_image_size
        shift = self.return_image_size * (1 - self.perc_overlapping)
        locations = np.arange(0, im_size_center + 0.0001, shift)

        return np.array(locations + (im_size1d - locations[-1]) / 2, dtype=int)
    
    def __call__(self, df, path_to_image: str, reader):
        """
        TODO

        Arguments:
            df: TODO
            path_to_image: TODO
            reader: TODO

        Returns:
            TODO: TODO
        """

        if self.input_im_size:
            input_im_size = self.input_im_size

        rows = {name: [] for name in list(df)}
        rows["__x__"] = []
        rows["__y__"] = []
        for _, row in df.iterrows():
            if self.input_im_size is None:
                input_im_size = reader.get_image_size(row, path_to_image)
            xs = self.get_points(input_im_size[0])
            ys = self.get_points(input_im_size[1])

            for x in xs:
                for y in ys:
                    row = dict(row)
                    row["__x__"] = x
                    row["__y__"] = y

                    for k in row:
                        rows[k].append(row[k])

        return pd.DataFrame(rows)


def get_mask(rgb):
    """
    TODO

    Arguments:
        rgb: TODO

    Returns:
        TODO: TODO
    """

    rgb = np.array(rgb, dtype=float) / 255.0

    ihc_hed = rgb2hed(rgb)

    gray = ihc_hed[..., 0] + ihc_hed[..., 1]  # - ihc_hed[..., 2]

    counts, positions = np.histogram(gray.flatten(), bins=50, range=(0.001, 0.04))
    argmax = np.argmax(counts)

    threshold1 = None
    threshold2 = None

    for pos in range(argmax, 48):
        if threshold1 is None:
            if counts[pos + 1] > counts[pos] and counts[pos + 2] > counts[pos + 1]:
                threshold1 = positions[pos]
        if threshold2 is None:
            if counts[pos + 1] > counts[pos]:
                threshold2 = positions[pos]
    if threshold1:
        threshold = threshold1
    elif threshold2:
        threshold = threshold2
    else:
        threshold = 0.04

    # use otsu as second threshold
    values_for_otsu = gray.flatten()
    values_for_otsu = values_for_otsu[values_for_otsu > 0.001]
    values_for_otsu = values_for_otsu[values_for_otsu < 0.04]
    threshold_from_otsu = threshold_otsu(values_for_otsu)

    # use the smaller threshold
    mask = gray > min([threshold, threshold_from_otsu])

    mask = morphology.binary_opening(mask, morphology.disk(1))
    mask = morphology.binary_closing(mask, morphology.disk(1))
    mask = morphology.binary_opening(mask, morphology.disk(3))
    mask = morphology.binary_closing(mask, morphology.disk(9))

    return mask


class EditDFWSIGrid(DataFrameManipulator):
    """
    TODO
    """

    def __init__(
        self,
        return_image_size,
        perc_overlapping: float = 0.0,
        plt_coordinates: bool = False,
        fn_thumbnail_to_mask=get_mask,
    ):
        """
        TODO

        Arguments:
            return_image_size: TODO
            perc_overlapping: TODO
            plt_coordinates: TODO
            fn_thumbnail_to_mask: TODO

        """
        super().__init__()
        self.return_image_size = return_image_size
        self.perc_overlapping = perc_overlapping
        self.plt_coordinates = plt_coordinates
        self.fn_thumbnail_to_mask = fn_thumbnail_to_mask

    def __get_coordinates__(self, thumbnail, thumbnail_mpp, return_mpp, min_mpp):
        """
        TODO

        Arguments:
            thumbnail: TODO
            thumbnail_mpp: TODO
            return_mpp: TODO
            min_mpp: TODO

        Returns:
            TODO: TODO
        """

        return_mpp = float(return_mpp)
        thumbnail_mpp = float(thumbnail_mpp)
        # see: https://colab.research.google.com/github/TIA-Lab
        # /tiatoolbox/blob/master/examples/example_wsiread.ipynb#scrollTo=MZ_yqoGJ_-6i
        wsi_thumb_mask = self.fn_thumbnail_to_mask(thumbnail)

        return_image_stride = self.return_image_size * (1 - self.perc_overlapping)

        lores_patch_size = int(return_image_stride / (thumbnail_mpp / return_mpp))
        nr_expected_rois = math.ceil(np.sum(wsi_thumb_mask) / (lores_patch_size ** 2))

        print(f"Created ~{nr_expected_rois} patches.")

        wsi_rois_mask = slic(
            thumbnail, mask=wsi_thumb_mask, n_segments=nr_expected_rois, compactness=1000, sigma=1
        )

        lores_rois_center = center_of_mass(
            wsi_rois_mask, labels=wsi_rois_mask, index=np.unique(wsi_rois_mask)[1:]
        )
        lores_rois_center = np.array(lores_rois_center)  # coordinates is Y, X
        lores_rois_center = lores_rois_center.astype(np.int32)
        selected_indices = wsi_thumb_mask[lores_rois_center[:, 0], lores_rois_center[:, 1]]
        lores_rois_center = lores_rois_center[selected_indices]

        distance_to_boarder = []
        for center_x, center_y in zip(lores_rois_center[:, 1], lores_rois_center[:, 0]):
            y, x = np.ogrid[: wsi_thumb_mask.shape[0], : wsi_thumb_mask.shape[1]]
            dist_from_center = np.sqrt((y - center_y) ** 2 + (x - center_x) ** 2)
            dist = np.min(dist_from_center[~wsi_thumb_mask])
            distance_to_boarder.append(dist)
        distance_to_boarder = np.array(distance_to_boarder)

        if self.plt_coordinates:
            # show the patches region and their centres of mass
            plt.figure(figsize=(20, 6))
            plt.subplot(1, 4, 1)
            # plt.subfigure(subf)
            plt.imshow(thumbnail)
            plt.subplot(1, 4, 2)
            plt.imshow(thumbnail)
            plt.scatter(lores_rois_center[:, 1], lores_rois_center[:, 0], s=5)
            plt.scatter(lores_rois_center[0:1, 1], lores_rois_center[0:1, 0], s=18, c="g")
            plt.scatter(lores_rois_center[1:2, 1], lores_rois_center[1:2, 0], s=18, c="y")
            plt.axis("off")
            plt.subplot(1, 4, 3)
            plt.scatter(
                lores_rois_center[:, 1], -lores_rois_center[:, 0], c=distance_to_boarder, s=5
            )
            plt.axis("off")
            plt.subplot(1, 4, 4)
            plt.imshow(wsi_thumb_mask)
            plt.show()

        return lores_rois_center * (thumbnail_mpp / min_mpp), distance_to_boarder * (
            thumbnail_mpp / min_mpp
        )

    def __call__(self, df, path_to_image, reader):
        """
        TODO

        Arguments:
            path_to_image: Absolute path to image.
            reader: TODO

        Returns:
            TODO: TODO
        """

        rows = {name: [] for name in list(df)}
        rows["__x__"] = []
        rows["__y__"] = []
        rows["__dist__"] = []
        for _, row in df.iterrows():
            try:
                thumbnail, min_mpp = reader.read_thumbnail(
                    row, path_to_image, 20, return_min_mpp=True
                )
            except openslide.OpenSlideUnsupportedFormatError:
                print("Warning: The file is damaged or has missing files.")
                continue
            coordinates, distance_to_boarders = self.__get_coordinates__(
                thumbnail, 20, reader.mpp, min_mpp[0]
            )

            for x, y, dist in zip(coordinates[:, 1], coordinates[:, 0], distance_to_boarders):
                row = dict(row)
                row["__x__"] = int(x)
                row["__y__"] = int(y)
                row["__dist__"] = dist

                for k in row:
                    rows[k].append(row[k])

        return pd.DataFrame(rows)

    
class RandomDataSetSplitFilter(DataFrameManipulator):
    """
    TODO
    """

    def __init__(self, num_of_folds, folds_to_use, seed=None, name_of_fold_column='__folds__'):
        """
        TODO

        Arguments:
            percentage_to_filter: TODO
            mode: TODO
            seed: TODO

        """
        DataFrameManipulator.__init__(self)
        self.num_of_folds = num_of_folds
        self.folds_to_use = folds_to_use
        self.seed = seed
        self.name_of_fold_column = name_of_fold_column

    def __call__(self, df, path_to_image, reader):
        """
        TODO

        Arguments:
            df: TODO
            path_to_image: Absolute path to image.
            reader: TODO

        Returns:
            TODO: TODO
        """
        if self.name_of_fold_column not in df:
            rng = np.random.default_rng(self.seed)
            df[self.name_of_fold_column] = rng.integers(self.num_of_folds, size=len(df))
        
        return df[df[self.name_of_fold_column].isin(self.folds_to_use)]
    

class RandomDataSetSplitFilterByColumnValue(DataFrameManipulator):
    """
    TODO
    """

    def __init__(self, column, num_of_folds, folds_to_use, seed=None, name_of_fold_column='__folds__'):
        """
        TODO

        Arguments:
            percentage_to_filter: TODO
            mode: TODO
            seed: TODO

        """
        DataFrameManipulator.__init__(self)
        self.column = column
        self.num_of_folds = num_of_folds
        self.folds_to_use = folds_to_use
        self.seed = seed
        self.name_of_fold_column = name_of_fold_column

    def __call__(self, df, path_to_image, reader):
        """
        TODO

        Arguments:
            df: TODO
            path_to_image: Absolute path to image.
            reader: TODO

        Returns:
            TODO: TODO
        """
        if self.name_of_fold_column not in df:
            rng = np.random.default_rng(self.seed)
            g = df.groupby(self.column)
            random_numbers = rng.integers(self.num_of_folds, size=len(g.indices.keys()))
            folds = np.zeros(len(df), dtype=int)
            for k, r in zip(g.indices, random_numbers):
                folds[g.indices[k]] = r
            df[self.name_of_fold_column] = folds
        
        return df[df[self.name_of_fold_column].isin(self.folds_to_use)]
    
    
class DataFrameFilter:
    """
    TODO
    """

    def __init__(self, mode):
        """
        TODO

        Arguments:
            mode: TODO

        """
        self.mode = mode

    def __call__(self, df, indices):
        """
        TODO

        Arguments:
            df: TODO
            indices: TODO

        Returns:
            TODO: TODO
        """

        if self.mode == 0:
            return df.loc[indices]
        elif self.mode == 1:
            return df.loc[~df.index.isin(indices)]
        else:
            return df.loc[indices], df.loc[~df.index.isin(indices)]



        
class HematoxylinFilter(DataFrameFilter, DataFrameManipulator):
    """
    TODO
    """

    def __init__(self, image_size, mode=0):
        """
        TODO

        Arguments:
            percentage_to_filter: TODO
            mode: TODO
            seed: TODO

        """
        DataFrameFilter.__init__(self, mode)
        DataFrameManipulator.__init__(self)
        from skimage.color import rgb2hed, hed2rgb
        self.center_start = image_size - (image_size/(2**0.5))
        
    def hematoxylin_filter(self, patch):
        ihc_hed = rgb2hed(patch[128:512-128,128:512-128])
        return np.mean(ihc_hed[:, :, 0] > 0.05) > 0.03
    
    def __call__(self, df, path_to_dataset, reader):
        """
        TODO

        Arguments:
            df: TODO
            path_to_image: Absolute path to image.
            reader: TODO

        Returns:
            TODO: TODO
        """
        indices = []
        for index, row in df.iterrows():
            loaded = reader(row, path_to_dataset)
            if self.hematoxylin_filter(loaded):
                indices.append(index)
        return DataFrameFilter.__call__(self, df, indices)
        

class RandomFilter(DataFrameFilter, DataFrameManipulator):
    """
    TODO
    """

    def __init__(self, percentage_to_filter, mode=0, seed=None):
        """
        TODO

        Arguments:
            percentage_to_filter: TODO
            mode: TODO
            seed: TODO

        """

        DataFrameFilter.__init__(self, mode)
        DataFrameManipulator.__init__(self)
        self.percentage_to_filter = percentage_to_filter
        self.seed = seed

    def __call__(self, df, path_to_image, reader):
        """
        TODO

        Arguments:
            df: TODO
            path_to_image: Absolute path to image.
            reader: TODO

        Returns:
            TODO: TODO
        """

        r = random.Random(self.seed)
        indices = r.sample(list(df.index), int(len(df) * self.percentage_to_filter))
        return DataFrameFilter.__call__(self, df, indices)


class RandomFilterByColumnValue(DataFrameFilter, DataFrameManipulator):
    """
    TODO
    """

    def __init__(self, column, percentage_to_filter, mode=0, seed=None):
        """
        TODO

        Arguments:
            column: TODO
            percentage_to_filter: TODO
            mode: TODO
            seed: TODO

        """

        DataFrameFilter.__init__(self, mode)
        DataFrameManipulator.__init__(self)
        self.column = column
        self.percentage_to_filter = percentage_to_filter
        self.seed = seed

    def __call__(self, df, path_to_image, reader):
        """
        TODO

        Arguments:
            df: TODO
            path_to_image: Absolute path to image.
            reader: TODO

        Returns:
            TODO: TODO
        """
        uv = list(df[self.column].unique())
        r = random.Random(self.seed)
        choosen = r.sample(uv, int(len(uv) * self.percentage_to_filter))
        indices = list(df[df[self.column].isin(choosen)].index)
        return DataFrameFilter.__call__(self, df, indices)


class LambdaRowFilter(DataFrameFilter, DataFrameManipulator):
    """
    TODO
    """

    def __init__(self, lambda_function, mode=0):
        """
        TODO

        Arguments:
            lambda_function: TODO
            mode: TODO

        """

        DataFrameFilter.__init__(self, mode)
        DataFrameManipulator.__init__(self)
        self.lambda_function = lambda_function

    def __call__(self, df, path_to_image, reader):
        """
        TODO

        Arguments:
            df: TODO
            path_to_image: Absolute path to image.
            reader: TODO

        Returns:
            TODO: TODO
        """
        return DataFrameFilter.__call__(self, df, df[df.apply(self.lambda_function, 1)].index)


class LambdaDFFilter(DataFrameManipulator):
    """
    TODO
    """

    def __init__(self, lambda_function):
        """
        TODO

        Arguments:
            lambda_function: TODO
            mode: TODO

        """
        DataFrameManipulator.__init__(self)
        self.lambda_function = lambda_function

    def __call__(self, df, path_to_image, reader):
        """
        TODO

        Arguments:
            df: TODO
            path_to_image: Absolute path to image.
            reader: TODO

        Returns:
            TODO: TODO
        """
        return self.lambda_function(df)
    
    
class ColumnFilter(DataFrameFilter, DataFrameManipulator):
    """
    TODO
    """

    def __init__(self, name_of_column, allowed_values, mode=0):
        """
        TODO

        Arguments:
            name_of_column: TODO
            allowed_values: TODO
            mode: TODO

        """

        DataFrameFilter.__init__(self, mode)
        DataFrameManipulator.__init__(self)
        self.name_of_column = name_of_column
        self.allowed_values = allowed_values

    def __call__(self, df, path_to_image, reader):
        """
        TODO

        Arguments:
            df: TODO
            path_to_image: Absolute path to image.
            reader: TODO

        Returns:
            TODO: TODO
        """

        if isinstance(self.allowed_values, list):
            return DataFrameFilter.__call__(
                self, df, df[df[self.name_of_column].isin(self.allowed_values)].index
            )
        else:
            return DataFrameFilter.__call__(
                self, df, df[df[self.name_of_column] == self.allowed_values].index
            )
