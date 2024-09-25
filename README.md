Voici un modèle de fichier README.md que vous pouvez utiliser pour documenter votre script :

markdown
Copier le code
# Script de Reconnaissance Passive

Ce script permet de scanner des domaines en mode passif à l'aide de différents outils comme Findomain et AssetFinder. Il récupère les sous-domaines, leur code HTTP, leur adresse IP, et enregistre les résultats dans un fichier formaté.

## Fonctionnalités

- Récupération des sous-domaines à l'aide de Findomain et AssetFinder.
- Récupération du code HTTP pour chaque sous-domaine.
- Résolution de l'adresse IP pour chaque sous-domaine.
- Les résultats sont enregistrés dans un fichier au format `domaine,sous-domaine,HTTP_code,port,IP_address,date_time`.
- Exécution des outils en parallèle pour gagner du temps.
- Support pour scanner plusieurs domaines à partir d'un fichier.
- Génération automatique d'un fichier de résultats avec un nom basé sur la date et l'heure du scan.

## Prérequis

Assurez-vous que les outils suivants sont installés :

- `Findomain`
- `AssetFinder`
- `Python 3.x`

Le script propose d'installer automatiquement ces outils si vous ne les avez pas déjà.

## Installation des outils requis

Si les outils ne sont pas installés, le script vous demandera si vous souhaitez les installer. Sinon, vous pouvez les installer manuellement :

### Installation de Findomain

```bash
wget https://github.com/Findomain/Findomain/releases/download/9.0.4/findomain-linux.zip
unzip findomain-linux.zip
chmod +x findomain
sudo mv findomain /usr/local/bin/
Installation d'AssetFinder
Assurez-vous que go est installé, puis installez AssetFinder avec la commande suivante :

bash
Copier le code
go install github.com/tomnomnom/assetfinder@latest
Ajoutez ~/go/bin à votre $PATH :

bash
Copier le code
echo 'export PATH=$PATH:~/go/bin' >> ~/.profile
source ~/.profile
Utilisation
Pour scanner un seul domaine :
bash
Copier le code
python3 reco.py -d example.com
Pour scanner plusieurs domaines à partir d'un fichier :
Créez un fichier texte avec une liste de domaines, un par ligne, puis exécutez :

bash
Copier le code
python3 reco.py -fd domains.txt
Exemple de fichier domains.txt :
Copier le code
example.com
domain2.com
domain3.org
Format de sortie
Les résultats sont enregistrés dans un fichier avec un nom au format suivant :

Copier le code
Scan_du_YYYY-MM-DD_HH-MM_results.txt
Le contenu du fichier suit la structure suivante :

Copier le code
domaine,sous-domaine,HTTP_code,port,IP_address,date_time
Exemple de sortie
Copier le code
example.com,www.example.com,200,0,93.184.216.34,2024-09-25 09:30:41
example.com,blog.example.com,404,0,93.184.216.34,2024-09-25 09:30:42
Remarques
Timeout : Le délai pour les requêtes HTTP est fixé à 4 secondes.
Port : Actuellement, le port est par défaut à 0, mais cette fonctionnalité peut être étendue à l'avenir.
