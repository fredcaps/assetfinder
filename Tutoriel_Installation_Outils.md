# Tutoriel : Installation des Outils et Modules pour le Projet

## 1. Mise à Jour du Système

Avant de commencer, vous devez vous assurer que votre système est à jour. Utilisez la commande suivante :

> sudo apt update && sudo apt upgrade -y

---

## 2. Installer Python et les Dépendances Python

Vous devez installer Python ainsi que le gestionnaire de paquets `pip` :

> sudo apt install python3 python3-pip -y

Ensuite, installez les bibliothèques Python requises :

> pip install psycopg2-binary pytz

Ces bibliothèques sont nécessaires pour les connexions à la base de données et la gestion des fuseaux horaires.

---

## 3. Installer les Outils Externes

### 3.1. Installation de Findomain

Téléchargez et installez Findomain avec les commandes suivantes :

> wget https://github.com/findomain/findomain/releases/download/4.0.0/findomain-linux  
> chmod +x findomain-linux  
> sudo mv findomain-linux /usr/local/bin/findomain

---

### 3.2. Installation de Subfinder

Assurez-vous d'avoir Go installé. Sinon, utilisez la commande suivante :

> sudo apt install golang-go -y

Ensuite, installez Subfinder :

> GO111MODULE=on go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

---

### 3.3. Installation d'Assetfinder

Installez Assetfinder avec la commande suivante :

> go install github.com/tomnomnom/assetfinder@latest

---

### 3.4. Installation de Amass

Installez Amass avec la commande suivante :

> sudo apt install amass -y

---

## 4. Vérification des Installations

Après avoir installé chaque outil, vérifiez que tout fonctionne correctement en exécutant les commandes suivantes :

> findomain --version  
> subfinder --version  
> assetfinder --version  
> amass -version

---

## 5. Exécution du Script Principal

Une fois les outils et modules installés, vous pouvez exécuter le script principal avec la commande suivante :

> python3 main.py

---


Ce guide vous permet d'installer et de configurer les outils et modules nécessaires pour le bon fonctionnement.
