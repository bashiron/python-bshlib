import re
import os
import shutil
import cv2 as cv
from pathlib import Path
from datetime import datetime, timedelta
from collections import namedtuple
from datetime import timezone

from exception import PathNotExist

# ----- SPANISH CONVERSIONS FOR PYTHON'S TIME AND DATE MODULES

MONTH_MAP = {
    1: 'Enero',
    2: 'Febrero',
    3: 'Marzo',
    4: 'Abril',
    5: 'Mayo',
    6: 'Junio',
    7: 'Julio',
    8: 'Agosto',
    9: 'Septiembre',
    10: 'Octubre',
    11: 'Noviembre',
    12: 'Diciembre'
}

WEEKDAY_MAP = {
    0: 'Lunes',
    1: 'Martes',
    2: 'Miércoles',
    3: 'Jueves',
    4: 'Viernes',
    5: 'Sábado',
    6: 'Domingo'
}

class Hdur(namedtuple('Hdur', 'h m s')):
    """Time duration structure capped at hours, containing hours, minutes and seconds.
    """

# ----- CLASSES

class _GetchUnix:
    """For getting 1 character from stdin.
    """
    def __init__(self):
        pass

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# ----- DECORATORS

# TODO: other possible behavior: the decorator takes a string param with the name of the PathLike param to convert
# TODO: could also take a param that defines whether to convert to `Path` or to `str`
def pathlike_compatible(fun):
    """Convert `PathLike` function args to `str`.
    """

    def cnv_any(a):
        """General conversion.
        """
        match a:
            case os.PathLike():
                return str(a)
            case _:
                return a

    def cnv_p(arg):
        """Convert positional argument.
        """
        return cnv_any(arg)

    def cnv_k(kwarg):
        """Convert keyword argument.
        """
        return kwarg[0], cnv_any(kwarg[1])

    def wrapper(*args, **kwargs):
        args = tuple(map(cnv_p, args))
        kwargs = dict(map(cnv_k, kwargs.items()))
        return fun(*args, **kwargs)

    return wrapper

# ----- FUNCTIONS

def get_methods(obj, spacing=20):
    """Expose object methods.
    """
    method_list = []
    for method_name in dir(obj):
        try:
            if callable(getattr(obj, method_name)):
                method_list.append(str(method_name))
        except Exception:
            method_list.append(str(method_name))
    process_func = (lambda s: ' '.join(s.split())) or (lambda s: s)
    for method in method_list:
        try:
            print(str(method.ljust(spacing)) + ' ' +
                  process_func(str(getattr(obj, method).__doc__)[0:90]))
        except Exception:
            print(method.ljust(spacing) + ' ' + ' getattr() failed')


# TODO: eventually use the 'regex' pypi package for extended regex operations
def gsub_file(path, pattern: re.Pattern, replacement):
    """Apply substitution to an entire file.
    """
    file = open(path, 'r+', encoding='utf-8')
    content = file.readlines()
    content = ''.join(content)
    file.truncate(0)
    file.seek(0)  # not necessary but just in case
    content = re.sub(pattern, replacement, content)
    file.write(content)
    file.close()

def try_birthttime(path: Path):
    try:
        # get birth time (many times not available)
        return path.stat().st_birthtime
    except AttributeError:
        # get modification time
        return path.stat().st_mtime

@pathlike_compatible
def vid_duration(video):
    """Return video duration in seconds.

    Parameters
    -----
    video : `os.PathLike[str]` or `str`
        Path to video.

    Returns
    -----
    ret : `int`
        Number of seconds.
    """
    vid = cv.VideoCapture(video)
    return vid.get(cv.CAP_PROP_FRAME_COUNT) / vid.get(cv.CAP_PROP_FPS)

@pathlike_compatible
def real_vid_birthtime(video, tz):
    """In the case of videos which birthtime is not available will calculate real creation/birth time by subtracting the
    duration of the video from the modification time.

    Parameters
    -----
    video : `os.PathLike[str]` or `str`
        Path to video.
    tz : `timezone`
        Timezone to convert birthtime timestamp to.

    Returns
    -----
    ret : `datetime`
        Real creation/birth date of video.
    """
    return datetime.fromtimestamp(os.stat(video).st_mtime).astimezone(tz) - timedelta(seconds=vid_duration(video))


def hour_capped_duration(seconds):
    """Return a named tuple created from an amount of seconds, capped at hours.

    Parameters
    -----
    seconds : int
        Amount of seconds to convert.

    Returns
    -----
    ret : Hdur
        Hdur object containing hours, minutes and seconds.
     """
    hs, ms = divmod(seconds, 3600)
    ms, ss = divmod(ms, 60)
    return Hdur(hs, ms, ss)

def super_copyfile(src, dst):
    """
    Copy file to destination, creating all intermediate directories if needed.

    Parameters
    -----
    src : `os.PathLike[str]` or `str`
        Path to file.
    dst : `os.PathLike[str]` or `str`
        Destination directory.
    """
    try:
        shutil.copy(src, dst)
    except IOError:
        os.makedirs(dst, exist_ok=False)
        super_copyfile(src, dst)


# ----- VALIDATION


def req_path(path):
    """Check for Path existance.

    Parameters
    -----
    path : `Path`
        Path.
    """
    if not path.exists():
        raise PathNotExist

# ----- MISC -----


# call to get 1 char from stdin
getc = _GetchUnix()

# stuff
