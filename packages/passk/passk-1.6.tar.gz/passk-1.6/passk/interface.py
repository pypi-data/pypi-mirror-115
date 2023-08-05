import tkinter
from tkinter.ttk import *
from tkinter import messagebox,filedialog
import datetime
import pickle
import ast
#import testSel
import passKeeper
import time
import os
import sys
import random, string
from simplenote import Simplenote
import binascii
import argparse # Parseur des arguments en ligne de commande
from Crypto import Random
import re

import getpass
from base64 import b64encode,b64decode
import dropbox

isSimplenote = False
isDropbox = False
lengthRan = 12
alphabet = string.ascii_letters + string.digits + string.punctuation
version = "1.5"

def connect2Simplenote(event):
    global note,isSimplenote,simplenote
    
    if args.s is not None and len(args.s)>0:
        login = args.s[0]
    else:
        login = input('Username ?')
    if args.s is not None and len(args.s)>1:
        password = args.s[1]
    else:
        password = getpass.getpass(prompt='Password Simplenote ? ')
    
    try:
        isSimplenote = True
        simplenote = Simplenote(login, password)
        noteliste = simplenote.get_note_list(tags=['passKeeper'])
        noteid = noteliste[0][0]['key']
        note = simplenote.get_note(noteid)
    except Exception as e:
        print(e)
        print("Erreur lors de la connexion à Simplenote")

        
parser = argparse.ArgumentParser(description='Lecture d''un fichier de mots de passes')
parser.add_argument('-f', metavar='file name', nargs='?',help='Nom du fichier à ouvrir',default='mdp.txt',const='mdp.txt')
parser.add_argument('-s', metavar='simplenote account', nargs='*',help='Login et mdp du compte simplenote',default="")
parser.add_argument('-salt', metavar='salt', nargs=1,help='Sel',default="")
parser.add_argument('-d', metavar='dropbox', nargs=1,help='Token Dropbox',default="")

args = parser.parse_args()
#print(args)

# Fichier par défaut : mdp.txt
def_file = args.f

# Si l'argument optionnel -s est passé, on se connecte à Simplenote
if args.s != "" and args.d != "":
    print("Il n'est pas possible de se connecter à la fois à Dropbox et à Simplenote")
    print("Connexion par défaut à Dropbox")
    args.s = ""
if args.s != "":
    print('simplenote')
    connect2Simplenote("")
if args.d != "":
    isDropbox = True
    client = dropbox.Dropbox(args.d[0])
    try:
        client.files_download_to_file(def_file,'/'+def_file)
    except:
        print('Problème lors du téléchargement Dropbox du fichier '+def_file)
    
try:
    # Création du cipher et saisie du mote de passe pour déchiffrer le fichier
    cipher = passKeeper.passCipher()
    if args.salt!="":
        cipher.getpassword(salt=b64decode(args.salt[0].encode('UTF-8')))
    else:
        cipher.getpassword()

    if isSimplenote:
        sauvegarde = cipher.decrypt(note[0]['content'],1)
    else:
        # Acces Dropbox ou local
        sauvegarde = cipher.decrypt_file(def_file,"",1)
    liste=pickle.loads(sauvegarde)
    print("Sauvegarde chargée")
    
except:
    print("Problème lors du chargement de la sauvegarde")
    liste = [["Exemple",[["mdp","ssss"],["connect","['http://mail.google.com',[['Email','adresse'],['next']]]"]]]]
    def_file = '' #'mdp'+time.strftime("_%d-%m-%Y_%I-%M-%S")+'.txt'
    #print("Création du fichier "+def_file)

def filltree(liste,tree):
    for elem in liste:
        # Ajout des themes a l'arbre
        identifier = tree.insert("","end",text=elem[0],values=("",""),tags=("theme"))
        # Ajout des items
        for item in elem[1]:
            identifier2 = tree.insert(identifier,"end",text=item[0],values=("",item[1]))
    # Colorisation
    tree.tag_configure('theme',foreground='blue')
    tree.tag_configure('affiche',foreground='orange')

def OnShow(event):
    # Affiche les mots de passe et etends les items
    global tree
    item = tree.selection()[0]
    text = tree.item(item,option='text')
    values = tree.item(item,option='values')
    tags = tree.item(item,option='tags')
    
    if len(tags) == 0:
        tree.item(item,option=None,values=(values[1],values[1]),tags=("affiche"))
        textTheme.delete(0,'end')
        textTheme.insert(0,text)
        textChamp.delete(0,'end')
        textChamp.insert(0,values[1])
    elif tags[0] == 'theme':
        textTheme.delete(0,'end')
        textTheme.insert(0,text)
        print('')
    else:
        tree.item(item,option=None,values=("",values[1]),tags=(""))
        textTheme.delete(0,'end')
        textChamp.delete(0,'end')
        
def OnLaunch(event):
    # Affiche les mots de passe et etends les items
    global tree
    item = tree.selection()[0]
    text = tree.item(item,option='text')
    values = tree.item(item,option='values')
    tags = tree.item(item,option='tags')
    
    #if text == 'connect':
#    num_theme = tree.index(tree.parent(item))
#    launchConnexion(values[1],num_theme)
        
def OnAdd():
    save()
    
def OnDelete(event):
    global tree
    result = messagebox.askquestion("", "Suppression de l'element selectionne ?", icon='warning')
    if result == 'yes':
        item = tree.selection()[0]
        tree.delete(item)
        save()
    
def getListe():
    # Conversion de l'arbre en liste
    global tree
    listebis = []
    for theme in tree.get_children():
        listeitems = []
        for item in tree.get_children(theme):
            text = tree.item(item,option='text')
            values = tree.item(item,option='values')
            listeitems.append([text,values[1]])
        text = tree.item(theme,option='text')
        listebis.append([text,listeitems])
    return listebis
    
def addTree():
    # Ajoute un element a l'arbre
    global tree
    if len(tree.selection())>0:
        item = tree.selection()[0]
        tags = tree.item(item,option='tags')
        if len(tags)>0 and tags[0]=='theme':
            # Ajout d'un nouveau theme apres le theme selectionne
            pos = tree.index(item)+1
            newitem = tree.insert(tree.parent(item),pos,text=textTheme.get(),values=("",""),tags=("theme"))
            # Un item par defaut est automatiquement ajoute
            tree.insert(newitem,0,text="---",values=("",""))
        else:
            # Ajout d'un nouvel item apres l'item selectionne
            pos = tree.index(item)+1
            tree.insert(tree.parent(item),pos,text=textTheme.get(),values=(textChamp.get(),textChamp.get()),tags=("affiche"))
        textTheme.delete(0,'end')
        textChamp.delete(0,'end')
        save()
    
    
def changeTree():
    # Modifie un element de l'arbre
    global tree
    
    if len(tree.selection())>0:
        item = tree.selection()[0]
        tags = tree.item(item,option='tags')
        text = tree.item(item,option='text')
        values = tree.item(item,option='values')
        if len(tags)>0 and tags[0]=='theme':
            # L'element selectionne est un theme, on change son nom
            tree.item(item,option=None,text=textTheme.get())
        else:
            # L'element selectionne est un item
            # On en cree un autre en backup
            pos = tree.index(item)+1
            textbkp=text+' - bkp '+ str(datetime.datetime.now().time())
            tree.insert(tree.parent(item),pos,text=textbkp,values=values,tags=tags)
            # Puis on modifie l'item precedent
            if textTheme.get() != '':
                text = textTheme.get()
            tree.item(item,option=None,text=text,values=('',textChamp.get()),tags=())
        textTheme.delete(0,'end')
        textChamp.delete(0,'end')
        save()
        
def moveUp(event):
    # Deplace un element vers le haut
    global tree
    
    if len(tree.selection())>0:
        item = tree.selection()[0]
        tags = tree.item(item,option='tags')
        if len(tags)>0 and tags[0]=='theme':
            pos = tree.index(item)-1
        else:
            pos = tree.index(item)-1
        
        tree.move(item,tree.parent(item),pos)
        
        
def moveDown(event):
    # Deplace un element vers le bas
    global tree
    
    if len(tree.selection())>0:
        item = tree.selection()[0]
        tags = tree.item(item,option='tags')
        if len(tags)>0 and tags[0]=='theme':
            pos = tree.index(item)+1
        else:
            pos = tree.index(item)+1
        
        tree.move(item,tree.parent(item),pos)
        
def save(file = def_file):
    global note
    message = pickle.dumps(getListe())
    if isSimplenote == True:
        note[0]['content']=cipher.encrypt(message,1)
        #print(note[0]['content'])
        status = simplenote.update_note(note[0])
        if status[1]==0:
            print("Sauvegarde effectuée sur Simplenote")
        else:
            print(status)
            print("Echec de la sauvegarde sur Simplenote")
        file = 'mdp '+time.strftime("%Y-%m-%d-%Hh%M")+'.bkp' # Un backup est fait sur la machine locale
    if file == '':
        print("Attention, modifications non sauvegardées")
        print("Pour cela, changer le nom du fichier")
        return
    try:
        cipher.encrypt_file(file,"",message,1)
        print("Sauvegarde effectuée dans : "+file)
        
        if isDropbox:
            f = open(file, 'rb')
            data = f.read()
            res = client.files_upload(data,'/'+file,mode=dropbox.files.WriteMode.overwrite)
            print("Uploaded:"+ str(res))
    except:
        print("Attention, erreur lors de la sauvegarde. Vérifier le nom de fichier")
    
        
def saveShortcut(event):
    save()
    

#def launchConnexion(string,num_theme):
#    liste = getListe()[num_theme]
#    [page_url,list_champs] = ast.literal_eval(string)
#    # replacement des valeurs de list_champs
#    for elem in list_champs:
#        for pairs in liste[1]:
#            if len(elem)>1:
#                if elem[1] == pairs[0]:
#                    elem[1] = pairs[1]
#    testSel.connect(page_url,list_champs)

def changepass(event):    
    cipher.changepassword()
    save()
    
def changefile(event):
    global def_file
    fname = filedialog.askopenfilename()
    if (os.path.isfile(fname) and messagebox.askokcancel(title="Change file",message="Ecraser le fichier existant ?") == 1):
        isSimplenote = False
        def_file = fname
        save(def_file)
    else:
        print("Fichier non changé")
        
def forceSave(event):
    save()

def generateRandom(event):
    pw = ''.join(random.choice(alphabet) for _ in range(lengthRan))
    textChamp.delete(0,'end')
    textChamp.insert(0,pw)

def changeRandom(event):
    global lengthRan,alphabet
    lengthRan = int(input("Longueur du mot de passe ? "))
    res = input("Type de caractères ?")
    alphabet = ""
    for l in res:
        for str in [string.ascii_lowercase,string.ascii_uppercase,string.digits,string.punctuation]:
            if l in str and not str in alphabet:
                alphabet=alphabet+str
    print("Alphabet : " + alphabet)
    
def randomSaltKey(event):
    """Affiche une clef ou un sel aléatoire"""
    print()
    salt = Random.new().read(8)
    key = Random.new().read(256)
    print('SALT')
    print('----')
    print(salt)
    print(b64encode(salt).decode('UTF-8'))
    print('KEY')
    print('---')
    print(key)
    print(b64encode(key).decode('UTF-8'))

def filtrerArbre(event):
    # Filtre l'affichage de l'arbre
    global tree,textFiltre
    string = textFiltre.get()
    first = True
    for item in tree.get_children():
        if re.search(re.compile(string.upper()), tree.item(item,option='text').upper()):
            if first:
                tree.selection_set(item)
                first = False
            else:
                tree.selection_add(item)
    return
    
def help(event):
    print("<Delete> : Suppression d'un élément")

    print("u        : Déplacer vers le haut")
    print("d        : Déplacer vers le bas")
                    
    print("F1       : Aide")
    print("F2       : Afficher le champ caché")
    print("F3       : Changer les paramètre du générateur de mots de passe")
    print("F4       : Générer un mot de passe")
    print("F5       : Ouvrir une page internet")
    print("F6       : Générer un sel et une clef aléatoirement")
    print("F7       : Copier la clef dans le presse papier")
                    
    #print("F8       : Se connecter à Simplenote")
    print("F9       : Changer le fichier de sauvegarde")
    print("F12      : Changer le mot de passe")
    print("Ctrl + s : Forcer la sauvegarde")

def c2clip(event):
    # Copie la clef dans le presse papier
    global tree,root
    item = tree.selection()[0]
    text = tree.item(item,option='text')
    values = tree.item(item,option='values')
    tags = tree.item(item,option='tags')
    root.clipboard_clear()
    root.clipboard_append(values[1])
    



# Creation de la fenetre principale
root = tkinter.Tk()
root.title("Passkeeper v "+version)

RWidth=root.winfo_screenwidth()
RHeight=root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (RWidth/2,RHeight-100))

# Creation des elements de la page des mots de passe

textFiltre = tkinter.ttk.Entry(root)
textFiltre.insert(0,"")
textFiltre.pack(fill=tkinter.X)
textFiltre.bind('<Return>', filtrerArbre)

tree = tkinter.ttk.Treeview(root)
tree["columns"]=("Clef")
tree.column("Clef",width=250)
tree.heading("Clef",text="VALEUR")

root.bind("<Delete>",OnDelete)

root.bind("<u>",moveUp)
root.bind("<d>",moveDown)

root.bind("<F1>",help)
root.bind("<F2>",OnShow)
root.bind("<F3>",changeRandom)
root.bind("<F4>",generateRandom)
root.bind("<F5>",OnLaunch)
root.bind("<F6>",randomSaltKey)
root.bind("<F7>",c2clip)

#root.bind("<F8>",connect2Simplenote)
root.bind("<F9>",changefile)
root.bind("<F12>",changepass)
root.bind('<Control-s>', saveShortcut)


# Barres de defilement
ysb = tkinter.ttk.Scrollbar(tree,orient="vertical",command=tree.yview)
xsb = tkinter.ttk.Scrollbar(tree,orient="horizontal",command=tree.xview)
ysb.pack(side=tkinter.RIGHT,fill=tkinter.Y)

tree.configure(yscrollcommand=ysb.set,xscrollcommand=xsb.set)

tree.pack(expand=1,fill=tkinter.BOTH)
#xsb.pack(side=tkinter.BOTTOM,fill=tkinter.X)

# Textbox pour modification de l'arbre
textTheme = tkinter.ttk.Entry(root)
textTheme.insert(0,"")
textTheme.pack(fill=tkinter.X)
textChamp = tkinter.ttk.Entry(root)
textChamp.insert(0,"")
textChamp.pack(fill=tkinter.X)

buttonAdd = tkinter.ttk.Button(root,text='ADD',width=10,command=addTree)
buttonAdd.pack(fill=tkinter.X)

buttonChange = tkinter.ttk.Button(root,text='CHANGE',width=10,command=changeTree)
buttonChange.pack(fill=tkinter.X)

# Lancement de l'affichage
filltree(liste,tree)
root.mainloop()


