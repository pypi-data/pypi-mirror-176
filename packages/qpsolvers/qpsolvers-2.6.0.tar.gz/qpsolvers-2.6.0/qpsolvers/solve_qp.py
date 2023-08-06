#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2022 Stéphane Caron and the qpsolvers contributors.
#
# This file is part of qpsolvers.
#
# qpsolvers is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# qpsolvers is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with qpsolvers. If not, see <http://www.gnu.org/licenses/>.

"""
Solve quadratic programs.
"""

import warnings
from typing import Optional, Union

import numpy as np
import scipy.sparse as spa
from numpy import eye, hstack, ones, vstack, zeros

from .check_problem_constraints import check_problem_constraints
from .exceptions import NoSolverSelected, SolverNotFound
from .solvers import available_solvers, dense_solvers, solve_function


def solve_qp(
    P: Union[np.ndarray, spa.csc_matrix],
    q: np.ndarray,
    G: Optional[Union[np.ndarray, spa.csc_matrix]] = None,
    h: Optional[np.ndarray] = None,
    A: Optional[Union[np.ndarray, spa.csc_matrix]] = None,
    b: Optional[np.ndarray] = None,
    lb: Optional[np.ndarray] = None,
    ub: Optional[np.ndarray] = None,
    solver: Optional[str] = None,
    initvals: Optional[np.ndarray] = None,
    sym_proj: bool = False,
    verbose: bool = False,
    **kwargs,
) -> Optional[np.ndarray]:
    """
    Solve a Quadratic Program defined as:

    .. math::

        \\begin{split}\\begin{array}{ll}
            \\mbox{minimize} &
                \\frac{1}{2} x^T P x + q^T x \\\\
            \\mbox{subject to}
                & G x \\leq h                \\\\
                & A x = b                    \\\\
                & lb \\leq x \\leq ub
        \\end{array}\\end{split}

    using the QP solver selected by the ``solver`` keyword argument.

    Parameters
    ----------
    P :
        Symmetric quadratic-cost matrix (most solvers require it to be definite
        as well).
    q :
        Quadratic-cost vector.
    G :
        Linear inequality matrix.
    h :
        Linear inequality vector.
    A :
        Linear equality matrix.
    b :
        Linear equality vector.
    lb :
        Lower bound constraint vector.
    ub :
        Upper bound constraint vector.
    solver :
        Name of the QP solver, to choose in
        :data:`qpsolvers.available_solvers`. This argument is mandatory.
    initvals :
        Primal candidate vector :math:`x` values used to warm-start the solver.
    sym_proj :
        Set to ``True`` to project the cost matrix :math:`P` to its symmetric
        part. Some solvers assume :math:`P` is symmetric and will return
        unintended results if it is not the case.
    verbose :
        Set to ``True`` to print out extra information.

    Note
    ----
    In quadratic programming, the matrix :math:`P` should be symmetric. Many
    solvers (including CVXOPT, OSQP and quadprog) leverage this property and
    may return unintended results when it is not the case. You can set
    ``sym_proj=True`` to project :math:`P` on its symmetric part, at the cost
    of a little computation time.

    Returns
    -------
    :
        Optimal solution if found, otherwise ``None``.

    Raises
    ------
    NoSolverSelected
        If the ``solver`` keyword argument is not set.

    SolverNotFound
        If the requested solver is not in :data:`qpsolvers.available_solvers`.

    ValueError
        If the problem is not correctly defined. For instance, if the solver
        requires a definite cost matrix but the provided matrix :math:`P` is
        not.

    Notes
    -----
    Extra keyword arguments given to this function are forwarded to the
    underlying solver. For example, we can call OSQP with a custom absolute
    feasibility tolerance by ``solve_qp(P, q, G, h, solver='osqp',
    eps_abs=1e-6)``. See the :ref:`Supported solvers <Supported solvers>` page
    for details on the parameters available to each solver.

    There is no guarantee that a ``ValueError`` is raised if the provided
    problem is non-convex, as some solvers don't check for this. Rather, if the
    problem is non-convex and the solver fails because of that, then a
    ``ValueError`` will be raised.
    """
    if solver is None:
        raise NoSolverSelected(
            "Set the `solver` keyword argument to one of the "
            f"available solvers in {available_solvers}"
        )
    if sym_proj:
        P = 0.5 * (P + P.transpose())
    if isinstance(A, np.ndarray) and A.ndim == 1:
        A = A.reshape((1, A.shape[0]))
    if isinstance(G, np.ndarray) and G.ndim == 1:
        G = G.reshape((1, G.shape[0]))
    check_problem_constraints(G, h, A, b)
    kwargs["initvals"] = initvals
    kwargs["verbose"] = verbose
    try:
        return solve_function[solver](P, q, G, h, A, b, lb, ub, **kwargs)
    except KeyError as e:
        raise SolverNotFound(
            f"solver '{solver}' is not in the list "
            f"{available_solvers} of available solvers"
        ) from e


def solve_safer_qp(
    P: np.ndarray,
    q: np.ndarray,
    G: np.ndarray,
    h: np.ndarray,
    sr: float,
    reg: float = 1e-8,
    solver: Optional[str] = None,
    initvals: Optional[np.ndarray] = None,
    sym_proj: bool = False,
) -> Optional[np.ndarray]:
    """
    Solve the "safer" Quadratic Program with repulsive inequality constraints,
    defined as:

    .. math::

        \\begin{split}\\begin{array}{ll}
            \\mbox{minimize} &
                \\frac{1}{2} x^T P x + q^T x +
                \\frac{1}{2} \\mathit{reg} \\|s\\|^2 - \\mathit{sr} \\1^T s
                \\\\
            \\mbox{subject to}
                & G x \\leq h
        \\end{array}\\end{split}

    Slack variables `s` (i.e. distance to inequality constraints) are added to
    the vector of optimization variables and included in the cost function.
    This pushes the solution of this "safer" QP is further inside the
    linear constraint region.

    Parameters
    ----------
    P :
        Symmetric quadratic-cost matrix.
    q :
        Quadratic-cost vector.
    G :
        Linear inequality matrix.
    h :
        Linear inequality vector.
    sr :
        This is the "slack repulsion" parameter that makes inequality
        constraints repulsive. In practice it weighs the linear term on slack
        variables in the augmented cost function. Higher values bring the
        solution further inside the constraint region but override the
        minimization of the original objective.
    reg :
        Regularization term that weighs squared slack variables in the cost
        function. Increase this parameter in case of numerical instability, and
        otherwise set it as small as possible compared, so that the squared
        slack cost is as small as possible compared to the regular cost.
    solver :
        Name of the QP solver to use.
    initvals :
        Primal candidate vector `x` values used to warm-start the solver.
    sym_proj :
        Set to `True` when the `P` matrix provided is not symmetric.

    Returns
    -------
    :
        Optimal solution to the relaxed QP, if found, otherwise ``None``.

    Raises
    ------
    ValueError
        If the quadratic program is not feasible.

    Note
    ----
    This is a legacy function.

    Notes
    -----
    This method can be found in the Inverse Kinematics resolution of Nozawa et
    al. (Humanoids 2016). It also appears in earlier works such as the
    "optimally safe" tension distribution algorithm of Borgstrom et al. (IEEE
    Transactions on Robotics, 2009).
    """
    warnings.warn(
        "The `solve_safer_qp` function is deprecated "
        "and will be removed in qpsolvers v2.7",
        DeprecationWarning,
        stacklevel=2,
    )
    if solver is None:
        raise NoSolverSelected(
            "Set the `solver` keyword argument to one of the "
            f"available dense solvers in {dense_solvers}"
        )
    if solver not in dense_solvers:
        raise NotImplementedError(
            "This function is only available for dense solvers"
        )
    n, m = P.shape[0], G.shape[0]
    E, Z = eye(m), zeros((m, n))
    P2 = vstack([hstack([P, Z.T]), hstack([Z, reg * eye(m)])])
    q2 = hstack([q, -sr * ones(m)])
    G2 = hstack([Z, E])
    h2 = zeros(m)
    A2 = hstack([G, -E])
    b2 = h
    x = solve_qp(
        P2,
        q2,
        G2,
        h2,
        A2,
        b2,
        solver=solver,
        initvals=initvals,
        sym_proj=sym_proj,
    )
    if x is None:
        return None
    return x[:n]
