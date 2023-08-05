# Determinant and some methods for ALAT (Advanced Linear Algebra)

import math
from .base import (
   aggregate,
   dot_mul,
   ismatrix, 
   dim, 
   issquare, 
   redim, 
   set_digits, 
   transpose, 
   scaler_div, 
   cross_mul, 
)
from .exceptions import (
   DimensionError, 
   MatrixError, 
   SquareMatrixError, 
   InvertibleMatrixError,
)

__all__ = [
   'Determinant', 'minors', 'cofactors', 'det', 'isinvertible', 'adj', 
   'inverse', 'cross_div', 'solve', 
]

class Determinant:
   """Determinant class for ALAT (Advanced Linear Algebra Toolkit)"""

   def __init__(self, matrix, digits=18):
      if not ismatrix(matrix):
         raise MatrixError("inconsistent matrix")
      
      if not issquare(matrix):
         raise SquareMatrixError("given matrix must be square")

      if not isinstance(digits, int):
         raise TypeError("'digits' argument must be int")

      self.matrix, self.digits, self.coefs = matrix, digits, []
      # Initial values of self.coefs are first row of given matrix.
      # Notice that if index of values are adds, in this case, we 
      # have to multiply this value by -1.
      _coefs = self.matrix[0].copy()
      for index, value in enumerate(_coefs):
         if index % 2 == 1 and not value == 0:
            _coefs[index] = -1 * value

      self.coefs.append(list(_coefs))

   def det1(self):
      """Returns determinant of 1x1 matrix."""
      if not dim(self.matrix) == (1, 1):
         raise DimensionError("given matrix is not suitable")

      return set_digits(self.matrix[0][0], self.digits)

   def det2(self):
      """Returns determinant of 2x2 matrix."""
      if not dim(self.matrix) == (2, 2):
         raise DimensionError("given matrix is not suitable")
      # We use frequently it. Because, we will want to reduce all 
      # matrices that have more dimension than two to 2x2 matrix.
      _s1 = self.matrix[0][0] * self.matrix[1][1]
      _s2 = self.matrix[0][1] * self.matrix[1][0]

      return set_digits(_s1 - _s2, self.digits)

   def parse(self):
      """Parses the given matrix one time."""
      if dim(self.matrix) == (1, 1):
         return None
      # This code block reduces dimension of given matrix one time 
      # and creates new parsed matrix.
      _parsed = []
      for i in range(dim(self.matrix)[1]):
         _matrix = self.matrix.copy()
         # We just parse matrix according to first row. Because 
         # determinant of each row will be same.
         del _matrix[0]
         _transposed = transpose(_matrix)
         del _transposed[i]
         _parsed.append(transpose(_transposed))

      return _parsed

   def parse_more(self):
      """Parses the given matrix one more time."""
      # Our aim in parsing matrix is to creates matrix that have 
      # only 2x2 dimension. Because, we can calculate easily 
      # determinant of 2x2 matrix.
      _parsed = self.parse()
      for matrix in _parsed:
         _det = Determinant(matrix, self.digits).parse()
         # Contnously, we should reduce dimension of matrix. This 
         # processing will be caused an error when matrix has 1x1
         # dimension. To fix it, we must break.
         for matrix in _det:
            if len(matrix) == 1:
               break
            _parsed.append(matrix)
      # Right here, we should add up coefficients that will be
      # multiplied with 2x2 matrix to 'self.coefs'. When we are
      # doing this, we have to consider index of coefficients. 
      # If index is odd, we are gonna multiply index by -1.
      for matrix in _parsed:
         if dim(matrix) >= (3, 3):
            _coefs = matrix[0].copy()
            for index, value in enumerate(_coefs):
               if index % 2 == 1 and not value == 0:
                  _coefs[index] = -1 * _coefs[index]
            self.coefs.append(_coefs)
      # We just want 2x2 matrix for calculating its determinant.
      _index = int(len(_parsed)-math.factorial(len(self.matrix))/2)
      _parsed = _parsed[_index:]
      # Right now, we should find determinant of each 2x2 matrix.
      for matrix in _parsed:
         if not ismatrix(matrix):
            break
         _value = Determinant(matrix, self.digits).det2()
         _parsed.append(_value)
      _parsed = _parsed[int(len(_parsed)/2):]
      
      return _parsed

   def det_more(self):
      """Returns determinant of given matrix."""
      # And then, we must multiply determinant of 2x2 matrix and
      # coefficients.
      _parsed, _coefs = self.parse_more(), self.coefs
      _row, _matrix, _limit = [], [], 3
      # Here, this block will convert it to an matrix. Because of
      # this it to use methods like 'dot_mul', 'aggregate' and so on.
      for value in _parsed:
         _row.append(value)
         if len(_row) == 3:
            _matrix.append(list(_row))
            _row = []
      # Right here, we are doing dot multiplication.
      while True:
         _coefs = [value for value in self.coefs if len(value)==_limit]
         _dot = dot_mul(_coefs, _matrix, self.digits)
         _agg = aggregate(_dot, axis=1)
         _limit += 1
         _matrix.clear()
         for i in _agg: 
            _matrix.append(i)
         if len(_matrix) == 1: break
         _matrix = redim(_agg, dim=(int(len(_agg)/_limit), _limit))

      return set_digits(_matrix[0][0], self.digits)

   def det(self):
      """Returns determinant of matrix that have any dimension."""
      # Finally, we can complete finding determinant of any matrix 
      # thanks to methods that are in above. 
      if dim(self.matrix)[0] == 1:
         return self.det1()
      if dim(self.matrix)[0] == 2:
         return self.det2()
      if dim(self.matrix)[0] >= 3:
         return self.det_more()
      
   def minors(self):
      """Returns minors map of any matrix."""
      if dim(self.matrix) == (1, 1):
         return None
      # Firstly, we must parse our matrix for each value and then each
      # of them is assigned to '_minors'.
      _row, _minors_map, _matrix, _minors = [], [], [], []
      for i in range(len(self.matrix)):
         for j in range(len(self.matrix[0])):
            _matrix = self.matrix.copy()
            del _matrix[i]
            _transposed = transpose(_matrix)
            del _transposed[j]
            _minors.append(transpose(_transposed))
      # After that, we find determinant of parsed matrix and append
      # them into new matrix.
      for det in _minors:
         _row.append(Determinant(det, self.digits).det())
         if len(_row) == len(self.matrix[0]):
            _minors_map.append(list(_row))
            _row = []
         
      return _minors_map

   def cofactors(self):
      """Returns cofactors map of any matrix."""
      if dim(self.matrix) == (1, 1):
         return None
      # cofactors of an square matrix is related with minors map.
      # But there is a basic different. Firstly, we get minors map
      # of a quare matrix and then multiply each value that has 
      # odd index in its row by -1
      _matrix = self.minors()
      for i in range(len(_matrix)):
         for j in range(len(_matrix[0])):
            if (i+j) % 2 == 1 and not _matrix[i][j] == 0:
               _matrix[i][j] = -1 * _matrix[i][j]

      return _matrix

# Some methods related with Determinant class.
def minors(matrix, digits=18):
   """Returns minors map of matrix. For example:

   >>> _matrix = [
      [-1, 2, 3], 
      [-4, 6, 8], 
      [7, -8, 9], 
   ]
   >>> result = minors(_matrix, digits=6)
   >>> print(result)
   [[118.0, -92.0, -10.0], [42.0, -30.0, -6.0], [-2.0, 4.0, 2.0]]         
    
   """
   return Determinant(matrix, digits).minors()

def cofactors(matrix, digits=18):
   """Returns cofactors map of given matrix. For example:
    
   >>> _matrix = [
      [-1, 2, 3], 
      [-4, 6, 8], 
      [7, -8, 9],
   ]
   >>> result = cofactors(_matrix, digits=6)
   >>> print(result)
   [[118.0, 92.0, -10.0], [-42.0, -30.0, 6.0], [-2.0, -4.0, 2.0]]
    
   """
   return Determinant(matrix, digits).cofactors()

def det(matrix, digits=18):
   """Returns determinant of given matrix. For example:
        
   >>> _matrix = [
      [0, 2, 1], 
      [3, -1, 2], 
      [4, 0, 1],
   ]
   >>> result = det(_matrix, digits=6)
   >>> print(result)
   14.0
    
   """
   return Determinant(matrix, digits).det()

def isinvertible(matrix):
   """Returns True, if given matrix is invertible."""
   if det(matrix, digits=18) != 0:
      return True
            
   return False

def adj(matrix, digits=18):
   """Returns adjoint of given matrix. For example:
    
   >>> _matrix = [
      [-1, 2, 3], 
      [-4, 6, 8], 
      [7, -8, 9],
   ]
   >>> result = adj(matrix)
   >>> print(result)
   [[118.0, -42.0, -2.0], [92.0, -30.0, -4.0], [-10.0, 6.0, 2.0]]
    
   """
   return transpose(cofactors(matrix, digits))

def inverse(matrix, digits=18):
   """Returns inverse of given matrix. For example:
    
   >>> _matrix = [
      [-1, 2, 3], 
      [-4, 6, 8], 
      [7, -8, 9],
   ]
   >>> result = inverse(matrix, digits=4)
   >>> print(result)
   [[3.277, -1.16, -0.05], [2.555, -0.83, -0.11], [-0.27, 0.166, 0.055]]
   
   """ 
   if not isinvertible(matrix): return None
   # inverse of an matrix that is invertible can be found with two
   # operations. These are determinant and adjoint. 
   _det, _adj = det(matrix, digits), adj(matrix, digits)
   _inverse = scaler_div(_det, _adj, "down", digits=digits)
    
   return _inverse

def cross_div(matrix1, matrix2, digits=18):
   """Divides given matrices with each other as cross. For example:
    
   >>> _matrix1 = [
      [4, 7, -3], 
      [-1, 4, 5], 
      [3, 7, 1],
   ]
   >>> _matrix2 = [
      [4, 3, -9],
      [3, -8, -1], 
      [4, -1, -7], 
   ]
   >>> result = cross_div(_matrix1, _matrix1, digits=4)
   >>> print(result)
   [[1.0, -1.1, 4.44], [0.0, 0.99, 0.0], [2.77, -1.1, 1.0]]
    
   """
   if not dim(matrix1) == dim(matrix2):
      raise DimensionError("given matrices is not suitable")

   if not isinvertible(matrix2):
      raise InvertibleMatrixError("'matrix2' argument must be invertible")
   # cross division is simply being found by taking inverse of second
   # matrix and then multiplication of these matrices will be enough. 
   matrix2 = inverse(matrix2, digits)
   _div = cross_mul(matrix1, matrix2, digits)

   return _div

def solve(matrix, digits=18):
   """Returns solution of given linear equation and given matrix must 
   be `augmented` form. Augmented form stands for matrices that have both
   coefficient and constant terms. In other words, number of column must
   be more one than number of row. An linear algebratic system has three
   diffenrent solution:

   + `Consistent` that returns solution of linear equation (Example 1), 
   + `Inconsistent` that returns `None` (Example 2), 
   + `Infinite` that returns `None`.

   ## Example 1
   >>> _matrix = [
      [1, -2, 3, 9], 
      [-1, 3, 0, -4], 
      [2, -5, 5, 17],
   ]
   >>> result = solve(_matrix)
   >>> print(result)
   [[1.0], [-1.0], [2.0]]

   ## Example 2
   >>> _matrix = [
      [1, -3, 1, 1], 
      [2, -1, -2, 2], 
      [1, 2, -3, -1],
   ]
   >>> result = solve(_matrix)
   >>> print(result)
   None
    
   """
   _row, _matrix, _target = [], [], []
   # Firstly, we have to seperate given linear equation into two parts.
   # One is coefficients matrix to '_matrix', other is constants matrix
   # to '_target'.
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
    
   if not dim(matrix)[1] - dim(matrix)[0] == 1:
      raise DimensionError("given matrix is not suitable")
   # We are creating '_matrix' arguments containing just coefficients.
   for i in range(len(matrix)):
      for j in range(len(matrix[0])-1):
         _row.append(matrix[i][j])
         if len(_row) == dim(matrix)[1] - 1:
            _matrix.append(list(_row))
            _row = []
   # And then, we are doing same thing to '_target'.  
   for i in range(len(matrix)):
      _target.append([matrix[i][-1]])
   # Don't forget! our coefficients matrix must ve invertible.
   if not isinvertible(_matrix): return None
   # If our coefficients matrix is invertible and then we can solve
   # the linear system rapidly.
   _matrix = inverse(_matrix, digits=digits)
   _solve = cross_mul(_matrix, _target, digits=digits)
    
   return _solve
   