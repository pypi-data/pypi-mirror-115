"""

Parametric Analysis
===================

.. code:: python

	import surpyval.parametric as para

	model = para.Weibull.fit(x)

"""
import autograd.numpy as np

from surpyval import nonparametric as nonp
from .parametric_fitter import ParametricFitter
from .parametric import Parametric

from .weibull import Weibull
from .gumbel import Gumbel
from .exponential import Exponential
from .expo_weibull import ExpoWeibull
from .normal import Normal
from .normal import Gauss
from .lognormal import LogNormal
from .lognormal import Galton
from .gamma import Gamma
from .beta import Beta
from .uniform import Uniform
from .logistic import Logistic
from .loglogistic import LogLogistic
from .mixture_model import MixtureModel
from .dist_from_hazard import Distribution

