import numpy as np
from lpsmap.ad3qp.factor_graph import PFactorGraph


class Variable(object):
    """AD3 binary variables packed as a tensor."""

    def __init__(self, scores):
        self.shape = scores.shape

        self._offset = None
        self._ix = np.arange(np.prod(self.shape)).reshape(self.shape)
        self._scores = scores

    def __getitem__(self, slice_arg):
        return Slice(self, slice_arg)

    def __repr__(self):
        return f"Variable(shape={self.shape})"

    # TODO: operator~,  same gist as above


class Slice(object):
    def __init__(self, var, slice_arg):
        self._base_var = var
        self._ix = self._base_var._ix[slice_arg]

    def __getitem__(self, slice_arg):
        return Slice(self._base_var, self._ix[slice_arg])

    @property
    def shape(self):
        return self._ix.shape

    @property
    def value(self):
        return self._base_var.value.flat[self._ix]

    def __repr__(self):
        return f"Slice(shape={self.shape})"


class FactorGraph(object):

    def __init__(self):
        self.variables = []
        self.factors = []

    def variable_from(self, scores):
        """Initialize a tensor of variables with user-specified scores."""
        var = Variable(scores=scores)
        self.variables.append(var)
        return var

    def variable(self, shape):
        """Initialize a tensor of variables with zero scores."""
        scores = np.zeros(shape)
        return self.variable_from(scores)

    def add(self, factor):
        """Connect a factor to the factor graph."""
        self.factors.append(factor)

    def _cat(self, scores):
        return np.concatenate(scores)

    def _ravel(self, x):
        return x.ravel()

    def _make_variables(self, pfg):
        offset = {}
        offset_ = 0

        pvars = []
        scores = []

        for var in self.variables:
            offset[var] = offset_
            offset_ += var._ix.size

            scores.append(self._ravel(var._scores))
            for i in range(var._ix.size):
                v = pfg.create_binary_variable()
                pvars.append(v)

        n_vars = offset_
        return offset, pvars, self._cat(scores)

    def _vars_to_pvar(self, var, offset, pvars):
            if isinstance(var, Variable):
                ix = var._ix + offset[var]
                my_pvars = pvars[ix.ravel()].tolist()
                return my_pvars

            elif isinstance(var, Slice):
                ix = var._ix + offset[var._base_var]
                my_pvars = pvars[ix.ravel()].tolist()
                return my_pvars

            elif isinstance(var, tuple):
                my_pvars = tuple(self._vars_to_pvar(v, offset, pvars)
                                 for v in var)
                return my_pvars

            else:
                raise NotImplementedError()

    def _make_factors(self, pfg, offset, pvars):
        pvars = np.array(pvars)  # so we may index by list

        scores_add = []

        for factor in self.factors:
            my_pvars = self._vars_to_pvar(factor._variables, offset, pvars)
            _, adds = factor._construct(pfg, my_pvars)
            scores_add.extend((self._ravel(a) for a in adds))

        return scores_add

    def solve(self):
        """Solve the LP-SparseMAP quadratic optimization problem.

        If succesful, all variables `u` connected to the factor graph will have
        the `u.value` attribute set.
        """
        pfg = PFactorGraph()

        offset, pvars, scores = self._make_variables(pfg)
        self._make_factors(pfg, offset, pvars)

        pfg.set_log_potentials(scores)
        value, u, add, status = pfg.solve_qp_ad3()
        u = np.array(u)

        for var in self.variables:
            k = offset[var]
            var.value = u[k:k + var._ix.size].reshape(var._ix.shape)
