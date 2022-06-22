import dask
import tile


@dask.delayed
def process(pipeline):
    pipeline.execute()


def processPipelines(files, args):
    tiles = []
    delayedPipelines = []
    for file in files:
        tiles.append(tile.Tile(file, args))

    for t in tiles:
        delayedPipelines.append(dask.delayed(process)(t.pipeline()))

    return delayedPipelines
