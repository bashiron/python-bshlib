import re
from pathlib import Path
import cv2 as cv
from os import stat
from datetime import datetime, timedelta

from os import PathLike
from datetime import timezone

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

# ----- DECORATORS

# TODO: other possible behavior: the decorator takes a string param with the name of the PathLike param to convert
def pathlike_compatible(fun):
    """Convert `PathLike` args to `str`.
    """

    def cnv_any(a):
        """General conversion.
        """
        match a:
            case PathLike():
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
    video : `PathLike[str]` or `str`
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
    video : `PathLike[str]` or `str`
        Path to video.
    tz : `timezone`
        Timezone to convert birthtime timestamp to.

    Returns
    -----
    ret : `datetime`
        Real creation/birth date of video.
    """
    return datetime.fromtimestamp(stat(video).st_mtime).astimezone(tz) - timedelta(seconds=vid_duration(video))





# ----- MISC -----

