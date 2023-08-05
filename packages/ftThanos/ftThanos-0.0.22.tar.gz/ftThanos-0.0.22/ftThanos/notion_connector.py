import requests, os, json, time

class notion_connector:
	ESC = "\x1b"
	BLACK = ESC + "[30m"
	BLUE = ESC + "[34m"
	RED = ESC + "[31m"
	GREEN = ESC + "[32m"
	DEFAULT = ESC + "[39m"
	verbose = False

	def __init__(self, **kwargs):
		env = self.dot_env_parser()
		TOKEN = env['TOKEN']
		self.head = {
		"Accept": "application/json",
		"Authorization": "Bearer " + TOKEN,
		"Content-Type": "application/json",
		"Notion-Version": "2022-06-28"
		}
		self.url = 'https://api.notion.com/v1'
		self.verbose = True
		print(self.BLUE + "[NOTION CONNECTOR] Verbose activate." + self.DEFAULT)

	def put_in_file(self, data, **kwargs):
		to_write = json.dumps(data, indent=4, sort_keys=True)
		if 'name' in kwargs:
			name = 'notion_' + kwargs['name']
		else:
			name = 'notion_output.json'
		if os.path.exists(name):
			os.remove(name)
		output = open(name, 'w')
		for line in to_write:
			output.write(line)
		print(self.GREEN + f"[NOTION CONNECTOR] Data was put in {name}." + self.DEFAULT)

################
# Parser de .env
################
	def dot_env_parser(self):
		ret = {}
		try :
			with open ('.env', 'r') as file:
				for line in file:
					lst = line.split('=')
					if len(lst) != 2:
						continue
					ret[lst[0]] = lst[1][:-1]
		except IOError:
			exit(print(self.RED + '[NOTION CONNECTOR] No .env detected.' + self.DEFAULT))
		if not 'TOKEN' in ret:
			exit(print(self.RED + '[NOTION CONNECTOR] Wrong parameters in .env, you should put in your file:\nTOKEN=[Your notion token]' + self.DEFAULT))
		return (ret)

	def getDatabase(self, dbId):
		url = self.url + '/databases/' + dbId + '/query'
		body = {
			"sorts": [],
			"page_size": 100
		}
		ret = []
		end_reply = {"next_cursor" : None}
		i = 0
		try :
			while (True):
				if end_reply['next_cursor'] is not None:
					if end_reply['has_more'] == True:
							body = {"sorts" : [],
									"start_cursor" : end_reply['next_cursor']
									}
				reply = requests.post(url, data=json.dumps(body), headers=self.head)
				reply.raise_for_status()
				end_reply = json.loads(reply.text)
				ret += end_reply['results']
				if end_reply['next_cursor'] is None:
					break
		except requests.exceptions.HTTPError as err:
			self.put_in_file(json.loads(reply.text), name='error.json')
			print(self.RED + '[NOTION CONNECTOR] ' + str(err) + 'on POST ' + url + self.DEFAULT)
		return (ret)


	def createDatabase(self, parentId)
		url = self.url + '/blocks/' + parentId + '/children'
		data = {
			"children": [
					{
					"object": "block",
					"type": "database_id",
					"database_id": {
						"title": "Unnamed"
					},
				}
			]
		}
		try :
			reply = requests.patch(url, hearders=self.head, json.dumps(data))
			reply.raise_for_status()
			print(self.GREEN + "[NOTION CONNECTOR] Success PATCH on " + url + self.DEFAULT)
		except requests.exceptions.HTTPError as err:
			self.put_in_file(json.loads(reply.text), name='error.json')
			print(self.RED + '[NOTION CONNECTOR] ' + str(err) + 'on PATCH ' + url + self.DEFAULT)




