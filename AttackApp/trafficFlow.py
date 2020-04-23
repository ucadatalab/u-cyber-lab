import http.client
import json
import time

ruta_diccionario = "/Documentos/scripts/servidores_hosts.json"
with open(ruta_diccionario, 'r') as f:  # Se realiza la lectura del fichero JSON
    servidores = json.load(f)

#Habría que controlar que no se envían los usernames ni las contraseñas ni las ips de gestion a los hosts.
for servidor in servidores.get("hosts"):
    ip = servidor.get("nics")['management']['IP']

    conn = http.client.HTTPSConnection(ip+":8000")
    conn.request("GET", "/")
    r1 = conn.getresponse()
    print(r1.status, r1.reason)

    data1 = r1.read()  # This will return entire content.
    # The following example demonstrates reading data in chunks.
    conn.request("GET", "/")
    r1 = conn.getresponse()

    while chunk := r1.read(200):
        print(repr(chunk))

    conn.close()


    time.sleep(5)  # Esperamos 5 segundos para volver a realizar otra petición
    ip = servidor.get("nics")['management']['IP']

    conn = http.client.HTTPSConnection(ip + ":8000")
    conn.request("GET", "/programa")
    r1 = conn.getresponse()
    print(r1.status, r1.reason)

    data1 = r1.read()  # This will return entire content.
    # The following example demonstrates reading data in chunks.
    conn.request("GET", "/")
    r1 = conn.getresponse()

    while chunk := r1.read(200):
        print(repr(chunk))

    conn.close()

#Aleatorización:

#quien nos vamos a conectar

#a quien se lo vamos a pedir

#tiempo entre peticiones

