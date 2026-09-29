import requests
import sys
from datetime import datetime

def grab_headers(url):
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        print(f"\n[*] {url} — {response.status_code}")
        print("-" * 40)
        for key, value in response.headers.items():
            print(f"{key:<30} {value}")
        return response.headers, response.status_code
    except requests.ConnectionError:
        print(f"[!] No se pudo conectar a {url}")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

def save_results(url, headers, status):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    domain = url.replace("https://", "").replace("http://", "").replace("/", "_")
    filename = f"headers_{domain}_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(f"URL: {url}\n")
        f.write(f"Status: {status}\n")
        f.write("-" * 40 + "\n")
        for key, value in headers.items():
            f.write(f"{key}: {value}\n")
    print(f"\n[*] Resultado guardado en {filename}")

def main():
    if len(sys.argv) < 2:
        print(f"Uso: python3 {sys.argv[0]} <url>")
        print(f"Ejemplo: python3 {sys.argv[0]} http://10.10.10.1")
        sys.exit(1)

    url = sys.argv[1]
    if not url.startswith("http"):
        url = f"http://{url}"

    headers, status = grab_headers(url)
    save_results(url, headers, status)

if __name__ == "__main__":
    main()