import dns.resolver
import sys
from datetime import datetime

results = []

def lookup(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        print(f"\n[{record_type}]")
        for r in answers:
            print(f"  {r.to_text()}")
            results.append((record_type, r.to_text()))
    except dns.resolver.NoAnswer:
        print(f"\n[{record_type}] Sin registros")
    except dns.resolver.NXDOMAIN:
        print(f"[!] Dominio no encontrado: {domain}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[{record_type}] Error: {e}")

def save_results(domain):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"dns_{domain}_{timestamp}.txt"
    with open(filename, "w") as f:
        for record_type, value in results:
            f.write(f"[{record_type}] {value}\n")
    print(f"\n[*] Resultado guardado en {filename}")

def main():
    if len(sys.argv) < 2:
        print(f"Uso: python3 {sys.argv[0]} <dominio>")
        print(f"Ejemplo: python3 {sys.argv[0]} google.com")
        sys.exit(1)

    domain = sys.argv[1]
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME"]

    print(f"[*] DNS lookup — {domain}")

    for record_type in record_types:
        lookup(domain, record_type)

    if results:
        save_results(domain)

if __name__ == "__main__":
    main()