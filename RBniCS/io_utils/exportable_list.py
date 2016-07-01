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
## @file functions_list.py
#  @brief Type for storing a list of FE functions.
#
#  @author Francesco Ballarin <francesco.ballarin@sissa.it>
#  @author Gianluigi Rozza    <gianluigi.rozza@sissa.it>
#  @author Alberto   Sartori  <alberto.sartori@sissa.it>

from RBniCS.io_utils.pickle_io import PickleIO

###########################     OFFLINE STAGE     ########################### 
## @defgroup OfflineStage Methods related to the offline stage
#  @{

class ExportableList(object):
    def __init__(self, import_export_backend):
        self._list = []
        if import_export_backend == "numpy":
            self._FileIO = NumpyIO
        elif import_export_backend == "pickle":
            self._FileIO = PickleIO
        else:
            raise RuntimeError("Invalid import/export backend")
    
    def append(self, element):
        self._list.append(element)
            
    def load(self, directory, filename):
        if self._list: # avoid loading multiple times
            return False
        if self._FileIO.exists_file(directory, filename):
            self._list = self._FileIO.load_file(directory, filename)
            return True
        else:
            return False
        
    def save(self, directory, filename):
        self._FileIO.save_file(self._list, directory, filename)
                         
    def __getitem__(self, key):
        return self._list[key]
        
    def __iter__(self):
        return iter(self._list)
        
    def __len__(self):
        return len(self._list)
     
#  @}
########################### end - OFFLINE STAGE - end ########################### 
