import requests
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

found = []

def check_dir(url, word):
    target = f"{url}/{word.strip()}"
    try:
        response = requests.get(target, timeout=3)
        if response.status_code not in [404, 400, 403]:
            print(f"[{response.status_code}] {target}")
            found.append((response.status_code, target))
    except:
        pass

def save_results(url):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = url.replace("https://", "").replace("http://", "").replace("/", "_")
    filename = f"dirs_{domain}_{timestamp}.txt"
    with open(filename, "w") as f:
        for status, path in found:
            f.write(f"[{status}] {path}\n")
    print(f"[*] Resultado guardado en {filename}")

def main():
    if len(sys.argv) < 3:
        print(f"Uso: python3 {sys.argv[0]} <url> <wordlist>")
        print(f"Ejemplo: python3 {sys.argv[0]} http://10.10.10.1 /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt")
        sys.exit(1)

    url = sys.argv[1].rstrip("/")
    wordlist = sys.argv[2]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 50

    try:
        with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
            words = f.readlines()
    except FileNotFoundError:
        print(f"[!] Wordlist no encontrada: {wordlist}")
        sys.exit(1)

    print(f"[*] Enumerando {url} con {len(words)} palabras — {workers} workers")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        for word in words:
            executor.submit(check_dir, url, word)

    print(f"\n[*] {len(found)} directorios encontrados")
    if found:
        save_results(url)

if __name__ == "__main__":
    main()