import concurrent.futures
from datetime import datetime
from network import get_http_ports_and_ip

def filter_and_write_results(subdomains, domain, output_file):
    unique_subdomains = set(subdomains)
    
    with open(output_file, 'a') as f:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(get_http_ports_and_ip, subdomain): subdomain for subdomain in unique_subdomains}
            
            for future in concurrent.futures.as_completed(futures):
                subdomain, http_codes, ports, ip_address = future.result()
                if "N/A" not in http_codes:  # Enregistre uniquement les sous-domaines valides
                    f.write(f"{domain},{subdomain},{http_codes},{ports},{ip_address},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
