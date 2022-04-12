import dask.array as da
import rasterio
import time


def multiply(array):
    daskArray = da.from_array(array, (1, 1000, 1000))
    multipliedDaskArray = da.where(daskArray >= 11, 10*daskArray, -9999)
    return multipliedDaskArray


def createRaster(array, data):
    convertedArray = array.astype(rasterio.int16)
    with rasterio.open("D:\\Documents\\MISSIONS\\DASK\\new.tif", 'w', **data) as dst:
        dst.write(convertedArray)


if __name__ == "__main__":
    rasterPath = "D:\\Documents\\MISSIONS\\DASK\\echant_bigger_5cm_pix_cc50.tif"

    with rasterio.open(rasterPath) as raster:
        npArray = raster.read()
        data = raster.profile
        data['nodata'] = -9999

    multipliedArray = multiply(npArray)
    createRaster(multipliedArray, data)