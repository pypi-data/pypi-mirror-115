from Crypto import Random
from Crypto.Cipher import AES
from pbkdf2 import PBKDF2
import getpass
import base64

class passCipher():
    def __init__(self):
        self.password = ""
        self.key = ""
        self.salt=b"\x986q\x12\xb0y\x99."
        self.nturn=3085
        
    def pad(s):
        length = AES.block_size - len(s) % AES.block_size
        return s + length * chr(length).encode('utf8')
    
    def unpad(s):
        return s[:-ord(s[len(s)-1:].decode('utf8'))]

    def encrypt(self,message,mode = 0):
    # Mode 0 -> Résultat binaire
    # Mode 1 -> Résultat ASCII
        if self.key == "":
            print("Clef vide, message non encrypté")
            return message
        elif mode == 1:
            return base64.urlsafe_b64encode(self.encrypt(message,0)).decode('utf8')#base64.encodestring(self.encrypt(message,0)).decode('utf8')
        if mode == 0:
            key_size=256
            messagepad = passCipher.pad(message)
            iv = Random.new().read(AES.block_size)
            return iv + AES.new(self.key, AES.MODE_CBC, iv).encrypt(messagepad)
        

    def decrypt(self,ciphertext,mode = 0):
        if self.key == "":
            print("Clef vide, message non decrypté")
            return ciphertext
        elif mode == 1:
            return self.decrypt(base64.urlsafe_b64decode(ciphertext.encode('utf8')),0)#self.decrypt(base64.decodestring(ciphertext.encode('utf8')),0)
        elif mode == 0:
            iv = ciphertext[:AES.block_size]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            return cipher.decrypt(ciphertext[AES.block_size:]).rstrip(b"\0")
            #return unpad(cipher.decrypt(ciphertext[AES.block_size:])) #.rstrip(b"\0")
        
        
    def keyfrompass(self):
        if not(self.password)=="":
            self.key = PBKDF2(self.password, self.salt, self.nturn,None).read(32)
        else:
            self.key = ""
        
    def setkey(self,key):
        self.key = key
        
    def getpassword(self,salt=""):
        self.password = getpass.getpass(prompt='Entrez votre mot de passe : ')
        if salt != "":
            self.salt=salt
        self.keyfrompass()
        
    def changepassword(self):
        password1 = getpass.getpass(prompt='Entrez votre ancien mot de passe : ')
        if password1==self.password:
            password1 = getpass.getpass(prompt='Entrez votre nouveau mot de passe : ')
            password2 = getpass.getpass(prompt='Entrez à nouveau votre nouveau mot de passe : ')
            if password1==password2:
                self.password = password1
                self.keyfrompass()
                print("Le mot de passe a été modifié")
                return
        print("Erreur, le mot de passe n'a pas été modifié")

    def encrypt_file(self,fileout,filein="",message="",mode=0):
        if filein=="":
            mess = message
        else:
            with open(filein, 'rb') as fo:
                mess = fo.read()
        if mode ==0:
            with open(fileout, 'wb') as fo:
                fo.write(self.encrypt(mess,mode))
        elif mode ==1:
            print(fileout)
            with open(fileout, 'w') as fo:
                fo.write(self.encrypt(mess,mode))

    def decrypt_file(self,filein, fileout="",mode=0):
        if mode ==0:
            with open(filein, 'rb') as fo:
                ciphertext = fo.read()
        elif mode ==1:
            with open(filein, 'r') as fo:
                ciphertext = fo.read()
        if not(fileout==""):
            with open(fileout, 'wb') as fo:
                fo.write(self.decrypt(ciphertext,mode))
        else:
            return self.decrypt(ciphertext,mode)

