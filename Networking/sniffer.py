from scapy.all import sniff, IP, TCP, UDP, ICMP
import sys

def procesar(pkt):
    if IP in pkt:
        src = pkt[IP].src
        dst = pkt[IP].dst
        proto = pkt[IP].proto

        if TCP in pkt:
            print(f"[TCP]  {src}:{pkt[TCP].sport} → {dst}:{pkt[TCP].dport}")
        elif UDP in pkt:
            print(f"[UDP]  {src}:{pkt[UDP].sport} → {dst}:{pkt[UDP].dport}")
        elif ICMP in pkt:
            print(f"[ICMP] {src} → {dst}  tipo={pkt[ICMP].type}")
        else:
            print(f"[IP]   {src} → {dst}  proto={proto}")

def main():
    interfaz = sys.argv[1] if len(sys.argv) > 1 else "eth0"
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    print(f"[*] Sniffing en {interfaz} — Ctrl+C para detener")
    sniff(iface=interfaz, prn=procesar, count=count, store=False)

if __name__ == "__main__":
    main()