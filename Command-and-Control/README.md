# Command-and-Control

Chat multi-cliente evolucionado a un C2 básico operador/agente, todavía falta Cifrado con Fernet.

## Arquitectura

```
[Operador] server.py  →  recibe output, manda comandos
[Agente]   client.py  →  ejecuta comandos con subprocess, devuelve resultado
```

## Qué cambió respecto a la versión anterior

| Antes                                         | Ahora                                                      |
| --------------------------------------------- | ---------------------------------------------------------- |
| Buffer de 32 bytes                            | 4096 bytes — no corta el output                            |
| Servidor hacía broadcast a todos los clientes | Seleccionás el agente con `use <id>`                       |
| Cliente solo reenviaba texto                  | Cliente ejecuta con `subprocess` y devuelve el output real |
| Sin manejo de sesiones                        | Comandos `list` / `use <id>` / `current_agent`             |
| Sin reconexión                                | Cliente reintenta la conexión automáticamente cada 5s      |

## Cómo probarlo en la VM

```bash
# Terminal 1 — levantar el servidor (operador)
python3 server.py
Host: 0.0.0.0
Port: 4444

# Terminal 2 — conectar el agente
python3 client.py
Host: 127.0.0.1
Port: 4444
```

Desde el servidor:

```
>> list          # ver agentes conectados
>> use 0         # seleccionar agente por ID
>> whoami
>> id
>> ls /etc
>> exit          # cerrar conexión con el agente
```

## Dependencias

Solo librería estándar de Python — no requiere `pip install`.

## Aviso

Para uso en entornos controlados y autorizados únicamente (HTB, VMs propias, laboratorios locales).
