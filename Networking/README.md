# Networking

Scripts de redes usando sockets a bajo nivel.

## Contenido

| Script       | Descripción                    |
| ------------ | ------------------------------ |
| `scanner.py` | Port scanner TCP con threading |

## scanner.py

Escanea puertos TCP en un host usando `connect_ex()` y `ThreadPoolExecutor` para correr hasta 100 conexiones en paralelo.

```bash
# Puertos 1-1024 (default)
python3 scanner.py 127.0.0.1

# Rango específico
python3 scanner.py 192.168.122.1 20 100
```

## Dependencias

Solo librería estándar de Python.
