"""
Reduced Hessian Generation - 2nd Edition

This module creates the reduced Hessian for use in various KIPET modules
"""
# Standard library imports
import os
from pathlib import Path

# Third party imports
import numpy as np
import pandas as pd
from pyomo.contrib.pynumero.interfaces.pyomo_nlp import PyomoNLP
from pyomo.environ import Constraint, Param, Set, SolverFactory, Suffix
from scipy.sparse import coo_matrix, csc_matrix, csr_matrix, triu
from scipy.sparse.linalg import spsolve

# KIPET library imports
from kipet.estimability_tools.parameter_handling import set_scaled_parameter_bounds

DEBUG = True

def get_kkt_info(model_object, solver_results):
    """Takes the results object from SolverFactory and uses PyNumero or k_aug to get the jacobian and Hessian
    information as dataframes. This is done in place and does not return anything.

    kkt_data (dict): dictionary with the following structure:

            {
            'J': J,   # Jacobian
            'H': H,   # Hessian
            'var_ind': var_index_names, # Variable index
            'con_ind': con_index_names, # Constraint index
            'duals': duals, # Duals
            }

    :return: None

    """
    kaug = SolverFactory('k_aug')
    
    kaug.options["print_kkt"] = ""
    res = kaug.solve(model_object, tee=True)

    num_vars = res['Problem'][0]['Number of variables']
    num_cons = res['Problem'][0]['Number of constraints']

    kaug_files = Path('GJH')
    
    var_index_names = pd.read_csv(self.sol_files['col'], sep=';', header=None)  # dummy sep
    con_index_names = pd.read_csv(self.sol_files['row'], sep=';', header=None)  # dummy sep

    var_index_names = [var_name for var_name in var_index_names[0]]
    con_index_names = [con_name for con_name in con_index_names[0].iloc[:-1]]
    # con_index_number = {v: k for k, v in enumerate(con_index_names)}

    n = len(var_index_names)
    m = len(con_index_names)

    hess_file = kaug_files.joinpath('H_print.txt')
    hess = pd.read_csv(hess_file, delim_whitespace=True, header=None, skipinitialspace=True)
    
    hess.columns = ['irow', 'jcol', 'vals']
    hess.irow -= 1
    hess.jcol -= 1
    # os.unlink(f'{kaug_files}hess_debug.in')

    jac_file = kaug_files.joinpath('A_print.txt')
    jac = pd.read_csv(jac_file, delim_whitespace=True, header=None, skipinitialspace=True)

    jac.columns = ['irow', 'jcol', 'vals']
    jac.irow -= 1
    jac.jcol -= 1
    # os.unlink(f'{kaug_files}jacobi_debug.in')

    # try:
    #    duals = read_duals(stub + '.sol')
    # except:
    duals = None

    J = coo_matrix((jac.vals, (jac.jcol, jac.irow)), shape=(m, n))
    Hess_coo = coo_matrix((hess.vals, (hess.irow, hess.jcol)), shape=(n, n))
    H = Hess_coo + triu(Hess_coo, 1).T

        

    self.delete_sol_files()

    self.kkt_data = {
        'J': J,
        'H': H,
        'var_ind': var_index_names,
        'con_ind': con_index_names,
        'duals': duals,
    }

    return None


def calculate_reduced_hessian(self, d=None, optimize=False, return_Z=False):
    """Calculate the reduced Hessian
    
    :param dict d: The current parameter values
    :param bool optimize: Option to optimize the problem (if not done already)
    :param bool return_Z: Option to add the Z_mat to the returned values

    .. note::

        If returning the Z_mat, the returned object will be a tuple of the reduced Hessian and the Z matrix.

    :return: The reduced Hessian and optionally the Z matrix
    :rtype: numpy.ndarray
    
    """
    if optimize:
        self.optimize_model(d)

    self.get_kkt_info()
    H = self.kkt_data['H']
    J = self.kkt_data['J']
    var_ind = self.kkt_data['var_ind']
    con_ind_new = self.kkt_data['con_ind']
    duals = self.kkt_data['duals']

    col_ind = [var_ind.index(f'{self.variable_name}[{v}]') for v in self.parameter_set]
    m, n = J.shape

    if self.param_con_method == 'global':

        dummy_constraints = [f'{self.global_constraint_name}[{k}]' for k in self.parameter_set]
        # print(dummy_constraints)
        jac_row_ind = [con_ind_new.index(d) for d in dummy_constraints]
        # duals_imp = [duals[i] for i in jac_row_ind]

        # print(J.shape, len(duals_imp))

        J_c = delete_from_csr(J.tocsr(), row_indices=jac_row_ind).tocsc()
        row_indexer = SparseRowIndexer(J_c)
        J_f = row_indexer[col_ind]
        J_f = delete_from_csr(J_f.tocsr(), row_indices=jac_row_ind, col_indices=[])
        J_l = delete_from_csr(J_c.tocsr(), col_indices=col_ind)
        # print(J_f, J_l)

    elif self.param_con_method == 'fixed':

        jac_row_ind = []
        duals_imp = None

        J_c = J.tocsc()  # delete_from_csr(J.tocsr(), row_indices=jac_row_ind).tocsc()
        row_indexer = SparseRowIndexer(J_c.T)
        J_f = row_indexer[col_ind].T
        # J_f = delete_from_csr(J_f.tocsr(), row_indices=jac_row_ind, col_indices=[])
        J_l = delete_from_csr(J_c.tocsr(), col_indices=col_ind)
        # print(J_f, J_l)

    else:
        None

    r_hess, Z_mat = self._reduced_hessian_matrix(J_f, J_l, H, col_ind)

    if not return_Z:
        return r_hess.todense()
    else:
        return r_hess.todense(), Z_mat


def _reduced_hessian_matrix(F, L, H, col_ind):
    """This calculates the reduced hessian by calculating the null-space based
    on the constraints

    :param csr_matrix F: Rows of the Jacobian related to fixed parameters
    :param csr_matrix L: The remainder of the Jacobian without parameters
    :param csr_matrix H: The sparse Hessian
    :param list col_ind: indices of columns with fixed parameters
    
    :return: sparse version of the reduced Hessian
    :rtype: csr_matrix

    """
    n = H.shape[0]
    n_free = n - F.shape[0]

    X = spsolve(L.tocsc(), -F.tocsc())

    col_ind_left = list(set(range(n)).difference(set(col_ind)))
    col_ind_left.sort()

    Z = np.zeros([n, n_free])
    Z[col_ind, :] = np.eye(n_free)

    if isinstance(X, csc_matrix):
        Z[col_ind_left, :] = X.todense()
    else:
        Z[col_ind_left, :] = X.reshape(-1, 1)

    Z_mat = coo_matrix(np.mat(Z)).tocsr()
    Z_mat_T = coo_matrix(np.mat(Z).T).tocsr()
    Hess = H.tocsr()
    reduced_hessian = Z_mat_T * Hess * Z_mat

    return reduced_hessian, Z_mat


def read_duals(sol_file):
    """Reads the duals from the sol file after solving the problem

    :param str sol_file: The absolute path to the sol file

    :return list duals: The list of duals values taken from the sol file
    
    """
    sol_file_abs = Path(sol_file)

    duals = []
    with sol_file_abs.open() as f:
        lines = f.readlines()

    lines_found = True
    num_of_vars = int(lines[9])

    for ln, line in enumerate(lines):
        line = line.rstrip('\n')
        line = line.lstrip('\t').lstrip(' ')

        if ln >= 12 and ln <= (num_of_vars + 11):
            duals.append(float(line))

    return duals


def delete_from_csr(mat, row_indices=[], col_indices=[]):
    """
    Remove the rows (denoted by ``row_indices``) and columns (denoted by 
    ``col_indices``) from the CSR sparse matrix ``mat``.
    WARNING: Indices of altered axes are reset in the returned matrix

    :param csr_matrix mat: Sparse matrix to delete rows and cols from
    :param list row_indicies: rows to delete
    :param list col_indicies: cols to delete

    :return csr_matrix mat: The sparse matrix with the rows and cols removed

    """
    if not isinstance(mat, csr_matrix):
        raise ValueError("works only for CSR format -- use .tocsr() first")

    rows = []
    cols = []
    if row_indices:
        rows = list(row_indices)
    if col_indices:
        cols = list(col_indices)

    if len(rows) > 0 and len(cols) > 0:
        row_mask = np.ones(mat.shape[0], dtype=bool)
        row_mask[rows] = False
        col_mask = np.ones(mat.shape[1], dtype=bool)
        col_mask[cols] = False
        return mat[row_mask][:, col_mask]
    elif len(rows) > 0:
        mask = np.ones(mat.shape[0], dtype=bool)
        mask[rows] = False
        return mat[mask]
    elif len(cols) > 0:
        mask = np.ones(mat.shape[1], dtype=bool)
        mask[cols] = False
        return mat[:, mask]
    else:
        return mat


class SparseRowIndexer:
    """Class used to splice sparse matrices"""

    def __init__(self, matrix):
        data = []
        indices = []
        indptr = []

        _class = 'csr'
        # print(f'LOOK HERE: {type(matrix)}')
        if isinstance(matrix, csc_matrix):
            _class = 'csc'
        #     print(_class)

        self._class = _class
        # Iterating over the rows this way is significantly more efficient
        # than matrix[row_index,:] and matrix.getrow(row_index)
        for row_start, row_end in zip(matrix.indptr[:-1], matrix.indptr[1:]):
            data.append(matrix.data[row_start:row_end])
            indices.append(matrix.indices[row_start:row_end])
            indptr.append(row_end - row_start)  # nnz of the row

        self.data = np.array(data, dtype=object)
        self.indices = np.array(indices, dtype=object)
        self.indptr = np.array(indptr)
        self.n_columns = matrix.shape[1]

    def __getitem__(self, row_selector):
        data = np.concatenate(self.data[row_selector])
        indices = np.concatenate(self.indices[row_selector])
        indptr = np.append(0, np.cumsum(self.indptr[row_selector]))

        shape = [indptr.shape[0] - 1, self.n_columns]

        if self._class == 'csr':
            return csr_matrix((data, indices, indptr), shape=shape)
        else:
            return csr_matrix((data, indices, indptr), shape=shape).T.tocsc()
