import re
from re import sub

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
    content = sub(pattern, replacement, content)
    file.write(content)
    file.close()
