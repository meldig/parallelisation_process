# interpolation :snake:

Ce script permet d'interpoler un raster fourni en entrée.

Utilisation de rioxarray pour la lecture et le regroupement des données. Dask pour découper la donnée (chunks) et paralléliser. Et on utilise rasterio pour effectuer l'interpolation.

### main :house_with_garden:

Ouverture du raster avec la fonction `open_rasterio()` de rioxarray, en renseignant le paramètre `chunks` on découpe la donnée.

Pour chaque chunk, on va calculer le mask qui va permettre d'interpoler et on interpole la tuile en cours grâce à la fonction interpolation. Le résultat est stocké dans un tableau.

Ensuite, pour chaque tuile interpolée, on va la transformer en DataArray (xarray). Ce qui va nous permettre de renseigner ses dimensions et ses coordonnées, ce qui va être utile pour le rassemblement de toutes les tuiles.

On exporte ensuite le raster grâce à la fonction `to_raster()`.

### interpolation :triangular_flag_on_post:

Cette fonction attend un tableau à interpoler et un mask.

Le mask est en fait un autre tableau, où les valeurs à interpoler sont représentées par des 0 dans le tableau (cf [rasterio.fill module](https://github.com/meldig/conda)).

La fonction retourne le tableau interpolé, sans valeurs de nodata grâce à la fonction `fillnodata()` de rasterio.

### merge_tiles :arrows_counterclockwise:

Cette fonction attend une liste de DataArrays et les bordures du tableau final.

Cette fonction retourne un tableau numpy qui sera le rassemblement de toutes les DataArrays.

### calculate_coordinates :earth_americas:

Cette fonction permet de calculer les coordonées d'une tuile pour pouvoir la replacer au bon endroit dans le raster final.

On a tout d'abord deux variables `x_axis` et `y_axis` qui sont simplement toutes les valeurs de pixel du raster en entrée selon les axes x et y.

Pour chaque tuile, on va ajouter à une liste un objet qui contiendra ses coordonnées. Pour cela, on va découper dans les tableaux `x_axis` et `y_axis` les valeurs de l'indice 0 jusqu'à la hauteur (resp. largeur) de la tuile en cours.

Une fois les valeurs prises dans le tableau, on retire celles-ci pour pouvoir établir le même procédé pour la tuile suivante.

Si on est arrivé sur la tuile la plus à droite du raster (ie. il n'y a plus de valeur à droite de celle-ci) : on réinitialise le tableau `x_axis` et on passe à la ligne de tuile juste en dessous.

On répète l'opération pour toutes les tuiles.

Au final, cette fonction nous retourne une liste de coordonnées que l'on utilisera pour construire nos DataArrays.
