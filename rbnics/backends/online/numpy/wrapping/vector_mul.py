# Copyright (C) 2015-2020 by the RBniCS authors
#
# This file is part of RBniCS.
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from numpy import dot

def vector_mul_vector(vector1, vector2):
    return dot(vector1, vector2)
