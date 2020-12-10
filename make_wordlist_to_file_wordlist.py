#!/usr/bin/python3

import sys
import socket
import requests

extension_list = ['.php', '.py', '.html', '.txt']

print("File url checker: Usage python3 file.py targetIP wordlistPath defaultDir(optional)")

target_host = sys.argv[1]
path_wordlist = sys.argv[2]
directory = sys.argv[3]

### Scanner
def dircheck(word):
	try:
		response_code = requests.get("http://" + target_host + directory + "/" + word).status_code
	except Exception:
		sys.exit(1)
	if response_code == 200:
		print("\nhttp://%s/%s : FOUND (CODE:200)" %(target_host, word))
		
	if response_code == 403:
		print("\nhttp://%s/%s : FORBIDDEN (CODE:403)" %(target_host, word))
	print("\nhttp://%s/%s : (CODE:%s)" %(target_host, word, response_code))

## Trying connection to the host
host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	status = host_socket.connect_ex( (target_host, 80) )
	host_socket.close()
	if (status == 0):
		print("*--- Testing connection...OK ---*")
		pass
	else:
		print("!!!--- Can't connect to the host %s" % target_host)
		sys.exit(1)
except socket.error:
	print("*--- \nException in connect_ex\n---*")
	sys.exit(1)

print("*--- Importing wordlist... ---*")
try:
	with open(path_wordlist, encoding='utf-8') as file:
		import_list = file.read().strip().split(' ')
except IOError:
	print("!!!--- Couldn't import wordlist ---!!!")
	sys.exit(1)
	
for i in range(len(import_list)):
	for x in range(len(extension_list)):
		result = import_list[i] + extension_list[x]
		dircheck(result)
print("*--- COMPLETE ---*")

