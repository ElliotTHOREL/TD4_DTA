class simplex_set:
    def __init__(self, vertices):
        self.vertices = sorted(vertices) 

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


