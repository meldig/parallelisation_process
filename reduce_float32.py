import dask.array as da
import rasterio


def multiply(array):
    # Tableau de chunks pour le dask array
    chunks = []
    chunk = int(input("Entrez une valeur pour le tuple de chunks : "))

    # Entrez -1 pour arrêter la boucle
    while chunk != -1:
        chunks.append(chunk)
        chunk = int(input("Entrez une valeur pour le tuple de chunks : "))

    # Création du dask array et transformation du tableau de chunks en tuple
    daskArray = da.from_array(array, tuple(chunks))

    # Si la valeur est >= au seuil on la multiplie par 10, sinon on la remplace par une valeur de nodata
    seuil = int(input("Entrez la valeur du seuil pour la multiplication : "))
    multipliedDaskArray = da.where(daskArray >= seuil, 10*daskArray, -9999)
    return multipliedDaskArray


def createRaster(array, data):
    # Conversion du type de tableau de float32 à rasterio.int16
    convertedArray = array.astype(rasterio.int16)

    # Création du nouveau raster
    with rasterio.open("D:\\Documents\\MISSIONS\\DASK\\new.tif", 'w', **data) as dst:
        dst.write(convertedArray)


if __name__ == "__main__":
    # Le chemin du raster en entée (sans guillemets)
    rasterPath = input("Entrez le chemin de votre raster : ")

    # Récupération des métadonnées du raster
    with rasterio.open(rasterPath) as raster:
        npArray = raster.read()
        data = raster.profile
        print(data)
        data['nodata'] = int(input("Entrez une valeur de nodata : "))

    multipliedArray = multiply(npArray)
    createRaster(multipliedArray, data)