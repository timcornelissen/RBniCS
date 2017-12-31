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

from sympy import MatrixSymbol, zeros
from rbnics.shape_parametrization.utils.symbolic.python_string_to_sympy import python_string_to_sympy
from rbnics.shape_parametrization.utils.symbolic.strings_to_sympy_symbolic_parameters import strings_to_sympy_symbolic_parameters
from rbnics.shape_parametrization.utils.symbolic.sympy_symbolic_coordinates import sympy_symbolic_coordinates

def compute_shape_parametrization_gradient(shape_parametrization_expression_on_subdomain):
    # Get the domain dimension and symbolic coordinates
    dim = len(shape_parametrization_expression_on_subdomain)
    x = sympy_symbolic_coordinates(dim, MatrixSymbol)
    # Get a sympy symbol for mu
    mu = strings_to_sympy_symbolic_parameters(shape_parametrization_expression_on_subdomain, MatrixSymbol)
    # Convert expression from string to sympy representation
    deformation = list()
    for deformation_i in shape_parametrization_expression_on_subdomain:
        deformation.append(python_string_to_sympy(deformation_i, x, mu))
    # Compute gradient
    gradient = zeros(dim, dim)
    for i in range(dim):
        for j in range(dim):
            gradient[i, j] = deformation[i].diff(x[j])
    # Convert to a tuple of tuple of strings
    gradient_str = list()
    for i in range(dim):
        gradient_str_i = list()
        for j in range(dim):
            gradient_str_i.append(str(gradient[i, j]).replace(", 0]", "]"))
        gradient_str.append(tuple(gradient_str_i))
    return tuple(gradient_str)
