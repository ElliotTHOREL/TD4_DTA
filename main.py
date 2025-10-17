from structure import simplex, simplex_set

def retrieve_simplex(line):
    info = line.split(" ")
    apparition_time = float( info[0] )
    dimension = int( info[1] )
    under_vertices = info[2:]
    return simplex(apparition_time, dimension, under_vertices)


def retrieve_data(filename):
    simplexes = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            simplexes.append( retrieve_simplex(line) )
    return simplex_set(simplexes)