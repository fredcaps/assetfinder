import subprocess
import argparse
import time
from datetime import datetime
from tools import collect_subdomains
from results import filter_and_write_results
from utils import print_message
import os

def main():
    # Message général d'exécution
    print("⚙  Exécution du script de collecte de sous-domaines et génération des rapports...")

    parser = argparse.ArgumentParser(description="Script de reconnaissance en mode passif")
    parser.add_argument("-d", help="Domaine unique (ex: example.com)")
    parser.add_argument("-fd", help="Fichier contenant une liste de domaines")
    args = parser.parse_args()

    tools = {
        "findomain": lambda domain: ["findomain", "-t", domain],
        "assetfinder": lambda domain: ["assetfinder", domain],
        # "amass": lambda domain: ["amass", "enum", "-passive", "-d", domain],  # Commenté
        "subfinder": lambda domain: ["subfinder", "-d", domain]               # Commenté
    }

    if args.d:
        domains = [args.d]
    elif args.fd and os.path.exists(args.fd):
        with open(args.fd) as f:
            domains = f.read().splitlines()
    else:
        print("Veuillez fournir un domaine avec -d ou un fichier avec -fd.")
        return

    start_time = time.time()
    output_file = f"Scan_du_{datetime.now().strftime('%Y-%m-%d_%H-%M')}_results.txt"

    # Boucle de traitement des domaines sans barre de progression
    for domain in domains:
        print(f"⚙  Traitement de {domain}...")
        subdomains = collect_subdomains(domain, tools)
        filter_and_write_results(subdomains, domain, output_file)
        print(f"⚙  Résultats pour {domain} enregistrés dans {output_file}.")

    duration = time.time() - start_time
    # Modification du message pour enlever les bordures supplémentaires
    print_message(f"⚙  Le script s'est terminé en {duration:.2f} secondes.")

    # Exécution du script database.py avec le fichier généré en argument
    try:
        print("⚙  Exécution du script database.py avec le fichier généré...")
        subprocess.run(["python", "database.py", output_file], check=True)
        print(f"⚙  Le script database.py a été exécuté avec succès avec le fichier {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Erreur lors de l'exécution de database.py : {str(e)}")

    # Exécution du script Generateur_rapport.py
    try:
        print("⚙  Exécution du script Generateur_rapport.py...")
        subprocess.run(["python", "Generateur_rapport.py"], check=True)
        print("⚙  Le script Generateur_rapport.py a été exécuté avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Erreur lors de l'exécution de Generateur_rapport.py : {str(e)}")

if __name__ == "__main__":
    main()
