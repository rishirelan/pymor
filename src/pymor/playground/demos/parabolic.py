#!/usr/bin/env python
# This file is part of the pyMor project (http://www.pymor.org).
# Copyright Holders: Felix Albrecht, Rene Milk, Stephan Rave
# License: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function

import numpy as np

from pymor.gui.qt import visualize_glumpy_patch
from pymor.analyticalproblems import ThermalBlockProblem
from pymor.discretizers import discretize_elliptic_cg
from pymor.discretizations import InstationaryDiscretization
from pymor.la.numpyvectorarray import NumpyVectorArray
from pymor.algorithms.timestepping import ImplicitEulerTimeStepper

def parabolic_demo():
    p = ThermalBlockProblem(parameter_range=(0.01, 1))
    d_stat, d_data = discretize_elliptic_cg(p, diameter=1./100)
    U0 = NumpyVectorArray(np.zeros(d_stat.operator.dim_source))
    time_stepper = ImplicitEulerTimeStepper(50)

    d = InstationaryDiscretization(operator=d_stat.operator, rhs=d_stat.rhs, mass=d_stat.l2_product,
                                   initial_data=U0, T=1, products=d_stat.products, time_stepper=time_stepper,
                                   parameter_space=d_stat.parameter_space, visualizer=d_stat.visualizer)

    mu = next(d.parameter_space.sample_randomly(1))
    R = d.solve(mu)
    d.visualize(R)


if __name__ == '__main__':
    parabolic_demo()
