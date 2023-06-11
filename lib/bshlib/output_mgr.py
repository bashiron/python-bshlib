from pathlib import Path
from os import makedirs, mkdir, listdir, remove
from re import compile, match

from typing import TextIO

class OutputMgr:

    def __init__(self, pj_root, out_path='output'):
        """
        Parameters
        -----
        pj_root : Path
            Project's root directory.
        out_path : str
            Relative path from the project's root where the manager will operate.
        """
        self.root = pj_root / out_path

    def create_root(self):
        try:
            makedirs(self.root)
        except FileExistsError:
            print('directory exists. skipping..')

    def mkfile(self, task):
        """Opens file in its appropiate task folder. The file is appended with a number.

        Parameters
        -----
        task : str
            Task.

        Returns
        -----
        ret : `TextIO`
            Open file handle.
        """
        return self.__strong_open(self.root / task / f"{task}_{self.next_num(task)}", 'wt')

    def create(self, task, content):
        """Creates file in its appropiate task folder. The file is appended with a number. Fills the file with
        provided content.

        Parameters
        -----
        task : `str`
            Task.
        content : `Any`
            Content to write to file.

        Returns
        -----
        ret : `Path`
            Path of the created file.
        """
        path = self.root / task / f"{task}_{self.next_num(task)}"
        self.__strong_open(path, 'wt').write(content)
        return path

    def clear(self, task):
        """Clears task directory.
        """
        for ch in (self.root / task):
            ch.unlink()

    def next_num(self, task):
        """Get next file number for task file.
        """
        taskdir = self.root / task
        if not taskdir.exists() or len(listdir(taskdir)) == 0:
            num = 0
        else:
            rx = compile(r'_(\d+)')
            nums = []
            for ch in taskdir.iterdir():
                nums.append(int(match(rx, ch.stem).group(0)))
            num = max(nums) + 1
        return num

    def __strong_open(self, path, mode):
        """Open file, creating parent directory if doesn't exist.

        Returns
        -----
        ret : `TextIO`
            Open file handle.
        """
        try:
            fd = open(path, mode)
        except FileNotFoundError:
            mkdir(path.parent)
            # retry
            fd = self.__strong_open(path, mode)
        return fd
