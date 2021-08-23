import json
import time
from module import *
from config import *

last_id = None

def flooding(message, sender, topology_file=topology_file, names_file=names_file,):
	"""
		This function receives a message and returns the nodes and a messages to
		return

		parameters:

			topology_file: File with JSON of all names must have the
						   parameter named type with the value of 
						   "topo", and a parameter named config, 
						   with a dictionary with IDs as key and 
						   a list of neighbors's IDs as values. 

			names_file: File with JSON of all names must have the
						parameter named type with the value of 
						"names", and a parameter named config, 
						with a diccionary of the data, ID as key
						JID as value. (String type, with extension)

			message: must be JSONable and have the following parameters:
				- "Nodo fuente" [text + @]
				- "Nodo destino" [text + @]
				- "Saltos" (nodos) recorridos [numeric]
				- "Distancia" [numeric]
				- "Listado de nodos" [text]
				- "Mensaje" [text]
				- "ID": ID of message [uuid]

			sender: JID of the sender

		returns:

			ID: string type
	"""
	start_time = time.time()
	info = eval(message)
	last_start_node = info["Nodo fuente"]
	last_end_node = info["Nodo destino"]
	last_message = info["Mensaje"]
	info["Saltos"] = info["Saltos"] + 1
	nodes = get_neighbors(topology_file, names_file, sender)
	info["Listado de nodos"] = nodes
	info["Distancia"] = info["Distancia"] - start_time + time.time()
	return (nodes, json.dumps(info))

#print(flooding('{"Nodo fuente":"yeet@alumchat.xyz", "Nodo destino":"swag@alumchat.xyz","Saltos":0, "Distancia": 0, "Listado de nodos":[], "Mensaje": "Hola mundo", "ID": 0}','yeet@alumchat.xyz'))



