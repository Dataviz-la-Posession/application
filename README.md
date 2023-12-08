# Application streamlit

### Création de l'environement virtuel (Obligatoire !)
Il faut ouvrir votre terminal dans le dossier du projet (Ou VScode)\
La création de l'environnement virtuel ne se fait qu'une seule fois
```
 python -m venv .venv
```

### Activation de l'environement virtuel (Obligatoire avec Powershell)
Ce dernier ira contenir toutes les dépendances de notre projet
```
.\.venv\Scripts\activate
```

### Installation des dépendances projet dans l'environnement virtuel
```
pip install -r requirements.txt
```

### Démarrage de l'application
Il ira cibler notre fichier de démarrage **`main.py`** dans le dossier app
```
streamlit run app\main.py
```