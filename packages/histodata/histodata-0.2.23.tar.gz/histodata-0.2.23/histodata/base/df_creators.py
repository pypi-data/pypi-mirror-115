import json
import os
import re
from typing import Optional as O

import pandas as pd


class DataFrameCreator:
    """
    Parent class for all dataframes. Subclasses need to implement their call method.
    """

    def __init__(self):
        pass

    def __call__(self, path_to_dataset: str):
        raise NotImplementedError


class CreateDFDummy(DataFrameCreator):
    """
    Creates a dummy DataFrame.
    """

    def __init__(self, num_of_entries: int = 100):
        """
        TODO

        Arguments:
            num_of_entries: TODO
        """

        super().__init__()
        self.num_of_entries = num_of_entries

    def __call__(self, path_to_dataset: str):
        """
        TODO

        Arguments:
            path_to_dataset: TODO
        """
        df = pd.DataFrame({"id": range(self.num_of_entries)})
        df["fold"] = df.apply(lambda row: row["id"] % 10, 1)
        df["is_even"] = df.apply(lambda row: (row["id"] % 2) == 0, 1)
        return df


class CreateDFFromJSON(DataFrameCreator):
    """
    Creates a DataFrame from a JSON file.
    """

    def __init__(self, path_to_json: str, key_to_use: O[str] = None):
        """
        TODO

        Arguments:
            path_to_json: TODO
            key_to_use: TODO
        """

        super().__init__()
        self.path_to_json = path_to_json
        self.key_to_use = key_to_use

    def __call__(self, path_to_dataset: str):
        """
        TODO

        Arguments:
            path_to_dataset: TODO

        Returns:
            TODO: TODO
        """

        if isinstance(self.path_to_json, list):
            df = pd.DataFrame()
            for path_to_json in self.path_to_json:
                path = os.path.join(path_to_dataset, path_to_json)
                with open(path) as f:
                    json_dict = json.load(f)
                if self.key_to_use:
                    tmp_df = pd.DataFrame(json_dict[self.key_to_use])
                else:
                    tmp_df = pd.DataFrame(json_dict)
                tmp_df["__from_csv__"] = path_to_json
                df = df.append(tmp_df)
            return df
        else:
            path = os.path.join(path_to_dataset, self.path_to_json)
            with open(path) as f:
                json_dict = json.load(f)
            if self.key_to_use:
                return pd.DataFrame(json_dict[self.key_to_use])
            else:
                return pd.DataFrame(json_dict)


class CreateDFFromCSV(DataFrameCreator):
    """
    Creates a DataFrame from CSV.
    """

    def __init__(self, path_to_csv: str, sep: str = ",", **argv):
        """
        TODO

        Arguments:
            path_to_csv: TODO
            sep: TODO
            **argv: TODO
        """
        super().__init__()
        self.path_to_csv = path_to_csv
        self.sep = sep
        self.argv = argv

    def __call__(self, path_to_dataset: str):
        """
        TODO

        Arguments:
            path_to_dataset: Absolute path to dataset

        Returns:
            TODO: TODO
        """
        if isinstance(self.path_to_csv, list):
            df = pd.DataFrame()
            for path_to_csv in self.path_to_csv:
                path = os.path.join(path_to_dataset, path_to_csv)
                tmp_df = pd.read_csv(path, sep=self.sep, **self.argv)
                tmp_df["__from_csv__"] = path_to_csv
                df = df.append(tmp_df)
            return df
        else:
            path = os.path.join(path_to_dataset, self.path_to_csv)
            return pd.read_csv(path, sep=self.sep, **self.argv)


class CreateDFFromFolder(DataFrameCreator):
    """
    Creates DataFrame based on a folder content.
    """

    def __init__(self, file_of_interest: str):
        """
        TODO

        Arguments:
            file_of_interest: TODO
        """

        super().__init__()
        self.file_of_interest = file_of_interest

        regex = ""
        tmp = file_of_interest
        self.var_names = []
        counter_unnamed = 0
        while len(tmp) > 0:
            var_start = tmp.find("{")
            var_unnamed_start = tmp.find("(")
            if (
                var_unnamed_start != -1
                and (var_unnamed_start < var_start or var_start == -1)
                and (var_unnamed_start == 0 or tmp[var_unnamed_start - 1] != "\\")
            ):
                regex += tmp[: var_unnamed_start + 1]
                tmp = tmp[var_unnamed_start + 1 :]
                self.var_names.append("unnamed_" + str(counter_unnamed))
                counter_unnamed += 1
            elif var_start == -1:  # No Variable could be found
                regex += tmp
                tmp = ""
            else:
                # ignore this var start
                if var_start > 0 and tmp[var_start - 1] == "\\":
                    regex += tmp[:var_start]
                    tmp = tmp[var_start:]
                else:
                    regex += tmp[:var_start]
                    tmp = tmp[var_start:]
                    var_end = tmp.find("}")
                    self.var_names.append(tmp[1:var_end])
                    # self.regex += '(?=.*)'
                    # regex += '(^[^/]*)'
                    regex += "(.*)"
                    tmp = tmp[var_end + 1 :]
        self.regex = re.compile(regex)

    def __call__(self, path_to_dataset: str):
        """
        TODO

        Arguments:
            path_to_dataset: Absolute path to dataset

        Returns:
            TODO: TODO
        """

        rows = {name: [] for name in self.var_names}
        rows["__path__"] = []
        for root, _, files in os.walk(path_to_dataset):
            for file in files:
                path = os.path.join(root, file)[len(path_to_dataset) :]
                if path.startswith("/"):
                    path = path[1:]
                result = self.regex.search(path)
                if result:
                    path_as_variable = False
                    row = {}
                    for vname, var in zip(self.var_names, result.groups()):
                        row[vname] = var
                        if var and var.find("/") != -1:
                            path_as_variable = True
                    if path_as_variable is False:
                        for k in row:
                            rows[k].append(row[k])
                        rows["__path__"].append(path)

        return pd.DataFrame(rows)
