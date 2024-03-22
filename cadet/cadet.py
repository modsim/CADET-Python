import warnings

from addict import Dict

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning)
    import h5py
import numpy
import subprocess
import pprint
import copy
import json

import filelock
import contextlib

from pathlib import Path

from cadet.cadet_dll import CadetDLL


class H5():
    pp = pprint.PrettyPrinter(indent=4)

    def transform(self, x):
        return x

    def inverse_transform(self, x):
        return x

    def __init__(self, *data):
        self.root = Dict()
        self.filename = None
        for i in data:
            self.root.update(copy.deepcopy(i))

    def load(self, paths=None, update=False, lock=False):
        if self.filename is not None:

            if lock is True:
                lock_file = filelock.FileLock(self.filename + '.lock')
            else:
                lock_file = contextlib.nullcontext()

            with lock_file:
                with h5py.File(self.filename, 'r') as h5file:
                    data = Dict(recursively_load(h5file, '/', self.inverse_transform, paths))
                    if update:
                        self.root.update(data)
                    else:
                        self.root = data
        else:
            print('Filename must be set before load can be used')

    def save(self, lock=False):
        if self.filename is not None:
            if lock is True:
                lock_file = filelock.FileLock(self.filename + '.lock')
            else:
                lock_file = contextlib.nullcontext()

            with lock_file:
                with h5py.File(self.filename, 'w') as h5file:
                    recursively_save(h5file, '/', self.root, self.transform)
        else:
            print("Filename must be set before save can be used")

    def save_json(self, filename):
        with Path(filename).open("w") as fp:
            data = convert_from_numpy(self.root, self.transform)
            json.dump(data, fp, indent=4, sort_keys=True)

    def load_json(self, filename, update=False):
        with Path(filename).open("r") as fp:
            data = json.load(fp)
            data = recursively_load_dict(data, self.inverse_transform)
            if update:
                self.root.update(data)
            else:
                self.root = data

    def append(self, lock=False):
        "This can only be used to write new keys to the system, this is faster than having to read the data before writing it"
        if self.filename is not None:
            if lock is True:
                lock_file = filelock.FileLock(self.filename + '.lock')
            else:
                lock_file = contextlib.nullcontext()

            with lock_file:
                with h5py.File(self.filename, 'a') as h5file:
                    recursively_save(h5file, '/', self.root, self.transform)
        else:
            print("Filename must be set before save can be used")

    def __str__(self):
        temp = []
        temp.append('Filename = %s' % self.filename)
        temp.append(self.pp.pformat(self.root))
        return '\n'.join(temp)

    def update(self, merge):
        self.root.update(merge.root)

    def __getitem__(self, key):
        key = key.lower()
        obj = self.root
        for i in key.split('/'):
            if i:
                obj = obj[i]
        return obj

    def __setitem__(self, key, value):
        key = key.lower()
        obj = self.root
        parts = key.split('/')
        for i in parts[:-1]:
            if i:
                obj = obj[i]
        obj[parts[-1]] = value


def is_dll(value):
    suffix = Path(value).suffix
    return suffix in {'.so', '.dll'}


class CadetMeta(type):
    _cadet_runner_class = None
    _is_file_class = None

    @property
    def is_file(cls):
        return bool(cls._is_file_class)

    @property
    def cadet_path(cls):
        if cls._cadet_runner_class is not None:
            return cls._cadet_runner_class.cadet_path

    @cadet_path.setter
    def cadet_path(cls, value):
        def __init__(cls):
            cls._cadet_runner_class = None
            cls._is_file_class = True

        if cls._cadet_runner_class is not None and cls._cadet_runner_class.cadet_path != value:
            del cls._cadet_runner_class

        if is_dll(value):
            cls._cadet_runner_class = CadetDLL(value)
            cls._is_file_class = False
        else:
            cls._cadet_runner_class = CadetFile(value)
            cls._is_file_class = True

    @cadet_path.deleter
    def cadet_path(cls):
        del cls._cadet_runner_class


class Cadet(H5, metaclass=CadetMeta):
    # cadet_path must be set in order for simulations to run
    def __init__(self, *data):
        super().__init__(*data)
        self._cadet_runner = None
        self.return_information = None
        self._is_file = None

    @property
    def is_file(self):
        if self._is_file is not None:
            return bool(self._is_file)
        if self._is_file_class is not None:
            return bool(self._is_file_class)

    @property
    def cadet_runner(self):
        if self._cadet_runner is not None:
            return self._cadet_runner
        if self._cadet_runner_class is not None:
            return self._cadet_runner_class

    @property
    def cadet_path(self):
        runner = self.cadet_runner
        if runner is not None:
            return runner.cadet_path

    @cadet_path.setter
    def cadet_path(self, value):
        if self._cadet_runner is not None and self._cadet_runner.cadet_path != value:
            del self._cadet_runner

        if is_dll(value):
            self._cadet_runner = CadetDLL(value)
            self._is_file = False
        else:
            self._cadet_runner = CadetFile(value)
            self._is_file = True

    @cadet_path.deleter
    def cadet_path(self):
        del self._cadet_runner

    def transform(self, x):
        return str.upper(x)

    def inverse_transform(self, x):
        return str.lower(x)

    def load_results(self):
        runner = self.cadet_runner
        if runner is not None:
            runner.load_results(self)

    def run(self, timeout=None, check=None):
        data = self.cadet_runner.run(simulation=self.root.input, filename=self.filename, timeout=timeout, check=check)
        # self.return_information = data
        return data

    def run_load(self, timeout=None, check=None, clear=True):
        data = self.cadet_runner.run(simulation=self.root.input, filename=self.filename, timeout=timeout, check=check)
        # self.return_information = data
        self.load_results()
        if clear:
            self.clear()
        return data

    def clear(self):
        runner = self.cadet_runner
        if runner is not None:
            runner.clear()


class CadetFile:

    def __init__(self, cadet_path):
        self.cadet_path = cadet_path

    def run(self, filename=None, simulation=None, timeout=None, check=None):
        if filename is not None:
            data = subprocess.run([self.cadet_path, filename], timeout=timeout, check=check, capture_output=True)
            return data
        else:
            print("Filename must be set before run can be used")

    def clear(self):
        pass

    def load_results(self, sim):
        sim.load(paths=["/meta", "/output"], update=True)


def convert_from_numpy(data, func):
    ans = Dict()
    for key_original, item in data.items():
        key = func(key_original)
        if isinstance(item, numpy.ndarray):
            item = item.tolist()

        if isinstance(item, numpy.generic):
            item = item.item()

        if isinstance(item, bytes):
            item = item.decode('ascii')

        if isinstance(item, Dict):
            ans[key_original] = convert_from_numpy(item, func)
        else:
            ans[key] = item
    return ans


def recursively_load_dict(data, func):
    ans = Dict()
    for key_original, item in data.items():
        key = func(key_original)
        if isinstance(item, dict):
            ans[key] = recursively_load_dict(item, func)
        else:
            ans[key] = item
    return ans


def set_path(obj, path, value):
    """paths need to be broken up so that subobjects are correctly made"""
    path = path.split('/')
    path = [i for i in path if i]

    temp = obj
    for part in path[:-1]:
        temp = temp[part]

    temp[path[-1]] = value


def recursively_load(h5file, path, func, paths):
    ans = Dict()
    if paths is not None:
        for path in paths:
            item = h5file.get(path, None)
            if item is not None:
                if isinstance(item, h5py._hl.dataset.Dataset):
                    set_path(ans, path, item[()])
                elif isinstance(item, h5py._hl.group.Group):
                    set_path(ans, path, recursively_load(h5file, path + '/', func, None))
    else:
        for key_original in h5file[path].keys():
            key = func(key_original)
            local_path = path + key
            item = h5file[path][key_original]
            if isinstance(item, h5py._hl.dataset.Dataset):
                ans[key] = item[()]
            elif isinstance(item, h5py._hl.group.Group):
                ans[key] = recursively_load(h5file, local_path + '/', func, None)
    return ans


def recursively_save(h5file, path, dic, func):
    if not isinstance(path, str):
        raise ValueError("path must be a string")
    if not isinstance(h5file, h5py._hl.files.File):
        raise ValueError("must be an open h5py file")

    # argument type checking
    if not isinstance(dic, dict):
        raise ValueError("must provide a dictionary")

    # save items to the hdf5 file
    for key, item in dic.items():
        key = str(key)
        value = None

        if not isinstance(key, str):
            raise ValueError("dict keys must be strings to save to hdf5")

        if isinstance(item, dict):
            recursively_save(h5file, path + key + '/', item, func)

        # handle int, float, string and ndarray of int32, int64, float64
        elif isinstance(item, str):
            value = numpy.array(item.encode('ascii'))
        elif isinstance(item, list) and all(isinstance(i, str) for i in item):
            value = numpy.array([i.encode('ascii') for i in item])
        else:
            try:
                value = numpy.array(item)
            except TypeError:
                raise ValueError('Cannot save %s/%s key with %s type.' % (path, func(key), type(item)))

        if value is not None:
            try:
                h5file[path + func(key)] = value
            except OSError as e:
                if str(e) == 'Unable to create link (name already exists)':
                    raise KeyError(f'Name conflict with upper and lower case entries for key "{path}{key}".')
                else:
                    raise
