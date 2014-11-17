# This file is part of the pyMOR project (http://www.pymor.org).
# Copyright Holders: Rene Milk, Stephan Rave, Felix Schindler
# License: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)

from pymor.operators.basic import (OperatorBase, NumpyGenericOperator, NumpyMatrixBasedOperator,
                                   NumpyMatrixOperator)
from pymor.operators.constructions import (LincombOperator, ConstantOperator, FixedParameterOperator,
                                           VectorArrayOperator, VectorOperator, VectorFunctional)
from pymor.operators.interfaces import OperatorInterface
