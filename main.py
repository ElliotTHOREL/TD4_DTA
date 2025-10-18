from structure import Simplex, Simplex_set

def retrieve_simplex(line):
    info = list(map(lambda x : x.replace('\n', ''), line.split(" ")))
    apparition_time = float( info[0] )
    dimension = int( info[1] )
    under_vertices = sorted(info[2:])
    return Simplex(apparition_time, dimension, under_vertices)


def retrieve_data(filename):
    simplexes = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            simplexes.append( retrieve_simplex(line) )
    return Simplex_set(simplexes)

if __name__ == "__main__":
    simplex_set = retrieve_data("filtration_B.txt")
    print(simplex_set.simplexes)
    print(simplex_set.matrix)
    bars = simplex_set.compute_bars()

    for bar in bars:
        print(bar)