# Copyright (C) 2015-2016 by the RBniCS authors
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
## @file numpy_io.py
#  @brief I/O helper functions
#
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

from RBniCS.utils.decorators import AbstractBackend, abstractmethod, abstractproperty

@AbstractBackend
class SeparatedParametrizedForm(object):
    def __init__(self, form):
        pass
    
    @abstractmethod
    def is_parametrized(self):
        pass
        
    @abstractmethod
    def name(self):
        pass
    
    @abstractmethod
    def separate(self):
        pass

    @abstractproperty        
    def coefficients(self):
        pass
    
    @abstractproperty
    def unchanged_forms(self):
        pass

    @abstractmethod        
    def replace_placeholders(self, i, new_coefficients):
        pass
    
    @abstractmethod
    def placeholders_names(self, i):
        pass

