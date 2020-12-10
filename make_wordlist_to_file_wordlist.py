#!/usr/bin/python3

import sys
import socket
import requests

extension_list = ['.php', '.py', '.html', '.txt']
	
## If no argument
try:
	if sys.argv[1] == '-h':
		print("File url checker: Usage python3 file.py target wordlistPath -Nf (for showing also 404)")
		sys.exit(1)
	target_host = sys.argv[1]
except Exception:
	print("File url checker: Usage python3 file.py target wordlistPath -Nf (for showing also 404)")
	sys.exit(1)
path_wordlist = sys.argv[2]
show_not_found = ""

try:
	if sys.argv[3] == '-Nf':
		show_not_found = sys.argv[3]
		print('*--- SHOWING ALSO 404 PAGES ---*')

except:
	print('*--- SHOWING ONLY HITS ---*')
### Scanner
def dircheck(word):
	try:
		response_code = requests.get("http://" + target_host + "/" + word).status_code
		result = ""
	except Exception:
		sys.exit(1)
	if show_not_found == '-Nf' and response_code == 404:
		result = "\nhttp://%s/%s : NOT FOUND (CODE:%s)" %(target_host, word, response_code)
		return result
		
	if response_code == 200:
		result = "\nhttp://%s/%s : FOUND (CODE:200)" %(target_host, word)
		return result
		
	if response_code == 403:
		result = "\nhttp://%s/%s : FORBIDDEN (CODE:403)" %(target_host, word)
		return result
	
	if response_code == 404:
		return
		'.php', '.py', '.html', '.txt'
	result = "\nhttp://%s/%s : (CODE:%s)" %(target_host, word, response_code)
	return result
## Trying connection to the host
##host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##try:
##	status = host_socket.connect_ex( (target_host, 80) )
##	host_socket.close()
##	if (status == 0):
##		print("*--- Testing connection...OK ---*")
##		pass
##	else:
##		print("!!!--- Can't connect to the host %s" % target_host)
##		sys.exit(1)
##except socket.error:
##	print("*--- \nException in connect_ex\n---*")
##	sys.exit(1)

print("*--- Importing wordlist... ---*")
try:
	with open(path_wordlist, encoding='utf-8') as file:
		import_list = file.read().strip().split('\n')
except IOError:
	print("!!!--- Couldn't import wordlist ---!!!")
	sys.exit(1)

response_list = []
for i in range(len(import_list)):
	for x in range(len(extension_list)):
		result = import_list[i] + extension_list[x]
		response = dircheck(result)
		if response != None:
			response_list.append(response)
		
## Print the responses
if len(response_list) == 0:
	print("*--- 0 RESULTS FOUND ---*")
	print("*--- COMPLETE ---*")

for i in range(len(response_list)):
	print(response_list[i])
print("*--- COMPLETE ---*")

