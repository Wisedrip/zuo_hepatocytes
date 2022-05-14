## overall heatmap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import multiprocess as mp
import bioframe
import cooler
import itertools
import click
import cooltools
import cooltools.eigdecomp
import cooltools.expected
import cooltools.saddle
from dask.distributed import Client, LocalCluster
from scipy.linalg import toeplitz
import os

# directory
dir = os.getcwd()
stages=[]  

for root, dirs, files in os.walk(dir):
    for file in files:
        if os.path.splitext(file)[1] == '.cool':
            t = os.path.splitext(file)[0] 
            stages.append(t)  

for stage in stages:
    coolfile=''.join([stage, '.cool'])
    c = cooler.Cooler(coolfile)
    obs_mat = c.matrix()[:]
    scale='linear'
    out=''.join([stage,'_all_by_all_log2_yor_obs.pdf'])
    dpi= 100
    colormap='YlOrRd'
    row_matrix= stage
    col_matrix= stage
    zmin=0.00000
    zmax=0.0008
    plt.figure(figsize=(10,10))
    plt.gcf().canvas.set_window_title("Contact matrix".format())
    plt.title("")
    plt.imshow(obs_mat, interpolation="none",vmin=zmin,vmax=zmax, cmap=colormap)
    plt.ylabel("{} coordinate".format(row_matrix))
    plt.xlabel("{} coordinate".format(col_matrix))
    cb = plt.colorbar()
    cb.set_label({"linear": "relative contact frequency", "log2": "log 2 ( relative contact frequency )",
      "log10": "log 10 ( relative contact frequency )",
      }[scale])
    plt.savefig(out, dpi=dpi, format='pdf')
