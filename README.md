# parallelisation_process

## Comment visualiser la parallélisation grâce à jupyterlab et dask-labextension ?

#### Mettre en place le notebook

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

```` python
import dask.distributed as dd  
from dask.distributed import Client  
client = Client()
````

- Cliquez ensuite sur l'icône dask dans la toolbar à gauche et cliquez sur la loupe.
- Vous avez maintenant à votre disposition plusieurs éléments de visualisation dask.

#### Utilisation du notebook

Dans le notebook, vous aurez à disposition plusieurs sections dans lesquelles vous pourrez écrire et exécuter du code.
- Pour exécuter une portion de code : Ctrl + Entrée
- Pour exécuter une portion de code et créer une nouvelle section : Shift + Entrée

L'intérêt de dask-labextension est de pouvoir visualiser vos jeux de données, mais aussi de voir comment les tâches s'exécutent.
Pour cela, je vous recommande d'ouvrir les deux fenêtres suivantes :
- Task Stream
- Progress

Enfin, pour la visualisation des divers objets dask, vous pouvez procéder comme ceci :
- En fin de section (dernière ligne), écrivez le nom de votre variable qui contient l'objet que vous voulez visualiser (Dask Array par exemple). Celui-ci apparaîtra juste en dessous avec différentes information.
- Si vous utilisez Delayed, la fonction visualize() vous permettra d'afficher le graphe des tâches. Vous pourrez l'exéctuer grâce à la fonction compute().
