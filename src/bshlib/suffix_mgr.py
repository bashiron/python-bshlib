from collections import namedtuple
from itertools import groupby
import re

Grouping = namedtuple('Grouping', ['unique', 'suffixed'])
sfx_rx = re.compile(r'(.+)_(\d+)$', re.MULTILINE)

class SuffixMgr:
    """
    Receives a list of `names` and manages the adding of duplicate names by suffixing them with a number.

    Keeps a register with the "unique" names and the "suffixed" names and their sequence.

    Also provides methods like `get_num` for manual adding and other operations.
    """
    __list: list[str]
    """List of names"""
    grouping: Grouping
    """Name register"""

    def __init__(self, ls: list[str]):
        self.__list = ls
        self.__compile()

    def add_new(self, item):
        """"
        Add new item to the list, handling the prefix.

        Parameters
        -----
        item : str
            Item to add.
        """
        if item in self.grouping.unique:
            self.__list.remove(item)
            self.__list.append(f'{item}_0')
            self.__list.append(f'{item}_1')
        elif item in self.grouping.suffixed.keys():
            self.__list.append(f'{item}_{self.__num(item) + 1}')
        else:
            self.__list.append(item)
        self.__compile()

    def get_num(self, item):
        """
        Get current number for item.

        Returns `None` if the name is new. You can add manually with the name as-is.

        Returns 0 if the name exists only once, with no suffix. You can add manually by removing the existing one and adding one with suffix `0` and another with `1`.

        Parameters
        -----
        item : str
            Item to look up.

        Returns
        -----
        int or None
            Current sequence number for name.
        """
        if item in self.grouping.unique:
            return 0
        elif item in self.grouping.suffixed.keys():
            return self.__num(item)
        else:
            return None

    def __num(self, item):
        """
        Get current number for item.

        Parameters
        -----
        item : str
            Item to look up.

        Returns
        -----
        int
            Current sequence number for name.
        """
        return max(self.grouping.suffixed[item])

    def __compile(self):
        """
        Compile register.
        """
        def name(i: str):
            m = sfx_rx.match(i)
            if m:
                return m.group(1)
            else:
                return ''

        def piece(i: str):
            return int(sfx_rx.match(i).group(2))

        uniq = []
        groups = {}
        ls = sorted(self.__list, key=name)
        for k, g in groupby(ls, key=name):
            if k == '':
                uniq.extend(g)
            else:
                groups[k] = [piece(i) for i in g]
        self.grouping = Grouping(unique=uniq, suffixed=groups)

    def update(self):
        """
        Compile internal register.

        Please run after modifying the list externally.
        """
        self.__compile()

    def conventional(self):
        """
        List the names that have a suffix.
        """
        return list(set(self.__list) - set(self.grouping.unique))

    @classmethod
    def extract(cls, string):
        """
        Extract number from suffix.
        """
        return int(sfx_rx.match(string).group(2))
