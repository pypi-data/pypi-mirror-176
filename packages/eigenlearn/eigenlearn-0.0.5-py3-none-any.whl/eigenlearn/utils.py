import numpy as np
from scipy import linalg

def reshape_data(data):
    data_ = data.reshape(-1, data.shape[-1]).T
    return data_

def svd_data(data):
    U, S, V = linalg.svd(data, full_matrices=False)
    return U, S, V

def find_rank(S_,data,method='mp'):
    S = S_.copy()
    if method == 'mp':
        limit = max_sv_from_mp(np.var((data[-256:,:])),data.shape)
        r = np.where(S<limit)[0][0]
        if r == 0:
            r = 1
    if method == 'sure':
        r = sure_(200, S, np.std((data[-256:,:].real)), data.shape)
    if method == 'svht':
        limit = svht(np.std((data[-256:,:])),data.shape,S)
        r = np.where(S<limit)[0][0]
        if r == 0:
            r = 1
    if method == 'svht_unk':
        limit = svht(None,data.shape,S)
        r = np.where(S<limit)[0][0]
        if r == 0:
            r = 1
    return r

# from lo-rank-denoising-tools by Will Clarke
def max_sv_from_mp(data_var, data_shape):
    """Calculate the upper Marchenko–Pastur limit for a pure noise
    Matrix of defined shape and data variance.

    :param data_var: Noise variance
    :type data_var: float
    :param data_shape: 2-tuple of data dimensions.
    :type data_shape: tuple
    :return: Upper MP singular value limit
    :rtype: float
    """
    # Make sure dimensions agree with utils.lsvd
    # utils.lsvd will always move largest dimension to first dim.
    if data_shape[1] > data_shape[0]:
        data_shape = (data_shape[1], data_shape[0])

    c = data_shape[1] / data_shape[0]
    sv_lim = data_var * (1 + np.sqrt(c))**2
    return (sv_lim * data_shape[0])**0.5

# from lo-rank-denoising-tools by Will Clarke -> modified
def sure_(rank, S, var, data_shape):
    def div_HARD(r, S, Nx, Nt):
        z = (Nx + Nt) * r - r**2
        for idx in range(r):
            for jdx in range(r, S.size):
                z += 2*S[jdx]**2 / (S[idx]**2 - S[jdx]**2)
        return z

    def SURE(r, S, v, Nx, Nt):
        return -2 * Nx * Nt * v \
               + np.sum(S[r:]**2) \
               + 4 * v * div_HARD(r, S, Nx, Nt)

    sure = np.zeros((data_shape[0],))
    rank = np.arange(1, data_shape[0] + 1)
    for r in rank:
        sure[r - 1] = SURE(r,
                           S,
                           var,
                           data_shape[0],
                           data_shape[-1])

    thresh_SURE = rank[np.argmin(sure[0:200])]
    return thresh_SURE

# Eq. derived from:
# The Optimal Hard Threshold for Singular Values is 4/√3
def svht(var,data_shape,S):
    if data_shape[1] > data_shape[0]:
        n = data_shape[1]
        m = data_shape[0]
    else:
        n = data_shape[0]
        m = data_shape[1]
    beta = m / n
    if var is None:
        omega = 0.56 * np.power(beta,3) - 0.95 * (beta**2) + (1.82*beta) + 1.43
        y_med = np.median(S)
        limit = omega * y_med
    else:
        lanbda = np.sqrt(2*(beta+1) + ((8*beta)/((beta+1)+np.sqrt((beta**2) + 14 * beta + 1))))
        limit = lanbda * np.sqrt(n) * var
    return limit

def inv_left(U,r,beta):
    Ut = U[:,0:r]
    l = U.shape[0]
    D = np.matmul(Ut,Ut.conj().T)-np.eye(l,dtype=U.dtype)
    Z = linalg.pinv(np.eye(l,dtype=U.dtype) + beta*np.matmul((D).conj().T,(D)))
    return Z