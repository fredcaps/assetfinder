
# README : Outil de Collecte et Analyse de Sous-domaines

## 1. Introduction

Cet outil permet de collecter, analyser et vérifier l'accessibilité des sous-domaines pour un domaine cible. Il utilise plusieurs outils externes pour effectuer la collecte des sous-domaines, ainsi que des vérifications réseau telles que les codes HTTP, les adresses IP et la disponibilité des ports.

---

## 2. Installation

Pour installer et configurer correctement l'outil, vous devez suivre deux tutoriels distincts :

### 2.1. Tutoriel d'installation des outils

Suivez les étapes décrites dans le fichier **[Tutoriel_Installation_Outils.txt](Tutoriel_Installation_Outils.txt)** pour installer les outils externes suivants :
- `Findomain`
- `Subfinder`
- `Assetfinder`
- `Amass`

### 2.2. Tutoriel d'installation et de configuration de PostgreSQL

Le fichier **[Installation_Configuration_PostgreSQL.txt](Installation_Configuration_PostgreSQL.txt)** explique comment installer et configurer PostgreSQL afin de stocker les résultats des scans dans une base de données.

Veuillez suivre ces fichiers dans l'ordre pour vous assurer que tous les composants de l'outil sont correctement installés et configurés.

---

## 3. Fonctionnement de l'Outil

### 3.1. Collecte des Sous-domaines

L'outil utilise plusieurs collecteurs de sous-domaines comme `Findomain`, `Subfinder`, `Assetfinder`, et `Amass` pour obtenir une liste complète des sous-domaines d'un domaine cible.

### 3.2. Validation des Sous-domaines

Les sous-domaines collectés sont ensuite vérifiés pour leur accessibilité. Les ports standards (80, 443) sont scannés pour déterminer la disponibilité des services HTTP et HTTPS, ainsi que d'autres informations réseau pertinentes.

### 3.3. Stockage des Résultats

Les résultats des scans (sous-domaines, adresses IP, codes HTTP) sont stockés dans une base de données PostgreSQL pour permettre un suivi et une analyse ultérieure.

### 3.4. Fonctionnalité : Rapport Minimaliste

L'outil propose également une fonctionnalité de **rapport minimaliste**, qui permet de générer un rapport simple sans que les données ne soient sauvegardées dans la base de données. Cette fonctionnalité est utile lorsque vous souhaitez obtenir rapidement un aperçu des résultats sans stockage persistant.

### 3.5. Rapports

Un rapport complet est généré à la fin du processus, contenant les informations collectées, ainsi qu'un comparatif avec les scans précédents pour identifier les changements (nouveaux sous-domaines, sous-domaines supprimés, modifications des codes HTTP).

---

## 4. Exécution

Après avoir suivi les étapes d'installation, vous pouvez exécuter l'outil avec la commande suivante :

> python3 main.py

---

## 5. Remarques Supplémentaires

Si des erreurs surviennent lors de l'exécution de l'outil, assurez-vous que tous les outils externes sont correctement installés et que les permissions d'exécution sont en place. Consultez également les fichiers de tutoriels pour vérifier la configuration de PostgreSQL et des autres outils.
