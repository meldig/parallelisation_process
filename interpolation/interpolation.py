import json
import glob

from dask.distributed import Client
import rioxarray
import numpy as np
import rasterio.fill
import xarray as xr
import dask
from osgeo import gdal


def create_coords(x_values, y_values):
    coords = []
    for i in range(len(y_values)):
        for j in range(len(x_values)):
            coords.append({
                "band": range(1),
                "x": x_values[j],
                "y": y_values[i]
            })

    return coords


@dask.delayed
def create_mask(chunk):
    mask = np.where(chunk < config.get("mask").get("limit"), 0, chunk)
    return mask


@dask.delayed
def interpolation(chunk, mask):
    return rasterio.fill.fillnodata(chunk, mask, config.get("interpolation").get("max_search_distance"))


@dask.delayed
def create_data_array(chunk, coords):
    return xr.DataArray(
        chunk,
        dims=["band", "y", "x"],
        coords=coords).rio.write_crs(2154)


@dask.delayed
def write_tile(tile, i):
    tile.rio.to_raster(config.get("directories").get("output") + "/" + str(i) + ".tif")


if __name__ == "__main__":
    with open("./config_dev.json") as file:
        config = json.load(file)

    client = Client(n_workers=config.get("client").get("n_workers"),
                    threads_per_worker=config.get("client").get("threads_per_worker"))

    open_rasterio = config.get('open_rasterio')

    ds = rioxarray.open_rasterio(filename=open_rasterio.get('filename'),
                                 chunks=(open_rasterio.get('chunks')[0], open_rasterio.get('chunks')[1], open_rasterio.get('chunks')[2]))

    x_split_values = []
    y_split_values = []

    for i in range(int(ds.data.shape[2] / ds.data.chunksize[2])):
        x_split_values.append(ds.data.chunksize[2])

    for j in range(int(ds.data.shape[1] / ds.data.chunksize[1])):
        y_split_values.append(ds.data.chunksize[1])

    coords_x = ds.coords["x"].data
    coords_x_splitted = np.array_split(coords_x, np.cumsum(x_split_values))

    coords_y = ds.coords["y"].data
    coords_y_splitted = np.array_split(coords_y, np.cumsum(y_split_values))

    tiles_to_write = []
    delayed_chunks = ds.data.to_delayed().ravel()
    coordinates = create_coords(coords_x_splitted, coords_y_splitted)

    for k in range(len(delayed_chunks)):
        mask = dask.delayed(create_mask)(delayed_chunks[k])
        interpoled = dask.delayed(interpolation)(delayed_chunks[k], mask)
        data_array = dask.delayed(create_data_array)(interpoled, coordinates[k])
        tiles_to_write.append(write_tile(data_array, k))

    dask.compute(*tiles_to_write)

    files = glob.glob(config.get("directories").get("output") + "/*.tif")
    options = gdal.TranslateOptions(noData=ds.attrs['_FillValue'])

    gdal.BuildVRT(config.get("gdal").get("VRT"), files)
    gdal.Translate(config.get("gdal").get("output_file"),
                   config.get("gdal").get("VRT"),
                   options=options)