import subprocess
import concurrent.futures
from utils import print_message

def run_tool(command, tool_name):
    try:
        print_message(f"Lancement de {tool_name} en mode passif...", symbol="=")
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print_message(f"Fin de {tool_name}", symbol="-")
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Erreur lors de l'exécution de {tool_name} : {str(e)}")
        return []

def collect_subdomains(domain, tools):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(run_tool, tool(domain), tool_name): tool_name for tool_name, tool in tools.items()}
        subdomains = set()
        for future in concurrent.futures.as_completed(futures):
            tool_name = futures[future]
            try:
                result = future.result()
                subdomains.update(result)
            except Exception as e:
                print(f"Erreur avec {tool_name}: {str(e)}")
    return list(subdomains)
