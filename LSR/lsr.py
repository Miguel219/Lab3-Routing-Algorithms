import asyncio
from asyncio.tasks import sleep
import slixmpp
import json
import logging
from getpass import getpass
from aioconsole import ainput, aprint
import time
from utils import *

hello = 'HELLO'
echo_send = "ECHO SEND"
echo_response = "ECHO RESPONSE"
message_type= "MESSAGE"
lsp = 'LSP'
inf = 1000

def json_to_object(jason_string):
    object = json.loads(jason_string)
    return object
def object_to_json(object):
    json_string = json.dumps(object)
    return json_string

class lsrUser(slixmpp.ClientXMPP):
    
    def __init__(self, jid, password, topo_file,names_file):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)
        
        self.topo_file = topo_file
        self.names_file = names_file
        #This array will contain all the LSPs of the nodes 
        self.network = []
        self.echo_sent = None
        self.LSP = {
            'type': lsp,
            'from': self.boundjid.bare,
            'sequence': 1,
            'neighbours':{}
        }
        self.id = get_ID(self.names_file, jid)
        self.neighbours_IDS = get_neighbors(self.topo_file, self.id)
        self.neighbours = []
        self.neighbours_JID()

    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        print("When you are ready press enter")
        start = await ainput()
        #Sending the hello and echo messages to all the neighbours nodes 
        for neighbour in self.neighbours:
            await self.send_hello_msg(neighbour)
        for neighbour in self.neighbours:
            await self.send_echo_message(neighbour, echo_send)

        self.network.append(self.LSP) 

        #Continusly send the LSP through the network
        self.loop.create_task(self.send_LSP())

        await sleep(2)

        print("If you are gonna be a sender type the JID of the recipient to continue else just wait ")
        send = await ainput()
        if send != None:
            message = await ainput('Message: ')

        #Waiting some time so that the network converges
        print("Waiting for network to converge")
        await sleep(20)
        print("Network converged, sending message")

        self.send_chat_message(self.boundjid.bare,send,message=message)
        
        print("press enter to exit")
        exit = await ainput()
        self.disconnect()

    #Function used to get the JID of all the nodes neighbours from the files topo and names
    def neighbours_JID(self):
        for id in self.neighbours_IDS:
            neighbour_JID = get_JID(self.names_file, id)
            self.neighbours.append(neighbour_JID)

    #Function called eveery time a message is received
    async def message(self, msg):
        body = json_to_object(msg['body'])
        if body['type'] == hello:
            print("Hello from: ", msg['from'])

        #If an echo type message is received send an echo response to the sender
        elif body['type'] == echo_send:
            print("Echoing back to: ", msg['from'])
            await self.send_echo_message(body['from'],echo_response)

        #If an echo response message is received calculate the time between nodes
        elif body['type'] == echo_response:
            distance = time.time()-self.echo_sent
            print("Distance to ", msg['from'], ' is ', distance)
            self.LSP['neighbours'][body['from']] = distance

        elif body['type'] == lsp:
            new = await self.update_network(body)
            await self.flood_LSP(body, new)

        #If we receive a message check if it is ment for us if it is print the content else send it through the network
        elif body['type'] == message_type:
            if body['to'] != self.boundjid.bare:
                print('Got a message that is not for me, sending it ')
                path = self.calculate_path(self.boundjid.bare, body['to'])
                self.send_chat_message(source = body['from'],to = body['to'], steps=body['steps'] +1, distance=body['distance'],visited_nodes= body['visited_nodes'].append(self.boundjid.bare),message=body['mesage'])
            elif body['to'] == self.boundjid.bare:
                print('Got a message!')
                print(body['from'], " : ", body['mesage'])

        
    async def send_hello_msg(self,to, steps = 1):
        you = self.boundjid.bare
        to = to 
        json = {
            'type': hello,
            'from':you,
            'to': to,
            'steps': steps
        }
        to_send = object_to_json(json)
        self.send_message(mto = to, mbody=to_send, mtype='chat')
    
    async def send_echo_message(self, to, type ,steps = 1):
        you = self.boundjid.bare
        to = to 
        json = {
            'type': type,
            'from':you,
            'to': to,
            'steps': steps
        }
        to_send = object_to_json(json)
        self.send_message(mto = to, mbody=to_send, mtype='chat')
        self.echo_sent = time.time()

    async def send_LSP(self):
        while True:
            for neighbour in self.neighbours:
                lsp_to_send = object_to_json(self.LSP)
                self.send_message(mto =neighbour,mbody=lsp_to_send,mtype='chat')
            await sleep(2)
            self.LSP['sequence'] += 1
    
    def send_chat_message(self,source,to,steps=0, distance = 0, visited_nodes = [],message="Hola mundo"):
        body ={
            'type':message_type,
            'from': source,
            'to': to,
            'steps': steps,
            'distance': distance,
            'visited_nodes':visited_nodes, 
            'mesage':message
        }
        to_send = object_to_json(body)
        path = self.calculate_path(self.boundjid.bare, to)
        self.send_message(mto=path[1]['from'],mbody = to_send,mtype='chat')

    #Function used to send proces an incoming LSP, it checks if its sequence is greater than the known one and if it is it stores it
    #Params:
    #lsp: The received lsp 
    #Returns: 1 if the lsp is new None if the lsp is already known
    async def update_network(self, lsp):
        for i in range(0,len(self.network)):
            node = self.network[i]
            if lsp['from'] == node['from']:
                if lsp['sequence'] > node['sequence']:
                    node['sequence'] = lsp['sequence']
                    node['neighbours'] = lsp['neighbours']
                    return 1
                if lsp['sequence'] <= node['sequence']:
                    return None
        self.network.append(lsp)
        return 1
    
    #Function used to calculate the shortest path from a to b
    #Params:
    #Source: source node JID
    #Dest: recipient node JID
    #Returns: a list with the LSPs of the nodes of the path
    def calculate_path(self, source, dest):
        distance = 0
        visited = []
        current_node = self.find_node_in_network(source)
        while current_node['from'] != dest:
            node_distances = [] 
            neighbours = current_node['neighbours']
            for neighbour in neighbours.keys():
                if neighbour == dest:
                    visited.append(current_node)
                    current_node = self.find_node_in_network(neighbour)
                    visited.append(current_node)
                    return visited
                elif neighbour not in visited:
                    distance_to_neighbour = neighbours[neighbour]
                    node_distances.append(distance_to_neighbour)
            min_distance = min(node_distances)
            node_index = node_distances.index(min_distance)
            all_nodes = list(current_node['neighbours'].keys())
            next_node_id = all_nodes[node_index]
            visited.append(current_node)
            next_node = self.find_node_in_network(next_node_id)
            current_node = next_node
            distance += min_distance
        return visited

    #Function used to find a LSP from a node JID
    #Params:
    #id: wanted node JID
    #retrun: the LSP if it is on the network Fals if it int
    def find_node_in_network(self, id):
        for i in range(len(self.network)):
            node = self.network[i]
            if id in node['from']:
                return node
        return False

    #Function used to flood an LSP to the network
    #Params:
    #lsp: the lsp to send
    #new: 1 if the lsp is new None if the lsp should not be flooded
    async def flood_LSP(self, lsp, new):
        for neighbour in self.neighbours:
            if new and neighbour != lsp['from']:
                    self.send_message(mto =neighbour,mbody=object_to_json(lsp),mtype='chat')


jid = input('Username: ')
password = getpass('Password: ')
topo_file = input('Topo File: ')
name_file = input('Name file: ')
#logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')

xmpp = lsrUser(jid, password,topo_file,name_file)
xmpp.connect()
xmpp.process(forever=False)