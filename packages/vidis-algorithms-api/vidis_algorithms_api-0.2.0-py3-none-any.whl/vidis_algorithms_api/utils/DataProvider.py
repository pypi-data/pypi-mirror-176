from typing import Optional, List, Iterable
import os
import re

import numpy as np
from vidis_algorithms_api.core import settings

FNAME_CONTAIN_NUMBER_PATTERN = r'(\d+).npy'


def glob_re(pattern: str, filenames: Iterable[str]) -> Iterable[int]:
    """
    1. ['any.npy', '2.npy', '1.npy']
    2. ['2.npy', '1.npy']
    3. ['2', '1']
    4. [1, 2]
    """
    return sorted(map(lambda filename: int(filename[:-4]), filter(re.compile(pattern).match, filenames)))


class DataProvider:
    def __init__(self, mmap_mode: Optional[str] = 'c'):
        self.mmap_mode = mmap_mode
        self.data_dir = settings.DATA_PATH

    def get_specter(self, path: str) -> np.ndarray:
        layers = []
        for filename in glob_re(FNAME_CONTAIN_NUMBER_PATTERN, os.listdir(os.path.join(self.data_dir, path))):
            layers.append(
                np.load(os.path.join(self.data_dir, path, f'{filename}.npy'), mmap_mode=self.mmap_mode)
            )
        return np.array(layers)
