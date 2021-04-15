import hashlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from datetime import datetime,date
import os
from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
from matcha.model.Connection import Connection
from random import *
from flask import *
from math import sin, cos, acos, radians

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



def distanceGPS(latA, longA, latB, longB):
    """Retourne la distance en km entre les 2 points A et B connus grâce à
       leurs coordonnées GPS.
    """
    # Rayon de la terre en kilomètres (sphère IAG-GRS80)
    RT = 6371
    # angle en radians entre les 2 points
    S = acos(sin(radians(latA))*sin(radians(latB)) + cos(radians(latA))*cos(radians(latB))*cos(radians(abs(longB-longA))))
    # distance entre les 2 points, comptée sur un arc de grand cercle
    return S*RT
 

def find_profil(criteres):
    liste = DataAccess().fetch('Users')
    profil_found=[]
    for user in liste:
        ok=1
        #profil actif
        if user.active==False:
            ok=0
        #Sexe
        if ok==1:
            if user.gender!=criteres['sexe']:
                ok=0
        #Critere Age
        if ok==1:
            if criteres['age_min']=="" and criteres['age_max']=="":
                ok=1
            else:
                if user.birthday:
                    age=calculate_age(user.birthday)
                    if age <criteres['age_min'] or age >criteres['age_max']:
                        ok=0
                else:
                    ok=0
        #Critere Distance
        if ok==1:
            if distanceGPS(float(criteres['latitude']),float(criteres['longitude']),float(user.latitude),float(user.longitude))>int(criteres['dist_max']):
                ok=0
        #Critere interets
        if ok==1 and len(criteres['interets'])>0:
            tags = DataAccess().fetch('Users_topic', conditions=('users_id',user.id))
            nb_int=0
            for interet in criteres['interets']:
                for tag in tags:
                    print(tag.tag)
                    if interet==tag.tag:
                        nb_int=nb_int+1
            print('total trouvé :', nb_int)
            if nb_int==0:
                ok=0
        #Selection du user
        if ok==1:
            profil_found.append(user.user_name)
    return profil_found

def calculate_age(born):
    today = date.today()
    try: 
        birthday = born.replace(year=today.year)
    except ValueError: 
        birthday = born.replace(year=today.year, month=born.month+1, day=1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year