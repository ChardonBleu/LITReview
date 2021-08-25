# Gestion de tournois d'échec

Projet 9 de la formation DA python d'Openclassrooms.

Site web de partage de critiques de livres et textes.

Installation
---
Télécharger les dossier et fichier et les copier dans un dossier de votre choix
Dans la console aller dans ce dossier choisi.

Environnement virtuel
---
https://docs.python.org/fr/3/library/venv.html?highlight=venv

Créer un environnement virtuel: 

```bash
python -m venv env
```

Activer cet environnement virtuel:
sur windows dans Visual Studio Code: 
```bash 
. env/Scripts/activate 
```
sur mac ou linux: 
```bash 
source env/bin/activate 
```
Packages
---

Puis installer les modules necessaires:
```bash 
python -m pip -r requirements.txt
```

Exécution
---
Se mettre dans le répertoire contenant le dossier application et taper dans la console:

```bash 
python manage.py runserver
```
Le serveur de développement se lance et son adresse s'affiche dans la console:
Django version 3.2.5, using settings 'LITReview.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

Aller sur le l'adresse http proposée pour consulter le site.


Générer un rapport flake-8 html
---

Se mettre dans le répertoire dont on veut scanner les fichiers *.py. Par exemple pour library:
```bash 
cd library
```

Puis dans la console excécuter:
```bash 
flake8 --format=html --htmldir=flake-report
```
Un nouveau rapport flake8 est généré. Aller dans le répertoire flake-report créé dans le répertoire library et ouvrir le fichier index.html dans un navigateur web.
Changer de répertoire pour tester d'autres fichiers *.py

Lancer les tests
---

Le fichier pytest.ini a été configuré pour exécuter coverage en même temps que pytest:
```bash 
addopts = --nomigrations --cov=. --cov-report=html
```

Depuis le répertoire racine lancer pytest
```bash 
pytest
```

Après excécution des tests aller consulter le résulat du coverage dans le dossier nouvellement créé htmlcov en ouvrant le fichier index.html dans un navigateur.


Ressources utilisées
---

Livres:
    Django 3 by exemples - Antonio Melé

Ressources web:

    Les webinaires Django d'Aurélien Massé:

    https://register.gotowebinar.com/recording/viewRecording/1222617758068117773/3364927104570569231/mentor@chappuis.net?registrantKey=4040626477816493579&type=ABSENTEEEMAILRECORDINGLINK

    https://register.gotowebinar.com/recording/viewRecording/3524698239153452814/9120062335571565067/mentor@chappuis.net?registrantKey=4082015394508660237&type=ABSENTEEEMAILRECORDINGLINK

    La documentation officielle de Django:

    https://docs.djangoproject.com/en/3.0/

    Les tutos de Tibault Houdon et son excellent site Docstring:

    https://www.docstring.fr/

    Le cours Boostrap d'Openclassrooms:

    https://openclassrooms.com/fr/courses/6391096-creez-des-sites-web-responsive-avec-bootstrap-4

    La documentation officielle de Bootstrap:

    https://getbootstrap.com/docs/4.3/getting-started/introduction/

Remerciements
---

Un très grand merci à mes trois mentors successifs:

Aurélien Massé pour ses excelletns webinaire d'introduction à Django,

Thierry Chappuis pour tous ses webinaires, lunchinaires, et la richesse de ses interventions sur le discord
http://discord.pythonclassmates.org/

Sandrine Suire pour sa trés grande disponibilité et son profond investissement dans le suivi de ses étudiants.

