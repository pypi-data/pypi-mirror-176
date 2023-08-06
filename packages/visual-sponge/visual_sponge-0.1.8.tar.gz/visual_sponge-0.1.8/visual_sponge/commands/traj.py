from pathlib import Path

from .. import MACROS, Model

__all__ = ["TRAJ"]

def TRAJ(traj, format_=None, m=None, append=False, **kwargs):
    """TRAJ(traj, format_=None, m=None, append=False, **kwargs)
  Load trajectory to the model

  :return: None
  :param traj: the trajectory
  :param format_: the trajectory format. If not given, the format will be guessed.
  :param m: the model to load. If not given, the working model will be used.
  :param append: whether to append or replace the trajectory in model
  :param **kwargs: options specified to the format.
    xyz
      frame=1
        the number of frames in the trajectory
    """
    if m is None:
        m = Model.WORKING
        if m is None:
            raise ValueError
    if format_ is None:
        if isinstance(traj, str):
            path = Path(traj)
            suffix = path.suffix
            if suffix != "txt":
                format_ = suffix[1:]
            else:
                raise NotImplementedError
        else:
            raise TypeError
    if format_ == "xyz":
        crds = traj_xyz(traj, **kwargs)
    else:
        raise NotImplementedError
    if append:
        m.crds.extend(crds)
    else:
        m.crds = crds
    MACROS.CMD = {"TRAJ": {"crds": crds, "append": append, "mid":m.id}}


def traj_xyz(traj, **kwargs):
    frames = kwargs.get("frames", 1)
    crds = [None] * frames
    with open(traj) as f:
        for frame in range(frames):
            num = int(f.readline())
            crd = [None] * num
            f.readline()
            for i in range(num):
                line = f.readline()
                words = line.split()
                crd[i] = [float(words[j + 1]) for j in range(3)]
            crds[frame] = crd
    return crds
