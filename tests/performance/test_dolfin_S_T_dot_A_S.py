# Copyright (C) 2015-2018 by the RBniCS authors
#
# This file is part of RBniCS.
#
# RBniCS is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RBniCS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with RBniCS. If not, see <http://www.gnu.org/licenses/>.
#

import pytest
from dolfin import assemble, dx, FunctionSpace, grad, inner, TrialFunction, TestFunction, UnitSquareMesh
from numpy import isclose
from numpy.linalg import norm
from rbnics.backends import FunctionsList
from rbnics.backends import transpose as factory_transpose
from rbnics.backends.dolfin import transpose as dolfin_transpose
from rbnics.backends.online.numpy import Matrix as NumpyMatrix
from test_utils import RandomDolfinFunction

transpose = None
all_transpose = {"dolfin": dolfin_transpose, "factory": factory_transpose}

class Data(object):
    def __init__(self, Th, N):
        self.N = N
        mesh = UnitSquareMesh(Th, Th)
        self.V = FunctionSpace(mesh, "Lagrange", 1)
        u = TrialFunction(self.V)
        v = TestFunction(self.V)
        self.a = lambda k: k*inner(grad(u), grad(v))*dx
        
    def generate_random(self):
        # Generate random vectors
        S = FunctionsList(self.V)
        for _ in range(self.N):
            b = RandomDolfinFunction(self.V)
            S.enrich(b)
        k = RandomDolfinFunction(self.V)
        # Generate random matrix
        A = assemble(self.a(k))
        # Return
        return (S, A)
        
    def evaluate_builtin(self, S, A):
        result_builtin = NumpyMatrix(self.N, self.N)
        for j in range(self.N):
            A_S_j = A*S[j].vector()
            for i in range(self.N):
                result_builtin[i, j] = S[i].vector().inner(A_S_j)
        return result_builtin
        
    def evaluate_backend(self, S, A):
        return transpose(S)*A*S
        
    def assert_backend(self, S, A, result_backend):
        result_builtin = self.evaluate_builtin(S, A)
        relative_error = norm(result_builtin - result_backend)/norm(result_builtin)
        assert isclose(relative_error, 0., atol=1e-12)
        
@pytest.mark.parametrize("Th", [2**i for i in range(3, 7)])
@pytest.mark.parametrize("N", [10 + 4*j for j in range(1, 4)])
@pytest.mark.parametrize("test_type", ["builtin"] + list(all_transpose.keys()))
def test_dolfin_S_T_dot_A_S(Th, N, test_type, benchmark):
    data = Data(Th, N)
    print("Th = " + str(Th) + ", Nh = " + str(data.V.dim()) + ", N = " + str(N))
    if test_type == "builtin":
        print("Testing", test_type)
        benchmark(data.evaluate_builtin, setup=data.generate_random)
    else:
        print("Testing", test_type, "backend")
        global transpose
        transpose = all_transpose[test_type]
        benchmark(data.evaluate_backend, setup=data.generate_random, teardown=data.assert_backend)
