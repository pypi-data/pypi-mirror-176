import pickle
import os
from typing import Union

import torch
import lmdb


class EEGSignalIO:
    r'''
    A general-purpose, lightweight and efficient EEG signal IO APIs for converting various real-world EEG signal datasets into samples and storing them in the database. Here, we draw on the implementation ideas of industrial-grade application Caffe, and encapsulate a set of EEG signal reading and writing methods based on Lightning Memory-Mapped Database (LMDB), which not only unifies the differences of data types in different databases, but also accelerates the reading of data during training and testing.

    .. code-block:: python

        eeg_io = EEGSignalIO('YOUR_PATH')
        key = eeg_io.write_eeg(np.random.randn(32, 128))
        eeg = eeg_io.read_eeg(key)
        eeg.shape
        >>> (32, 128)
    
    Args:
        cache_path (str): Where the database is stored.
        cache_size (int): The maximum capacity of the database. (default: :obj:`1099511627776`)
    '''
    def __init__(self, cache_path: str, cache_size: int = 1024 * 1024 * 1024 * 1024) -> None:
        self.cache_path = cache_path
        self.cache_size = cache_size

        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path, exist_ok=True)

    @property
    def write_pointer(self):
        return len(self)

    def __len__(self):
        with lmdb.open(self.cache_path, self.cache_size, lock=False) as env:
            with env.begin() as transaction:
                return transaction.stat()['entries']

    def write_eeg(self, eeg: Union[any, torch.Tensor], key: Union[str, None] = None) -> str:
        r'''
        Write EEG signal to database.

        Args:
            eeg (any): EEG signal samples to be written into the database.
            key (str, optional): The key of the EEG signal to be inserted, if not specified, it will be an auto-incrementing integer.

        Returns:
            int: The index of written EEG signals in the database.
        '''

        if key is None:
            key = str(self.write_pointer)

        if eeg is None:
            raise RuntimeError(f'Save None to the LMDB with the key {key}!')

        with lmdb.open(self.cache_path, self.cache_size, lock=False) as env:
            with env.begin(write=True) as transaction:
                transaction.put(key.encode(), pickle.dumps(eeg))
            return key

    def read_eeg(self, key: str) -> any:
        r'''
        Query the corresponding EEG signal in the database according to the index.

        Args:
            key (str): The index of the EEG signal to be queried.
            
        Returns:
            any: The EEG signal sample.
        '''

        with lmdb.open(self.cache_path, self.cache_size, lock=False) as env:
            with env.begin() as transaction:
                eeg = transaction.get(key.encode())

            if eeg is None:
                raise RuntimeError(f'Unable to index the EEG signal sample with key {key}!')

            return pickle.loads(eeg)