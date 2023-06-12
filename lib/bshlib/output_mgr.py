from pathlib import Path
from os import mkdir
from re import compile
from os import rename, PathLike

from typing import TextIO


class OutputMgr:
    root: Path

    def __init__(self, out_root):
        """
        Parameters
        -----
        out_root : `PathLike[str]` or `str`
            Output root from where the manager will operate.
        """
        match out_root:
            case Path():
                self.root = out_root
            case PathLike() | str():
                self.root = Path(out_root)
            case _:
                raise TypeError

    def create_root(self):
        try:
            mkdir(self.root)
        except FileExistsError:
            print('directory exists. skipping..')

    def create_task_root(self, task):
        try:
            mkdir(self.root / task)
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
        for ch in (self.root / task).iterdir():
            ch.unlink()

    def conventional(self, task):
        """Return a list of paths of every file that follows the numeric sequence filename convention.

        Parameters
        -----
        task : `str`
            Task.

        Returns
        -----
        ret : `list` of `Path`
            Paths of conventional files.
        """
        taskdir = self.root / task
        good_files = list(taskdir.iterdir())
        rx = compile(task + r'_\d+')
        pred = lambda e: rx.match(e.stem) is not None
        good_files = list(filter(pred, good_files))
        return good_files

    def rearrange(self, task):
        """Rename the task files so they follow a sequential order again. Useful for gaps in the numeric naming sequence
        caused by file deletion.

        Parameters
        -----
        task : `str`
            Task.
        """
        files = self.conventional(task)
        nums = map(lambda e: self.extract_number(e), files)
        ordered = list(zip(files, nums))
        ordered.sort(key=lambda e: e[1])

        i = 0
        for path, _ in ordered:
            rename(path, path.with_stem(f"{task}_{i}"))
            i += 1

    def next_num(self, task):
        """Get next file number for task file.
        """
        taskdir = self.root / task
        files = self.conventional(task)

        if not taskdir.exists() or len(files) == 0:
            num = 0
        else:
            num = max([self.extract_number(ch) for ch in files]) + 1
        return num

    def extract_number(self, path):
        """Extract the sequence number from the file.

        Parameters
        -----
        path : `Path`
            Path of the file to extract from.
        """
        rx = compile(r'.*_(\d+)')
        return int(rx.match(path.stem).group(1))

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
