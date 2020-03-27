# Copyright (C) 2015-2020 by the RBniCS authors
#
# This file is part of RBniCS.
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from rbnics.utils.decorators import ABCMeta, AbstractBackend, abstractmethod

@AbstractBackend
class ParametrizedTensorFactory(object, metaclass=ABCMeta):
    def __init__(self, tensor):
        pass

    @abstractmethod
    def create_interpolation_locations_container(self):
        pass

    @abstractmethod
    def create_snapshots_container(self):
        pass

    @abstractmethod
    def create_empty_snapshot(self):
        pass

    @abstractmethod
    def create_basis_container(self):
        pass

    @abstractmethod
    def create_POD_container(self):
        pass

    def interpolation_method_name(self):
        return "DEIM"

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def is_parametrized(self):
        pass

    @abstractmethod
    def is_time_dependent(self):
        pass
