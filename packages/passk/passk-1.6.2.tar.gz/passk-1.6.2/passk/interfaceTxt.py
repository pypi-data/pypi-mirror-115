# -*- coding: utf8 -*-
import datetime
import pickle
import ast
import passk.passKeeper
import time
import os
import sys
import random, string
import binascii
import argparse # Parseur des arguments en ligne de commande
from Crypto import Random
import re
import sys
import pyperclip as pc

import getpass
from base64 import b64encode,b64decode
import dropbox
import time

isDropbox = False
lengthRan = 12
alphabet = string.ascii_letters + string.digits + string.punctuation
version = "1.6"

        
parser = argparse.ArgumentParser(description='Lecture d''un fichier de mots de passes')
parser.add_argument('-f', metavar='file name', nargs='?',help='Nom du fichier à ouvrir',default='mdp.txt',const='mdp.txt')
parser.add_argument('-salt', metavar='salt', nargs=1,help='Sel',default="")
parser.add_argument('-d', metavar='dropbox', nargs=1,help='Token Dropbox',default="")

args = parser.parse_args()

# Fichier par défaut : mdp.txt
def_file = args.f

if args.d != "":
    isDropbox = True
    #client = dropbox.client.DropboxClient(args.d[0])
    client = dropbox.Dropbox(args.d[0])
    #print('Linked account: ', client.account_info())

    try:
        client.files_download_to_file(def_file,'/'+def_file)
        #f, metadata = client.get_file_and_metadata('/'+def_file)
        #f, metadata = client.files_download('/'+def_file)
        print(metadata)
        out = open(def_file, 'wb')
        out.write(f.read())
        out.close()
    except:
        print('Problème lors du téléchargement Dropbox du fichier '+def_file)
    
try:
    # Création du cipher et saisie du mot de passe pour déchiffrer le fichier
    cipher = passKeeper.passCipher()
    if args.salt!="":
        cipher.getpassword(salt=b64decode(args.salt[0].encode('UTF-8')))
    else:
        cipher.getpassword()

    # Acces Dropbox ou local
    sauvegarde = cipher.decrypt_file(def_file,"",1)
    liste=pickle.loads(sauvegarde)
    print("Sauvegarde chargée")
    
except:
    print("Problème lors du chargement de la sauvegarde")
    sys.exit()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

        
def show(liste,filter=None):
    if filter==None:
        filter=[True]*len(liste)
    # Affiche les mots de passe et etends les items
    for i,(elem,toshow) in enumerate(zip(liste,filter)):
        if toshow:
            print(str(i)+" - " +elem[0]+"\r")   

def showElem(liste):
    # Affiche les mots de passe et etends les items

    numb = input_nb(liste[1])
    if int(numb)==-1:
        return
    if (numb==''):
        print(liste[0])
        print('-'*len(liste[0]))
        show(liste[1])
    else:
        print(numb+" - " +liste[1][int(numb)][0])
        if numb[0]=='0' and len(numb)>1:
            print("    " +liste[1][int(numb)][1])
        else:
            pc.copy(liste[1][int(numb)][1])
        showElem(liste)

def input_nb(liste):
    inp = input("Nombre ? (999 = exit)")
    
    # Car plus facile que -1 sur clavier virtuel
    if (inp=="999"):
        inp=-1
    
    if (is_number(inp)):
        return inp
    if (inp==""):
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        pc.copy('')
        show(liste)
        return input_nb(liste)
    else:
        filter=[]
        for elem in liste:
            filter.append(inp.upper() in elem[0].upper())
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        pc.copy('')
        show(liste,filter)
        return input_nb(liste)


#numb = input_nb()

while True:
    #show(liste)
    numb = input_nb(liste)
    
    if int(numb) == -1:
        break
    else:
        showElem(liste[int(numb)])
        
os.system('cls' if os.name == 'nt' else "printf '\033c'")

