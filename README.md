# parallelisation_process

## Comment visualiser la parallélisation grâce à jupyterlab et dask-labextension ?

- Créer un environnement conda (voir : [meldig/conda](https://github.com/meldig/conda))
- Ajouter tous les packages requis pour faire fonctionner votre programme
- Installer jupyterlab et nodejs :

``conda install jupyterlab <br />
conda install -c conda-forge nodejs``

- Si votre jupyterlab n'est pas en version 3.x : 
``conda update jupyterlab``
- Installer l'extension dask pour jupyterlab : ``pip install dask lab-extension``
