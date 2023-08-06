"""Plot casm.project.Prim structures"""
import numpy as np

def conventional_fcc_unit_cell():
    """Integer transformation matrix from primitive to conventional FCC cell

    Assumes primitive FCC lattice column vector matrix:

        [[   0, a/2,  a/2 ],
         [ a/2,   0,  a/2 ],
         [ a/2, a/2,    0 ]]

    Returns
    -------
    T: 3x3 np.array
        np.array([[ -1,  1,  1],
                  [  1, -1,  1],
                  [  1,  1, -1]])
    """
    return np.array([[-1, 1, 1], [1, -1, 1], [1, 1, -1]])

def conventional_bcc_unit_cell():
    """Integer transformation matrix from primitive to conventional BCC cell

    Assumes primitive BCC lattice column vector matrix:

        [[ -a/2,  a/2,  a/2 ],
         [  a/2, -a/2,  a/2 ],
         [  a/2,  a/2, -a/2 ]]

    Returns
    -------
    T: 3x3 np.array
        np.array([[ 0,  1,  1 ],
                  [ 1,  0,  1 ],
                  [ 1,  1,  0 ]])
    """
    return np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])

def plot_prim(prim,
              super_cell=None,
              unit_cell=None,):
    if unit_cell is None:
        unit_cell = np.identity(3)
    if super_cell is None:
        super_cell = np.identity(3)
    T = np.dot(unit_cell, super_cell)
    a = 1.0
    L = np.array([[   0, a/2,  a/2 ],
                  [ a/2,   0,  a/2 ],
                  [ a/2, a/2,    0 ]])
    print(np.dot(L, T))
    return T.tolist()
