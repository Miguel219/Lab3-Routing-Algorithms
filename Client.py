import uuid
import json
import logging
import threading
import slixmpp
import base64, time
from flooding import *
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser


"""
    This class will be helpful to send message and receive
    messages.

    Atributes:

        jid: string expected with the jid as xmpp format
             example string: "test@alumchat.xyz"

        password: string expected with the password for
                  authentication

        recipient: string expected with the jid as xmpp 
                   format of the recipient

        message: string expected with the message to send

        type_: routing type

    Methods:
        Start: This method is helpful to delete the user

        message: This method is helpful to recieve the message
                 and ask the user to send new message
    
"""
class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message, type_, listening):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.recipient = recipient
        self.listening = listening
        self.msg = message
        self.type_ = type_
        self.jid_ = jid
        self.lastid = []


        #Handle events
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("register", self.register)

    async def start(self, event):
        #Send presence
        self.send_presence()
        await self.get_roster()


        if(not self.listening and self.type_=="flooding"):
            #Send message of type chat
            info = {}
            info["Nodo fuente"] = self.jid_
            info["Nodo destino"] = self.recipient
            info["Saltos"] = 0
            info["Distancia"] = 0
            info["Listado de nodos"] = []
            info["Mensaje"] = self.msg
            info["ID"] = str(uuid.uuid4())
            self.lastid.append(info["ID"])

            receivers, message = flooding(json.dumps(info), self.jid_)

            for receiver in receivers:
                print("Message sent to :",receiver)
                self.send_message(mto=receiver,
                                  mbody=message,
                                  mtype='chat')

    def register(self, iq):
        iq = self.Iq()
        iq['type'] = 'set'
        iq['register']['username'] = self.boundjid.user
        iq['register']['password'] = self.password

        #Send the iq so we can register

        try:
            iq.send()
            print("Succesful authentication", self.boundjid,"\n")
        except IqError as e:
            #Something went wrong
            print("Error on registration ", e,"\n")
            self.disconnect()
        except IqTimeout:
            #Server is not answering
            print("THE SERVER IS NOT WITH YOU")
            self.disconnect()
        except Exception as e:
            #Something else went wrong
            print(e)
            self.disconnect()

    def message(self, msg):
        if(self.type_=="flooding"):
            if msg['type'] in ('chat'):
                recipient = str(msg['from']).split('/')[0]
                body = msg['body']

                info = eval(str(body))

                if(info["ID"] not in self.lastid):
                    self.lastid.append(info["ID"])

                    print('\n\n\t',recipient,":", info["Mensaje"],'\n\tSaltos:', info["Saltos"],'\n\tDistancia:', info["Distancia"],'\n\n')

                    #Send messages
                    receivers, message = flooding(str(body), self.jid_)
                    for receiver in receivers:
                        if(receiver!=recipient):
                            print("Message sent to :",receiver)
                            self.send_message(mto=receiver,
                                              mbody=message,
                                              mtype='chat')