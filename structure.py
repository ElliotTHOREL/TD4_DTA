class simplex_set:
    def __init__(self, simplexes):
        self.simplexes = sorted(simplexes) 
        self.matrix = self.get_matrix()

    def compute_bars(self):
        pass

    def get_matrix(self):
        pass

class simplex:
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


class matrix:
    def __init__(self):
        self.columns = []   # list of ints (dec repr of bitstring)

    def __index__(self, coord):
        # coord = (i, j)

        if not isinstance(coord, tuple):
            raise Exception("wrong type")
        
        if coord[1] < 0 or coord[1] >= len(self.columns) or coord[0] < 0 or coord[0] > len(self.columns):
            raise Exception("Index out of range")
        
        return int(self.columns[coord[1]] & 2**coord[0] > 0)

    def __repr__(self):
        return_string = ""

        for i in range(len(self.columns)):
            return_string = ''.join(([return_string] + [str(self.__index__((i, j))) for j in range(len(self.columns))] + ['\n']))

        return return_string

    def make_echelon_form(self):
        pass

    def is_echelon_form(self):
        pass

    def bars(self):
        pass 


matr = matrix()
matr.columns = [int(b'0110', 2), int(b'1011', 2), int(b'1100', 2), int(b'0101', 2)]
#matr.columns = [1+4, 3, 4]
print(matr)
print(int(b'101', 2))