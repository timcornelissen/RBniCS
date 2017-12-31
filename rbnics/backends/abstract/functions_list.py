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

from rbnics.utils.decorators import ABCMeta, AbstractBackend, abstractmethod

# Type for storing a list of FE functions. From the user point of view this is
# the same as a matrix. Indeed, given a TruthMatrix A, a TruthVector F
# and a FunctionsList Z, overriding __mul__ and __rmul__ operators
# allow to write expressions like transpose(Z)*A*Z and transpose(Z)*F
@AbstractBackend
class FunctionsList(object, metaclass=ABCMeta):
    def __init__(self, V_or_Z, component=None):
        pass
    
    @abstractmethod
    def enrich(self, functions, component=None, weights=None, copy=True):
        pass
        
    @abstractmethod
    def clear(self):
        pass
        
    @abstractmethod
    def save(self, directory, filename):
        pass
        
    @abstractmethod
    def load(self, directory, filename):
        pass
        
    # self * other [used e.g. to compute Z*u_N or S*eigv]
    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __len__(self):
        pass
            
    # key may be an integer or a slice
    @abstractmethod
    def __getitem__(self, key):
        pass
        
    @abstractmethod
    def __setitem__(self, key, item):
        pass
        
    @abstractmethod
    def __iter__(self):
        pass
