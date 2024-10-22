# Tutoriel : Installation des Outils pour le Projet

## 1. Mise à Jour du Système

Avant de commencer, vous devez vous assurer que votre système est à jour. Utilisez la commande suivante :

> sudo apt update && sudo apt upgrade -y

---

## 2. Installer Python et les Dépendances Python

Vous devez installer Python ainsi que le gestionnaire de paquets `pip` :

> sudo apt install python3 python3-pip -y

Ensuite, installez la bibliothèque `requests` :

> pip install requests

---

## 3. Installer les Outils Externes

### 3.1. Installation de Findomain

Téléchargez et installez Findomain avec les commandes suivantes :

> wget https://github.com/findomain/findomain/releases/download/4.0.0/findomain-linux  
> chmod +x findomain-linux  
> sudo mv findomain-linux /usr/local/bin/findomain

---

### 3.2. Installation de Subfinder

Assurez-vous d'avoir installé Go avant d'exécuter cette commande. Si Go n'est pas installé, utilisez la commande suivante :

> sudo apt install golang-go -y

Ensuite, installez Subfinder :

> GO111MODULE=on go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

---

### 3.3. Installation de Amass

Pour installer Amass, utilisez la commande suivante :

> sudo apt install amass -y

---

### 3.4. Installation de Httprobe

Installez Httprobe avec la commande suivante :

> go install github.com/tomnomnom/httprobe@latest

---

### 3.5. Installation de Aquatone

Pour capturer des captures d'écran des sous-domaines, installez Aquatone avec les commandes suivantes :

> wget https://github.com/michenriksen/aquatone/releases/download/v1.7.0/aquatone_linux_amd64_1.7.0.zip  
> unzip aquatone_linux_amd64_1.7.0.zip  
> sudo mv aquatone /usr/local/bin/

---

## 4. Vérification des Installations

Après avoir installé chaque outil, vérifiez que tout fonctionne correctement en exécutant les commandes suivantes :

> findomain --version  
> subfinder --version  
> amass -version  
> httprobe --version  
> aquatone --version

---

## 5. Exécution du Script Principal

Une fois les outils installés, vous pouvez exécuter le script principal avec la commande suivante :

> python3 main.py

---

## 6. Remarques Supplémentaires

Si un outil ne s'exécute pas correctement, assurez-vous que les permissions sont correctement configurées. Vous pouvez utiliser la commande suivante pour corriger les permissions :

> chmod +x [nom_de_l'outil]

Vous pouvez également créer un environnement virtuel pour isoler les dépendances Python avec les commandes suivantes :

> python3 -m venv venv  
> source venv/bin/activate  
> pip install -r requirements.txt

---

Ce guide vous permet d'installer et de configurer tous les outils nécessaires pour le bon fonctionnement de votre projet. Si des ajustements sont nécessaires, assurez-vous de vérifier les configurations spécifiques dans vos fichiers Python.
