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

from rbnics.problems.stokes_optimal_control.stokes_optimal_control_reduced_problem import StokesOptimalControlReducedProblem
from rbnics.utils.decorators import Extends, ReducedProblemFor
from rbnics.problems.stokes_optimal_control.stokes_optimal_control_problem import StokesOptimalControlProblem
from rbnics.problems.base import PODGalerkinReducedProblem
from rbnics.reduction_methods.stokes_optimal_control import StokesOptimalControlPODGalerkinReduction

StokesOptimalControlPODGalerkinReducedProblem_Base = PODGalerkinReducedProblem(StokesOptimalControlReducedProblem)

@Extends(StokesOptimalControlPODGalerkinReducedProblem_Base) # needs to be first in order to override for last the methods
@ReducedProblemFor(StokesOptimalControlProblem, StokesOptimalControlPODGalerkinReduction)
class StokesOptimalControlPODGalerkinReducedProblem(StokesOptimalControlPODGalerkinReducedProblem_Base):
    pass
        