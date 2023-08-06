import ctypes
import pandas as pd
from cython import boundscheck, nonecheck, wraparound, cdivision
from zedsuite.utils import RANDOM_NAME, CythonWrapper
from cython cimport sizeof
from zedsuite.genesess cimport _genESeSS
from libc.stdlib cimport malloc, free
from libc.string cimport strcpy
from libcpp.vector cimport vector


class GenESeSS(CythonWrapper):
    def __init__(
        self,
        helpmsg: bool = False,
        version: bool = False,
        configfile: str = None,
        data: [[]] = None,
        datafile: str = None,
        data_len: ctypes.c_uint = None, # len in genESeSS.cc
        data_type: str = None,
        data_dir: str = None,
        partition: list = None,
        eps: ctypes.c_double = None,
        timer: int = 0,
        derivative: bool = None,
        force: bool = None,
        outfile: str = None,
        dotcfg: str = None,
        dot: str = None,
        sym_frq_display_depth_: ctypes.c_uint = None,
        featurization: bool = None,
        runl: ctypes.c_uint = None,
        modelruns: ctypes.c_uint = None,
        runfile: str = None,
        symderiv: str = None,
        allsym: str = None,
        verbose: int = 0
    ) -> None:

        super().__init__()

        self.argc = 1
        self.argv = ['genESeSS']
        self.program_info = False

        # Program information:
        if helpmsg:
            self.program_info = True
            self._add_flag('-h')
        if version:
            self.program_info = True
            self._add_flag('-V')

        # Usage:
        if configfile is not None:
            self._add_param('-c', configfile)
        self.data = [[]]
        if data is not None:
            if type(data) is pd.DataFrame or type(data) is pd.Series:
                self.data = data.values.tolist()
            else:
                self.data = data
        if datafile is not None:
            self._add_param('-f', datafile)
        if data_len is not None:
            self._add_param('-x', str(data_len))
        if data_type is not None:
            self._add_param('-T', data_type)
        if data_dir is not None:
            self._add_param('-D', data_dir)
        if partition is not None:
            self._add_param('-P', ' '.join([str(n) for n in partition]))
        if eps is not None:
            self._add_param('-e', str(eps))
        if timer is not None:
            self._add_param('-t', str(timer))
        if derivative is not None:
            self._add_param('-u', str(int(derivative)))
        if force is not None:
            self._add_flag('-F')

        # Output options:
        self.outfile = "result.txt"
        if outfile is not None:
            self.outfile = outfile
            self._add_param('-o', self.outfile)
        if dotcfg is not None:
            self._add_param('-d', dotcfg)
        if dot is not None:
            self._add_param('-d', dot)
        if sym_frq_display_depth_ is not None:
            self._add_param('-W', str(sym_frq_display_depth_))
        if featurization is not None:
            self._add_param('-y', str(int(featurization)))
        if runl is not None:
            self._add_param('-r', str(runl))
        if modelruns is not None:
            self._add_param('-N', str(modelruns))
        if runfile is not None:
            self._add_param('-R', runfile)
        if symderiv is not None:
            self._add_param('-S', symderiv)
        if allsym is not None:
            self._add_param('-H', allsym)
        if verbose is not None:
            self._add_param('-v', str(verbose))

        # Result variables:
        self.inference_error = None
        self.epsilon_used = None
        self.synchronizing_string_found = None
        self.symbol_frequency = None
        self.probability_morph_matrix = None
        self.connectivity_matrix = None

    @boundscheck(False)
    @nonecheck(False)
    @wraparound(False)
    @cdivision(True)
    def run(self) -> bool:
        # convert self.argv to a char** to be passed to main()
        argv = <char **> malloc(self.argc * sizeof(ctypes.c_char_p))
        for i, arg in enumerate(self.argv):
            argv[i] = <char *> malloc(len(arg) * sizeof(char))
            strcpy(argv[i], bytes(arg, 'utf-8'))

        cdef vector[vector[unsigned int]] data_vec = self.data

        # _genESeSS() defined in genESeSS.cc
        _genESeSS(self.argc, argv, data_vec)

        for i in range(self.argc):
            free(argv[i])
        free(argv)

        # if passed help or version flags
        if self.program_info:
            return

        success = True
        with open(self.outfile, 'r') as f:
            for line in f:
                split = line.split(':')

                if split[0] == '%ANN_ERR':
                    self.inference_error = float(split[1].strip())
                elif split[0] == '%MRG_EPS':
                    self.epsilon_used = float(split[1].strip())
                elif split[0] == '%SYN_STR':
                    try:
                        self.synchronizing_string_found = [int(val.strip()) for val in split[1].strip().split(' ')]
                    except:
                        self.synchronizing_string_found = None
                elif split[0] == '%SYM_FRQ':
                    try:
                        self.symbol_frequency = [float(val.strip()) for val in split[1].strip().split(' ')]
                    except:
                        self.symbol_frequency = None
                elif split[0] == '%PITILDE':
                    try:
                        size = int(split[1].strip().split('(')[1].split(')')[0])
                        self.probability_morph_matrix = []
                        next(f) # skip #PITILDE line
                        for i in range(size):
                            self.probability_morph_matrix.append([float(val) for val in next(f).strip().split(' ')])
                    except:
                        self.probability_morph_matrix = None
                elif split[0] == '%CONNX':
                    try:
                        size = int(split[1].strip().split('(')[1].split(')')[0])
                        self.connectivity_matrix = []
                        next(f) # skip #CONNX line
                        for i in range(size):
                            self.connectivity_matrix.append([int(val) for val in next(f).strip().split(' ')])
                    except:
                        self.connectivity_matrix = None

        if self.probability_morph_matrix is None or self.connectivity_matrix is None:
            success = False

        return success
