import urllib, json
import twill
import os
from twill.commands import *
import os.path
from tqdm import tqdm
import requests
import getpass
#Supress twill output

f = open(os.devnull,"w")
twill.set_output(f)

cwd = os.getcwd()

login=0
#Visit moodle and login
while(login==0):
	go('http://moodle.iitb.ac.in')
	a=show()
	if(a.find("Login using IITB LDAP")!=-1):
		print("Cannot open moodle! Please ensure IITB vpn is connected")
	else:

		print("Moodle opened!")

		print("Enter your IITB roll number:")

		inp1=raw_input()
		fv("1", "username", str(inp1))

		print("Enter your password:")
		inp2=getpass.getpass()
		fv("1", "password", str(inp2))

		submit()
		go('http://moodle.iitb.ac.in/user/profile.php')
		html=show()
		if(html.find("My courses")!=-1):
			login=1
		else:
			print("Invalid authentication details. Please try again!")
		



print("Logged in")



proceed=1
while(proceed==1):
	go('http://moodle.iitb.ac.in/user/profile.php')
	list_links=showlinks()
	print("Enter course number:(eg:CS 213) ")
	inp=raw_input()

	final_list=[]
	text_list=[]
	for l in list_links:
		if(l.url.find('view.php')!=-1 and l.url.find('course')!=-1 and l.text.find(str(inp))!=-1):
			final_list=final_list+[l.url]
			text_list=text_list+[l.text]


	if(len(final_list)==0):
		print("No course matches the search input")
	else:	
		for i in range(len(final_list)):
			if(os.path.exists(cwd+"/"+str(inp))==False):
				os.makedirs(cwd+"/"+str(inp))

			go(str(final_list[i]))
			print(text_list[i]) #Course
			list_links=showlinks()

			new=0
			for l in list_links:
				if(l.url.find('discuss.php')!=-1):
					if(new==0):
						new=l.url
						new_name=l.text


			go(str(new))
			

			check=0
			num=0
			prev_new=0


			it=0



			prev_new=final_list[i]

			while(check==0):
				download=set()
				download_name=set()	
				list_links=showlinks()

				print("Post number "+str(num))
				print("Post name: "+str(new_name))
				prev=new
				new=0
				

				it=0
				for l in list_links:
					if(l.url.find('discuss.php')!=-1 and l.url.find('post')==-1):
						if(it==1):
							new=l.url
							new_name=l.text
						it=it+1
					else:
						if(l.url.find('attachment')!=-1):
							download.add(l.url)
							download_name.add(l.text)

				if(new==prev_new or new==0 or new==prev):
					check=1
				else:
					prev_new=prev
					go(str(new))
					
					num=num+1
				download_name=list(download_name)
				i=1

				for obj in download:
					if(os.path.exists(cwd+"/"+str(inp)+"/"+str(download_name[i]))==False):
						print("Downloading "+download_name[i])
						#obj
						url=obj
						response=requests.get(url,stream=True)
						with open(cwd+"/"+str(inp)+"/"+str(download_name[i]), "wb") as handle:
						    for data in tqdm(response.iter_content()):
						        handle.write(data)
					else:
						print("File "+ download_name[i]+" exists, skipping file")
					
					i=i+1

			print("")

	print("Do you want to download files from another course? Enter (y/n):")
	inp=raw_input()
	if(inp!="y"):
		proceed=0





