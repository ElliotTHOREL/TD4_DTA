

class Simplex_set:
    def __init__(self, simplexes):
        self.simplexes = sorted(simplexes) 
        self.matrix = self.get_matrix()

    def compute_bars(self):
        self.matrix.make_echelon_form()
        print("echelon form")
        print(self.matrix)
        bars = self.matrix.bars()  # list of (indexA, indexB) tuples --> (dim sigma_indexA, f(indexA), f(indexB))
        print(bars)

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
        for index_simp, simplex in enumerate(self.simplexes):
            column = 0

            for index_vert, vertex in enumerate(simplex.under_vertices):
                face = tuple(simplex.under_vertices[:index_vert] + simplex.under_vertices[index_vert+1:])

                if face in vertex_to_index.keys():
                    column ^= 2**vertex_to_index[face] 

            columns.append(column)

        return Matrix(columns)



class Simplex:
    def __init__(self, apparition_time, dimension, under_vertices):
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


class Matrix:
    def __init__(self, columns = []):
        self.columns = columns  # list of ints (dec repr of bitstring)
        self.size = len(columns)

    def __index__(self, coord):
        # coord = (i, j)

        if not isinstance(coord, tuple):
            raise Exception("wrong type")
        
        if coord[1] < 0 or coord[1] >= self.size or coord[0] < 0 or coord[0] > self.size:
            print(coord)
            raise Exception("Index out of range")
        
        return int(self.columns[coord[1]] & 2**coord[0] > 0)

    def __repr__(self):
        return_string = ""

        for i in range(len(self.columns)):
            return_string = ''.join(([return_string] + [str(self.__index__((i, j))) for j in range(len(self.columns))] + ['\n']))

        return return_string

    def make_echelon_form(self):
        """Method to transform the matrix into echelon form"""
        self.zero_columns = set()   # set of column indices that are zero-columns 
                                    # i.e. actual cycles
        self.low1 ={}   # map a row to the column that has its lowest 1 in it
                        # i.e. map a cycle to its death 


        for j in range(self.size):
            column = self.columns[j]
            while True:
                lower1 =column.bit_length()-1 # compute the row index of the lowest 1

                if lower1 ==-1: #zero-column
                    self.zero_columns.add(j)
                    self.columns[j] = 0
                    break
                elif lower1 in self.low1:
                    # We compute the sum with the given column (i.e. xor operation)
                    column = column ^ self.columns[self.low1[lower1]]
                else: 
                    self.low1[lower1] = j
                    self.columns[j] = column
                    break

    def bars(self):
        """Method to compute the bars of the matrix"""
        bars = []
        for cycle in self.zero_columns:
            if cycle in self.low1:
                bars.append((cycle, self.low1[cycle]))
            else:
                bars.append((cycle, float('inf')))

        return bars

if __name__ == "__main__":
    columns = [int(b'0110', 2), int(b'1011', 2), int(b'1100', 2), int(b'0101', 2)]
    matr = Matrix(columns)
    #matr.columns = [1+4, 3, 4]
    print(matr)
    matr.make_echelon_form()
    print("jdhdhf")
    print(matr)
    print(matr.bars())
