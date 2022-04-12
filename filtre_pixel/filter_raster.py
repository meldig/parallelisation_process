import dask.array as da
import rasterio


def filter(array, data):
    chunks = []
    chunk = int(input("Valeur à ajouter au tuple de chunks : "))

    while chunk != -1:
        chunks.append(chunk)
        chunk = int(input("Valeur à ajouter au tuple de chunks : "))

    daskArray = da.from_array(array, tuple(chunks))
    print(daskArray)

    seuil = int(input("Entrez une valeur pour le seuil à partir duquel la valeur sera filtrée : "))
    filteredDaskArray = da.where(daskArray >= seuil, daskArray, data['nodata'])

    return filteredDaskArray


def createRaster(array, data):
    outputRaster = input("Entrez le chemin de votre sortie raster : ")
    with rasterio.open(outputRaster, 'w', **data) as dst:
        dst.write(array)


if __name__ == "__main__":
    rasterPath = input("Entrez le chemin de votre raster : ")

    with rasterio.open(rasterPath) as src :
        array = src.read()
        data = src.profile
        data['nodata'] = int(input("Entrez une valeur de nodata : "))

    filteredArray = filter(array, data)
    createRaster(filteredArray, data)