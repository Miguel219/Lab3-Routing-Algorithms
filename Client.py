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
        self.jid_ = jid

        #Handle events
        if(type_=='flooding'):
            self.add_event_handler("session_start", self.start_flooding)
            self.add_event_handler("message", self.message_flooding)

    async def start_flooding(self, event):
        #Send presence
        self.send_presence()
        await self.get_roster()

        print("here")
        if(self.listening):
            #Send message of type chat
            print("here11")
            info = {}
            info["Nodo fuente"] = self.jid_
            info["Nodo destino"] = self.recipient
            info["Saltos"] = 0
            info["Distancia"] = 0
            info["Listado de nodos"] = []
            info["Mensaje"] = self.msg
            info["ID"] = str(uuid.uuid4())

            receivers, message = flooding(json.dumps(info), self.jid_)

            for receiver in receivers:
                self.send_message(mto=receiver,
                                  mbody=message,
                                  mtype='chat')

    def message_flooding(self, msg):
        #Print message
        if msg['type'] in ('chat'):
            recipient = msg['to']
            body = msg['body']
            
            print(str(recipient) +  ": " + str(body))

            #Send messages
            receivers, message = flooding(str(body), self.jid_)
            for receiver in receivers:
                self.send_message(mto=receiver,
                                  mbody=message,
                                  mtype='chat')