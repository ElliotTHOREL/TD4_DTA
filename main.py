from structure import Simplex, Simplex_set
import time
import argparse

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
    if not is_ball:
        # the d-sphere is the (d+1)-ball without the center
        d += 1

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




def run_from_file(in_file, out_file):
    start = time.perf_counter()  
    simplex_set = retrieve_data(in_file)
    bars = simplex_set.compute_bars()
    end = time.perf_counter()
    print(f"Finished, time: {end - start:.6f} seconds")
    with open(out_file, 'w') as f:
        for bar in bars:
            f.write(' '.join(list(map(str, bar)) + ['\n']))


def run_sphere_or_ball(d: int, is_ball: bool, out_file: str):
    start = time.perf_counter()
    simplex_set = create_sphere_or_ball(d, is_ball)
    bars = simplex_set.compute_bars()
    end = time.perf_counter()
    print(f"Finished, time: {end - start:.6f} seconds")
    with open(out_file, 'w') as f:
        for bar in bars:
            f.write(' '.join(list(map(str, bar)) + ['\n']))


def run_filtration(type: str, argument):

    if type in ["filtration", "classical_space", "dummy"]:
        #On lit un fichier pour l'input
        if type == "filtration":
            file_name = f"filtration_{argument.upper()}"
            in_file = f"datasets/filtration/{file_name}.txt"
            out_file = f"results/filtration/{file_name}.out"
        elif type == "classical_space":
            file_name = argument
            in_file = f"datasets/classical_space/{file_name}.txt"
            out_file = f"results/classical_space/{file_name}.out"    
        elif type == "dummy":
            file_name = argument
            in_file = f"datasets/dummy/{file_name}.txt"
            out_file = f"results/dummy/{file_name}.out"

        run_from_file(in_file, out_file)



    elif type in ["sphere", "ball"]:
        d=int(argument)
        if type == "sphere":
            is_ball = False
            out_file = f"results/sphere/{d}-sphere.out"
        else:
            is_ball = True
            out_file = f"results/ball/{d}-ball.out"

        run_sphere_or_ball(d, is_ball, out_file)

    else:
        raise ValueError(f"Invalid type: {type}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type", type=str, help="Type of filtration", choices=["filtration", "classical_space", "dummy", "sphere", "ball"])
    parser.add_argument("argument", type=str, 
    help="""if type is filtration -> letter corresponding \n
    if type is sphere or ball -> dimension of the sphere or ball \n
    if type is classical_space or dummy -> filename without the extension""")
    
    args = parser.parse_args()
    run_filtration(args.type, args.argument)

