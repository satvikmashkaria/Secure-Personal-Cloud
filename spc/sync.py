import sys
import requests
import getpass
import pickle
import hashlib
import os
import wget

pass_file = "pass.p"

def take_pass() :
	passwd = getpass.getpass("Enter the new password: ")
	conf_passwd = getpass.getpass("Again enter the password")
	if passwd != conf_passwd :
		print("Passwords didn't match")
		take_pass()
	return passwd 

def take_option() :
	option = str(input("Enter the method of encryption (AES/DES3/Twofish): "))
	if option != 'AES' and option != 'DES3' and option != 'Twofish' :
		raise Exception("Invalid encryption method")
	return option


# with open()
def init() :
	with open(pass_file, 'rb') as f :
		data = pickle.load(f)
	if data['md5'] == 'null' :
		passwd = take_pass()
		with open(pass_file, 'wb') as f :
			pickle.dump({'md5': passwd, 'option' : data['option']}, f)
		# return passwd
	else :
		if len(sys.argv) > 1 :
			if 'c' in sys.argv[1] :
				passwd = take_pass()
				with open(pass_file, 'wb') as f :
					pickle.dump({'md5': passwd, 'option' : data['option']}, f)
			# return passwd 
			# return data['md5']	
	if data['option'] == 'null' :
		op = take_option()
		with open(pass_file, 'wb') as f :
			pickle.dump({'md5': data['md5'], 'option' : op}, f)
		# return passwd
	else :
		if len(sys.argv) > 1 :
			if 'o' in sys.argv[1] :
				op = take_option()
				print(op)
				with open(pass_file, 'wb') as f :
					pickle.dump({'md5': data['md5'], 'option' : op}, f)
			# return passwd 
			
			# return data['md5']	
init()

with open(pass_file, 'rb') as f :
	data = pickle.load(f)
file_passwd = data['md5']
option = data['option']
# print(option)
# passwd = init()
# option = str(input("Enter method of encryption (AES/DES3/Twofish): "))

stoc_for_all = False
ctos_for_all = False
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, 'rb') as file2:
	    for chunk in iter(lambda: file2.read(4096), b""):
	        hash_md5.update(chunk)
    return hash_md5.hexdigest()

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

file_name = "login_info.p"
file = open(file_name,'rb')
d = pickle.load(file)

user = d['Username']
passwd = d['Password']

client = requests.session()
url="http://127.0.0.1:8000/api/v1/rest-auth/login/"

login_data = {
	'username': user,
	'password': passwd,
}

r = client.post(url, data=login_data)

dicti = r.json()

with open("root_dir.p",'rb') as f:
	root_dir = pickle.load(f)['root_dir']

#download wala part ========================================================

os.chdir(root_dir)
# client = requests.session()
currpath = ""

url="http://127.0.0.1:8000/api/v1/rootfinder/"

r = client.options(url)
parent_id = r.json()["root"]

from en_de import AESde
from en_de import DES3de
from en_de import TWOde


def filedownload(path,name,infofile, passwd, option):
	url = "http://127.0.0.1:8000/files/download/?name="+infofile
	filename = wget.download(url,out=path)
	if option == 'AES' :
		key = hashlib.sha256(passwd.encode('utf-8')).digest()
		AESde(key[:32], filename)
	if option == 'DES3' :
		key = hashlib.sha256(passwd.encode('utf-8')).digest()
		DES3de(key[:32], filename)
	if option == 'Twofish' :
		Twode(key, filename)
	try:
		print('goes here')
		os.remove(path+filename)
	except:
		pass
	try:
		if path == '':
			os.rename(filename,name)
		else:
			os.rename(filename,path+"/"+name)
	except:
		print("shit")
		pass




def recur(path,id, passwd, option):
	url = "http://127.0.0.1:8000/api/v1/filedownload/"+str(id)+"/"
	# print()
	global stoc_for_all
	global ctos_for_all
	r = client.get(url)
	# print(r)
	infolist = r.json()

	for info in infolist['info']:
		try:
			dircontent = os.listdir(path)
		except:
			dircontent = os.listdir()
		# print("info dicti is :"+str(info))
		name = info['name']
		# name = name.split("/")[-1]
		# print("naam hai :" + name)
		# print(dircontent)

		if (name in dircontent):
			# print(dircontent)
			if path == '':
				iskifile = name
			else:
				iskifile = path+"/"+name
			if md5(iskifile) == info['md5sum']:
				print("haan same hai")
			else:
				print("change ho gaya")

				if stoc_for_all == True:
					filedownload(path,name,info['file'], passwd, option)
				elif ctos_for_all == True:
					print("query is 2 kuchh nahi karna")
				else:

					q = int(input("files confict. You have 4 options: \
											1: Server to your system for this file\
											2: Your system to server for this file\
											3: Server to your system for all files\
											4: Your system to server for all file "))
					if q == 1:
						filedownload(path,name,info['file'], passwd, option)
					elif q == 2:
						print("query is 2 kuchh nahi karna")
					elif q == 3:
						filedownload(path,name,info['file'], passwd, option)
						stoc_for_all = True
					else:
						print("query is 2 kuchh nahi karna")
						ctos_for_all = True


		else:
			filedownload(path,name,info['file'], passwd, option)


	url = "http://127.0.0.1:8000/api/v1/folderlist/"+str(id)+"/"
	r = client.get(url)
	# print(r)
	infolist = r.json()["folderlist"]
	# print(infolist)

	for info in infolist:
		try:
			dircontent = os.listdir(path)
		except:
			dircontent = os.listdir()
		if (info['name'] in dircontent):
			name = info["name"]
			folderid = info["id"]
			if path =='':
				folderpath = name
			else:
				folderpath = path + "/" + name
			# os.mkdir(folderpath)
			# print(folderpath)
			recur(folderpath,folderid, passwd, option)
		else:
			name = info["name"]
			folderid = info["id"]
			if path =='':
				folderpath = name
			else:
				folderpath = path + "/" + name
			os.mkdir(folderpath)
			print(folderpath)
			recur(folderpath,folderid, passwd, option)



recur(currpath,parent_id, file_passwd, option)

#upload wala part ========================================================


from enc import enc_upload

def fileupload(path,name,parent_id, passwd, option):
	# print(passwd)
	# print(option)
	loc = path+"/"+name
	file_data = {
	'name' : name,
	'md5sum' : md5(loc),
	}
	file = enc_upload(path, name, passwd, option)
	# print(name)
	
	print(str(file))

	upfiles = {
		# 'name' : name,
		'file' : file,
	}
	
	# print(file_data['name'])
	url = "http://127.0.0.1:8000/api/v1/uploadfile/"+str(parent_id)+"/"
	r = client.post(url,data = file_data, files=upfiles)
	os.remove(loc+'.enc')
	return r.json()['status']


def createfolder(name,parent_id):
	url = "http://127.0.0.1:8000/api/v1/createfolder/"+str(parent_id)+"/"

	folder_data = {
		'name' : name,
	}
	r = client.post(url,data = folder_data)

	# print(parent_id)
	return r.json()["key"]




def recur(path,parent_id, passwd, option):
	for f in listdir_nohidden(path):
		if os.path.isfile(path+"/"+f) == True:
			# print("goes here")
			status = fileupload(path,f,parent_id, passwd, option)
			if(status == "yes"):
				print("uploading "+path+"/"+f+"......")
		elif os.path.isdir(path+"/"+f) == True:
			# print("goes here also")
			key = createfolder(f,parent_id)
			path2 = path + "/" + f
			recur(path2,key, passwd, option)

url="http://127.0.0.1:8000/api/v1/rootfinder/"

r = client.options(url)
parent_id = r.json()["root"]


# name = path.split("/")[-1]

# new_parent_id = createfolder(name,parent_id) #extract name from path
recur(root_dir,parent_id, file_passwd, option)






