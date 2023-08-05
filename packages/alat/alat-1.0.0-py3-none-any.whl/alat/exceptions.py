# Exceptions for ALAT (Advanced Linear Algebra Toolkit).

__all__ = [
   "MatrixError", 
   "SquareMatrixError", 
   "DimensionError", 
   "InvertibleMatrixError", 
   "PointsError", 
   "InconsistentCharacterError", 
   "VectorsError", 
   "VectorsCountError", 
   "ZeroVectorsError"
]

class MatrixError(Exception):
   """Raises error if matrix has incomplete value or etc."""

class SquareMatrixError(Exception):
   """Raises error if matrix is not square while calculating
   determinant."""

class DimensionError(Exception):
   """Raises error if matrix has missing or extra value."""

class InvertibleMatrixError(Exception):
   """Raises error if matrix is not invertible."""
    
class PointsError(Exception):
   """Raises error if count of given x and y axis points are not equal."""
    
class InconsistentCharacterError(Exception):
   """Raises error if message contains inconsistent character."""
    
class VectorsError(Exception):
   """Raises error if given vectors is not suitable."""
    
class VectorsCountError(Exception):
   """Raises error if count of given vectors is not suitable."""
    
class ZeroVectorsError(Exception):
   """Rasies error if given vectors are zero."""