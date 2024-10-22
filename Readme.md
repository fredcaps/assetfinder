# README : Outil de Collecte et Analyse de Sous-domaines

## 1. Introduction

Cet outil permet de collecter, analyser et vérifier l'accessibilité des sous-domaines pour un domaine cible. Il utilise plusieurs outils externes pour effectuer la collecte des sous-domaines, ainsi que des vérifications réseau telles que les codes HTTP, les adresses IP et la disponibilité des ports.

Les résultats sont stockés dans une base de données PostgreSQL pour un suivi continu, et des rapports peuvent être générés pour comparer les scans actuels avec les précédents.

---

## 2. Installation et Configuration

### 2.1. Installation des outils externes

Suivez les étapes décrites dans le fichier **[Tutoriel_Installation_Outils.txt](Tutoriel_Installation_Outils.txt)** pour installer les outils externes suivants :
- `Findomain`
- `Subfinder`
- `Assetfinder`
- `Amass`

### 2.2. Installation et configuration de PostgreSQL

Le fichier **[Installation_Configuration_PostgreSQL.txt](Installation_Configuration_PostgreSQL.txt)** vous guidera à travers l'installation de PostgreSQL et la création de la base de données `scans` avec les bonnes configurations.

### 2.3. Configuration du script Python

Modifiez le fichier `database.py` pour définir correctement les informations de connexion à PostgreSQL :

```python
def connect_db():
    connection = psycopg2.connect(
        database=os.getenv("DB_NAME", "scans"),        # Nom de la base de données
        user=os.getenv("DB_USER", "scanner"),          # Nom d'utilisateur PostgreSQL
        password=os.getenv("DB_PASSWORD", "password"), # Mot de passe PostgreSQL
        host=os.getenv("DB_HOST", "localhost"),        # Adresse du serveur PostgreSQL
        port=os.getenv("DB_PORT", "5432")              # Port PostgreSQL
    )
    return connection
```

---

## 3. Fonctionnement de l'Outil

### 3.1. Collecte des Sous-domaines

L'outil utilise plusieurs collecteurs de sous-domaines comme `Findomain`, `Subfinder`, `Assetfinder`, et `Amass` pour obtenir une liste complète des sous-domaines d'un domaine cible.

### 3.2. Validation des Sous-domaines

Les sous-domaines collectés sont ensuite vérifiés pour leur accessibilité. Les ports standards (80, 443) sont scannés pour déterminer la disponibilité des services HTTP et HTTPS, ainsi que d'autres informations réseau pertinentes. Ce traitement est effectué par le fichier `network.py`.

### 3.3. Stockage des Résultats dans PostgreSQL

Les résultats des scans (sous-domaines, adresses IP, codes HTTP) sont stockés dans une base de données PostgreSQL à l'aide du fichier `results.py`. Chaque scan est enregistré avec un identifiant unique `scan_id`.

---

## 4. Génération de Rapports

L'outil peut générer deux types de rapports :

1. **Rapport complet** : Ce rapport contient toutes les informations collectées et est sauvegardé dans la base de données pour un suivi ultérieur.
2. **Rapport minimaliste** : Ce rapport est généré sans enregistrer les données dans la base de données, permettant une visualisation rapide des résultats.

La génération des rapports est gérée par `Generateur_rapport.py` et `rapport_minimaliste.py`.

---

## 5. Exécution

L'outil peut être exécuté avec les commandes suivantes :

1. Pour traiter un domaine spécifique :

> python3 main.py -d domaine_cible


2. Pour traiter une liste de domaines contenue dans un fichier :

> python3 main.py -fd fichier_de_domaines.txt


3. Pour générer un rapport minimaliste sans sauvegarder les résultats dans la base de données :

> python3 main.py -d domaine_cible --minimaliste

4. Pour générer un rapport minimaliste sans sauvegarder les résultats dans la base de données avec une liste de domaine dans un fichier:

> python3 main.py -fd fichier_de_domaines.txt --minimaliste


---

## 6. Remarques Supplémentaires

Si vous rencontrez des erreurs lors de l'exécution, assurez-vous que tous les outils externes sont correctement installés et configurés. Consultez également les fichiers de tutoriels pour vérifier la configuration de PostgreSQL et des autres outils.
