import subprocess
import xml.etree.ElementTree as ET
import sys
import os
from datetime import datetime

def run_nmap(target, flags="-sV -T4"):
    print(f"[*] Escaneando {target} con flags: {flags}")
    result = subprocess.run(
        ["nmap", flags, "-oX", "-", target],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"[!] Error: {result.stderr}")
        sys.exit(1)
    return result.stdout

def parse_xml(xml_output):
    root = ET.fromstring(xml_output)
    hosts = []

    for host in root.findall("host"):
        addr = host.find("address").get("addr")
        status = host.find("status").get("state")

        ports = []
        for port in host.findall(".//port"):
            port_id = port.get("portid")
            proto = port.get("protocol")
            state = port.find("state").get("state")
            service = port.find("service")
            svc_name = service.get("name", "?") if service is not None else "?"
            svc_version = service.get("version", "") if service is not None else ""
            ports.append({
                "port": port_id,
                "proto": proto,
                "state": state,
                "service": svc_name,
                "version": svc_version
            })

        hosts.append({"ip": addr, "status": status, "ports": ports})

    return hosts

def print_results(hosts):
    for host in hosts:
        print(f"\n[Host] {host['ip']} — {host['status']}")
        print(f"{'Puerto':<10} {'Proto':<6} {'Estado':<10} {'Servicio':<15} Versión")
        print("-" * 60)
        for p in host["ports"]:
            if p["state"] == "open":
                print(f"{p['port']:<10} {p['proto']:<6} {p['state']:<10} {p['service']:<15} {p['version']}")

def save_results(hosts, target):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scan_{target.replace('.', '_')}_{timestamp}.txt"
    with open(filename, "w") as f:
        for host in hosts:
            f.write(f"[Host] {host['ip']} — {host['status']}\n")
            f.write(f"{'Puerto':<10} {'Proto':<6} {'Estado':<10} {'Servicio':<15} Versión\n")
            f.write("-" * 60 + "\n")
            for p in host["ports"]:
                if p["state"] == "open":
                    f.write(f"{p['port']:<10} {p['proto']:<6} {p['state']:<10} {p['service']:<15} {p['version']}\n")
    print(f"\n[*] Resultado guardado en {filename}")

def main():
    if len(sys.argv) < 2:
        print(f"Uso: python3 {sys.argv[0]} <target> [flags]")
        print(f'Ejemplo: python3 {sys.argv[0]} 10.10.10.1 "-sV -T4 -p-"')
        sys.exit(1)

    target = sys.argv[1]
    flags = sys.argv[2] if len(sys.argv) > 2 else "-sV -T4"

    xml_output = run_nmap(target, flags)
    hosts = parse_xml(xml_output)
    print_results(hosts)
    save_results(hosts, target)

if __name__ == "__main__":
    main()