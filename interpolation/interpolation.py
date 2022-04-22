import json

import rioxarray
import rioxarray.merge
import xarray as xr
import dask
import dask.array as da
import rasterio.fill
import numpy as np


@dask.delayed
def interpolation(array, mask):
    return rasterio.fill.fillnodata(array, mask, config.get('interpolation').get('max_search_distance'))


@dask.delayed
def merge_tiles(tiles, bounds):
    return rioxarray.merge.merge_arrays(tiles, bounds=bounds)


def calculate_coordinates(arrays):
    x_axis = ds.coords['x'].data
    y_axis = ds.coords['y'].data
    coords = []

    for array in arrays:
        array_band, array_height, array_width = array.shape
        coords.append({
            "band": range(array_band),
            "y": y_axis[:array_height],
            "x": x_axis[:array_width]
        })

        array_width = array.shape[2]
        if len(x_axis[array_width:]) == 0:
            x_axis = ds.coords['x'].data
            array_height = array.shape[1]
            y_axis = y_axis[array_height:]
        else:
            x_axis = x_axis[array_width:]

    return coords


if __name__ == "__main__":
    with open("./config.json") as file:
        config = json.load(file)

    interpoled_data = []
    data_arrays = []

    open_rasterio = config.get('open_rasterio')

    ds = rioxarray.open_rasterio(filename=open_rasterio.get('filename'),
                                 chunks=(open_rasterio.get('chunks')[0], open_rasterio.get('chunks')[1], open_rasterio.get('chunks')[2]))

    chunks = ds.data.to_delayed().ravel()

    for chunk in (c.compute() for c in chunks):
        mask = dask.delayed(np.where)(chunk < config.get('mask').get('limit'), .0, chunk)
        res = dask.delayed(interpolation)(chunk, mask.compute())
        interpoled_data.append(da.from_delayed(res, chunk.shape, chunk.dtype))

    coordinates = calculate_coordinates(interpoled_data)

    for i in range(len(interpoled_data)):
        data_arrays.append(
            xr.DataArray(
                interpoled_data[i],
                dims=["band", "y", "x"],
                coords=coordinates[i]
            ).rio.write_crs(2154)
        )

    merged_data = dask.delayed(merge_tiles)(data_arrays, ds.rio.bounds()).compute()
    xr.DataArray(merged_data).rio.to_raster(config.get('to_raster').get('output_file'))