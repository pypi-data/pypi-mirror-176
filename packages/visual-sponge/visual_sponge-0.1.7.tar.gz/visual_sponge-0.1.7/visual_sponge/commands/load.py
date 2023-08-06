from pathlib import Path

from .. import MACROS, Model

__all__ = ["LOAD"]

def LOAD(fname, fformat=None, **kwargs):
    """
        This function loads the file
    
    :param fname: the file name to load
    :param fformat: the file format. If not given, the format will be guessed based on the suffix of the file name.
    :paran kwargs: other options
    """
    if fformat is None:
        path = Path(fname)
        suffix = path.suffix
        if suffix != "txt":
            fformat = suffix
        else:
            raise NotImplementedError
    if fformat == ".pdb":
        atoms = load_pdb(fname, **kwargs)
    elif fformat == ".xyz":
        atoms = load_xyz(fname, **kwargs)
    else:
        raise NotImplementedError
    MACROS.CMD = {"LOAD": {"atoms": atoms}}

def load_pdb(fname, **kwargs):
    pass

def load_xyz(fname, **kwargs):
    with open(fname) as f:
        num = int(f.readline())
        f.readline()
        lines = f.read().split("\n")[:num]
        keywords = ["elem", "x", "y", "z"]
        atoms = [{ keywords[i]:word for i, word in enumerate(line.split())} for line in lines ]
    return atoms
