import pandas as pd
import numpy as np
import os

def cdf(fname):
    with open(fname, "r") as f:
        arr = [float(n) for n in f.read().split()]
        arr = sorted(arr)
        y = [round(1 / len(arr) * (i + 1), 2) for i in range(len(arr))]
        df = pd.DataFrame(data = {'x': arr, 'y': y})
        df.to_csv(os.path.join('processed', fname), sep = '\t', index=False, header=False)
        # os.system("""gnuplot -e "filename='{}'" -c plot.gnu""".format(os.path.join('processed', fname)))

def bar(fname):
    with open(fname, "r") as f:
        arr = [float(n) for n in f.read().split()]
        return np.mean(arr)

def run(walk_dir = 'vgg'):
    lat_dir = os.path.join(walk_dir, 'latency')
    for root, subdirs, files in os.walk(lat_dir):
        for file in files:
            if not os.path.exists(os.path.join('processed', root)):
                os.makedirs(os.path.join('processed', root))
            cdf(os.path.join(root, file))
    
    algo = []
    col = []
    thr_dir = os.path.join(walk_dir, 'thruput')
    for root, subdirs, files in os.walk(thr_dir):
        for file in files:
            if not os.path.exists(os.path.join('processed', root)):
                os.makedirs(os.path.join('processed', root))
            algo.append(file.split('.')[0])
            col.append(bar(os.path.join(root, file)))
    
    m = max(col)
    col /= m
    df = pd.DataFrame(data = {'x': algo, 'y': col})
    df.to_csv(os.path.join('processed', walk_dir, 'thruput', 'thruput.txt'), sep = '\t', index=False, header=False)

    os.system("gnuplot -c algo.gnu")
    os.system("gnuplot -c hitrate.gnu")
    os.system("gnuplot -c thruput.gnu")


run('vgg')