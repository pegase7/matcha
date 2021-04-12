import hashlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import os
from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
from matcha.model.Connection import Connection
from random import *
from flask import *

class hashit:
    def hashing(self,texte,hash_type):
        texte=texte.encode('utf-8')     
        hash_1=hashlib.new(hash_type)
        hash_1.update(texte)           
        return hash_1.hexdigest()


def hash_pwd(pwd,login):
    Hash=hashit()
    pwd=pwd+login[:2] #salage avec le 2 premieres lettres du login
    result_hash=Hash.hashing(pwd,'SHA1')
    return result_hash


def ft_send(unique, nature):
    if nature == 'registration':
        lien = 'http://127.0.0.1:5000/validation/'+unique
    elif nature == 'password':
        lien = 'http://127.0.0.1:5000/newpassword/'+unique
    f_time = time.asctime(time.localtime(time.time())).split()
    Fromadd = "matcha@ik.me"
    Toadd = session['user']['email']   ##  Spécification du destinataire
    message = MIMEMultipart()    
    message['From'] = Fromadd   
    message['To'] = Toadd 
    message['Date'] =  f_time[0]+', '+f_time[2]+' '+f_time[1]+' '+f_time[4]+' '+f_time[3]+' +0100' +'\r\n'
    if nature == 'registration':
        message['Subject'] = "inscription"
        msg = "Bomjour, " + session['user']['name'] +" merci de valider votre inscription  en cliquant sur  ce lien " + lien 
    elif nature == 'password':
        message['Subject'] = "Reinitialisation du mot de passe" 
        msg = "Bomjour, merci de suivre ce lien pour réinitialiser votre mot de passe "+ lien
    message.attach(MIMEText(msg.encode('utf-8'), 'plain', 'utf-8'))  
    serveur = smtplib.SMTP('mail.infomaniak.com', 587)  ## Connexion au serveur sortant 
    serveur.starttls()    ## Spécification de la sécurisation
    serveur.login(Fromadd, "42Flask@lyon")    ## Authentification
    texte= message.as_string().encode('utf-8')  
    Toadds = [Toadd]
    serveur.sendmail(Fromadd, Toadds, texte)    ## Envoi du mail
    serveur.quit() 


def coordonnees(c): #separe latitude et longitude  
    debut=c.find('(')
    virgule=c.find(',')
    fin=c.find(')')
    lat=c[debut+1:virgule]
    lon=c[virgule+1:fin]
    coor=(lat,lon)
    return (coor)


def lien_unique():
    a=''
    for _ in range(17): # compose une chaine aleatoire de lettres et de chiffres
        ok=False
        while ok==False:
            x=randint(48,122)
            if (x >=58 and x <=64) or (x>= 91 and x<=96):
                ok = False
            else:
                ok = True
        a=a+chr(x)
    return(a)


def verif_login(login):
    message ='ok'
    if len(login) < 3:
        message = 'Le login doit comporter au moins 3 caractéres et etre uniquement compose de lettres et chiffres'
    for letter in login:
        if not(letter >='a' and letter <='z' or letter >='A' and letter<='Z' or letter >='0' and letter <='9'): 
         message = 'Le login doit comporter au moins 3 caractéres et etre uniquement compose de lettres et chiffres'
    if 0 != len(DataAccess().fetch("Users", conditions=('user_name',login))):
         message = 'Le login '+login+" est deja utilisé, merci d'en choisir un autre !"
    return message   


def verif_password(pwd,pwd2):
    message = 'ok'
    if len(pwd) < 8:
        message = 'Le mot de passe doit avoir au moins 8 caracteres !!!'
    if pwd != pwd2:
        message = 'Les 2 mots de passe ne sont pas vraiment identiques !!!'
    maj=min=nbr=0
    for letter in pwd:
        if letter >='a' and letter <='z':
            min=min+1
        if letter >='A' and letter <='Z':
            maj=maj+1
        if letter >='0' and letter <='9':
            nbr=nbr+1
    if maj== 0 or min == 0 or nbr == 0:
        message='Votre mot de passe doit comporter au moins une minuscule, une majuscule et un chiffre'
    return message


def verif_identity(nom,prenom):
    message = 'ok'
    if len(nom) <2 or len(prenom) <2:
        message = "Nom et prénom doivent obligatoirement comporter au moins 2 caracteres"
    return message