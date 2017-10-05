# Copyright (C) 2015-2017 by the RBniCS authors
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

from dolfin import FunctionSpace
from rbnics.backends.dolfin.wrapping.function_copy import function_copy

def functions_list_mul_online_matrix(functions_list, online_matrix, FunctionsListType):
    V = functions_list.V_or_Z
    assert isinstance(V, FunctionSpace)
    
    output = FunctionsListType(V)
    assert isinstance(online_matrix.M, int)
    for j in range(online_matrix.M):
        assert len(online_matrix[:, j]) == len(functions_list)
        output_j = function_copy(functions_list[0])
        output_j.vector().zero()
        for (i, fun_i) in enumerate(functions_list):
            online_matrix_ij = float(online_matrix[i, j])
            output_j.vector().add_local(fun_i.vector().array()*online_matrix_ij)
        output_j.vector().apply("add")
        output.enrich(output_j)
    return output

def functions_list_mul_online_vector(functions_list, online_vector):
    output = function_copy(functions_list[0])
    output.vector().zero()
    for (i, fun_i) in enumerate(functions_list):
        online_vector_i = float(online_vector[i])
        output.vector().add_local(fun_i.vector().array()*online_vector_i)
    output.vector().apply("add")
    return output