import os
import ctypes
import pandas as pd
from zedsuite.utils import RANDOM_NAME, CythonWrapper
from cython import boundscheck, nonecheck, wraparound, cdivision
from cython cimport sizeof
from zedsuite.zutil cimport _lsmash
from libc.stdlib cimport malloc, free
from libc.string cimport strcpy


class Llk(CythonWrapper):
    def __init__(
        self,
        helpmsg: bool = False,
        version: bool = False,
        seq: pd.DataFrame = None,
        seqfile: str = None,
        data_dir: str = None,
        data_len: ctypes.c_uint = None,
        pfsafile: str = None
    ) -> None:

        super().__init__()

        self.argc = 1
        self.argv = ['llk']

        # Program information:
        if helpmsg:
            self._add_flag("-h")
        if version:
            self._add_flag("-V")

        # Usage:
        self.seqfile = None
        if seq is not None:
            self.seqfile = os.path.abspath(RANDOM_NAME(path=self.temp_dir))
            seq.to_csv(
                self.seqfile,
                sep=" ",
                line_terminator=(" " if type(seq) is pd.Series else "\n"),
                index=False,
                header=False
            )
            self._add_param("-s", self.seqfile)
        if seqfile is not None:
            self._add_param("-s", seqfile)
        if data_dir is not None:
            self._add_param("-D", data_dir)
        if data_len is not None:
            self._add_param("-x", str(data_len))
        if pfsafile is not None:
            self._add_param("-f", pfsafile)

        # Results
        self.llk_vec = None

    def run(self) -> [float]:
        # convert self.argv to a char** to be passed to main()
        argv = <char **> malloc(self.argc * sizeof(ctypes.c_char_p))
        for i, arg in enumerate(self.argv):
            argv[i] = <char *> malloc(len(arg) * sizeof(char))
            strcpy(argv[i], bytes(arg, 'utf-8'))

        # llk() defined in _llk.cc
        self.llk_vec = _llk(self.argc, argv)
        # cdef unsigned int argc = self.argc
        # cdef vector[double] llk_vec
        # openmp.omp_set_dynamic(1)
        # with nogil, parallel():
        #     llk_vec = _llk(argc, argv)
        # self.llk_vec = llk_vec

        for i in range(self.argc):
            free(argv[i])
        free(argv)

        return self.llk_vec


class Lsmash(CythonWrapper):
    def __init__(
        self,
        helpmsg: bool = False,
        version: bool = False,
        seq: pd.DataFrame = None,
        seqfile: str = None,
        data_dir: str = None,
        data_type: str = None,
        data_len: ctypes.c_uint = None,
        partition: list = None,
        derivative: bool = None,
        pfsafiles: list = None,
        timer: bool = None,
        sae: bool = None,
        repeat: ctypes.c_uint = None,
        outfile: str = None,
        random_mc: ctypes.c_uint = None,
        print_mc: bool = None,
    ) -> None:

        super().__init__()

        self.argc = 1
        self.argv = ['lsmash']

        # Program information:
        if helpmsg:
            self._add_flag("-h")
        if version:
            self._add_flag("-V")

        # Usage:
        self.seqfile = None
        if seq is not None:
            self.seqfile = os.path.abspath(RANDOM_NAME(path=self.temp_dir))
            seq.to_csv(self.seqfile, sep=" ", index=False, header=False)
            self._add_param("-f", self.seqfile)
        if seqfile is not None:
            self._add_param("-f", seqfile)
        if data_dir is not None:
            self._add_param("-D", data_dir)
        if data_type is not None:
            self._add_param("-T", data_type)
        if data_len is not None:
            self._add_param("-x", str(data_len))
        if partition is not None:
            self._add_param("-P", " ".join([str(n) for n in partition]))
        if derivative is not None:
            self._add_param("-u", str(derivative))
        if pfsafiles is not None:
            self._add_param("-F", " ".join([str(n) for n in pfsafiles]))
        if timer is not None:
            self._add_param("-t", str(timer))
        if sae is not None:
            self._add_param("-S", str(sae))
        if repeat is not None:
            self._add_param("-n", str(repeat))
        if outfile is not None:
            self._add_param("-o", outfile)
        if random_mc is not None:
            self._add_param("-R", str(random_mc))
        if print_mc is not None:
            self._add_param("-m", str(print_mc))

        # Results
        self.dist_matrix = None

    @boundscheck(False)
    @nonecheck(False)
    @wraparound(False)
    @cdivision(True)
    def run(self) -> pd.DataFrame:
        # convert self.argv to a char** to be passed to main()
        cdef char** argv = <char **> malloc(self.argc * sizeof(ctypes.c_char_p))
        for i, arg in enumerate(self.argv):
            argv[i] = <char *> malloc(len(arg) * sizeof(char))
            strcpy(argv[i], bytes(arg, 'utf-8'))

        # lsmash() defined in _lsmash.cc
        self.dist_matrix = _lsmash(self.argc, argv)

        # testing parallelization without GIL
        # cdef unsigned int argc = self.argc
        # cdef matrix_dbl dist_matrix
        # openmp.omp_set_dynamic(1)
        # with nogil, parallel():
        #     dist_matrix = _lsmash(argc, argv)
        # self.dist_matrix = dist_matrix

        for i in range(self.argc):
            free(argv[i])
        free(argv)

        return self.dist_matrix
