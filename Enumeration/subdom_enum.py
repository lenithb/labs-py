import requests
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

found = []

def check_subdomain(domain, word):
    subdomain = f"http://{word.strip()}.{domain}"
    try:
        response = requests.get(subdomain, timeout=3)
        print(f"[{response.status_code}] {subdomain}")
        found.append((response.status_code, subdomain))
    except:
        pass

def save_results(domain):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"subdomains_{domain}_{timestamp}.txt"
    with open(filename, "w") as f:
        for status, sub in found:
            f.write(f"[{status}] {sub}\n")
    print(f"[*] Resultado guardado en {filename}")

def main():
    if len(sys.argv) < 3:
        print(f"Uso: python3 {sys.argv[0]} <dominio> <wordlist>")
        print(f"Ejemplo: python3 {sys.argv[0]} example.com /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt")
        sys.exit(1)

    domain = sys.argv[1]
    wordlist = sys.argv[2]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 50

    try:
        with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
            words = f.readlines()
    except FileNotFoundError:
        print(f"[!] Wordlist no encontrada: {wordlist}")
        sys.exit(1)

    print(f"[*] Enumerando subdominios de {domain} con {len(words)} palabras")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        for word in words:
            executor.submit(check_subdomain, domain, word)

    print(f"\n[*] {len(found)} subdominios encontrados")
    if found:
        save_results(domain)

if __name__ == "__main__":
    main()