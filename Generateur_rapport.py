import os
import psycopg2
from datetime import datetime
import pytz

# Connexion à la base de données
conn = psycopg2.connect(
    dbname="scans",         # Nom de votre base de données actuelle
    user="scanner",         # Votre utilisateur PostgreSQL
    password="password",    # Mot de passe PostgreSQL
    host="localhost"
)
cur = conn.cursor()

# Récupération de tous les scans
cur.execute("SELECT * FROM scan_results ORDER BY scan_id DESC, scan_time DESC")
scans = cur.fetchall()

# Fonction pour générer le rapport HTML
def generate_html_report(scans):
    # Convertir l'heure en heure de Montréal
    montreal_tz = pytz.timezone('America/Montreal')

    # Calculer les statistiques globales
    total_scans = len(set(scan[0] for scan in scans))
    total_subdomains = len(set(scan[2] for scan in scans))
    total_domains = len(set(scan[1] for scan in scans))

    # Générer l'entête du rapport avec le bon design pour les statistiques
    html = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Rapport de Scan</title>
        <style>
            body {{
                font-family: 'Roboto', sans-serif;
                margin: 20px;
                background-color: #f9f9f9;
                color: #333;
            }}
            h1, h2, h3 {{
                color: #4CAF50;
            }}
            .stat-box {{
                padding: 10px;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                background-color: #f1f1f1;
                color: #4CAF50;
                font-weight: bold;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                text-align: center;
                width: fit-content;
                display: inline-block;
                margin-right: 15px;
            }}
            .stats {{
                display: flex;
                gap: 20px;
                margin-bottom: 20px;
                justify-content: flex-start;
            }}
            .added {{
                background-color: lightgreen;
            }}
            .removed {{
                background-color: lightcoral;
            }}
            .modified {{
                background-color: lightyellow;
            }}
            .unchanged {{
                background-color: lightgray;
            }}
            .scan-result {{
                border: 1px solid #ddd;
                padding: 10px;
                margin-bottom: 20px;
                border-radius: 5px;
                background-color: #fff;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #4CAF50;
                color: white;
            }}
            .legend-table {{
                width: 50%;
                margin: 20px auto;
                border: 1px solid #ddd;
                text-align: center;
            }}
            .legend-table td {{
                padding: 10px;
                font-weight: bold;
            }}
            .old-value {{
                color: red;
                font-weight: bold;
            }}
            .new-value {{
                color: green;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>Rapport de Scan du {date}</h1>
        <h3>Légende des Codes Couleurs</h3>
        <table class="legend-table">
            <tr>
                <td style="background-color: lightgreen;">Ajouté</td>
                <td style="background-color: lightyellow;">Modifié</td>
                <td style="background-color: lightcoral;">Supprimé</td>
                <td style="background-color: lightgray;">Déjà présent</td>
            </tr>
        </table>
        <div class="stats">
            <div class="stat-box">Total de Scans: {total_scans}</div>
            <div class="stat-box">Total de Sous-domaines Scannés: {total_subdomains}</div>
            <div class="stat-box">Total de Domaines Scannés: {total_domains}</div>
        </div>
    """.format(
        total_scans=total_scans, 
        total_subdomains=total_subdomains, 
        total_domains=total_domains, 
        date=datetime.now(montreal_tz).strftime("%Y-%m-%d à %H:%M")
    )

    scan_data = {}
    for scan in scans:
        scan_id, domain, subdomain, http_code, port, ip_address, scan_time = scan
        if scan_id not in scan_data:
            scan_data[scan_id] = []
        scan_data[scan_id].append((domain, subdomain, http_code, port, ip_address, scan_time))

    sorted_scan_ids = sorted(scan_data.keys(), reverse=True)
    for i, scan_id in enumerate(sorted_scan_ids):
        current_scan = scan_data[scan_id]
        previous_scan = scan_data[sorted_scan_ids[i + 1]] if i + 1 < len(sorted_scan_ids) else []

        # Initialisation des ajouts, modifications et suppressions pour chaque scan
        additions = 0
        modifications = 0
        deletions = 0

        # Compte des sous-domaines du scan actuel
        current_subdomains_count = len(current_scan)

        previous_scan_dict = {(domain, subdomain): (http_code, port, ip_address) for domain, subdomain, http_code, port, ip_address, scan_time in previous_scan}

        # Parcourir le scan actuel pour compter les ajouts et les modifications
        current_scan_keys = set()
        for domain, subdomain, http_code, port, ip_address, scan_time in current_scan:
            key = (domain, subdomain)
            current_scan_keys.add(key)
            if key not in previous_scan_dict:
                additions += 1
            elif (http_code != previous_scan_dict[key][0] or port != previous_scan_dict[key][1] or ip_address != previous_scan_dict[key][2]):
                modifications += 1

        # Compter les suppressions en comparant avec le scan précédent
        for domain, subdomain in previous_scan_dict:
            if (domain, subdomain) not in current_scan_keys:
                deletions += 1

        # Maintenant que les compteurs sont calculés, insérez-les dans le HTML
        html += f"""
        <div class="scan-result">
            <h2>Rapport du Scan ID: {scan_id}</h2>
            <h3>Date: {current_scan[0][5].astimezone(montreal_tz).strftime("%Y-%m-%d %H:%M:%S")}</h3>
            <div class="stats">
                <div class="stat-box">Sous-domaines: {current_subdomains_count}</div>
                <div class="stat-box">Ajouts: {additions}</div>
                <div class="stat-box">Modifications: {modifications}</div>
                <div class="stat-box">Suppressions: {deletions}</div>
            </div>
            <h2>Résultats des Scans</h2>
            <table>
                <tr>
                    <th>Domaine</th>
                    <th>Sous-domaine</th>
                    <th>Code HTTP</th>
                    <th>Port</th>
                    <th>Adresse IP</th>
                    <th>Heure du Scan</th>
                </tr>
        """

        # Générer les lignes du tableau avec les classes appropriées
        for domain, subdomain, http_code, port, ip_address, scan_time in current_scan:
            key = (domain, subdomain)
            if key not in previous_scan_dict:
                # Ajouté
                row_class = "added"
                html += f"""
                <tr class="{row_class}">
                    <td>{domain}</td>
                    <td>{subdomain}</td>
                    <td>{http_code}</td>
                    <td>{port}</td>
                    <td>{ip_address}</td>
                    <td>{scan_time.astimezone(montreal_tz).strftime("%Y-%m-%d %H:%M:%S")}</td>
                </tr>
                """
            elif (http_code != previous_scan_dict[key][0] or port != previous_scan_dict[key][1] or ip_address != previous_scan_dict[key][2]):
                # Modifié
                row_class = "modified"
                prev_http_code, prev_port, prev_ip_address = previous_scan_dict[key]

                # Comparer chaque champ et mettre en évidence les changements
                if http_code != prev_http_code:
                    http_code_display = f"<span class='old-value'>{prev_http_code}</span> &rarr; <span class='new-value'>{http_code}</span>"
                else:
                    http_code_display = f"{http_code}"

                if port != prev_port:
                    port_display = f"<span class='old-value'>{prev_port}</span> &rarr; <span class='new-value'>{port}</span>"
                else:
                    port_display = f"{port}"

                if ip_address != prev_ip_address:
                    ip_address_display = f"<span class='old-value'>{prev_ip_address}</span> &rarr; <span class='new-value'>{ip_address}</span>"
                else:
                    ip_address_display = f"{ip_address}"

                html += f"""
                <tr class="{row_class}">
                    <td>{domain}</td>
                    <td>{subdomain}</td>
                    <td>{http_code_display}</td>
                    <td>{port_display}</td>
                    <td>{ip_address_display}</td>
                    <td>{scan_time.astimezone(montreal_tz).strftime("%Y-%m-%d %H:%M:%S")}</td>
                </tr>
                """
            else:
                # Inchangé
                row_class = "unchanged"
                html += f"""
                <tr class="{row_class}">
                    <td>{domain}</td>
                    <td>{subdomain}</td>
                    <td>{http_code}</td>
                    <td>{port}</td>
                    <td>{ip_address}</td>
                    <td>{scan_time.astimezone(montreal_tz).strftime("%Y-%m-%d %H:%M:%S")}</td>
                </tr>
                """

        # Ajouter les suppressions
        for domain, subdomain in previous_scan_dict:
            if (domain, subdomain) not in current_scan_keys:
                # Suppression
                prev_http_code, prev_port, prev_ip_address = previous_scan_dict[(domain, subdomain)]
                html += f"""
                <tr class="removed">
                    <td>{domain}</td>
                    <td>{subdomain}</td>
                    <td>{prev_http_code}</td>
                    <td>{prev_port}</td>
                    <td>{prev_ip_address}</td>
                    <td></td>
                </tr>
                """

        html += """
        </table>
        </div>
        """

    html += """
    </body>
    </html>
    """

    # Créer le répertoire 'rapport_scans' s'il n'existe pas
    if not os.path.exists("rapport_scans"):
        os.makedirs("rapport_scans")

    # Générer le nom de fichier avec la date et l'heure actuelles
    current_time = datetime.now(montreal_tz).strftime("%Y-%m-%d-%H-%M")
    filename = f"rapport_scans/rapport_scans_{current_time}.html"

    # Écrire le rapport HTML dans le fichier
    with open(filename, "w") as file:
        file.write(html)

    # Afficher un message avec le lien et le nom du fichier généré
    print(f"Génération terminée ! Le rapport a été enregistré sous le nom : {filename}")

# Générer le rapport HTML
generate_html_report(scans)

# Fermer la connexion à la base de données
cur.close()
conn.close()
