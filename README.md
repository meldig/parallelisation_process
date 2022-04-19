# parallelisation_process

## Comment visualiser la parallélisation grâce à jupyterlab et dask-labextension ?

- Créer un environnement conda (voir : [meldig/conda](https://github.com/meldig/conda))
- Ajouter tous les packages requis pour faire fonctionner votre programme
- Installer jupyterlab et nodejs :

````
conda install jupyterlab 
conda install -c conda-forge nodejs
````
- Si votre jupyterlab n'est pas en version 3.x : 
``conda update jupyterlab``
- Installer l'extension dask pour jupyterlab : ``pip install dask-labextension``
- Lancer jupyter avec la commande : ``jupyter lab``
- Exécuter dans un nouveau notebook :

````
import dask.distributed as dd  
from dask.distributed import Client  
client = Client()
````

- Cliquez ensuite sur l'icône dask dans la toolbar à gauche et cliquez sur la loupe.
- Vous avez maintenant à votre disposition plusieurs éléments de visualisation dask.