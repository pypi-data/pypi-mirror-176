# Vectors for ALAT (Advanced Linear Algebra Toolkit)

import math
from .exceptions import (
   DimensionError,
   MatrixError,
   VectorsError, 
   VectorsCountError,
   ZeroVectorsError,
)
from .base import (
   concat,
   dim,
   ismatrix,
   set_digits,
   scaler_mul,
   transpose,
   zeros,
   ones, 
)
from .base2 import (
   cofactors, 
   det, 
   solve,
)

__all__ = ["Vectors"]

class Vectors:
   """Vectors class for ALAT (Advanced Linear Algebra Toolkit).
   Each vector must be tuple."""
   
   def __init__(self, *vectors):
      # All vectors
      self.vectors = []
      for vector in vectors:
         if isinstance(vector, tuple):
               self.vectors.append(vector)
         else:
               raise TypeError("vectors must be tuple")
      # If points of vectors are not int or float, returns error.
      _points = []
      for vector in self.vectors:
         for point in vector:
               if not isinstance(point, (int, float)):
                  _points.append(1)
      if not _points == []:
         raise VectorsError("inconsistent vectors")
      
   def dim(self):
      """Returns dimesion of given vectors. For example:
      
      >>> result = Vectors((4, 7, 0), (6, 2))
      >>> print(result.dim())
      [3, 2]
      
      """
      # Dimension of any vector means count of points of vector. 
      _dim = [len(vector) for vector in self.vectors]
      # Generally, if number of result is one, we return just
      # that result.
      return _dim[0] if len(_dim) == 1 else _dim 
   
   def length(self, digits=18):
      """Returns length of vectors. For example:
      
      >>> result = Vectors((3, 4), (5, 12))
      >>> print(result.length(digits=18))
      [5, 12]
      
      """
      _pow, _length = 0, []
      # Firstly, we assign pow of points of each vector
      # to '_sqrt', 
      for vector in self.vectors:
         for point in vector:
               _pow += point ** 2
         # And then we take squares of added up points.
         _length.append(set_digits(math.sqrt(_pow), digits))

      return _length[0] if len(_length) == 1 else _length
   
   def isequal(self):
      """Returns True, if given vectors are equals."""
      _equal = []
      # Vector equality means points of each vector are
      # same with others.
      for i in range(len(self.vectors)):
         if self.vectors[0] == self.vectors[i]:
               _equal.append(1)
      if [_equal] == ones((1, len(self.vectors))):
         return True
      
      return False
   
   def iszero(self):
      """Returns True, if given vectors are zeros."""
      _iszero = []
      # Zero vector means each point of vectors are zero.
      for vector in self.vectors:
         _zeros = [list(vector)] == zeros((1, len(vector)))
         _iszero.append(True) if _zeros else _iszero.append(False)
               
      return _iszero[0] if len(_iszero) == 1 else _iszero
   
   def unit(self, digits=18):
      """Returns unit vectors from given vectors. For example:
      
      >>> result = Vectors((3, 4), (5, 12))
      >>> print(result.unit(digits=5))
      [(0.6, 0.8), (0.3846, 0.923)]
      
      """ 
      # We can find correspnding unit vector from any vector. For that
      # we create an matrix from vectors.
      _matrix, _unit, _start, _length = [], [], 0, self.length(digits)
      for vector in self.vectors:
         _matrix.append(list(vector))

      if isinstance(_length, (int, float)): _length = [_length]
      # And then we need to find lengths of all vectors. If length of
      # any vector is zero, this code block an error. Because there is
      # not unit vectors of zero vectors. 
      for length in _length:
         if length == 0.0:
               raise ZeroVectorsError("zero vector don't convert to unit")
         # Finally, we use 'scaler_mul' method to find unit vectors.
         _value = scaler_mul((1/length), [_matrix[_start]], digits)
         _start += 1
         for value in _value: _unit.append(tuple(value))
               
      return _unit[0] if len(_unit) == 1 else _unit
   
   def addition(self, digits=18):
      """Adds up given vectors. For example:
      
      >>> result = Vectors((1, 2), (4, 3), (-2, 0))
      >>> print(result.addition(digits=18))
      (3.0, 5.0)
      
      """
      # Also, we can add up vectors. For this, dim of each vector
      # must be same.
      _isdim, _zeros = [], zeros((1, len(self.vectors[0])))
      for i in range(len(self.vectors)):
         if len(self.vectors[0]) == len(self.vectors[i]):
               _isdim.append(1)
               
      if not [_isdim] == ones((1, len(self.vectors))):
         raise DimensionError("given vectors are not suitable") 
      # And we add up corresponding vectors points. 
      for vector in self.vectors:
         for i in range(len(vector)):
               _zeros[0][i] += set_digits(vector[i], digits)
               
      for total in _zeros: return tuple(total) 
         
      
   def scaler_mul(self, scaler, digits=18):
      """Multiplies given scaler and vectors. For example:
      
      >>> result = Vectors((4, 7), (-1, 0))
      >>> print(result.scaler_mul(-1, digits=18))
      [(-1.0, -7.0), (1.0, 0.0)]
      
      """
      _mul = []
      if not isinstance(scaler, (int, float)):
         raise TypeError("'scaler' argument must be int or flaot")
      # Points of each vector multiplies with an scaler.
      for vector in self.vectors:
         _matrix = scaler_mul(scaler, [list(vector)], digits)
         for vec in _matrix:
               _mul.append(tuple(vec))
      
      return _mul[0] if len(_mul) == 1 else _mul
   
   def distance(self, digits=18):
      """Returns distance between two given vectors. For example:
      
      >>> result = Vectors((0, 2, 2), (2, 0, 1))
      >>> print(result.distance(digits=18))
      3.0
      
      """
      _d, _total = [], 0
      # This method find distance between two vectors.
      if not len(self.vectors) == 2:
         raise VectorsCountError("count of given vectors must be two")
      
      if not self.dim()[0] == self.dim()[1]:
         raise DimensionError("given vectors are not suitable")
      # Firstly, we must find pow of distance between each point.
      for i in range(self.dim()[0]):
         _value = (self.vectors[0][i]-self.vectors[1][i])**2
         _d.append(_value)
      # And then we must add up the results.
      for total in _d: _total += total
      # Squares of the difference of two vectors.
      _distance = set_digits(math.sqrt(_total), digits)

      return _distance
   
   def dot_mul(self, digits=18):
      """Returns dot production of given two vectors. For example:
      
      >>> result = Vectors((1, 2, -3), (3, -2, 4))
      >>> print(result.dot_mul(digits=18))
      -13.0
      
      """
      # Dot production of two given vectors.
      _dot = 0
      if not len(self.vectors) == 2:
         raise VectorsCountError("count of given vectors must be two")
      
      if not self.dim()[0] == self.dim()[1]:
         raise DimensionError("given vectors are not suitable")
      # Basically, we multiply each point with corresponding points.
      for i in range(self.dim()[0]):
         _value = self.vectors[0][i]*self.vectors[1][i]
         _dot += _value
      
      return set_digits(_dot, digits)
   
   def iscs(self):
      """Returns True, if there is Cauchy-Schwarz inequality."""
      if len(self.vectors) == 2:
         if self.dim()[0] == self.dim()[1]:
            _dot1 = abs(self.dot_mul(digits=100))
            _vector1, _vector2 = self.vectors[0], self.vectors[1]
            _set1 = Vectors(_vector1, _vector1)
            _set2 = Vectors(_vector2, _vector2)
            _dot2 = _set1.dot_mul(digits=100)
            _dot3 = _set2.dot_mul(digits=100)
            if _dot2 * _dot3 >= _dot1:
                  return True
      
      return False
   
   def istriangle(self):
      """Returns True, if there is Triangular inequality."""
      if len(self.vectors) == 2:
         if len(self.vectors[0]) == len(self.vectors[1]):
               _part1 = self.addition(digits=100)
               _part2 = (Vectors(_part1).length(digits=100))
               _part3 = (Vectors(self.vectors[0]).length(100))
               _part4 = (Vectors(self.vectors[1]).length(100))
               if _part2 <= _part3 + _part4:
                  return True
         
      return False
   
   def ispythagorean(self):
      """Returns True, if there is Pythagorean inequality."""
      if len(self.vectors) == 2:
         if len(self.vectors[0]) == len(self.vectors[1]):
               _part1 = self.addition(digits=100)
               _part2 = (Vectors(_part1).length(digits=100))**2
               _part3 = (Vectors(self.vectors[0]).length(100))**2
               _part4 = (Vectors(self.vectors[1]).length(100))**2
               if _part2 == _part3 + _part4:
                  return True
         
      return False
   
   def angle(self, method="degrees", digits=18):
      """Returns angle between two vectors, `method` must be `'degrees'`,
       `'radians'` or `'decimal'`. For example:
      
      >>> result = Vectors((-4, 0, 2, -2), (2, 0, -1, 1))
      >>> print(result.angle(method="degrees")))
      180.0
      
      """
      # We can find angle between two vectors.
      if not len(self.vectors) == 2:
         raise VectorsCountError("count of given vectors must be two")
      # For that, vectors have same dimension.
      if not self.dim()[0] == self.dim()[1]:
         raise DimensionError("given vectors are not suitable")
      
      if not method in ("degrees", "radians", "decimal"):
         raise AttributeError("'method' argument must be 'degrees', "
                              "'radians' or 'decimal'")
      if True in self.iszero():
         raise ZeroVectorsError("zero vector is not acceptable")
      
      _value, _pow, _len = self.dot_mul(digits), 0, []
      # We must find the squares of added up vectors for first vector. 
      for i in self.vectors[0]: _pow += i**2
      _len.append(math.sqrt(_pow))
      _pow = 0
      # And same way, we do that for second vector.
      for i in self.vectors[1]: _pow += i**2   
      _len.append(math.sqrt(_pow))
      # This code block find angle between two vectors. 
      _angle = _value/(_len[0]*_len[1])
      # Lastly, we can return the results that is appropriate form
      # (according to 'method' argument).
      if method == "decimal":
         return set_digits(_angle, digits)
      if method == "radians":
         return set_digits(math.acos(_angle), digits)
      if method == "degrees":
         _degrees = math.degrees(math.acos(_angle))
         return set_digits(_degrees, digits)
   
   def  isorthonal(self):
      """Returns True, if given vectors are orthogonal."""
      # Determines vectors are orthonal with each other or not.
      _dim0 = [list(self.vectors[0])] == zeros((1, self.dim()[0]))
      _dim1 = [list(self.vectors[1])] == zeros((1,self.dim()[1]))
      if len(self.vectors) == 2:
         if self.dim()[0] == self.dim()[1]:
            # Each of two vector doesn't be zero vector.
            if not (_dim0 and _dim1):
               # If dot multiplication is 0.0, 
               # these two vectors are orthonal.
               _isorthogonal = self.angle(method="degrees")
               if _isorthogonal == 90.0: 
                  return True

      return False
   
   def isparallel(self):
      """Returns True if given two vectors are parallel."""
      # If angle of two vectors is 180.0, these two vector are parallel.
      _dim0 = [list(self.vectors[0])] == zeros((1, self.dim()[0]))
      _dim1 = [list(self.vectors[1])] == zeros((1,self.dim()[1]))
      if len(self.vectors) == 2:
         if self.dim()[0] == self.dim()[1]:
            # Each of two vector does't be zero vector.
            if not (_dim0 and _dim1):
               _isparallel = self.angle(method="degrees")
               if _isparallel == 180.0:
                  return True
      
      return False
   
   def cross_mul(self, digits=18):
      """Returns cross production of given two vectors. This method uses
      determinant property, so each vector must contains '`i`', '`j`'
      and '`k`' component. For example:
      
      >>> result = Vectors((1, -2, 1), (3, 1, -2))
      >>> print(result.cross_mul(digits=6))
      (3.0, 5.0, 7.0)
      
      """
      # We can do cross multiplication between two vector. There is
      # basic method for that using determinant. 
      if not len(self.vectors) == 2:
         raise VectorsCountError("count of given vectors must be two")
      # Think that, each point of vectors represents i, j, k, so each
      # vectors must contain these points.
      if not self.dim()[0] == self.dim()[1] == 3:
         raise DimensionError("given vectors are not suitable")
      # Firstly, we create new matrix from given two vectors, 
      _matrix = [[1,1,1],list(self.vectors[0]),list(self.vectors[1])]
      # and then we take cofactors map of this matrix. 
      _cofactors = cofactors(_matrix, digits)
      # Cross multiplication will be first row of cofactors map.
      _cross = tuple(_cofactors[0])
   
      return _cross
   
   def to_matrix(self, digits=18):
      """Converts vectors to matrix. For example:
      
      >>> result = Vectors((7, 0), (-2, 5), (8, 3))
      >>> print(result.to_matrix())
      [
         [7, 0], 
         [-2, 5], 
         [8, 3]
      ]
      """
      # Basically, we turn our vectors to an matrix. Under
      # some conditions, this can be useful.
      _row, _matrix = [], []
      for vector in self.vectors:
         for value in vector:
               _row.append(set_digits(value, digits))
               if len(_row) == len(vector):
                  _matrix.append(list(_row))
                  _row = []
      
      if ismatrix(_matrix): return _matrix
      else: raise MatrixError("inconsistent matrix")

   def lincom(self, lincomof, digits=18):
      """Linear combination. Writes `lincomof` vector as a linear 
      combination of given vectors. Howover, If it is not writible, 
      in this case, returns None. For example:
      
      ## Example 1
      >>> result = Vectors((2, 0, 1), (0, 1, 0), (-2, 0, 0))
      >>> print(result.lincom(lincomof=(2, 4, 2)))
      [[2.0], [4.0], [1.0]]
      # It means:
      (2, 4, 2) = 2.0*(2, 0, 1) + 4.0*(0, 1, 0) + 1.0*(-2, 0, 0)

      ## Example 2
      >>> result = Vectors((1, 2, 3), (0, 1, 2), (-1, 0, 1))
      >>> print(result.lincom(lincomof=(1, 1, 1)))
      None

      """
      _matrix = []
      if not isinstance(lincomof, tuple):
         raise TypeError("'lincomof' argument must be tuple")
      # Firstly, we must create a matrix and assign vectors in it as
      # reverse.
      for i in range(len(self.vectors)):
         _matrix.append(list(self.vectors[i]))
      # Right now, we transpose main matrix and target matrix.
      _matrix, _target = transpose(_matrix), transpose([list(lincomof)])
      # After that, we must concat these matrices and solve linear
      # equation that will be created.
      _solve = solve(concat(_matrix, _target, 1), digits)
      if _solve == None: return None

      return _solve

   def isspanning(self, R):
      """Returns True, if every given vector can be written as a linear
      combination. `R` argument indicates dimension of vector
      space."""
      _matrix = []
      if not isinstance(R, int): return False
      # Firstly, we must create an matrix from given vectors.
      for i in range(len(self.vectors)):
         _matrix.append(list(self.vectors[i]))
      # We should check the matrix that was created is real matrix or
      # just a any object.
      if not ismatrix(_matrix): return False
      # Also, we check the 'R' argument is appropriate for it.
      if dim(_matrix) != (R, R): return False
      _matrix = transpose(_matrix)
      # we can indicates whether given vectors are spanning of 'R' by
      # checking determinant of matrix. If determinant of matrix is not
      # equal to 0, in this case, given vectors span to 'R'.
      if det(_matrix) != 0: return True

      return False

   def isindependent(self, R):
      """Returns True, if given vectors are linearly independent in R."""
      _matrix = []
      if not isinstance(R, int): return False
      # Linearly independent means all coefficients must be zero. 
      # Previously, we make zero matrix according to 'R' argument.
      _lincomof = transpose(zeros(dim=(1, R)))
      # And then we create main matrix from given vectors.
      for i in range(len(self.vectors)):
         _matrix.append(list(self.vectors[i]))
      if not ismatrix(_matrix): return False
      _matrix = transpose(_matrix)
      if not dim(_matrix)[0] == dim(_lincomof)[0]: return False
      # Right now, we concat our two 'main' and 'lincomof' matrix
      _solve = solve(concat(_matrix, _lincomof, 1))
      if _solve == _lincomof:
         return True

      return False

   def isdependent(self, R):
      """Returns True, if given vectors are linearly dependent in R."""
      _matrix = []
      if not isinstance(R, int): return False
      # Linearly independent means all coefficients must be zero. 
      # Previously, we make zero matrix according to 'R' argument.
      _lincomof = transpose(zeros(dim=(1, R)))
      # And then we create main matrix from given vectors.
      for i in range(len(self.vectors)):
         _matrix.append(list(self.vectors[i]))
      if not ismatrix(_matrix): return False
      _matrix = transpose(_matrix)
      if not dim(_matrix)[0] == dim(_lincomof)[0]: return False
      # Right now, we concat our two 'main' and 'lincomof' matrix
      _solve = solve(concat(_matrix, _lincomof, 1))
      if _solve != _lincomof and _solve is not None:
         return True

      return False
