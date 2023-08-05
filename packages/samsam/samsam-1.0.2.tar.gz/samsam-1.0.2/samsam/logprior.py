# -*- coding: utf-8 -*-

# Copyright 2021 Jean-Baptiste Delisle
#
# This file is part of samsam.
#
# samsam is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# samsam is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with samsam.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from scipy.special import beta as sp_beta, erf as sp_erf

log2pi = np.log(2.0 * np.pi)
halflog2pi = log2pi / 2.0


def uniform(x, a=0.0, b=1.0):
  r"""
  Uniform distribution over an interval :math:`[a,b[`.

  Parameters
  ----------
  x : float
    Value of the variable.
  a : float
    Interval lower bound.
  b : float
    Interval upper bound.

  Returns
  -------
  lp : float
    Log-probability of x.
  """

  if x < a or x >= b:
    raise Exception('uniform: out of bounds.')
  return (-np.log(b - a))


def uniform_periodic(x, period):
  r"""
  Uniform distribution over a periodic interval.

  Parameters
  ----------
  x : float
    Value of the variable.
  period : float
    Periodicity.

  Returns
  -------
  lp : float
    Log-probability of x.
  """

  return (-np.log(period))


def loguniform(x, loga=0.0, logb=1.0):
  r"""
  Log-uniform distribution over an interval :math:`[a,b[`.

  Parameters
  ----------
  x : float
    Value of the variable.
  loga : float
    Logarithm of the lower bound.
  logb : float
    Logarithm of the upper bound.

  Returns
  -------
  lp : float
    Log-probability of x.
  """

  if x <= 0:
    raise Exception('loguniform: out of bounds.')
  logx = np.log(x)
  return (-logx + uniform(logx, loga, logb))


def moduniform(x, y, a=0.0, b=1.0):
  r"""
  Uniform distribution for the module :math:`\sqrt{x^2+y^2}`
  over an interval :math:`[a,b[`.

  Parameters
  ----------
  x : float
    Value of the abscissa.
  y : float
    Value of the ordinate.
  a : float
    Interval lower bound.
  b : float
    Interval upper bound.

  Returns
  -------
  lp : float
    Log-probability of x.
  """

  r = np.sqrt(x**2 + y**2)
  if r <= a or r >= b:
    raise Exception('moduniform: out of bounds.')
  return (-(log2pi + np.log(r * (b - a))))


def normal(x, mu=0.0, sig=1.0):
  r"""
  Normal distribution with parameters (mu,sig).

  Parameters
  ----------
  x : float
    Value of the variable.
  mu : float
    Mean.
  sig : float
    Standard-deviation.

  Returns
  -------
  lp : float
    Log-probability of x.
  """

  return (-(halflog2pi + np.log(sig) + ((x - mu) / sig)**2 / 2.0))


logtruncnorm_dic = {}


def _lazy_logtruncnorm(mu, sig, a, b):
  r"""
  Lazy computation of the normalizing coefficient for truncnormal.
  """
  if (mu, sig, a, b) not in logtruncnorm_dic:
    xa = (a - mu) / (np.sqrt(2) * sig)
    xb = (b - mu) / (np.sqrt(2) * sig)
    logtruncnorm_dic[(mu, sig, a,
      b)] = -np.log(np.sqrt(np.pi / 2) * sig * (sp_erf(xb) - sp_erf(xa)))
  return (logtruncnorm_dic[(mu, sig, a, b)])


def truncnormal(x, mu=0.0, sig=1.0, a=0, b=np.inf):
  r"""
  Truncated normal distribution with parameters (mu,sig,a,b).

  Parameters
  ----------
  x : float
    Value of the variable.
  mu : float
    Mean.
  sig : float
    Standard-deviation.
  a : float
    Lower bound.
  b : float
    Upper bound.

  Returns
  -------
  lp : float
    Log-probability of x.
  """

  if x < a or x >= b:
    raise Exception('truncnormal: out of bounds.')
  return (_lazy_logtruncnorm(mu, sig, a, b) - ((x - mu) / sig)**2 / 2.0)


def lognormal(x, mu=0.0, sig=1.0):
  r"""
  Log-normal distribution with parameters (mu,sig).

  Parameters
  ----------
  x : float
    Value of the variable.
  mu : float
    Mean of :math:`\log(x)`.
  sig : float
    Standard-deviation of :math:`\log(x)`.

  Returns
  -------
  lp : float
    Log-probability of x.
  """

  if x <= 0:
    raise Exception('lognormal: out of bounds.')
  logx = np.log(x)
  return (-logx + normal(logx, mu, sig))


logbeta_dic = {}


def _lazy_logbeta(a, b):
  r"""
  Lazy computation of log(beta(a,b))
  """
  if (a, b) not in logbeta_dic:
    logbeta_dic[(a, b)] = np.log(sp_beta(a, b))
  return (logbeta_dic[(a, b)])


def beta(x, a, b):
  r"""
  Beta distribution with parameters (a, b).

  Parameters
  ----------
  x : float
    Value of the variable.
  a, b : float
    Shape parameters.

  Returns
  -------
  lp : float
    Log-probability of x.
  """

  if x <= 0 or x >= 1:
    raise Exception('beta: out of bounds.')
  return ((a - 1.0) * np.log(x) + (b - 1.0) * np.log(1.0 - x) -
    _lazy_logbeta(a, b))


def modbeta(x, y, a, b):
  r"""
  Beta distribution with parameters (a, b)
  for the module :math:`\sqrt{x^2+y^2}`.

  Parameters
  ----------
  x : float
    Value of the abscissa.
  y : float
    Value of the ordinate.
  a, b : float
    Shape parameters.

  Returns
  -------
  lp : float
    Log-probability of x.
  """

  r = np.sqrt(x**2 + y**2)
  if r == 0 or r >= 1:
    raise Exception('modbeta: out of bounds.')
  return ((a - 2.0) * np.log(r) + (b - 1.0) * np.log(1.0 - r) -
    _lazy_logbeta(a, b) - log2pi)
