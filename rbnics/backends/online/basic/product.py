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

from itertools import product as cartesian_product
from numbers import Number
from rbnics.backends.abstract import ParametrizedTensorFactory as AbstractParametrizedTensorFactory
from rbnics.backends.basic.wrapping import DelayedTranspose
from rbnics.utils.decorators import overload, ThetaType

def product(backend):
    class _Product(object):
        @overload(ThetaType, backend.AffineExpansionStorage, ThetaType + (None,))
        def __call__(self, thetas, operators, thetas2):
            order = operators.order()
            first_operator = None
            assert order in (1, 2)
            if order == 1: # vector storage of affine expansion online data structures (e.g. reduced matrix/vector expansions)
                first_operator = operators[0]
                assert isinstance(first_operator, (backend.Matrix.Type(), backend.Vector.Type(), backend.Function.Type(), Number))
                assert thetas2 is None
                assert len(thetas) == len(operators)
                for (index, (theta, operator)) in enumerate(zip(thetas, operators)):
                    if index == 0:
                        output = theta*operator
                    elif theta != 0.:
                        output += theta*operator
            elif order == 2: # matrix storage of affine expansion online data structures (e.g. error estimation ff/af/aa products)
                first_operator = operators[0, 0]
                assert isinstance(first_operator, (backend.Matrix.Type(), backend.Vector.Type(), Number))
                assert thetas2 is not None
                # no checks here on the first dimension of operators should be equal to len(thetas), and
                # similarly that the second dimension should be equal to len(thetas2), because the
                # current operator interface does not provide a 2D len method
                for (i, j) in cartesian_product(range(len(thetas)), range(len(thetas2))):
                    if i == 0 and j == 0:
                        output = thetas[0]*operators[0, 0]*thetas2[0]
                    elif thetas[i] != 0. and thetas2[j] != 0.:
                        output += thetas[i]*operators[i, j]*thetas2[j]
            else:
                raise ValueError("product(): invalid operands.")
            # Return
            return ProductOutput(output)
        
        @overload(ThetaType, backend.NonAffineExpansionStorage, ThetaType + (None, ))
        def __call__(self, thetas, operators, thetas2):
            from rbnics.backends import evaluate, product, sum, transpose
            assert operators._type in ("error_estimation_operators_11", "error_estimation_operators_21", "error_estimation_operators_22", "operators")
            if operators._type.startswith("error_estimation_operators"):
                assert operators.order() is 2
                assert thetas2 is not None
                assert "inner_product_matrix" in operators._content
                assert "delayed_functions" in operators._content
                delayed_functions = operators._content["delayed_functions"]
                assert len(delayed_functions) is 2
                output = transpose(sum(product(thetas, delayed_functions[0])))*operators._content["inner_product_matrix"]*sum(product(thetas2, delayed_functions[1]))
                # Return
                assert not isinstance(output, DelayedTranspose)
                return ProductOutput(output)
            elif operators._type == "operators":
                assert operators.order() is 1
                assert thetas2 is None
                assert "truth_operators_as_expansion_storage" in operators._content
                sum_product_truth_operators = sum(product(thetas, operators._content["truth_operators_as_expansion_storage"]))
                assert isinstance(sum_product_truth_operators, (AbstractParametrizedTensorFactory, Number))
                if isinstance(sum_product_truth_operators, AbstractParametrizedTensorFactory):
                    sum_product_truth_operators = evaluate(sum_product_truth_operators)
                elif isinstance(sum_product_truth_operators, Number):
                    pass
                else:
                    raise TypeError("Invalid operator type")
                assert "basis_functions" in operators._content
                basis_functions = operators._content["basis_functions"]
                assert len(basis_functions) in (0, 1, 2)
                if len(basis_functions) is 0:
                    output = sum_product_truth_operators
                elif len(basis_functions) is 1:
                    output = transpose(basis_functions[0])*sum_product_truth_operators
                    assert not isinstance(output, DelayedTranspose)
                elif len(basis_functions) is 2:
                    output = transpose(basis_functions[0])*sum_product_truth_operators*basis_functions[1]
                    assert not isinstance(output, DelayedTranspose)
                else:
                    raise ValueError("Invalid length")
                # Return
                return ProductOutput(output)
            else:
                raise ValueError("Invalid type")
                
    # Auxiliary class to signal to the sum() function that it is dealing with an output of the product() method
    class ProductOutput(object):
        def __init__(self, sum_product_return_value):
            self.sum_product_return_value = sum_product_return_value
            
    return (_Product(), ProductOutput)
