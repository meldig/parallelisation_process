import dask_rasterio as dr
import dask.array as da
import sys
import numpy as np
import rasterio


def getDaskArray(filepath):
    return dr.read_raster(filepath)


def filterArray(array, lim):
    return np.where(array >= lim, array, -9999)


def multiply(array):
    multipliedArray = np.where(array >= 14, 100*array, -9999)
    multipliedDaskArray = da.from_array(multipliedArray, chunks=(1, 5, 365))
    multipliedDaskArray.dtype = rasterio.int16
    return multipliedDaskArray


def createRaster(rasterArray):
    with rasterio.open("D:\\Documents\\MISSIONS\\DASK\\echant_5cm_pix_cc50.tif") as src:
        data = src.profile
        srcTransform = src.transform

    with rasterio.open(
        "D:\\Documents\\MISSIONS\\DASK\\new.tif",
        "w",
        driver="GTiff",
        height=rasterArray.shape[1],
        width=rasterArray.shape[2],
        count=data['count'],
        dtype=rasterArray.dtype,
        crs=data['crs'],
        transform=srcTransform,
        nodata=-9999
    ) as dst:
        dst.write(rasterArray)


if __name__ == "__main__":
    np.set_printoptions(threshold=sys.maxsize)

    array = getDaskArray("D:\\Documents\\MISSIONS\\DASK\\echant_5cm_pix_cc50.tif")
    finalDaskArray = multiply(array)
    createRaster(finalDaskArray)