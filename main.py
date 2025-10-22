from structure import Simplex, Simplex_set
import time

def retrieve_simplex(line: str):
    apparition_time, dimension, *under_vertices = list(map(lambda x : x.replace('\n', ''), line.split(" ")))

    return Simplex(float(apparition_time), int(dimension), sorted(under_vertices))


def retrieve_data(filename: str):
    simplexes = []

    with open(filename, 'r') as file:
        for line in file.readlines():
            simplexes.append( retrieve_simplex(line) )

    return Simplex_set(simplexes)


if __name__ == "__main__":
    c = 'B'

    file_name = f"filtration_{c}"
    start = time.perf_counter()

    simplex_set = retrieve_data(f"{file_name}.txt")
    bars = simplex_set.compute_bars()

    print(f"Finished, time: {time.perf_counter() - start:.6f} seconds")

    with open(f"{file_name}.out", 'w') as f:
        for bar in bars:
            f.write(' '.join(list(map(str, bar)) + ['\n']))
