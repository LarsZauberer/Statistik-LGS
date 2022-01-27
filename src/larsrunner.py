from larsalgo import Problem
import random
import numpy as np
import pandas as pd
import time as t
import threading
import psutil
from rich.progress import track

data = pd.DataFrame(columns=['algorithm', 'time', 'cpu', 'matrix_size'])
data = {"algorithm": [], "time": [], "cpu": [], "matrix_size": []}

cpu = [-1, 0]

def getCPU(index):
    global cpu
    cpu = [index, psutil.cpu_percent(interval=1)]
    

for i in track(range(1000), description="Calculating..."):
    try:
        size = random.randint(2, 100)
        A = [[random.randint(0, 100) for _ in range(size)] for _ in range(size)]
        b = [random.randint(0, 100) for _ in range(size)]
        p = Problem(A, b)
        thread = threading.Thread(target=getCPU, args=(i,))
        thread.start()
        s = t.time()
        p.toTriangle()
        # print(p.A)
        # print(p.b)
        p.solveBackwards()
        if cpu[0] == i:
            mycpu = cpu[1]
        else:
            mycpu = None
        # data.append({'algorithm': 'Homemade', 'time': t.time() - s, 'cpu': mycpu, 'matrix_size': len(A)}, ignore_index=True)
        data["algorithm"].append("Homemade")
        data["time"].append(t.time() - s)
        data["cpu"].append(mycpu)
        data["matrix_size"].append(len(A))
        
        # print(p.x)
    except Exception as e:
        print(f"Fehler: {e}")
        continue
         
    A = np.array(A)
    b = np.array(b)
    thread = threading.Thread(target=getCPU, args=(i,))
    thread.start()
    s = t.time()
    x = np.linalg.solve(A, b)
    if cpu[0] == i:
        mycpu = cpu[1]
    else:
        mycpu = None
    data["algorithm"].append("Numpy")
    data["time"].append(t.time() - s)
    data["cpu"].append(mycpu)
    data["matrix_size"].append(len(A))
    
    for index, item in enumerate(x):
        if round(item, 2) != round(p.x[index], 2):
            print(f"Fehler: {item} != {p.x[index]}")
            break

data = pd.DataFrame(data)
data.to_csv("data.csv")
    