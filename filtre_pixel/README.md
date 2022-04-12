# filter_raster

Ce script permet de filtrer les valeurs d'un raster en entrée (converti en tableau).

Utilisation de dask pour la parallélisation et de rasterio pour la lecture et l'écriture des rasters.

### main

On récupère le tableau de valeurs correspondant au raster en entrée grâce à la fonction read().
On récupère les métadonnées du raster en entrée dans la variable data et on indique une valeur de 'nodata' (pas de valeur pour le pixel)

### filter

Cette fonction attend deux paramètres : le tableau de valeurs et les métadonnées du raster en entrée.

Dans le tableau chunks, on va mettre les valeurs des chunks souhaitée pour la création du Dask Array (voir : [Dask Array Chunks](https://docs.dask.org/en/stable/array-chunks.html)).

On converti ensuite notre tableau de valeurs en Dask Array, puis grâce à la commande da.where on affecte la valeur de nodata aux valeurs inférieures au seuil indiqué par l'utilisateur.

### createRaster

Cette fonction attend deux arguments : le Dask Array et les métadonnées du raster en entrée.

On écrit le nouveau raster grâce à l'option 'w' (write) de rasterio.open.