# float32_to_int16

Ce script permet de convertir les valeurs d'un raster en entrée (converti en tableau) de float32 à int16.

Utilisation de dask pour la parallélisation et de rasterio pour la lecture et l'écriture des rasters.

### main

On récupère le tableau de valeurs correspondant au raster en entrée grâce à la fonction read().
On récupère les métadonnées du raster en entrée dans la variable data et on indique une valeur de 'nodata' (pas de valeur pour le pixel)

### multiply

Cette fonction attend deux paramètres : le tableau de valeurs et les métadonnées du raster en entrée.

Dans le tableau chunks, on va mettre les valeurs des chunks souhaitée pour la création du Dask Array (voir : [Dask Array Chunks](https://docs.dask.org/en/stable/array-chunks.html)).

On converti ensuite notre tableau de valeurs en daks array, puis grâce à la commande da.where on multiplie par 10 les valeurs supérieures au seuil indiqué par l'utilisateur. Les autres auront la valeur de nodata renseignée précédemment.

### createRaster

Cette fonction attend deux arguments : le dask array et les métadonnées du raster en entrée.

On converti les valeurs du Dask Array en rasterio.int16 grâce à la fonction astype. Cette étape est paralléliser grâce à Dask, elle va utiliser tous les coeurs de votre machine (voir dans jupyter lab).

On écrit ensuite le nouveau raster grâce à l'option 'w' (write) de rasterio.open.