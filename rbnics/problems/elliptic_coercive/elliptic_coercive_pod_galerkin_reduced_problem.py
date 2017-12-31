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

from rbnics.problems.base import LinearPODGalerkinReducedProblem, ParametrizedReducedDifferentialProblem
from rbnics.problems.elliptic_coercive.elliptic_coercive_problem import EllipticCoerciveProblem
from rbnics.problems.elliptic_coercive.elliptic_coercive_reduced_problem import EllipticCoerciveReducedProblem
from rbnics.reduction_methods.elliptic_coercive import EllipticCoercivePODGalerkinReduction
from rbnics.utils.decorators import ReducedProblemFor

EllipticCoercivePODGalerkinReducedProblem_Base = LinearPODGalerkinReducedProblem(EllipticCoerciveReducedProblem(ParametrizedReducedDifferentialProblem))

# Base class containing the interface of a projection based ROM
# for elliptic coercive problems.
@ReducedProblemFor(EllipticCoerciveProblem, EllipticCoercivePODGalerkinReduction)
class EllipticCoercivePODGalerkinReducedProblem(EllipticCoercivePODGalerkinReducedProblem_Base):
    pass
