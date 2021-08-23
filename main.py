import logging
import threading
import slixmpp
import base64, time
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp.xmlstream.stanzabase import ET, ElementBase 
from getpass import getpass
from argparse import ArgumentParser  
from Client import *

"""
Main file 
"""

if __name__ == '__main__':
    parser = ArgumentParser(description=Client.__doc__)

    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")
    parser.add_argument("-r", "--routing", dest="routing",
                        help="Type of routing")

    parser.add_argument("-t", "--listening", dest="listening",
                        help="Just listening or writing inital message")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = input("Username: ")
    if args.password is None:
        args.password = getpass("Password: ")
    if args.routing is None:
        args.routing = input("Type of routing: ")
    if args.routing is None:
        args.listening = False

    try:
        recipient = ''
        message = ''
        if(not args.listening):
            recipient = input("Write the recipient JID: ") 
            message = input("Write the message: ")
        xmpp = Client(args.jid, args.password, recipient, message, args.routing, args.listening)
        xmpp.register_plugin('xep_0030') # Service Discovery
        xmpp.register_plugin('xep_0199') # XMPP Ping
        xmpp.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        xmpp.register_plugin('xep_0096') # Jabber Search
        xmpp.register_plugin('xep_0077') ### Band Registration
        xmpp.connect()
        xmpp.process(forever=False)
    except KeyboardInterrupt as e:
        print('\nNice chat, dont forget I read all of it!\n')