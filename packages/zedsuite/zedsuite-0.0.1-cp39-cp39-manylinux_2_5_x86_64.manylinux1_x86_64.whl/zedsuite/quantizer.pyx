import ctypes
import os
import csv
import shutil
import numpy as np
import pandas as pd
from zedsuite.utils import RANDOM_NAME, process_train_labels, CythonWrapper
cimport cython
from zedsuite.quantizer cimport _quantizer
from libc.stdlib cimport malloc, free
from libc.string cimport strcpy


class Quantizer(CythonWrapper):
    def __init__(
        self,
        helpmsg: bool = False,
        version: bool = False,
        percentage: ctypes.c_double = None,
        pruned: bool = None,
        detrend: ctypes.c_uint = None,
        normalized: bool = None,
        epsilon: ctypes.c_double = -1,
        min_alphabet_size: ctypes.c_uint = 2,
        max_alphabet_size: ctypes.c_uint = 3,
        verbose: ctypes.c_uint = 0,
        output: str = None,
        save_quantized: ctypes.c_uint = None,
        consider_single_symbol: ctypes.c_uint = None,
        n_quantizations: ctypes.c_uint = 1,
        return_failed: bool = True,
        clean: bool = True,
    ) -> None:

        super().__init__()

        self.argc = 1
        self.argv = ['quantizer']

        # Program information:
        if helpmsg:
            self._add_flag("-h")
        if version:
            self._add_flag("-V")

        # Usage of Binary:
        if percentage is not None:
            self._add_param("-x", str(percentage))
        if pruned is not None:
            self._add_param("-r", str(int(pruned)))
        if detrend is not None:
            self._add_param("-d", str(detrend))
        if normalized is not None:
            self._add_param("-n", str(int(normalized)))
        if epsilon is not None:
            self._add_param("-e", str(epsilon))
        if min_alphabet_size is not None:
            self._add_param("-a", str(min_alphabet_size))
        if max_alphabet_size is not None:
            self._add_param("-A", str(max_alphabet_size))
        if verbose is not None:
            self._add_param("-v", str(verbose))
        if output is not None:
            self._add_param("-o", output)
        if save_quantized is not None:
            self._add_param("-q", str(save_quantized))
        if consider_single_symbol is not None:
            self._add_param("-f", str(consider_single_symbol))
        if n_quantizations is not None:
            self._add_param("-M", str(n_quantizations))

        # Additional options
        self._num_quantizations = n_quantizations
        self._return_failed = return_failed
        self._verbose = verbose
        self._fitted = False
        self._clean = clean
        self._feature_order = []
        self._temp_data_dir = RANDOM_NAME(clean=self._clean)

        self.parameters = {}
        self.lib_files = []
        self.training_X = None
        self.supervised = True

        # Results
        self.rc = None

    def run(self) -> bool:
        # convert self.argv to a char** to be passed to main()
        c_argv = <char **> malloc(self.argc * cython.sizeof(ctypes.c_char_p))
        for i, arg in enumerate(self.argv):
            c_argv[i] = <char *> malloc(len(arg) * cython.sizeof(char))
            strcpy(c_argv[i], bytes(arg, 'utf-8'))

        # _quantizer() defined in _quantizer.cc
        if self._verbose > 0:
            print("./", end="")
            [print(arg, end=" ") for arg in self.argv]
            print("\nQUANTIZING")
        self.rc = _quantizer(self.argc, c_argv)
        if self._verbose > 0:
            print("\nQUANTIZED")

        for i in range(self.argc):
            free(c_argv[i])
        free(c_argv)

        return self.rc

    def fit(self, data_dir, label=None, *, force_refit=False):
        if self._num_quantizations == 0:
            return data_dir
        if self._fitted and not force_refit:
            return None
        if (label is None) and (type(data_dir) is not str):
            self.supervised = False
            label = pd.DataFrame([1] * data_dir.shape[0])
        if type(data_dir) is not str:
            if os.path.exists(self._temp_data_dir):
                shutil.rmtree(self._temp_data_dir)
            os.mkdir(self._temp_data_dir)
            data_dir = data_dir.reset_index(drop=True)
            data_dir, label = process_train_labels(data_dir, label)

            # binary expects different dir format for unsupervised/single class case
            classes = set(label[list(label)[0]])
            if len(classes) == 1:
                self.supervised = False
                outfile = "dataset"
                data_dir.reindex(index=label[label[list(label)[0]] == 1].index).to_csv(
                    os.path.join(self._temp_data_dir, outfile),
                    sep=" ",
                    index=False,
                    header=False,
                )
            else:
                file = open(os.path.join(self._temp_data_dir, "library_list"), "w")
                for i in classes:
                    outfile = "train_class_" + str(i)
                    df_i = data_dir.reindex(index=label[label[list(label)[0]] == i].index)
                    df_i.to_csv(
                        os.path.join(self._temp_data_dir, outfile),
                        sep=" ",
                        index=False,
                        header=False,
                    )
                    file.write(
                        outfile + " " + str(i) + " " + str(df_i.shape[0]) + " " + "\n"
                    )
                file.close()
            self.data_dir = self._temp_data_dir

        else:
            self.data_dir = data_dir

        # size = data_dir.shape[0] * data_dir.shape[1]
        # self._sample_size = min(1, 100000 / size)
        self._add_param("-D", self.data_dir)
        self._add_param("-t", "2" if self.supervised else "0")
        self.run()

        # if self._problem_type == 'supervised':
        self._note_lib_files(self.data_dir)

        prune_range_list = []
        detrending_list = []
        normalization_list = []
        partition_list = []

        valid_params_path = os.path.join(self.data_dir, "valid_parameter")
        with open(valid_params_path) as f:
            valid_parameters = f.read().splitlines()
        if self._clean:
            try:
                shutil.rmtree(self._temp_data_dir)
            except:
                pass
        valid_parameters.sort()  # sorts normally by alphabetical order
        valid_parameters.sort(key=len, reverse=True)  # sorts by descending length

        # combined previous two for-loops into one
        parameters = {}
        for param in valid_parameters:
            pr, d, n, pa = self._read_quantizer_params(param)
            key = self._write_quantizer_params(pr, d, n, pa)
            param_set = {
                "prune_range": pr,
                "detrending": d,
                "normalization": n,
                "partition": pa,
            }
            parameters[key] = param_set

            # don't include duplicate quantizations
            if key not in self._feature_order:
                self._feature_order.append(key)

        assert (
            len(self._feature_order) != 0
        ), "Quantization failed, try manual quantization or normalize the data."

        self.parameters = parameters
        self._fitted = True
        return self

    def transform(self, data, *, output_type="matrix"):
        if self._num_quantizations == 0:
            return data
        assert self._fitted, (
            "'fit()' or 'fit_transform()' must be called prior to running 'transform()'"
        )

        if not isinstance(data, pd.DataFrame):
            if not os.path.isdir(self.data_dir):
                os.mkdir(self.data_dir)

        success = []
        for _, name in enumerate(self._feature_order):
            p_dict = self.parameters[name]
            result = self._try_apply_quantizer(
                data, **p_dict
            )
            if result is None:
                success.append(result)
            else:
                success.append(True)
            yield result

        if isinstance(data, pd.DataFrame):
            assert not all(
                v is None for v in success
            ), "All quantizations failed on train"

    def fit_transform(self, data_dir, label=None, *, output_type="matrix", force_refit=False):
        self.fit(data_dir, label=label, force_refit=force_refit)
        if type(data_dir) is not str:
            return self.transform(data_dir)
        X = []
        for lib_file in self.lib_files:
            lib_path = os.path.join(data_dir, lib_file)
            X_ = self.transform(lib_path, output_type=output_type)
            if X_ is None:
                return None
            X.append(X_)
        X_ = np.vstack(X)
        self.training_X = X_
        if output_type == "filename":
            X_ = X
        return X_

    def _note_lib_files(self, data_dir):
        library_list = os.path.join(data_dir, "library_list")
        if os.path.isfile(library_list):
            with open(library_list) as f:
                train_data = [row.split(" ")[:2] for row in f.read().splitlines()]
        else:
            train_data = [["dataset", -1]]
        for lib, _ in train_data:
            self.lib_files.append(lib)

    @staticmethod
    def _detrend(df, *, detrend_level):
        return df.diff(axis=1).dropna(how="all", axis=1)

    @staticmethod
    def _normalize(df):
        df_stdev = df.std(axis=1)
        pos_stdev_0 = df_stdev==0
        df_stdev[pos_stdev_0] = 1

        standard_normal_rows = df.subtract(df.mean(axis=1),
                                           axis=0).divide(df_stdev,
                                                          axis=0)
        return standard_normal_rows

    @staticmethod
    def _prune_func(df, lower_bound, upper_bound):
        for index in df.index:
            X = []
            for val in df.loc[index].values:
                if val <= float(lower_bound) or val >= float(upper_bound):
                    X = np.append(X, val)
            pruned_ = np.empty([1, len(df.loc[index].values) - len(X)])
            pruned_[:] = np.nan
            X = np.append(X, pruned_)
            df.loc[index] = X
        return df

    def _try_apply_quantizer(
        self,
        data,
        *,
        partition,
        prune_range=None,
        detrending=None,
        normalization=None,
        outfile=None,
        verbose=False
    ):
        max_col_len = 0
        if type(data) is str:
            with open(data, "r") as infile:
                csv_reader = csv.reader(infile, delimiter=" ")
                for row in csv_reader:
                    len_ = len(row)
                    if len_ > max_col_len:
                        max_col_len = len_
            unquantized = pd.read_csv(
                data,
                delimiter=" ",
                dtype="float",
                header=None,
                names=range(max_col_len),
            )
        else:
            unquantized = data.copy().astype(float)

        # columns_list = list(unquantized.columns)
        # index_list = unquantized.index
        if prune_range:
            if verbose:
                print("PRUNING")
            unquantized = self._prune_func(unquantized, prune_range[0], prune_range[1])
        # pd.DataFrame(unquantized).to_csv("debug1")
        if detrending:
            if verbose:
                print("DETRENDING")
            unquantized = self._detrend(unquantized, detrend_level=detrending)
        # pd.DataFrame(unquantized).to_csv("debug2")
        if normalization:
            if verbose:
                print("NORMALIZING")
            unquantized = self._normalize(unquantized)
        # unquantized.to_csv("debug3")
        if outfile is None:
            # _outfile = filename
            pass
        else:
            _outfile = outfile
        # if type(data) is not str:
        partition = [float(i) for i in partition]
        # unquantized.dropna(how="all", axis=1).to_csv("unq.csv", sep=",", header=False, index=False)
        # pd.DataFrame(np.digitize(unquantized.values, bins=partition)).to_csv("test.csv", sep=",", header=False, index=False)
        quantized = pd.DataFrame(
            np.digitize(unquantized.values, bins=partition) #, index=data.index
        )
        # quantized[unquantized.isnull()] = np.nan
        if (
            not self._correct_num_symbols(quantized.values, partition)
            and not self._return_failed
        ):
            print("Dropping invalid quantization.")
            return None
        return quantized

        # if not os.path.isfile(_outfile):
        #     print("Failed to apply quantization! Retrying...")
        #     self._try_apply_quantizer(
        #         _outfile,
        #         partition=partition,
        #         prune_range=prune_range,
        #         detrending=detrending,
        #         normalization=normalization,
        #         outfile=outfile,
        #         verbose=verbose,
        #     )
        # return True

    @staticmethod
    def _correct_num_symbols(quantized_matrix, partition):

        expected_num_symbols = len(partition) + 1
        i = 0
        for row in quantized_matrix:
            num_symbols = len(np.unique(row))
            if num_symbols == 1:
                # print("SINGLE SYMBOL STREAM SOMEHOW PASSED CHECK: {}".format(partition))
                pass
            if num_symbols != expected_num_symbols:
                # np.savetxt("foo.csv", quantized_matrix, delimiter=",")
                return False
            i += 1

        return True

    @staticmethod
    def _read_quantizer_params(parameters):

        parameters_ = parameters.split("L")[0]
        prune_range = []
        for index, char in enumerate(parameters_):
            if char == "R":
                for char_ in parameters_[index + 2 :]:
                    if char_ != "]":
                        prune_range.append(char_)
                    else:
                        break
            elif char == "D":
                detrending = int(parameters_[index + 1])
            elif char == "N":
                normalization = int(parameters_[index + 1])
        if prune_range:
            prune_range = "".join(prune_range).split(" ")

        partition = parameters_.split("[")[-1].strip("]").split()
        no_negative_zero_partition = []
        for p in partition:
            if repr(float(p)) == "-0.0":
                p_ = p[1:]
            else:
                p_ = p
            no_negative_zero_partition.append(p_)

        return prune_range, detrending, normalization, no_negative_zero_partition

    @staticmethod
    def _write_quantizer_params(prune_range, detrending, normalization, partition):
        """

        """
        params = []
        if prune_range:
            params.append("R")
            params += prune_range
        if detrending:
            params.append("D")
            params.append(detrending)
        if normalization:
            params.append("N")
            params.append(normalization)
        if partition:
            params.append("P")
            params += str([float(p) for p in partition]).replace(" ", "")
        params_string = "".join([str(p) for p in params])
        return params_string
