import os
import re
from pathlib import Path
from typing import TextIO

def task_op(function):
    """Check that `task` attribute is set. Can only be used to decorate `OutputMgr`'s methods since it takes an
    `OutputMgr` object as first argument.
    """
    def wrapper(mgr, *args, **kwargs):
        mgr.task_check()
        return function(mgr, *args, **kwargs)

    return wrapper

class OutputMgr:
    root: Path
    task: str | None

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
            case os.PathLike() | str():
                self.root = Path(out_root)
            case _:
                raise TypeError
        self.task = None

    def switch(self, task):
        """Switch to operating on `task`.
        """
        self.task = task

    def create_root(self):
        try:
            os.mkdir(self.root)
        except FileExistsError:
            print('directory exists. skipping..')

    @task_op
    def create_task_root(self):
        try:
            os.mkdir(self.root / self.task)
        except FileExistsError:
            print('directory exists. skipping..')

    @task_op
    def mkfile(self):
        """Opens file in its appropiate task folder. The file is appended with a number.

        Returns
        -----
        ret : `TextIO`
            Open file handle.
        """
        return self.__strong_open(self.root / self.task / f"{self.task}_{self.next_num()}", 'wt')

    @task_op
    def create(self, content):
        """Creates file in its appropiate task folder. The file is appended with a number. Fills the file with
        provided content.

        Parameters
        -----
        content : `Any`
            Content to write to file.

        Returns
        -----
        ret : `Path`
            Path of the created file.
        """
        path = self.root / self.task / f"{self.task}_{self.next_num()}"
        self.__strong_open(path, 'wt').write(content)
        return path

    @task_op
    def clear(self):
        """Clears task directory.
        """
        for ch in (self.root / self.task).iterdir():
            ch.unlink()

    @task_op
    def conventional(self):
        """Return a list of paths of every file that follows the numeric sequence filename convention.

        Returns
        -----
        ret : `list` of `Path`
            Paths of conventional files.
        """
        taskdir = self.root / self.task
        good_files = list(taskdir.iterdir())
        rx = re.compile(self.task + r'_\d+')
        pred = lambda e: rx.match(e.stem) is not None
        good_files = list(filter(pred, good_files))
        return good_files

    @task_op
    def rearrange(self):
        """Rename the task files so they follow a sequential order again. Useful for gaps in the numeric naming sequence
        caused by file deletion.
        """
        files = self.conventional()
        nums = map(lambda e: self.extract_number(e), files)
        ordered = list(zip(files, nums))
        ordered.sort(key=lambda e: e[1])

        i = 0
        for path, _ in ordered:
            os.rename(path, path.with_stem(f"{self.task}_{i}"))
            i += 1

    @task_op
    def next_num(self):
        """Get next file number for task file.
        """
        taskdir = self.root / self.task
        files = self.conventional()

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
        rx = re.compile(r'.*_(\d+)')
        return int(rx.match(path.stem).group(1))

# ----- MISC -----

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
            os.mkdir(path.parent)
            # retry
            fd = self.__strong_open(path, mode)
        return fd

    def task_check(self):
        if self.task is None:
            raise UnboundLocalError('task not yet set')
