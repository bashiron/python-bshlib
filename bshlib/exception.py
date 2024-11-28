class PathNotExist(Exception):
    def __str__(self):
        return "Path does not exist"
