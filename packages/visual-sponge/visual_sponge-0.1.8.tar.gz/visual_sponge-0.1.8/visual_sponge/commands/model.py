from pathlib import Path

from .. import MACROS, Model

__all__ = ["MODEL"]

def MODEL(m, format_=None, **kwargs):
    """MODEL(m, format_=None, **kwargs)
  Get a new Model instance

  :return: a new Model instance
  :param m: the model
  :param format_: the model format. If not given, the format will be guessed.
  :param **kwargs: options specified to the format.
    xyz
      guess_bond=False
        whether to guess the bonded information based on distance
      as_first_frame=True
        whether to use the coordinates in the file as the coordinates in the first frame
    """
    if format_ is None:
        if isinstance(m, str):
            path = Path(m)
            suffix = path.suffix
            if suffix != "txt":
                format_ = suffix[1:]
            else:
                raise NotImplementedError
        else:
            raise TypeError
    if format_ == "pdb":
        atoms, model = model_pdb(m, **kwargs)
    elif format_ == "xyz":
        atoms, model = model_xyz(m, **kwargs)
    else:
        raise NotImplementedError
    MACROS.CMD = {"MODEL": {"atoms": atoms, "name": path.stem, "crds": model.crds}}
    Model.WORKING = model
    return model

def model_pdb(m, **kwargs):
    raise NotImplementedError

def model_xyz(m, **kwargs):
    guess_bond = kwargs.get("guess_bond", False)
    as_first_frame = kwargs.get("as_first_frame", True)
    if guess_bond:
        raise NotImplementedError
    with open(m) as f:
        num = int(f.readline())
        atoms = [{} for i in range(num)]
        if as_first_frame:
            crds = [None for i in range(num)]
        else:
            crds = None
        f.readline()
        for i in range(num):
            line = f.readline()
            words = line.split()
            atoms[i]["elem"] = words[0]
            if as_first_frame:
                crds[i] = [float(words[j + 1]) for j in range(3)]
    return atoms, Model(name=Path(m).stem, atoms=atoms, crds=[crds])
