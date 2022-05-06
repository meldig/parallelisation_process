# interpolation :snake:

Ce script permet d'interpoler un raster fourni en entrée.

Utilisation de rioxarray pour la lecture et le regroupement des données. Dask pour découper la donnée (chunks) et paralléliser. Et on utilise rasterio pour effectuer l'interpolation.

### main :house_with_garden:

Création du client qui va permettre de gérer le nombre de workers et le nombre de threads par worker.

Ouverture du raster avec la fonction `open_rasterio()` de rioxarray, en renseignant le paramètre `chunks` on découpe la donnée.

Pour calculer les coordonnées, on récupère la taille des chunks dans un tableau, puis on split le tableau contenant les valeurs de coordonnées (`ds.data.coords["x"]`) en fonction de ce dernier. On effectue le `cumsum`car la fonction split de numpy split en fonction des valeurs dans le tableau et non en fonction des indices. On créer ensuite les objets contenant les coordonnées grâce à la fonction `create_coords`.

Pour chaque chunk, on va calculer le mask (grâce à la fonction `create_mask`) qui va permettre d'interpoler et on interpole la tuile en cours grâce à la fonction `interpolation`. Dans la foulée on créé le DataArray (fonction `create_data_array`) et on exporte la tuile au format GTiff. Cette approche permet de ne pas conserver les tableaux interpolés en mémoire.

On rassemble ensuite les tuiles grâce à la création d'un fichier VRT et la fonction Translate (voir [VRT](https://gdal.org/drivers/raster/vrt.html) et [Translate](https://gdal.org/programs/gdal_translate.html)) 

### interpolation :triangular_flag_on_post:

Cette fonction attend un tableau à interpoler et un mask.

Le mask est en fait un autre tableau, où les valeurs à interpoler sont représentées par des 0 dans le tableau (cf [rasterio.fill module](https://github.com/meldig/conda)).

La fonction retourne le tableau interpolé, sans valeurs de nodata grâce à la fonction `fillnodata()` de rasterio.

### write_tiles :pencil2:

Fonction qui attend une tuile à écrire et un indice.

Permet d'exporter la tuile au format GTiff.
