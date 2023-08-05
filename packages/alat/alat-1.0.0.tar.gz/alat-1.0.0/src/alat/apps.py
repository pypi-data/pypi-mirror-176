# Some applications for ALAT (Advanced Linear Algebra Toolkit)

from .exceptions import (
   DimensionError, 
   PointsError,
)
from .base import (
   ones, 
   set_digits,
   transpose, 
   scaler_mul, 
   cross_mul,
)
from .base2 import (
   cofactors, 
   det, 
   inverse,
)

__all__ = [
   "PolyCurveFitting", 
   "LeastSquaresReg", 
   "Area", 
   "Volume",
]

class PolyCurveFitting:
   """
   Polynomial Curve Fitting.
    
   # Paramaters:
   `x` argument represents just x axis point and must gives as  list. `y`
   argument represents just y axis points. If the any points of axises
   are misssing and `placeholder` argument is True, in this case missing
   values are trasformed to zero. `digits` argument represents digits
   number of result points. For example:
    
   >>> x = [1, 2, 3] 
   >>> y = [4, 0, 12]
   >>>  result = PolyCurveFitting(x, y, placeholder=False, digits=18)
   >>> print(result.fit())
   [24.0, -28.0, 8.0]
   # It means: f(x) = 24.0 - 28.0x + 8.0x**2  
   """
    
   def __init__(self, x, y, placeholder=False, digits=18):
      if isinstance(x, list) and isinstance(y, list):
         self.x, self.y = x, y
      else:
         raise TypeError("'x' and 'y'  argument must be list")
      
      if not len(self.x) == len(self.y) and placeholder is False:
         raise DimensionError("'x' and 'y' argument must be same length")
      # If x and y axis points are not equal and  'placeholder' method is
      # True, we must fill in x or y axises lists with '0' (zero).
      if not len(self.x) == len(self.y) and placeholder is True:
         if len(self.x) > len(self.y):
               bound = len(self.x) - len(self.y)
               while True:
                  self.y.append(0)
                  bound -= 1
                  if bound == 0: break
         else:
               bound = len(self.y) - len(self.x)
               while True:
                  self.x.append(0)
                  bound -= 1
                  if bound == 0: break
      self.digits = digits

   def fit(self):
      """Fits polynomial curve fitting."""
      # We are creating new matrix.
      _row, _matrix, _poly_curve_fitting = [], [], []
      for element in self.x:
         _start, _bound = 0, len(self.x)
         while True:
               _value = element**_start
               _row.append(_value)
               _start += 1
               if _start == _bound:
                  _matrix.append(list(_row))
                  _row = []
                  break
      # y axis points must be transposed.
      _target = transpose([self.y])
      # If inverse of matrix which created above is None, 
      # returns None.
      _inverse = inverse(_matrix, self.digits)
      if _inverse is None:
         return None
      _mul = cross_mul(_inverse, _target, self.digits)
      # Each points in '_mul' argument must be extract 
      # into '_poly_curve_fitting'.
      for row in _mul:
         for value in row:
               _poly_curve_fitting.append(value)
         
      return _poly_curve_fitting
   
class LeastSquaresReg:
   """Least Squares Regression.
   
   # Paramaters:
   `x` argument represents just x axis point and must given as list. `y`
   argument represents just y axis points. If the any points of axises
   are misssing and `placeholder` argument is True, in this case missing
   values are trasformed to zero. `digits` argument represents digits
   number of result points. For example:
   
   >>> x = [1, 2, 3, 4, 5]
   >>> y = [1, 2, 4, 4, 6]
   >>> result = LeastSquaresReg(x, y, placeholder=False, digits=4)
   >>> print(result.fit())
   [-0.199, 1.2]
   # It means: f(x) = -0.199 + 1.2x
   
   """
   def __init__(self, x, y, placeholder=False, digits=18):
      if isinstance(x, list) and isinstance(y, list):
         self.x, self.y = x, y
      else:
         raise TypeError("'x' and 'y' arguments must be list")
      
      if not len(self.x) == len(self.y) and placeholder is False:
         raise PointsError("count of given x and y axis point "
                           "must be equal")
      # If x and y axis points are not equal and 'placeholder' method is
      #  True, we must fill in x or y axises lists with '0' (zero).
      if not len(self.x) == len(self.y) and placeholder is True:
         if len(self.x) > len(self.y):
               bound = len(self.x) - len(self.y)
               while True:
                  self.y.append(0)
                  bound -= 1
                  if bound == 0: break
         else:
               bound = len(self.y) - len(self.x)
               while True:
                  self.x.append(0)
                  bound -= 1
                  if bound == 0: break
      self.digits = digits
      
   def fit(self):
      "Fits least squares regression."
      # It's initial matrix. In forward, we are gonna
      # assign valid values into it.
      _matrix, _least_squares_reg = ones(dim=(2, len(self.x))), []
      for i in range(len(self.x)):
         _matrix[1][i] = self.x[i]
      # Neccesary operations for this application.
      _transposed_matrix = transpose(_matrix)
      _target = transpose([self.y])
      _p0 = cross_mul(_matrix, _transposed_matrix, self.digits)
      _p1 = cofactors(_p0, self.digits)
      _p1 = scaler_mul(1/50, _p1, self.digits)
      _p2 = cross_mul(_matrix, _target, self.digits)
      _result = cross_mul(_p1, _p2, self.digits)
      # And then, we must extract each points into 
      # '_least_squares_reg' as we did above.
      for row in _result:
         for value in row:
               _least_squares_reg.append(value)
         
      return _least_squares_reg

class Area:
   """Area of triangle can be calculated using determinant. 
   
   # Parameters:
   `points` argument represents points of corner of triangle and must     
   be given three points. `digits` argument represents digits of result. 
   For example:
   
   >>> result = Area((1, 0), (2, 2), (4, 3))
   >>> print(result.calculate())
   1.5
   
   """
   def __init__(self, *points, digits=18):
      # Just three points are acceptable.
      if not len(points) == 3:
         raise PointsError("too many or missing points")

      self.x, self.y = [], []
      # And then, we are extracting points into x and y axis lists.
      for point in points:
         if isinstance(point, tuple):
               self.x.append(point[0])
               self.y.append(point[1])
         else:
            raise TypeError("'points' argument must be tuple")
      self.digits = digits
      
   def calculate(self):
      """Calculates area of triangle."""
      # It's initial matrix. In forward, it will change.
      _matrix = ones(dim=(3, 3))
      for i in range(3):
         _matrix[1][i] = self.y[i]
      for j in range(3):
         _matrix[0][j] = self.x[j]
      # Neccesary operitons.
      _transposed_matrix = transpose(_matrix)
      _area = det(_transposed_matrix, self.digits)
      _area = set_digits(_area, self.digits)/2
      
      return (-1) * _area if _area < 0 else _area
   
class Volume:
   """Area of tetrahedron can be calculated using determinant. 
   
   # Parameters:
   `points` argument represents points of corner of tetrahedron and must
   be given four points. `digits` argument represents digits of result.
   For example:
   
   >>> result = Volume((0, 4, 1), (4, 0, 0), (3, 5, 2), (2, 2, 5))
   >>> print(result.calculate())
   12.0
   
   """
   def __init__(self, *points, digits=18):
      # Just four points are acceptable.
      if not len(points) == 4:
         raise PointsError("too many or missing points")   

      self.x, self.y, self.z = [], [], []
      # We are extracting points into x, y and z axis lists.
      for point in points:
         if isinstance(point, tuple):
               self.x.append(point[0])
               self.y.append(point[1])
               self.z.append(point[2])
         else:
               raise TypeError("'points' arguments must be tuple")
      self.digits = digits
      
   def calculate(self):
      """Calculates volume of tetrahedron."""
      # It's initial matrix. In forward, it will change.
      _matrix = ones((4, 4))
      for i in range(4):
         _matrix[0][i] = self.x[i]
      for j in range(4):
         _matrix[1][j] = self.y[j]
      for k in range(4):
         _matrix[2][k] = self.z[k]
      # Neccesary operations.
      _transposed_matrix = transpose(_matrix)
      _volume = det(_transposed_matrix, self.digits)
      _volume = set_digits(_volume, self.digits)/6

      return (-1) * _volume if _volume < 0 else _volume
