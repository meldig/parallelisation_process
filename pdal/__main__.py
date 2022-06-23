import pickle

import dask
import do
from dask.distributed import Client
from os import listdir
from os.path import join

if __name__ == "__main__":
    temp_directory = './temp'
    input_directory = 'D:/Documents/MISSIONS/DASK/pdal/input'
    output_dir = 'D:/Documents/MISSIONS/DASK/pdal/output'
    files = []
    pipelines = []

    if len(listdir(temp_directory)) != 0:
        for f in listdir(temp_directory):
            with open(join(temp_directory, f), 'rb') as p:
                pipelines.append(pickle.load(p))
        delayed = do.processPipelines(output_dir=output_dir, pipelines=pipelines)
    else:
        files = [join(input_directory, f) for f in listdir(input_directory)]
        delayed = do.processPipelines(output_dir=output_dir, files=files)
        client = Client(n_workers=2, threads_per_worker=1)

    dask.compute(*delayed)