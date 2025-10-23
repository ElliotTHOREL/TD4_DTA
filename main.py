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


def create_sphere_or_ball(d: int, is_ball: bool):
    """is_ball : False -> sphere, True -> ball"""

    simplexes=[]
    for i in range(1, 2**(d+1)-1 + int(is_ball)):
        vertices =[]
        number = i
        vertix = 0
        while number > 0:
            if number % 2 == 1:
                vertices.append(str(vertix))
            number = number // 2
            vertix += 1
        simplexes.append(Simplex(0, len(vertices)-1, sorted(vertices)))
    return Simplex_set(simplexes)






if __name__ == "__main__":
    #from file
    """
    c = 'B'
    file_name = f"filtration_{c}"
    """
    file_name = "projective_plan"
    start = time.perf_counter()
    simplex_set = retrieve_data(f"{file_name}.txt")  

    #sphere or ball
    """
    d=4
    is_ball = True
    file_name = f"filtration_{d}-{'ball' if is_ball else 'sphere'}"
    start = time.perf_counter()
    simplex_set = create_sphere_or_ball(d, is_ball) 
    """
    
    bars = simplex_set.compute_bars()

    print(f"Finished, time: {time.perf_counter() - start:.6f} seconds")

    with open(f"{file_name}.out", 'w') as f:
        for bar in bars:
            f.write(' '.join(list(map(str, bar)) + ['\n']))
