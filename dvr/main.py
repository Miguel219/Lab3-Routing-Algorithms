import getpass
from client import Client
import logging
from settings import *



if __name__ == '__main__':
    if DEBUG:
        # create logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # set how logger will format logs
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # add formatting to logger
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    initialMenu = 0
    while initialMenu != 3:
        try:
            initialMenu = int(input("""
--------------------------------------------------
Ingresa el número de la opción que deseas realizar:
1. Registrarse 
2. Iniciar sesión con una cuenta existente
3. Salir
--------------------------------------------------
>"""))
            
            if(initialMenu == 1):
                jid = str(input("JID: "))
                password = str(getpass.getpass("Contraseña: "))
                xmpp = Client(jid, password, login=False)         
                xmpp.connect()
                xmpp.process(forever=False)

            elif(initialMenu == 2):
                jid = str(input("JID: "))
                password = str(getpass.getpass("Contraseña: "))
                xmpp = Client(jid, password)
                # i = int(input("I:"))
                # jid = ('miguelcas_a@alumchat.xyz', #0
                #         'miguelcas_b@alumchat.xyz', #1
                #         'miguelcas_c@alumchat.xyz', #2
                #         'miguelcas_d@alumchat.xyz', #3
                #         'miguelcas_e@alumchat.xyz', #4
                #         'miguelcas_f@alumchat.xyz', #5
                #         'miguelcas_g@alumchat.xyz') #6
                # password = 'hola'
                # xmpp = Client(jid[i], password)
                xmpp.connect()
                xmpp.process(forever=False)
                if(not xmpp.logged):
                    print("No se pudo iniciar sesión, revisa tus credenciales")
                    xmpp.disconnect()

            elif(initialMenu == 3):
                print("Gracias por utilizar la aplicación!")
            else:
                print("Ingresa una opción correcta")
        except: 
            print("Ingresa una opción correcta")