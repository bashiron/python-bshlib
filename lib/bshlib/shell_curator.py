# TODO: lookup how a library like [jc](https://github.com/kellyjonbrazil/jc) or nushell curates shell output
def curate_output(string):
    """Curate text output of shell command. *Don't* use for binary output.

    Parameters
    -----
    string : `str`
        Text ouput.

    Returns
    -----
    list[str]
        List of lines of output.
    """
    # curate something like:
    # /home/bashiron/bashi/projects/mime-getter-benchmark/test_ground/piano.svg
    #   inode/x-empty
    return [s.strip() for s in string.splitlines()]
