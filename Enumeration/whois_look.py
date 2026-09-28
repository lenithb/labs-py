import whois
import sys
from datetime import datetime

def lookup(domain):
    try:
        w = whois.whois(domain)
        print(f"\n[*] WHOIS | {domain}")
        print("-" * 40)
        print(f"Registrante   : {w.name or 'N/A'}")
        print(f"Organización  : {w.org or 'N/A'}")
        print(f"País          : {w.country or 'N/A'}")
        print(f"Registrador   : {w.registrar or 'N/A'}")
        print(f"Creado        : {w.creation_date}")
        print(f"Vence         : {w.expiration_date}")
        print(f"Actualizado   : {w.updated_date}")
        print(f"Name servers  : {', '.join(w.name_servers) if w.name_servers else 'N/A'}")
        print(f"Emails        : {', '.join(w.emails) if w.emails else 'N/A'}")
        return w
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

def save_results(domain, w):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"whois_{domain}_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(str(w))
    print(f"\n[*] Resultado guardado en {filename}")

def main():
    if len(sys.argv) < 2:
        print(f"Uso: python3 {sys.argv[0]} <dominio>")
        print(f"Ejemplo: python3 {sys.argv[0]} google.com")
        sys.exit(1)

    domain = sys.argv[1]
    w = lookup(domain)
    save_results(domain, w)

if __name__ == "__main__":
    main()