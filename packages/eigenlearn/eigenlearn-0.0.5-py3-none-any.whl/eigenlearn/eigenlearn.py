import numpy as np

from src.eigenlearn.utils import reshape_data, svd_data, find_rank, inv_left



def learn(data, r='svht_unk', beta=10):
    data = np.asarray(data)
    if len(data.shape)>2:
        data = reshape_data(data)
    U, S, V = svd_data(data)
    if type(r) == int:
        r = r
    else:
        r = find_rank(S, data, method=r)
    Z = inv_left(U, r, beta)
    return Z, r, S

def solve(data, Z):
    solution = np.matmul(Z, data)
    return solution