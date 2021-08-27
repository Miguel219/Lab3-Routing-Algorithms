
def get_JID(names_file,ID):
	"""
		This function receives the ID in the topology and returns 
		the JID on alumchat

		parameters:

			names_file: File with JSON of all names must have the
						parameter named type with the value of 
						"names", and a parameter named config, 
						with a diccionary of the data, ID as key
						JID as value. (String type, with extension)

			ID:	The ID on the topology (String or character type)

		returns:

			JID: string type
	"""
	file = open(names_file, "r")
	file = file.read()
	info = eval(file)
	if(info["type"]=="names"):
		names = info["config"]
		JID = names[ID]
		return(JID)
	else:
		raise Exception('The file has not a valid format for names')

def get_ID(names_file, JID):
	"""
		This function receives the JID on alumchat and returns 
		the ID in the topology

		parameters:

			names_file: File with JSON of all names must have the
						parameter named type with the value of 
						"names", and a parameter named config, 
						with a diccionary of the data, ID as key
						JID as value. (String type, with extension)

			JID:	The JID on alumchat (String or character type)

		returns:

			ID: string type
	"""
	file = open(names_file, "r")
	file = file.read()
	info = eval(file)
	if(info["type"]=="names"):
		names = info["config"]
		JIDS = {v: k for k, v in names.items()}
		name = JIDS[JID]
		return(name)
	else:
		raise Exception('The file has not a valid format for names')


def get_neighbors(topology_file, ID):
	"""
		This function returns a list of the neighbors of a node

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

			JID:	The JID on alumchat (String or character type)

		returns:

			ID: string type
	"""
	file = open(topology_file, "r")
	file = file.read()
	info = eval(file)
	if(info["type"]=="topo"):
		names = info["config"]
		neighbors_IDs = names[ID]
		return(neighbors_IDs)
	else:
		raise Exception('The file has not a valid format for topology')
	return  