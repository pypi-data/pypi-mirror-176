# Cryptography for ALAT (Advanced Linear Algebra Toolkit)

from .exceptions import (
   DimensionError, 
   InconsistentCharacterError, 
   InvertibleMatrixError,
)
from .base import cross_mul
from .base2 import (
   isinvertible, 
   inverse, 
)

__all__ = ["Crypt"]

numbers = {
   "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, 
   "8": 8, "9": 9, 
}

alphabets = {
   "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16,   
   "H": 17, "I": 18, "J": 19, "K": 20, "L": 21, "M": 22, "N": 23,   
   "O": 24, "P": 25, "Q": 26, "R": 27, "S": 28, "T": 29, "U": 30,   
   "V": 31, "W": 32, "X": 33, "Y": 34, "Z": 35, "a": 36, "b": 37, 
   "c": 38, "d": 39, "e": 40, "f": 41, "g": 42, "h": 43, "i": 44, 
   "j": 45, "k": 46, "l": 47, "m": 48, "n": 49, "o": 50, "p": 51, 
   "q": 52, "r": 53, "s": 54, "t": 55, "u": 56, "v": 57, "w": 58, 
   "x": 59, "y": 60, "z": 61, 
}

whitespaces = {
   "!": 62, "'": 63, "^": 64, "$": 65, "%": 66, "&": 67, "/": 68, 
   "(": 69, ")": 70, "{": 71, "}": 72, "[": 73, "]": 74, "=": 75, 
   "*": 76, "-": 77, "?": 78, "_": 79, "~": 80, ";": 81, ",": 82, 
   "`": 83, ".": 84, ":": 85, "<": 86, ">": 87, "|": 88, '"': 89,      
   "@": 90, "é": 91, " ": 92
}

class Crypt:
   """Cryptography for ALAT (Advanced Linear Algebra Toolkit)."""

   def to_matrix(self, msg, dim):
      """Converts message to matrix form.
      
      ## Parameters:
      `msg` argument represents message that will be converted to 
      matrix and must be str. `dim` argument represents dimension
      of matrix that will be created and must be tuple. For example:

      >>> _msg = "What's going on!"
      >>> print(len(_msg))
      9
      >>> result = Crypt().to_matrix(msg=_msg, dim=(4, 4))
      >>> print(result)
      [[32, 43, 36, 55], [63, 54, 92, 42], [50, 44, 49, 42], [92, 50,
       49, 62]]

      """
      _row, _matrix = [], []

      if not isinstance(msg, str):
         raise TypeError("'msg' argument must be str")
      if not isinstance(dim, tuple):
         raise TypeError("'dim' argument must be tuple")
      # Be carefull! Length of message is to appropriate width 
      # dimension of matrix that will be created.
      if not len(msg) == dim[0] * dim[1] and not len(dim) == 2:
         raise DimensionError("given 'dim' argument is not suitable")
      # Each characters of message must be in alphabets, numbers, 
      # or whitespaces.
      for char in msg:
         if char in numbers.keys():
            _row.append(numbers[char])
         elif char in alphabets.keys():
            _row.append(alphabets[char])
         elif char in whitespaces.keys():
            _row.append(whitespaces[char])
         else:
            error_msg = "Inconsistent character: '%s'" % char
            raise InconsistentCharacterError(error_msg)
         # And then generates main matrix from rows.
         if len(_row) == dim[1]:
            _matrix.append(list(_row))
            _row = []

      return _matrix

   def encode(self, msg, dim, encoding_matrix, digits=18):
      """Encodes raw matrix.
      
      ## Parameters:
      `msg` argument represents message that will be converted 
      to matrix and must be string. `dim` argument represents 
      dimension of matrix that will be created and must be tuple. 
      `encoding_matrix` argument represents matrix that will be
      encoded the message and must be invertible. For example:

      >>> _msg = "What's going on!"
      >>> print(len(_msg))
      9
      >>> _matrix = [
         [4, -1, -3, 1], 
         [-9, 4, 0, -9], 
         [3, 2, 4, -9],
         [8, 7, 0, 0]
      ]
      >>> result = Crypt().encode(msg=_msg, encoding_matrix=_matrix
      dim=(4, 4), digits=18)
      >>> print(result)
      [[289.0, 597.0, 48.0, -679.0], [378.0, 631.0, 179.0, -1251.0], 
      [287.0, 518.0, 46.0, -787.0], [561.0, 640.0, -80.0, -799.0]]

      """
      # 'encoding_matrix' must be invertible
      if not isinvertible(encoding_matrix):
         raise InvertibleMatrixError("given matrix must be invertible")
      # Firstly, converts message to a matrix.
      _to_matrix = self.to_matrix(msg, dim)
      _encode = cross_mul(_to_matrix, encoding_matrix, digits)

      return _encode

   def decode(self, encoded_matrix, decoding_matrix, digits=18):
      """Decodes encoded message.
      
      ## Parameters:
      `encoded_matrix` argument represents encoded matrix. 
      `decoding_matrix` represents matrix that will decode encoded 
      matrix and must be invertible. For example:

      >>> _msg = "What's going on!"
      >>> _matrix = [
         [4, -1, -3, 1], 
         [-9, 4, 0, -9], 
         [3, 2, 4, -9],
         [8, 7, 0, 0]
      ]
      >>> _encoded = Crypt().encode(msg=_msg, encoding_matrix=_matrix
      dim=(4, 4), digits=18)
      >>> print(_encoded)
      [[289.0, 597.0, 48.0, -679.0], [378.0, 631.0, 179.0, -1251.0], 
      [287.0, 518.0, 46.0, -787.0], [561.0, 640.0, -80.0, -799.0]]

      >>> result = Crypt().decode(_encoded, _matrix, digits=18)
      >>> print(result)
      [[32.0, 43.0, 36.0, 55.0], [63.0, 54.0, 92.0, 42.0], [50.0, 44.0,
      49.0, 42.0], [92.0, 50.0, 49.0, 62.0]]

      """
      if not isinvertible(decoding_matrix):
         raise InvertibleMatrixError("given matrix must be invertible")
      # Firstly, finds inverse of 'decoding_matrix'.
      _inverse = inverse(decoding_matrix, digits)
      # And then, multiplies encoded matrix with decoding matrix.
      _decode = cross_mul(encoded_matrix, _inverse, digits)
      # Finally, we round each value of matrix.
      for i in range(len(_decode)):
         for j in range(len(_decode[0])):
            _decode[i][j] = float(round(_decode[i][j]))

      return _decode

   def to_str(self, encoded_matrix, decoding_matrix, digits=18):
      """Converts encoded matrix to message.
      
      ## Parameters:
      `encoded_matrix` argument represents encoded matrix. 
      `decoding_matrix` argument represents decoding matrix that will
      decode encoded matrix and must be invertible. For example:

      >>> _msg = "What's going on!"
      >>> _matrix = [
         [4, -1, -3, 1], 
         [-9, 4, 0, -9], 
         [3, 2, 4, -9],
         [8, 7, 0, 0]
      ]
      >>> _encoded = Crypt().encode(msg=_msg, encoding_matrix=_matrix
      dim=(4, 4), digits=18)
      >>> print(_encoded)
      [[289.0, 597.0, 48.0, -679.0], [378.0, 631.0, 179.0, -1251.0], 
      [287.0, 518.0, 46.0, -787.0], [561.0, 640.0, -80.0, -799.0]]

      >>> result = Crypt().to_str(_encoded, _matrix, digits=18)
      >>> print(result)
      "What's going on!"

      """
      # Converts encoded matrix to string. For that, replaces keys and
      # values of numbers, alphabets, whitespaces.
      _alphabets, _numbers, _whitespaces = {}, {}, {}
      for key, value in numbers.items():
         _numbers[value] = key
      for key, value in alphabets.items():
         _alphabets[value] = key
      for key, value in whitespaces.items():
         _whitespaces[value] = key
      # And then, decodes encoded matrix.
      _decode = self.decode(encoded_matrix, decoding_matrix, digits)
      _string = ""
      # Lastly, concats characters.
      for row in _decode:
         for char in row:
            if char in _alphabets.keys():
               _string += _alphabets[char]
            elif char in _numbers.keys():
               _string += _numbers[char]
            else:
               _string += _whitespaces[char]

      return _string
