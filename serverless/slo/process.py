import pandas as pd
import numpy as np
import os

def process(fname):
    df = pd.read_csv(fname, sep = '\t')
    i = 0
    for c in df:
        col = df[c].dropna()
        n = len(col)
        x = [1 / n * i for i in range(n)]
        d = pd.DataFrame(data = {'x': x, c: col})
        d.to_csv('{}.{}'.format(fname, i), index = False, sep='\t')
        i += 1

def run():
    for root, subdirs, files in os.walk('thruput'):
        for file in files:
            if not file.endswith(".txt"): continue
            process(os.path.join(root, file))

    os.system("""gnuplot -e "fname='{}'" -e "plot_title='{}'" -e "y_title='{}'" -c thruput.gnu"""
        .format('alex',
                'Throughput of AlexNet under diff. latency SLO',
                'Throughput (#images/s)'))

    os.system("""gnuplot -e "fname='{}'" -e "plot_title='{}'" -e "y_title='{}'" -c thruput.gnu"""
        .format('vgg',
                'Throughput of MobileNet-V2 under diff. latency SLO',
                'Throughput (#images/s)'))
    
    os.system("""gnuplot -e "fname='{}'" -e "plot_title='{}'" -e "y_title='{}'" -c thruput.gnu"""
        .format('inception',
                'Throughput of TF-coco under diff. latency SLO',
                'Throughput (#images/s)'))


    # Batch
    for root, subdirs, files in os.walk('batch'):
        for file in files:
            if not file.endswith(".txt"): continue
            process(os.path.join(root, file))

    os.system("""gnuplot -e "fname='{}'" -e "plot_title='{}'" -e "y_title='{}'" -c batch.gnu"""
        .format('alex',
                'Batch size of AlexNet under diff. latency SLO',
                'Batch size (#images)'))

    os.system("""gnuplot -e "fname='{}'" -e "plot_title='{}'" -e "y_title='{}'" -c batch.gnu"""
        .format('vgg',
                'Batch size of MobileNet-V2 under diff. latency SLO',
                'Batch size (#images)'))
    
    os.system("""gnuplot -e "fname='{}'" -e "plot_title='{}'" -e "y_title='{}'" -c batch.gnu"""
        .format('inception',
                'Batch size of TF-coco under diff. latency SLO',
                'Batch size (#images)'))

    # Latency
    os.system("""gnuplot -e "fname='{}'" -e "plot_title='{}'" -e "y_title='{}'" -c latency.gnu"""
        .format('alex',
                'Latency of AlexNet under diff. atch size',
                'Latency (s)'))

    os.system("""gnuplot -e "fname='{}'" -e "plot_title='{}'" -e "y_title='{}'" -c latency.gnu"""
        .format('vgg',
                'Latency of MobileNet-V2 under diff. Batch size',
                'Latency (s)'))
    os.system("""gnuplot -e "fname='{}'" -e "plot_title='{}'" -e "y_title='{}'" -c latency.gnu"""
        .format('inception',
                'Latency of TF-coco under diff. Batch size',
                'Latency (s)'))


run()