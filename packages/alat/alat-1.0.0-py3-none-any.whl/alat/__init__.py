"""ALAT - Advanced Linear Algebra Toolkit

ALAT project was developed for linear algebra calculations.

Resources: 
Elementary Linear Algebra, Sixth Edition by Ron LARSON, David C. FALVO

Started date: 04-07-2022
"""

__author__ = "Can Gulmez (ahmetcangulmez02@gmail.com)"
__version__ = "1.0.0"
__licence__ = "MIT License"

from .apps import (
   PolyCurveFitting, 
   LeastSquaresReg, 
   Area, 
   Volume,
)
from .base import (
   ismatrix, 
   set_digits, 
   dim, 
   issquare, 
   diagonal, 
   iszero, 
   ishomogen, 
   isones, 
   isidentity, 
   zeros, 
   ones, 
   identity, 
   arbitrary, 
   sequential, 
   random, 
   isequal, 
   highest, 
   lowest, 
   aggregate,
   iselementary, 
   mean, 
   sort, 
   stdev, 
   mode, 
   median,
   mix, 
   redim, 
   addition, 
   scaler_mul, 
   subtraction, 
   dot_mul, 
   transpose, 
   remove, 
   concat, 
   islt, 
   isut,
   istriangular, 
   cross_mul, 
   scaler_div, 
   dot_div    
)
from .base2 import (
   minors, 
   cofactors, 
   det, 
   isinvertible, 
   adj, 
   inverse, 
   cross_div, 
   solve
)
from .vectors import Vectors
from .crypt import Crypt
