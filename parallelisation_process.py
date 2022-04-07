import dask
import sys
import dask.array as da
import rasterio
import numpy as np
import dask_rasterio as dr


def getDaskArray(filepath):
    return dr.read_raster(filepath)


def calc(array):
    filteredNpArray = np.where(array >= 15, array, -9999)
    res = da.from_array(np.asarray(filteredNpArray), chunks=(1, 5, 365))
    return res


def createRaster(daskArray, filepath, prof):
    dr.write_raster(filepath, daskArray, **prof)


if __name__ == "__main__":
    # np.set_printoptions(threshold=sys.maxsize)

    filepath = "INPUT FILE"
    daskArray = getDaskArray(filepath)
    filteredArray = calc(daskArray)

    with rasterio.open(filepath) as src:
        print(src.profile.copy())
        print(src.read().shape)
        createRaster(filteredArray, "OUTPUT FILE", src.profile.copy())
