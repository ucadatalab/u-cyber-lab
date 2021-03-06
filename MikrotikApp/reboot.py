from tiempo import tiempo


def reboot(ssh):
    '''
         :param ssh: Recibe una conexión SSH al o los dispositivos que se desean reiniciar.
         :return:
    '''

    print("El dispositivo se reiniciará a las: ")
    time_string = tiempo(ssh)
    print(time_string) #Hora en la cual el dispositivo se reiniciará
    stdin, stdout1, stderr = ssh.exec_command('/system script remove [/system script find]') #Elimina todos los scripts
    stdin, stdout2, stderr = ssh.exec_command('/system scheduler remove [/system scheduler find]') #Elimina todos los planificadores del dispositivo
    stdout = stdout2.readlines()
    print(stdout)
    print(time_string)
    '''
        Se crea el script y el planificador de tal forma que se reinicia el dispositivo
    '''
    stdin, stdout3, stderr = ssh.exec_command('/system script add name="reinicio" source="/system reboot"') #
    stdin, stdout4, stderr = ssh.exec_command('/system scheduler add name=reinicio start-time='+time_string+' on-event=reinicio') #
    stdout = stdout4.readlines()

    print(stdout)
    print("Reiniciando...")
    ssh.close()



