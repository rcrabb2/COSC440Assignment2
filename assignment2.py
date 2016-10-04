#A lot of this was based on an article by devconsole titled https://www.devconsole.info/?p=211
#I made changes to it so that it would work the dictionary types used in Linux

import os,sys
import codecs
import argparse
import hashlib
import urllib2
 
def main():
	found = False	
	print "This program uses the shadow file in linux to break a password for a specific user."
	parse = argparse.ArgumentParser(description='A simple dictionary attack /etc/shadow .')
	parse.add_argument('-f', action='store', dest='path', help='Path to shadow file \'/etc/shadow\'')
	argus=parse.parse_args()
	if argus.path == None:
		print "invalid password"
		exit
	else:
		user=("What is the username for which you want to find?")
		passFile = open(argus.path,'r')
        	for line in passFile.readlines():
			line = line.replace("\n","").split(":")
            		if  not line[1] in [ 'x', '*','!' ]:
				user = line[0]
				cryptPass = line[1]
				testPass(cryptPass,user)
			if(found==None or user==None):
				print "User or password doesn't exist/have password"
		exit

def testPass(cryptPass,user):
	
	readOnline = urllib2.open('https://github.com/dwyl/english-words/blob/master/words.txt')
	dictionaryFile = readOnline.read()
	dicFile = open (dictionaryFile,'r')
	cryptType = cryptPass.split("$")[1]
	
	if cryptType == '6':
		print "SHA-512 encryption used"
		salt = cryptPass.split("$")[2]
		insalt = "$" + cyrptType + "$" + salt + "$"
		m = hashlib.sha512()
		for word in dicFile.readlines():
			word=word.strip('\n')
			cryptWord = m.update(word,insalt)
			if(cryptWord == cryptPass):
				print "User "+ user + " password is " + word
				found=True
	elif cryptType == '1':
		print "MD5 encryption used"
		salt = cryptPass.split("$")[2]
		insalt = "$" + cyrptType + "$" + salt + "$"
		m = hashlib.md5()
		for word in dicFile.readlines():
			word=word.strip('\n')
			cryptWord = m.update(word,insalt)
			if(cryptWord == cryptPass):
				print "User "+ user + " password is " + word
				found=True
	elif cryptType == '2':
		print "SHA-256"
		salt = cryptPass.split("$")[2]
		insalt = "$" + cyrptType + "$" + salt + "$"
		m = hashlib.sha256()
		for word in dicFile.readlines():
			word=word.strip('\n')
			cryptWord = m.update(word,insalt)
			if(cryptWord == cryptPass):
				print "User "+ user + " password is " + word
				found=True
	if (found==False):
		print "Password is not found in dictionary"
