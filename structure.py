from typing import Any

class Simplex:
    def __init__(self, apparition_time: float, dimension: int, under_vertices: list[Any]):
        self.apparition_time = apparition_time
        self.dimension = dimension
        self.under_vertices = under_vertices

    def __lt__(self, other):
        if self.apparition_time < other.apparition_time:
            return True
        elif self.apparition_time == other.apparition_time and self.dimension < other.dimension:
            return True
        elif self.apparition_time == other.apparition_time and self.dimension == other.dimension:
            return "".join(self.under_vertices) < "".join(other.under_vertices)

    def __eq__(self, other):
        return self.apparition_time == other.apparition_time and self.dimension == other.dimension and self.under_vertices == other.under_vertices
    
    def __repr__(self):
        return f"f(sigma) = {self.apparition_time}, dim = {self.dimension}, sigma = ({self.under_vertices})"


class Simplex_set:
    def __init__(self, simplexes: list[Simplex]):
        self.simplexes = sorted(simplexes) 
        self.matrix = self.get_matrix()

    def compute_bars(self):
        self.matrix.make_echelon_form()
        bars = self.matrix.bars()           # list of (indexA, indexB) tuples

        converted_bars = []

        for indexA, indexB in bars:
            dimA = self.simplexes[indexA].dimension
            fA = self.simplexes[indexA].apparition_time
            fB = self.simplexes[indexB].apparition_time if indexB != float('inf') else float('inf')

            converted_bars.append((dimA, fA, fB))

        return converted_bars


    def get_matrix(self):
        vertex_to_index = {}
        
        for index, simplex in enumerate(self.simplexes):
            vertex_to_index[tuple(simplex.under_vertices)] = index

        columns = []
        for simplex in (self.simplexes):
            col_values = set()
            col_max = -1

            for index_vert in range(len(simplex.under_vertices)):
                face = tuple(simplex.under_vertices[:index_vert] + simplex.under_vertices[index_vert+1:])

                if face in vertex_to_index:
                    col_values.add( vertex_to_index[face] )
                    col_max = max(col_max, vertex_to_index[face])
            
            columns.append(Column(values=col_values, pmax=col_max))

        return Matrix(columns)

class Column:
    def __init__(self, values: set[int] = set(), pmax: int = -1):
        self.__values = values
        self.__max = pmax if pmax != -1 else (max(values) if values else -1)

    def __eq__(self, other):
        return self.__values == other.get_values()
    
    def __repr__(self):
        return f"{str(self.__values)}, max = {self.__max}"
    
    def __xor__(self, other):
        if not isinstance(other, Column):
            raise Exception (f"{other.__name__()} must be of type Column but is of type {type(other)}")
        
        values = self.__values ^ other.get_values()

        pmax = None  # we start with an unknown max state
        other_max = other.get_max(allow_unknown=True)
        if self.__max is not None and other_max is not None:  # both values have a known max
            if self.__max != other_max:  # if the maxes are distinct we can infer a new max value.
                pmax = max(self.__max, other_max)

        return Column(values=values, pmax=pmax)
    
    def __ixor__(self, other):
        self.__values ^= other.get_values()

        self.__max = None
        # we put max on None to signify it is unknown. We could check for an efficient method
        # if the maxes of the columns do not collide, but that is never the case in our algorithm
        return self

    
    def __len__(self):
        return len(self.__values)
    
    def __contains__(self, a):
        return a in self.__values

    def set_values(self, values: set[int], pmax: int = -1):
        self.__values = values
        self.__max = pmax if pmax != -1 else (max(values) if values else -1)

    def get_values(self):
        return self.__values

    def get_max(self, allow_unknown: bool = False):
        if not allow_unknown and self.__max is None:
            # if we have an unknown max value we must compute it here
            self.__max = max(self.__values) if self.__values else -1
        
        return self.__max
    

class Matrix:
    def __init__(self, columns: list[Column] = []):
        self.columns = None
        self.size = None
        self.zero_columns = None
        self.pivots = None

        if columns:
            self.set_columns(columns=columns)

    def set_columns(self, columns: list[Column]):
        self.columns = columns
        self.size = len(columns) if columns else None

    def __index__(self, coord: tuple[int, int]):     # coord: (i, j)
        if not isinstance(coord, tuple):
            raise Exception("wrong type")
        
        if coord[1] < 0 or coord[1] >= self.size or coord[0] < 0 or coord[0] > self.size:
            # we assume a square matrix
            raise Exception("Index out of range")
        
        return int(coord[0] in self.columns[coord[1]])

    def __repr__(self):
        return_string = ""

        for i in range(len(self.columns)):
            return_string = ''.join(([return_string] + [str(self.__index__((i, j))) for j in range(len(self.columns))] + ['\n']))

        return return_string

    def add_column(self, c1: Column, c2: Column):
        # returns the XOR of two columns, adding them element-wise mod 2
        return c1 ^ c2
    
    def get_lower1(self, c: Column):
        # returns the row index of the 1 with the lowest position in the matrix, given a column c.
        # If the column is empty return -1
        return c.get_max()

    def make_echelon_form(self):
        """
        Transform the matrix into echelon form using Gaussian elimination.
        """

        self.zero_columns = set()  # set of indexes of zero-columns
        self.pivots = {}           # dict[index : column with pivot on index]

        for j in range(self.size):
            column = self.columns[j]
            lower1 = self.get_lower1(column)

            while True:
                # current column is empty
                if lower1 == -1:
                    self.zero_columns.add(j)
                    self.columns[j] = column
                    break

                # there exists a column to the left with a "pivot collision"
                elif lower1 in self.pivots:
                    column ^= self.columns[self.pivots[lower1]]
                    lower1 = self.get_lower1(column)                # update the stored lowest 1 for this column
                
                # current column has a pivot element with no collisions to the left
                else:
                    self.pivots[lower1] = j     # register current column as holder of pivot on index lower1 
                    self.columns[j] = column
                    break


    def bars(self):
        """Method to compute the bars of the matrix, independent of the simplex to index bijection"""
        bars = []
        for cycle in self.zero_columns:
            if cycle in self.pivots:
                bars.append((cycle, self.pivots[cycle]))
            else:
                bars.append((cycle, float('inf')))

        return bars
