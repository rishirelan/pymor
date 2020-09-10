# This file is part of the pyMOR project (http://www.pymor.org).
# Copyright 2013-2020 pyMOR developers and contributors. All rights reserved.
# License: BSD 2-Clause License (http://opensource.org/licenses/BSD-2-Clause)

from pymor.core.base import abstractmethod
from pymor.core.cache import CacheableObject
from pymor.operators.constructions import induced_norm
from pymor.parameters.base import ParametricObject, Mu
from pymor.tools.frozendict import FrozenDict
from pymor.tools.deprecated import Deprecated


class Model(CacheableObject, ParametricObject):
    """Interface for model objects.

    A model object defines a discrete problem
    via its `class` and the |Operators| it contains.
    Furthermore, models can be
    :meth:`solved <Model.solve>` for given
    |parameter values| resulting in a solution |VectorArray|.

    Attributes
    ----------
    solution_space
        |VectorSpace| of the solution |VectorArrays| returned by :meth:`solve`.
    output_dim
        Dimension of the model output returned by :meth:`output`. `None` if the
        model has no output.
    linear
        `True` if the model describes a linear problem.
    products
        Dict of inner product operators associated with the model.
    """

    solution_space = None
    output_dim = None
    linear = False
    products = FrozenDict()

    def __init__(self, products=None, error_estimator=None, visualizer=None,
                 name=None, **kwargs):
        products = FrozenDict(products or {})
        if products:
            for k, v in products.items():
                setattr(self, f'{k}_product', v)
                setattr(self, f'{k}_norm', induced_norm(v))

        self.__auto_init(locals())

    @abstractmethod
    def _solve(self, mu=None, return_output=False, **kwargs):
        """Perform the actual solving."""
        pass

    def solve(self, mu=None, return_output=False, **kwargs):
        """Solve the discrete problem for the |parameter values| `mu`.

        The result will be :mod:`cached <pymor.core.cache>`
        in case caching has been activated for the given model.

        Parameters
        ----------
        mu
            |Parameter values| for which to solve.
        return_output
            If `True`, the model output for the given |parameter values| `mu` is
            returned as a 2D |NumPy array| with dimension :attr:`output_dim` in
            axis 1. (For stationary problems, axis 0 has dimension 1. For
            time-dependent problems, the dimension of axis 0 depends on the number
            of time steps.)

        Returns
        -------
        The solution |VectorArray|. When `return_output` is `True`,
        the output |NumPy array| is returned as second value.
        """
        if not isinstance(mu, Mu):
            mu = self.parameters.parse(mu)
        assert self.parameters.assert_compatible(mu)
        return self.cached_method_call(self._solve, mu=mu, return_output=return_output, **kwargs)

    def output(self, mu=None, **kwargs):
        """Return the model output for given |parameter values| `mu`.

        Parameters
        ----------
        mu
            |Parameter values| for which to compute the output.

        Returns
        -------
        The computed model output as a 2D |NumPy array| with dimension
        :attr:`output_dim` in axis 1. (For stationary problems, axis 0 has
        dimension 1. For time-dependent problems, the dimension of axis 0 
        depends on the number of time steps.)
        """
        return self.solve(mu=mu, return_output=True, **kwargs)[1]

    def estimate_error(self, U, mu=None):
        """Estimate the model error for a given solution.

        The model error could be the error w.r.t. the analytical
        solution of the given problem or the model reduction error w.r.t.
        a corresponding high-dimensional |Model|.

        Parameters
        ----------
        U
            The solution obtained by :meth:`~solve`.
        mu
            |Parameter values| for which `U` has been obtained.

        Returns
        -------
        The estimated error.
        """
        if getattr(self, 'error_estimator') is not None:
            return self.error_estimator.estimate_error(U, mu=mu, m=self)
        else:
            raise NotImplementedError('Model has no error estimator.')

    @Deprecated('estimate_error')
    def estimate(self, U, mu=None):
        return self.estimate_error(U, mu)

    def visualize(self, U, **kwargs):
        """Visualize a solution |VectorArray| U.

        Parameters
        ----------
        U
            The |VectorArray| from
            :attr:`~pymor.models.interface.Model.solution_space`
            that shall be visualized.
        kwargs
            See docstring of `self.visualizer.visualize`.
        """
        if getattr(self, 'visualizer') is not None:
            return self.visualizer.visualize(U, self, **kwargs)
        else:
            raise NotImplementedError('Model has no visualizer.')
