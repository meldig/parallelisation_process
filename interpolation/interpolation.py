import json
import glob

from dask.distributed import Client
import rioxarray
import numpy as np
import rasterio.fill
import xarray as xr
import dask
from osgeo import gdal


# Cette fonction permet de créer un tableau d'objets (coordonnées) qui servira à créer les DataArrays
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


# Cette fonction permet de créer le mask pour un chunk donné
@dask.delayed
def create_mask(chunk):
    mask = np.where(chunk < config.get("mask").get("limit"), 0, chunk)
    return mask


# Cette fonction permet d'interpoler un chunk donné. Elle retourne un tableau numpy
@dask.delayed
def interpolation(chunk, mask):
    return rasterio.fill.fillnodata(chunk, mask, config.get("interpolation").get("max_search_distance"))


# Cette fonction permet de créer un DataArray à partir d'un chunk. L'intérêt d'utiliser les DataArrays est que l'on peut facilement
# les convertir en raster
@dask.delayed
def create_data_array(chunk, coords):
    return xr.DataArray(
        chunk,
        dims=["band", "y", "x"],
        coords=coords).rio.write_crs(2154)


# Cette fonction permet d'exporter un chunk au format .tif
@dask.delayed
def write_tile(tile, i):
    tile.rio.to_raster(config.get("directories").get("output") + "/" + str(i) + ".tif")


if __name__ == "__main__":
    with open("./config_dev.json") as file:
        config = json.load(file)

    print("Ouvreture du raster\n")

    # Le client permet de gérer le nombre de threads à utiliser. Les threads sont répartis par workers
    client = Client(n_workers=config.get("client").get("n_workers"),
                    threads_per_worker=config.get("client").get("threads_per_worker"))

    open_rasterio = config.get('open_rasterio')

    # Ouverture du raster. On récupère un DataArray construit à partir d'un tableau Dask. On accède au tableau Dask grâce à
    # l'attribut data : ds.data
    ds = rioxarray.open_rasterio(filename=open_rasterio.get('filename'),
                                 chunks=(open_rasterio.get('chunks')[0], open_rasterio.get('chunks')[1], open_rasterio.get('chunks')[2]))

    x_split_values = []
    y_split_values = []

    print("Calcul des coordonnées\n")

    # Remplissage des tableaux avec les dimensions des chunks. Par exemple, s'il y a 17 chunks de 7000x7000 par ligne, on aura
    # 17 fois 7000 dans le tableau x_split_values
    for i in range(int(ds.data.shape[2] / ds.data.chunksize[2])):
        x_split_values.append(ds.data.chunksize[2])

    for j in range(int(ds.data.shape[1] / ds.data.chunksize[1])):
        y_split_values.append(ds.data.chunksize[1])

    # Tableau qui contient toutes les coordonnées du raster selon l'axe x
    coords_x = ds.coords["x"].data
    # Tableau contenant autant de tableaux que de chunks selon l'axe x. La fonction array_split avec deux tableau en paramètre
    # permet de découper le premier tableau en fonction du deuxième qui contient les indices de découpe.
    coords_x_splitted = np.array_split(coords_x, np.cumsum(x_split_values))

    # Idem qu'au dessus selon l'axe y
    coords_y = ds.coords["y"].data
    coords_y_splitted = np.array_split(coords_y, np.cumsum(y_split_values))

    # Tableau d'objets delayed, exécution en parallèle
    tiles_to_write = []
    # Récupération de tous les chunks du raster
    delayed_chunks = ds.data.to_delayed().ravel()
    coordinates = create_coords(coords_x_splitted, coords_y_splitted)

    print("Interpolation + conversion en data array\n")

    # Pour chaque chunk
    for k in range(len(delayed_chunks)):
        # Calcul du mask
        mask = dask.delayed(create_mask)(delayed_chunks[k])
        # Interpolation du chunk
        interpoled = dask.delayed(interpolation)(delayed_chunks[k], mask)
        # Création du DataArray
        data_array = dask.delayed(create_data_array)(interpoled, coordinates[k])
        # Rangement dans le tableau
        tiles_to_write.append(dask.delayed(write_tile)(data_array, k))

    # Lancement de l'exécution en parallèle
    dask.compute(*tiles_to_write)

    # Ici, tous les fichiers .tif sont dans le répertoire de sortie, il y a autant de fichiers que de chunks.
    # Il suffit maintenant de les rassembler

    print("Exportation\n")

    # Récupération de tous les fichiers
    files = glob.glob(config.get("directories").get("output") + "/*.tif")
    # Établissement de la valeur de nodata. La même que pour le raster en entrée
    options = gdal.TranslateOptions(noData=ds.attrs['_FillValue'])

    # Construction du VRT
    gdal.BuildVRT(config.get("gdal").get("VRT"), files)
    # Passage du VRT au fichier .tif rassemblé
    gdal.Translate(config.get("gdal").get("output_file"),
                   config.get("gdal").get("VRT"),
                   options=options)