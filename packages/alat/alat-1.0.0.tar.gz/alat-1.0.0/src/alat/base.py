# Base functions for ALAT (Advanced Linear Algebra Toolkit)

import math
import random as _random

from .exceptions import (
MatrixError, 
SquareMatrixError,
DimensionError,
)

__all__ = [
   "ismatrix", "set_digits", "dim", "issquare", "diagonal", "iszero", 
   "ishomogen", "isones", "isidentity", "zeros", "ones", "identity",
   "arbitrary", "sequential", "random", "isequal", "highest", "lowest", 
   "aggregate", "iselementary", "mean", "sort", "stdev", "mode", 
   "median", "mix", "redim", "addition", "scaler_mul", "subtraction", 
   "dot_mul", "transpose", "remove", "concat", "islt", "isut",
   "cross_mul", "istriangular", "scaler_div", "dot_div"
]

def ismatrix(matrix):
   """Returns True, if given object is matrix."""
   # 'ismatrix' is much important function. Each functions after 
   # that are based on this. A matrix must be like that:
   _all_values, _right_values, _all_rows, _right_rows = [],[],[],[]
   # 1. matrix must be list.
   if isinstance(matrix, list):
      for row in matrix:
         # 2. each row of matrix must be list.
         if isinstance(row, list):
               for value in row:
                  _all_values.append(value)
                  # 3. each value of matrix must be int, float,
                  # True means one or False means zero.
                  if isinstance(value, (int, float)):
                     _right_values.append(value)
         _all_rows.append(row)
         if isinstance(row, list):
               _right_rows.append(row)
      # 4. and lastly, each row of matrix must be same length.
      if len(_right_rows) == len(_all_rows):
         _status = len(_right_values) / len(matrix)
         if str(_status)[-1] == "0": 
               return True

   return False

def set_digits(value, digits):
   """Sets digits of result. For example:
   
   >>> result = set_digits(-4.10721508, 4)
   >>> print(result)
   -4.107
   
   """
   # This list just contains things that are not number 
   _not_int = []
   if not isinstance(value, (int, float)):
      raise TypeError("'value' argument must be int or float")            
   
   if not isinstance(digits, int):
      raise TypeError("'digits' argument must be int")
   
   for digit in str(value):
      if digit in ("-", "+", "."):
         _not_int.append(digit)
         
   return float(str(value)[:digits + len(_not_int)])
   
def dim(matrix):
   """Returns dimension of given matrix. For example:
   
   >>> _matrix = [
      [4, 7, 3], 
      [0, 1, 9],
   ]
   >>> result = dim(_matrix)
   >>> print(result)
   (2, 3)
   
   """
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
   
   # (row, column)
   return (len(matrix), len(matrix[0])) 

def issquare(matrix):
   """Returns True, if given matrix is square."""
   if ismatrix(matrix) and dim(matrix)[0] == dim(matrix)[1]:
         return True
      
   return False

def diagonal(matrix):
   """Returns main diagonal of given matrix. For example:
   
   >>> _matrix = [
      [4, 3, 0], 
      [1, 5, 7], 
      [0, 3, 8],
   ] 
   >>> result = diagonal(_matrix)
   >>> print(result)
   [[4.0, 5.0,  8.0]]
   
   """
   # Main diagonal can be useful under some problems. For 
   # examples, in calculating determinant or determines 
   # elementary matrix.
   if not issquare(matrix):
      raise SquareMatrixError("given matrix must be square")
   
   return [[float(matrix[i][i]) for i in range(dim(matrix)[0])]]

def ishomogen(matrix):
   """Returns True, if given matrix is homogeneous."""
   # Homogeneous matrix contains zero in each last value of row.
   if ismatrix(matrix):
      _homo = [1 for i in range(len(matrix)) if matrix[i][-1]==0]

      if len(_homo) == len(matrix): 
         return True

   return False

def iszero(matrix):
   """Returns True, if given matrix is zeros."""
   # Zero matrix just contains zero number.
   if ismatrix(matrix):
      _all_values = [value for row in matrix for value in row]
      _right_values = [0 for value in _all_values if value==0]

      if len(_all_values) == len(_right_values): 
         return True

   return False  

def isones(matrix):
   """Returns True, if given matrix is ones."""
   # One matrix just contains one number.
   if ismatrix(matrix):
      _all_values = [value for row in matrix for value in row]
      _right_values = [1 for value in _all_values if value==1]

      if len(_all_values) == len(_right_values): 
         return True

   return False  

def isidentity(matrix):
   """Returns True, if given matrix is identity."""
   # Identity matrix is special matrix. It contains
   # zeros and ones number and just main diagonal of
   # identity matrix contains ones.
   if issquare(matrix):
      _values = [value for row in matrix for value in row]
      _ones = [1 for i in range(len(matrix)) for j in \
         range(len(matrix[0])) if matrix[i][j] == 1]
      _zeros = [0 for i in range(len(matrix)) for j in \
         range(len(matrix[0])) if matrix[i][j] == 0]

      if len(_values) == len(_ones) + len(_zeros) and \
         [_ones] == diagonal(matrix): return True

   return False

def zeros(dim):
   """Returns zeros matrix. For example:
   
   >>> result = zeros(dim=(3, 3))
   >>> print(result)
   [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
   
   """
   # Generates new matrix just contains zero numbers.
   if not isinstance(dim, tuple):
      raise TypeError("'dim' argument must be tuple")

   _row = [float(0) for x in range(dim[1])]
   _matrix = [list(_row) for x in range(dim[0])]
   
   return _matrix

def ones(dim):
   """Returns ones matrix. For example:
   
   >>> result = ones(dim=(3, 3))
   >>> print(result)
   [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]
   
   """
   # Generates new matrix just containing one numbers.
   if not isinstance(dim, tuple):
      raise TypeError("'dim' argument must be tuple")

   _row = [float(1) for x in range(dim[1])]
   _matrix = [list(_row) for x in range(dim[0])]
   
   return _matrix

def identity(dim):
   """Returns identity matrix. For example:
   
   >>> result = identity(dim=(3, 3))
   >>> print(result)
   [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
   
   """
   # Generates identity matrix.
   _matrix = zeros(dim)
   if not len(_matrix) == len(_matrix[0]):
      raise SquareMatrixError("given matrix must be square")
   
   for i in range(len(_matrix)):
      _matrix[i][i] = float(1)
   
   return _matrix

def arbitrary(dim, value):
   """Returns an arbitrary matrix. For Example:
   
   >>> result = arbitrary(dim=(3, 3), value=4)
   >>> print(result)
   [[4.0, 4.0, 4.0], [4.0, 4.0, 4.0], [4.0, 4.0, 4.0]]
   
   """
   # Generates an matrix just contaning 'value' argument.
   if not isinstance(dim, tuple):
      raise TypeError("'dim' argument must be tuple")
   if not isinstance(value, (int, float)):
      raise TypeError("'value' argument must be int or float")

   _row = [float(value) for x in range(dim[1])]
   _matrix = [list(_row) for x in range(dim[0])]

   return _matrix


def sequential(dim, interval, step=1):
   """Returns a sequential matrix. `interval` argument represents 
   interval and must be tuple. `step` argument represents step and 
   must be int. For example:
   
   ## Example 1
   >>> result = sequential(dim=(2, 4), interval=(5, 50), step=5)
   >>> print(result)
   [
      [5.0, 10.0, 15.0, 20.0], 
      [25.0, 30.0, 35.0, 40.0],
   ]
   
   ## Example 2
   >>> result = sequential(dim=(4, 2), interval=(8, 1), step=-1)
   >>> print(result)
   [
      [8.0, 7.0, 6.0, 5.0], 
      [4.0, 3.0, 2.0, 1.0],
   ]
   
   ## Example 3
   >>> result = sequential(dim=(1, 10), interval=(5, -4), step=-1)
   >>> print(result)
   [[5.0, 4.0, 3.0, 2.0, 1.0, 0.0, -1.0, -2.0, -3.0, -4.0]]
   
   """
   _sequential, _row, _matrix = [], [], []
   if not (isinstance(dim, tuple) and isinstance(interval, tuple)):
      raise TypeError("'dim' or 'interval' agument must be tuple")
   
   if not len(interval) == 2:
      raise AttributeError("'interval' argument must contains "
                           "just start and stop points")
   # Can be some unusual sitiutions. It can cause infinite loops. 
   # For this, these conditions must be considered.
   _interval1, _interval2, _step = interval[0], interval[1], step
   if (_interval1 < _interval2 and not _step == abs(_step)) and \
      (_interval1 > _interval2 and _step == abs(_step)) and \
      (_interval1 == _interval2): return []
   # In here, we are generating values and then appending into 
   # '_sequential'.
   while True:
      _sequential.append(_interval1 + _step)
      _interval1 += _step
      if _step == abs(_step):
         if _interval1 >= _interval2: break
      else:
         if _interval1 <= _interval2: break
   # Right now, we have to shape our '_sequential' list 
   # according to given 'dim' argument.
   _row.append(float(interval[0]))
   for i in _sequential:
      _row.append(float(i))
      if len(_row) == dim[1]:
         _matrix.append(list(_row))
         _row = []
         if len(_matrix) == dim[0]:
               break
      
   return _matrix

def random(dim, method="random", interval=None, digits=18):
   """Returns a random matrix. `method` argument can take three objects.
   These are `'random'`, `'uniform'`, `'randint'`. `interval` argument
   represents interval for `'uniform'` and `'randint'` objects. For
   example:
   
   ## Example 1
   >>> result = random(dim=(3, 3), method="random", interval=None 
   digits=3)
   >>> print(result)
   [[0.12, 0.35, 0.41], [0.26, 0.41, 0.78], [0.45, 0.39, 0.73]]
   
   ## Example 2
   >>> result = random(dim=(3, 3), method="uniform", interval=(1, 5),
   digits=3)
   >>> print(result)
   [[4.87, 1.25, 3.05], [3.63, 2.45, 2.19], [1.92, 1.74, 4.39]]
   
   ## Example 3
   >>> result = random(dim=(3, 3), method="randint", interval=(-5, 5))
   >>> print(result)
   [[-4.0, 0.0, 1.0], [1.0, 4.0, 4.0], [-3.0, 2.0, 0.0]]
   
   """
   # Initial matrix and then its value will be changed
   _matrix = zeros(dim)
   if not isinstance(dim, tuple):
      raise TypeError("'dim' argument must be tuple")
   
   if not method in ("random", "uniform", "randint"):
      raise AttributeError("'method' argument must be 'random' "
                              ", 'uniform' or 'randint'")
   # In here, values of our initial matrix are being changed
   # by 'method' argument.
   # 'random' keyword generates numbers between zero and one floats.
   if method == "random" and interval is None:
      for i in range(len(_matrix)):
         for j in range(len(_matrix[0])):
               _matrix[i][j] = set_digits(_random.random(), digits)
   # 'uniform' keyword expects an interval and generates float numbers
   # according to interval argument
   elif method == "uniform" and interval is not None:
      a, b = interval
      for i in range(len(_matrix)):
         for j in range(len(_matrix[0])):
               _matrix[i][j] = set_digits(_random.uniform(a, b), digits)
   # 'randint' keyword expects an interval and generates integer numbers.
   elif method == "randint" and interval is not None:
      a, b = interval
      for i in range(len(_matrix)):
         for j in range(len(_matrix[0])):
               _matrix[i][j] = float(_random.randint(a, b))
   else:
      raise AttributeError("given attributes are inconsistent")
   
   return _matrix

def isequal(*matrices):
   """Returns True, if given matrices are equal to each other."""
   _all_matrices, _isequal = [], []
   for matrix in matrices:
      # If given objects matrix and then appends them into
      # '_all_matrices'.
      if ismatrix(matrix):
         _all_matrices.append(matrix)
   # Checks each rows with next matrix. If it's True, and appends 
   # into '_isequal'.
   for i in range(len(_all_matrices)):
      if _all_matrices[0] == _all_matrices[i]:
         _isequal.append(1)
   if [_isequal] == ones((1, len(_all_matrices))):
      return True
   
   return False

def highest(matrix):
   """Returns the highest value in given matrix. For example: 
   
   >>> _matrix = [
      [4, 7, 3], 
      [0, 7, 9], 
      [3, 6, 7], 
   ]
   >>> result = highest(_matrix)
   >>> print(result)
   9.0
   
   """
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
   # Each value of matrix are assigned into '_values'. 
   # And then selects the biggest value.   
   _values = [value for row in matrix for value in row]

   return float(max(_values))

def lowest(matrix):
   """Returns the lowest value in given matrix. For example:
   
   >>> _matrix = [
      [4, 7, 3], 
      [0, 7, 9],
      [3, 6, 7], 
   ]
   >>> result = lowest(_matrix)
   >>> print(result)
   0.0
   
   """
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
   # Each value of matrix are assigned into '_values'. 
   # And then selects the lowest value.   
   _values = [value for row in matrix for value in row]

   return float(min(_values))

def aggregate(matrix, axis=0):
   """Returns aggregated matrix due to axis. For example:
   
   >>> _matrix = [
      [4, 7, 1], 
      [3, 1, 5], 
      [0, 8, 9], 
   ]
   
   ## Example 1:
   >>> result = aggregate(_matrix, axis=0)
   >>> print(result)
   [[7.0, 16.0, 15.0]]
   
   ## Example 2:
   >>> result = aggregate(_matrix, axis=1)
   >>> print(result)
   [[12.0], [9.0], [17.0]]
   
   """
   # Adds up rows or columns with each other according to 'axis'.
   _matrix, _total = [], 0
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
   
   if not axis in (0, 1):
      raise AttributeError("'axis' argument must be 0 or 1")
   
   # 0 (zero) represents horizontal axis.
   if axis == 0:
      for i in range(len(matrix[0])):
         for row in matrix:
               _total += row[i]
         _matrix.append(float(_total))
         _total = 0
      _matrix = [_matrix]
   # 1 (one) represents vertical axis.
   if axis == 1:
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
               _total += matrix[i][j]
         _matrix.append([float(_total)])
         _total = 0
   
   return _matrix

def iselementary(matrix):
   """Returns True, if given matrix is elementary."""
   # Elementary matrix means identity matrix that was changed by one
   #  operations.
   _is_different = []
   if ismatrix(matrix) and issquare(matrix):
      _identity = identity(dim = dim(matrix))
      # In here, this code block assigns values that are different from
      #  identity matrix.
      for i in range(len(matrix)):
         for j in range(len(matrix[0])):
               if not matrix[i][j] == _identity[i][j]:
                  _is_different.append(matrix[i][j])
      # If that operation that was mentioned above is not 
      # multiplication operation (*) with zero.
      if len(_is_different) == 1 and _is_different[0] != 0:
         return True
      # If just row places of matrix was changed with each other.
      if ones((1, len(matrix))) == aggregate(matrix, axis=0):
         return True
      
   return False

def mean(matrix, digits=18):
   """Returns mean of given matrix. For example:
   
   >>> _matrix = [
      [4, -2, 0], 
      [7, 6, -1],
      [-9, 0, 4], 
   ]
   >>> result = mean(_matrix, digits=6)
   >>> print(result)
   1.0
   
   """
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
   # total of all values of matrix
   _sum = sum([value for row in matrix for value in row])

   return set_digits(_sum/(len(matrix) * len(matrix[0])), digits)

def sort(matrix, reverse=False):
   """Sorts matrix. `reverse` argument represents whether 
   values of matrix will be increased and must be bool. 
   For example:
   
   >>> _matrix = [
      [8, -2], 
      [0, -5]
   ]
   >>> result = sort(_matrix, reverse=True)
   >>> print(result)
   [
      [8, 0],
      [-2, -5],
   ]
   """
   _row, _matrix = [], []
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
   # Each value are assigned into '_sorted'.
   _sorted = [matrix[i][j] for i in range(len(matrix)) \
      for j in range(len(matrix[0]))]
   # And its sorting type (increasing or decreasing)
   # is determined according to 'reverse' argument.
   _sorted.sort(reverse=reverse)
   # Lastly, new matrix is created.
   for i in _sorted:
      _row.append(i)
      if len(_row) == len(matrix[0]):
         _matrix.append(_row)
         _row = []
         
   return _matrix
      
def stdev(matrix, digits=18):
   """Returns standard deviation of given matrix. For example:
   
   >>> _matrix = [[85, 86, 100, 76, 81, 93, 84, 99, 71, 69, 93, 
   85, 81, 87, 89]]
   >>> print(stdev(_matrix, 4))
   8.698

   """
   _pow = 0
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
   # Calculates mean of given matrix.
   _mean = mean(matrix, digits)
   for i in range(len(matrix)):
      for j in range(len(matrix[0])):
         # And each value is subtract from mean and added to '_pow'.
         _pow += math.pow(abs(_mean - matrix[i][j]), 2)
   # Lastly, '_pow' is divided count of values.
   _stdev = math.sqrt(_pow/(dim(matrix)[0]*dim(matrix)[1]))
   
   return set_digits(_stdev, digits)

def mode(matrix):
   """Returns mode or modes of given matrix. For example:
   
   ## Example 1
   >>> _matrix = [
      [4, 7, 0, -2], 
      [-2, -5, 7, 3],
   ]
   >>> result = mode(_matrix)
   >>> print(result)
   [-2, 7]
   
   ## Example 2 
   >>> _matrix = [
      [4, 0], 
      [-3, 5],
   ]
   >>> result = mode(_matrix)
   >>> print(result)
   None
   
   """
   _modes = []
   # Mode means value/s that repeated the most
   _array = [value for row in matrix for value in row]
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
   # Sometimes, any value of matrix doesn't repeat, In 
   # this case, we return None
   if len(_array) == len(list(set(_array))):
      return None
   # We use dict data type, because we want to find values
   # and its corresponding count.
   _dict = {value: _array.count(value) for value in _array}
   # And then we determine value/s that was repeated mostly 
   # and put in it '_mode'.
   for key, value in _dict.items():
      if _dict[key] == max(_dict.values()):
         _modes.append(key)

   return _modes[0] if len(_modes) == 1 else _modes

def median(matrix):
   """Returns median of given matrix. For example:
   
   >>> _matrix = [
      [7, 2, 6], 
      [-3, -5, 0]
   ]
   >>> result = median(_matrix)
   >>> print(result)
   1.0

   """
   if not ismatrix(matrix):
      raise MatrixError('inconsistent matrix')
   # All values of matrix are assigned to '_median'
   _median = [value for row in matrix for value in row]
   _median.sort()

   if len(_median)%2 == 1:
      return float(_median[round(len(_median)/2)-1])
   else:
      _first,_second = int(len(_median)/2),int(len(_median)/2+1)
      return (_median[_first-1] + _median[_second-1])/2

def mix(matrix):
   """Mixes given matrix. For example:
   
   >>> _matrix = [
      [6, 4, 0], 
      [-2, -2, 7], 
      [0, -1, 0]
   ]
   >>> result = mix(_matrix)
   >>> print(result)
   [
      [-2, 0, -1],
      [-2, 7, 0], 
      [6, 0, 4],
   ]
   
   """
   _row, _matrix = [], []
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
   # This code block appends all values into '_mix'
   _mix = [matrix[i][j] for i in range(len(matrix)) \
      for j in range(len(matrix[0]))]
   _random.shuffle(_mix)
   # Lastly, new matrix is generated.
   for i in _mix:
      _row.append(i)
      if len(_row) == len(matrix[0]):
         _matrix.append(list(_row))
         _row = []
         
   return _matrix

def redim(matrix, dim):
   """Reshapes given matrix. For example:
   
   >>> _matrix = [
      [4, -2, 0, 1], 
      [-9, 8, 7, -3], 
      [2, 7, -5, 7],
   ]
   >>> result = redim(_matrix, (6, 2))
   >>> print(result)
   [
      [4, -2], 
      [0, 1], 
      [-9, 8], 
      [7, -3], 
      [2, 7], 
      [-5, 7],
   ]
   """
   _row, _matrix = [], []
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
   
   if not isinstance(dim, tuple):
      raise TypeError("'dim' agument must be tuple")
   # All values of matrix are assigned into '_all_values'.
   _values = [matrix[i][j] for i in range(len(matrix)) \
      for j in range(len(matrix[0]))]
   # An error can occur related with dimension invalidness.
   if not (len(matrix)*len(matrix[0]) == dim[0] * dim[1]):
      raise DimensionError("given 'dim' is not suitable") 
   # This code block generates new matrix according to 'dim'.
   for value in _values:
      _row.append(value)
      if len(_row) == dim[1]:
         _matrix.append(list(_row))
         _row = []
         
   return _matrix

def addition(*matrices, digits=18):
   """Adds up matrices. For example:
   
   >>> _matrix1 = [
      [1, 7],
      [9, 8],
   ]
   >>> _matrix2 = [
      [9, 8], 
      [6, 1], 
   ]
   >>> _matrix3 = [
      [3, 8], 
      [0, 7]
   ]
   >>> result = addition(_matrix1, _matrix2, _matrix3)
   >>> print(result)
   [[13.0, 23.0], [15.0, 16.0]]

   """
   # Adds up so many matrices with each other.
   _matrix, _row = [],[]
   _matrices, _dims = [], []
   for matrix in matrices:
      if not ismatrix(matrix):
         raise MatrixError("inconsistent matrix")
      # Appends matrix and dimemsion of it to lists.
      _matrices.append(matrix)
      _dims.append((len(matrix), len(matrix[0])))
   # Checks all matrices have same dimesion.  
   for i in range(len(_matrices)):
      if not _dims[0] == _dims[i]:
         raise DimensionError("given matrices must be same dim")
   # Lastly, this code block are gonna add up all matrices and
   # returns new matrix.
   for i in range(len(_matrices[0])):
      for matrix in _matrices:
         _row.append(matrix[i])
      _matrix.append(_row)
      _row = []
   _addition = []
   for matrix in _matrix:
      agg = aggregate(matrix, axis=0)
      for row in agg:
         _addition.append(row)
   for row in _addition:
      for i in range(len(_addition[0])):
         row[i] = set_digits(row[i], digits)
                  
   return _addition

def scaler_mul(scaler, matrix, digits=18):
   """Multiplies given scaler and matrix. For example:
   
   >>> _matrix = [
      [-4, 1], 
      [0, -3], 
      [-5, 2]
   ]
   >>> result = scaler_mul(2, _matrix, digits=6)
   >>> print(result)
   [[-8.0, 2.0], [0.0, -6.0], [-10.0, 4.0]]
   
   """
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
  # Previously, copies given matrix
   _matrix = matrix.copy()
   # And then, each value of matrix multiplies with 'scaler'
   for i in range(len(_matrix)):
      for j in range(len(_matrix[0])):
         _matrix[i][j] = _matrix[i][j] * scaler
         _matrix[i][j] = set_digits(_matrix[i][j], digits)

   return _matrix

def subtraction(matrix1, matrix2, digits=18):
   """Subtracts `matrix2` from `matrix1`. For example:
   
   >>> _matrix1 = [
      [4, -3], 
      [0, 0], 
   ]
   >>> _matrix2 = [
      [5, 0], 
      [-6, 8]
   ]
   >>> result = subtraction(_matrix1, _matrix2)
   # It means: _matrix1 - _matrix2
   >>> print(result)
   [
      [-1, -3], 
      [6, -8]
   ]
   """
   if not ismatrix(matrix1) and not ismatrix(matrix2):
      raise MatrixError("inconsistent matrix")
   
   if not dim(matrix1) == dim(matrix2):
      raise DimensionError("given matrices must be same dimension")
   # We can easily subtract an matrix from another. For that, we 
   # are gonna multiply 'matrix2' with -1 scaler and then adds up 
   # with each other. 
   _matrix2 = scaler_mul(-1, matrix2, digits)
   _subtraction = addition(matrix1, _matrix2, digits=digits)
   
   return _subtraction

def dot_mul(matrix1, matrix2, digits=18):
   """Multiplies matrices as dot. For example:
   
   >>> _matrix1 = [
      [4, 7],
      [3, 5],
      [0, 8],
   ]
   >>> _matrix2 = [
      [-2, -3],
      [-4, -1],
      [-7, -1],
   ]
   >>> result = dot_mul(_matrix1, _matrix2, digits=6)
   >>> print(result)
   [[-8.0, -21.0], [-12.0, -5.0], [0.0, -8.0]]
   
   """
   _row, _matrix = [], []
   if not ismatrix(matrix1) and not ismatrix(matrix2):
      raise MatrixError("inconsistent matrix")
   
   if not isinstance(digits, int):
      raise TypeError("'digits' argument must be int")
   
   if not dim(matrix1) == dim(matrix2):
      raise DimensionError("given matrices are not suitable")
   # This code block multilpies each value with surrounding value of
   #  other matrix and generates new matrix.
   for i in range(len(matrix1)):
      for j in range(len(matrix2[0])):
         _value = matrix1[i][j] * matrix2[i][j]
         _row.append(set_digits(_value, digits))
         if len(_row) == len(matrix1[0]):
               _matrix.append(_row)
               _row = []
               
   return _matrix

def transpose(matrix):
   """Returns transpose of given matrix. For example:
   
   >>> _matrix = [
      [4, 3, 1], 
      [2, 5, 0],
   ]
   >>> result = transpose(_matrix)
   >>> print(result)
   [[4, 2], [3, 5], [1, 0]]                                        
   
   """
   _row, _matrix = [], []
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
   # Transpose is so much useful method in linear algebra.
   # Just changes replaces of row or columns.
   for j in range(len(matrix[0])):
      for i in range(len(matrix)):
         _row.append(matrix[i][j])
         if len(_row) == dim(matrix)[0]:
               _matrix.append(list(_row))
               _row = []
   
   return _matrix

def remove(matrix, place, axis):
   """Removes column or row of matrix. `place` argument means which
   column or row will be removed and must be int or tuple. `axis`
   argument must be `'0'` that means row or `'1'` means column. For
   example:
   
   ## Example 1
   >>> _matrix = [
      [0, 2, 1], 
      [3, -1, 2], 
      [4, 0, 1],
   ]
   >>> result = remove(matrix=_matrix, place=2, axis=1)
   >>> print(result)
   [
      [0, 2], 
      [3, -1], 
      [4, 0],
   ]
   
   ## Example 2
   >>> result = remove(matrix=_matrix, place=(0, 2), axis=0)
   >>> print(result)
   [[3, -1, 2]]
   
   """
   # Removes any row or column with this functions.
   _matrix = matrix.copy()
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
   
   if not isinstance(place, (tuple, int)):
      raise TypeError("'index' argument must be int or tuple")
   
   if not axis in (0, 1):
      raise AttributeError("'axis' argument must be zero or one")

   if isinstance(place, int):
      if axis == 0:
         del _matrix[place]
      else:
         _matrix = transpose(_matrix)
         del _matrix[place]
         _matrix = transpose(_matrix)
   else:
      _index = list(place)
      _index.reverse()
      if axis == 0:
         for i in _index:
               del _matrix[i]
      else:
         _matrix = transpose(_matrix)
         for i in _index:
               del _matrix[i]
         try:
               _matrix = transpose(_matrix)
         except ZeroDivisionError:
               _matrix = []
   
   return _matrix

def concat(matrix1, matrix2, axis=0):
   """Concats matrices with each other. For example:
   
   ## Example 1:
   >>> _matrix = [
      [4, -1, 0],
      [-2, 0, 3],
   ]
   >>> _matrix2 = [
      [7, -8, 5]
   ]
   >>> result = concat(_matrix, _matrix2, axis=0)
   >>> print(result)
   [
      [4, -1, 0],
      [-2, 0, 3],
      [7, -8, 5],
   ]
   
   ## Example 2:
   >>> _matrix3 = [
      [4, -7], 
      [3, -2],
   ]
   >>> _matrix4 = [
      [0], 
      [-5],
   ]
   >>> result = concat(_matrix3, _matrix4, axis=1)
   >>> print(result)
   [
      [4, -7, 0], 
      [3, -2, -5],
   ]
   """
   _new_matrix = matrix1.copy()
   if not ismatrix(matrix1) and ismatrix(matrix2):
      raise MatrixError("inconsistent matrix")
   
   if not axis in (0, 1):
      raise AttributeError("'axis' argument must be 0 or 1")
   # Concats two matrix one after the other with axis is 0
   if axis == 0:
      if not dim(matrix1)[1] == dim(matrix2)[1]:
         raise DimensionError("given dimension  of matrices "
                              "is not suitable")
      for row in matrix2:
         _new_matrix.append(list(row))
   # COncats two matrix side by side with axis is 1
   if axis == 1:
      if not dim(matrix1)[0] == dim(matrix2)[0]:
         raise DimensionError("given dimension of matrices "
                              "is not suitable")
      for i in range(len(_new_matrix)):
         _new_matrix[i] = _new_matrix[i] + matrix2[i]
         
   return _new_matrix

def islt(matrix):
   """Returns True, if given matrix is upper triangular."""
   _isupper = []
   if issquare(matrix):
      for i in range(dim(matrix)[0]-1):
         for value in matrix[i][i+1:]:
               _isupper.append(value)
      if [_isupper] == zeros(dim=(1, len(_isupper))):
         return True
      
   return False
      
def isut(matrix):
   """Returns True, if given matrix is lower triangular."""
   if issquare(matrix):
      _transpossed_triangular = transpose(matrix)
      if islt(_transpossed_triangular):
         return True
      
   return False

def istriangular(matrix):
   """Returns True, if given matrix upper or lower triangular."""
   if isut(matrix) or islt(matrix):
      return True
      
   return False
   
def cross_mul(matrix1, matrix2, digits=18):
   """Multiplies two given matrices as cross. For example:
   
   >>> _matrix1 = [
      [1, -2, 4], 
      [3, 0, -2],
   ]
   >>> _matrix2 = [
      [4, -7], 
      [-3, 0], 
      [-1, 1],
   ]
   >>> result = cross_mul(_matrix1, _matrix2, digits=6)
   >>> print(result)
   [[6.0, -3.0], [14.0, -23.0]]
   
   """
   # It multiplies two matrix with each other as cross.
   _row, _matrix, _total = [], [], 0
   if not ismatrix(matrix1) and not ismatrix(matrix2):
      raise MatrixError("inconsistent matrix")
   
   if not dim(matrix1)[1] == dim(matrix2)[0]:
      raise DimensionError("given matrices are not suitable")
   # For this, previously we should take transpose of 'matrix2' 
   matrix2, _index = transpose(matrix2), dim(matrix1)[1]
   # multiplies two matrix and generates new matrix.
   for i in range(len(matrix1)):
      for j in range(len(matrix2)):
         for k in range(len(matrix2[0])):
               _value = matrix1[i][k] * matrix2[j][k]
               _total += _value
               _index -= 1
               if _index == 0:
                  _row.append(set_digits(_total, digits))
                  _total = 0
                  _index = dim(matrix1)[1]
                  if len(_row) == dim(matrix2)[0]:
                     _matrix.append(list(_row))
                     _row = []
   return _matrix
   
def scaler_div(scaler, matrix, scaler_status="up", digits=18):
   """Divides a scaler to given matrix. `scaler_satus` indicates
   whether scaler divides given matrix or otherwise `scaler_status` 
   can take only 'up' or 'down' object. For example:
   
   >>> _matrix = [
      [3, 12, 9], 
      [6, 15, 0], 
      [0, 27, 1],
   ]
   >>> result = scaler_div(3, _matrix, "up", digits=4)
   >>> print(result)
   [[1.0, 0.25, 0.33], [0.5, 0.2, 'Undefined'], ['Undefined', 0.
   11, 3.0]]
   
   """
   _row, _matrix = [], []
   if not ismatrix(matrix):
      raise MatrixError("inconsistent matrix")
   
   if not scaler_status in ("up", "down"):
      raise AttributeError("'scaler_status' argument must be 'up'"
                           "or 'down' object")
   for row in matrix:
      for value in row:
         # In here, ZeroDivisionError accurs, for pass it
         # we define "Undefined"
         if value == 0 and scaler_status == "up":
            _value = "Undefined"
         else:
            if scaler_status == "up":
               _value = set_digits(scaler/value, digits)
            if scaler_status == "down":
               _value = set_digits(value/scaler, digits)
         # After we did scaler division and then generates 
         # new matrix.
         _row.append(_value)
         if len(_row) == dim(matrix)[1]:
               _matrix.append(_row)
               _row = []

   return _matrix

def dot_div(matrix1, matrix2, digits=18):
   """Divides given matrices with each other as dot. For example:
   
   >>> _matrix1 = [
      [-4, 0], 
      [6, -1], 
      [-5, 3]
   ]
   >>> _matrix2 = [
      [2, 1], 
      [0, 9], 
      [8, 7]
   ]
   >>> result = dot_div(_matrix1, _matrix2, digits=4)
   >>> print(result)
   [[-2.0, 0.0], ['Undefined', -0.1], [-0.6, 0.42]]
   
   """
   if not ismatrix(matrix1) and not ismatrix(matrix2):
      raise MatrixError("inconsistent matrix")
   
   if not dim(matrix1) == dim(matrix2):
      raise DimensionError("given matrices is not sutible")
   # For doing dot division, we needs to divide 'matrix2' to
   # scaler 1.
   matrix2 = scaler_div(1, matrix2, "up", digits=digits)
   # Under some consitions, as mentioned above, 'matrix2' can
   # contain "Undefined" value. To fix it, we divide two part.
   if ismatrix(matrix2):
      _matrix = dot_mul(matrix1, matrix2, digits=digits)
      for i in range(len(_matrix)):
         for j in range(len(_matrix[0])):
            _matrix[i][j] = set_digits(_matrix[i][j], digits)
   else:
      # If there is "Undefined" value into 'matrix2', we changes
      # "Undefined" value with 1.0 and records coordinates of it.
      _undefined_values = []
      for i in range(len(matrix2)):
         for j in range(len(matrix2[0])):
               if matrix2[i][j] == "Undefined":
                  matrix2[i][j] = 1.0
                  _undefined_values.append((i, j))
      # After dot division, we fix it.
      _matrix = dot_mul(matrix1, matrix2, digits=digits)
      for index in _undefined_values:
         i, j = index
         _matrix[i][j] = "Undefined"
   
   return _matrix
