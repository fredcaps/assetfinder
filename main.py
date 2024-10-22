import os
import subprocess
import argparse
import time
from datetime import datetime
from tools import collect_subdomains
from results import filter_and_write_results
from utils import print_message

def main():
    # Message général d'exécution
    print("⚙  Exécution du script de collecte de sous-domaines et génération des rapports...")

    # Définition des arguments du script
    parser = argparse.ArgumentParser(
        description="Script de reconnaissance en mode passif",
        add_help=False  # On désactive l'aide par défaut
    )

    # Ajout manuel de l'option d'aide en français
    parser.add_argument(
        '-h', '--help', action='help', default=argparse.SUPPRESS,
        help="Afficher ce message d'aide et quitter."
    )

    # Argument pour un domaine unique avec description et metavar personnalisés
    parser.add_argument(
        "-d", metavar="DOMAIN", help="Domaine unique (ex: example.com)"
    )

    # Argument pour un fichier de domaines avec description et metavar personnalisés
    parser.add_argument(
        "-fd", metavar="FILE", help="Fichier contenant une liste de domaines"
    )

    # Argument pour générer un rapport minimaliste
    parser.add_argument(
        "--minimaliste", action="store_true", help="Générer un rapport minimaliste au lieu des rapports complets"
    )

    args = parser.parse_args()

    # Si aucun argument n'est passé, afficher un message d'aide
    if not args.d and not args.fd:
        parser.print_help()  # Affiche le message d'aide
        print("\n⚠️  Erreur : Vous devez fournir soit un domaine avec l'option -d, soit un fichier avec l'option -fd.\n")
        return

    # Outils de collecte de sous-domaines
    tools = {
        "findomain": lambda domain: ["findomain", "-t", domain],
        "assetfinder": lambda domain: ["assetfinder", domain],
        # "amass": lambda domain: ["amass", "enum", "-passive", "-d", domain],  # Commenté
        "subfinder": lambda domain: ["subfinder", "-d", domain]               # Commenté
    }

    # Vérification des domaines
    if args.d:
        domains = [args.d]
    elif args.fd and os.path.exists(args.fd):
        with open(args.fd) as f:
            domains = f.read().splitlines()
    else:
        print("Veuillez fournir un domaine avec -d ou un fichier avec -fd.")
        return

    # Début du traitement
    start_time = time.time()
    output_file = f"Scan_du_{datetime.now().strftime('%Y-%m-%d_%H-%M')}_results.txt"

    # Traitement des domaines
    for domain in domains:
        print(f"⚙  Traitement de {domain}...")
        subdomains = collect_subdomains(domain, tools)
        filter_and_write_results(subdomains, domain, output_file)
        #print(f"⚙  Résultats pour {domain} enregistrés dans {output_file}.")

    # Durée d'exécution
    duration = time.time() - start_time
    print_message(f"⚙  Le script s'est terminé en {duration:.2f} secondes.")

    # Si l'argument minimaliste est passé, exécuter rapport_minimaliste.py
    if args.minimaliste:
        try:
            print("⚙  Exécution du script rapport_minimaliste.py...")
            subprocess.run(["python", "rapport_minimaliste.py", output_file, "-o", "Rapport_minimaliste"], check=True)
            print(f"⚙  Le script rapport_minimaliste.py a été exécuté avec succès.")
            
            # Ajout du lien pour le fichier HTML minimaliste
            minimaliste_html_report = f"Rapport_minimaliste/rapport_scans_{datetime.now().strftime('%Y-%m-%d-%H-%M')}.html"
            if os.path.exists(minimaliste_html_report):
                print(f"⚙  Le rapport minimaliste HTML a été généré avec succès. Vous pouvez consulter le rapport ici : file://{os.path.abspath(minimaliste_html_report)}")
            else:
                print(f"⚠️  Le fichier HTML minimaliste {minimaliste_html_report} n'a pas été trouvé.")
                
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Erreur lors de l'exécution de rapport_minimaliste.py : {str(e)}")
    else:
        # Si l'argument minimaliste n'est PAS passé, exécuter database.py et Generateur_rapport.py
        try:
            print("⚙  Exécution du script database.py avec le fichier généré...")
            subprocess.run(["python", "database.py", output_file], check=True)
            print(f"⚙  Le script database.py a été exécuté avec succès")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Erreur lors de l'exécution de database.py : {str(e)}")

        # Exécution du script Generateur_rapport.py
        try:
            print("⚙  Exécution du script Generateur_rapport.py...")
            subprocess.run(["python", "Generateur_rapport.py"], check=True)
            print("⚙  Le script Generateur_rapport.py a été exécuté avec succès.")
            
            # Ajout d'une phrase avec le lien du fichier HTML généré
            html_report = f"rapport_scans/rapport_scans_{datetime.now().strftime('%Y-%m-%d-%H-%M')}.html"
            if os.path.exists(html_report):
                print(f"⚙  Le rapport HTML a été généré avec succès. Vous pouvez consulter le rapport ici : file://{os.path.abspath(html_report)}")
            else:
                print(f"⚠️  Le fichier HTML {html_report} n'a pas été trouvé.")

        except subprocess.CalledProcessError as e:
            print(f"⚠️  Erreur lors de l'exécution de Generateur_rapport.py : {str(e)}")

    # Suppression du fichier de résultats à la fin du script
    if os.path.exists(output_file):
        os.remove(output_file)

if __name__ == "__main__":
    main()
