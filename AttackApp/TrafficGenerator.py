from scp import SCPClient

from GUIControllerAttack import *
from sshConnection import *
from updateFile import *
import json
from os import remove


def generarTrafico(clientes_hosts, servidores_hosts, tiempo = 0, ruta_diccionario = "", ruta_trafficFlow = ""):
    '''
    :param clientes_hosts: Se recibe un vector que contiene los clientes desde los que se enviarán peticiones GET
    :param servidores_hosts: Se recibe un vector que contiene los servidores hacia los que se enviarán peticiones GET
    :param tiempo: Recibe el tiempo que estará activo la generación de tráfico que por defecto será 0 ( y tendremos que pararla manualmente)
    :param ruta_diccionario: Recibe una ruta a los diccionarios
    :param ruta_trafficFlow:
    :return:
    '''

    #Primero, escribimos en un diccionario JSON la lista de servidores a los cuales queremos generar el tráfico
    with open('Diccionarios\\servidores_hosts.json', 'w') as file:
        json.dump(servidores_hosts, file, indent=4)

    #Ruta por defecto donde se guardará el diccionario y el archivo trafficFlow.py
    ruta_diccionario_origen = "Diccionarios\servidores_hosts.json"
    ruta_diccionario_destino = "/home/kali/Documents/Diccionarios/servidores_hosts.json"

   # if(ruta_trafficFlow == ""):
    ruta_trafficFlow_origen = "trafficFlow.py"
    ruta_trafficFlow_destino = "/home/kali/Documents/scripts/trafficFlow.py"

    print("Estoy antes del bucle  for")
    salida = ""

    for host in clientes_hosts.get("hosts"):

        username = host.get("username")
        password = host.get('password')
        port = int(host.get('port'))
        sistema = host.get('SO')
        print("sistema = "+sistema)
        ip = host.get("nics")['management']['IP']
        ssh = connection(ip, port, username, password)
        # Cargamos el diccionario y el fichero trafficFlow dentro del host correspondiente
        # Revisar, se le está pasando una ruta y no cargan los ficheros debido a que no coge la que está por defecto en updatefile
        updateFile(ssh, ruta_diccionario_origen, sistema, ruta_destino=ruta_diccionario_destino)
        updateFile(ssh, ruta_trafficFlow_origen, sistema, ruta_destino=ruta_trafficFlow_destino)
        print("He terminado de cargar los archivos")
        #Eliminamos el archivo enviado a la Raspberry Pi cliente para que en la siguiente llamada no se sobreescriba el archivo
        #añadiendose más cantidad de dispositivos hosts.
        remove("Diccionarios\servidores_hosts.json")
        print("Generando tráfico...")
        if(sistema == "Kali Linux"):
            stdin, stdout, stderr = ssh.exec_command('tmux | python3  /home/kali/Documents/scripts/trafficFlow.py | tmux detach')

        elif(sistema == "Ubuntu Mate"):
            stdin, stdout, stderr = ssh.exec_command(
                'tmux | python3  /home/ucase/Documentos/trafficFlow.py | tmux detach')


        print(salida)

        ssh.close()


        #Para parar la ejecución del script usar el siguiente comando: pkill -f nombre-del-script.py


def apagarTrafico(clientes_hosts):
    '''
    :param clientes_hosts: Recibe un diccionario de los clientes que están generando el tráfico
    :return:
    '''
    for host in clientes_hosts.get("hosts"):

        username = host.get("username")
        password = host.get('password')
        port = int(host.get('port'))
        sistema = host.get('SO')
        print("sistema = "+sistema)
        ip = host.get("nics")['management']['IP']
        ssh = connection(ip, port, username, password)
        print("Apagando tráfico...")
        if(sistema == "Kali Linux"):
            stdin, stdout, stderr = ssh.exec_command('tmux attach | exit | pkill -f trafficFlow.py')
            print("Se ha terminado de generar tráfico")
        elif(sistema == "Ubuntu Mate"):
            stdin, stdout, stderr = ssh.exec_command(
                'python3  /home/ucase/Documentos/trafficFlow.py')




        ssh.close()