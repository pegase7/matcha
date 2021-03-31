from flask import *
from PIL import Image  
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import psycopg2
from UserManager import USERS_MANAGER # a supprimer a terme et progressivement
from datetime import datetime
from random import *
from flask_socketio import SocketIO, join_room, send, emit, leave_room
from time import localtime, strftime
from hashage import *
from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
from matcha.model.Connection import Connection
import logging
from pickle import NONE
from matcha.model.Room import Room


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'd66HR8dç"f_-àgjYYic*dh'
app.debug = True # a supprimer en production
socketio = SocketIO(app)
logging.basicConfig(level=logging.DEBUG)
ROOMS = ["lounge", "news", "games", "coding"]

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

def lien_unique():
    a=''
    for i in range(17): # compose une chaine aleatoire de lettres et de chiffres
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
    users = USERS_MANAGER().get_users()
    for u in users:
        if u[3].lower()==login.lower():
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

@app.route('/',methods=['GET', 'POST'])
def homepage():
    #users = USERS_MANAGER().get_users()
    if request.method=="POST":
        user=request.form.get('login')
        pwd=request.form.get('password')
        us = DataAccess().find('Users', conditions=('user_name', user))
        if us==None:
            rep='Utilisateur inconnu, merci de vous inscrire'
            return  render_template('home.html', rep = rep)
        if  not (us.password == pwd):
            rep = "Mauvais mot de passe, merci de réessayer"
            return  render_template('home.html', rep = rep)
        session['user']= {'name' : user}
        return redirect(url_for('accueil'))
        #for u in users:
        #    if u[3] == user:
         #       if u[4] == pwd:#if u[4] ==hash_pwd(pwd,user):
         #           if u[7]:#verifier si l'utilisateur est actif
           #             session['user']= {'name' : user}
         #               date_connexion = datetime.now()# rajouter cette info dans la fiche user a ce moment
            #            return redirect(url_for('accueil'))
          #          else:
           #             rep = "vous n'avez pas encore confirmé votre inscription"
           #     else:
           #         rep = "Mauvais mot de passe, merci de réessayer"
            
    else:   
        return render_template('home.html')

@app.route('/photo/',methods=['GET', 'POST'])
def photo():
    if "user" not in session:
        return redirect(url_for('homepage')) 
    ph1="/static/photo/"+session['user']['name']+"1.jpg"
    ph2="/static/photo/"+session['user']['name']+"2.jpg"
    ph3="/static/photo/"+session['user']['name']+"3.jpg"
    ph4="/static/photo/"+session['user']['name']+"4.jpg"
    ph5="/static/photo/"+session['user']['name']+"5.jpg"
    if request.method=="POST":
        f = request.files['maphoto']
        b=f.filename
        num = request.form.get('numphoto')
        photo_name = session['user']['name'] + num + '.jpg'
        if request.form.get('bou')=='raz':
            os.remove('static/photo/'+photo_name)
            return render_template('photo.html',ph1 = ph1, ph2=ph2,ph3=ph3,ph4=ph4,ph5=ph5)
        path = 'static/photo'
        f.save(os.path.join(path, photo_name))     
    return render_template('photo.html',ph1 = ph1, ph2=ph2,ph3=ph3,ph4=ph4,ph5=ph5)
    
@app.route('/accueil/')
def accueil():
    if "user" in session:
        username = session['user']['name']
        print(f"\n\n{username}\n\n")
        #print(f"\n\n{session}\n\n")
        liste = DataAccess().fetch('Users')
        # print("liste : ", liste)
        for element in liste:
            print("element :\n",element)
        return render_template('accueil.html', username=username, rooms=ROOMS, liste=liste)
    else:
        return redirect(url_for('homepage'))   

@app.route('/test/')
def test():
    return render_template('test.html')

@app.route('/test2/',methods=['GET', 'POST'])
def test2():
    if request.method=="POST":
        a=request.form.get('bou')
        return a
    return render_template('test2.html')

@app.route('/profil/')
def profil():
    if "user" not in session:
        return redirect(url_for('homepage')) 
    #users = USERS_MANAGER().get_users()
    user = session['user']['name']
    ph1="/static/photo/"+session['user']['name']+"1.jpg"
    us = DataAccess().find('Users', conditions=('user_name', user))
    nom = us.last_name
    login = us.user_name
    prenom = us.first_name
    bio= us.description
    orientation = us.orientation
    email= us.email
    sexe=us.gender
    b=str(us.birthday) #champ date transformé en texte
    naissance=b[8:]+'/'+b[5:7]+'/'+b[:4] #conversion date americaine en europeene
    latitude=us.latitude
    longitude=us.longitude
    return render_template('profil.html',ph1=ph1, nom = nom, prenom = prenom, sexe=sexe, orientation=orientation,bio=bio,email =email, naissance=naissance, latitude=latitude,longitude=longitude)

@app.route('/recherche/',methods=['GET', 'POST'])
def recherche():
    if "user" not in session:
        return redirect(url_for('homepage')) 
    return render_template('recherche.html')

@app.route('/registration/',methods=['GET', 'POST'])
def registration():
    if request.method=="POST":
        user=request.form.get('login')
        if verif_login(user) !='ok':
            return render_template('registration.html', message = verif_login(user))
        mail=request.form.get('courriel')
        pwd=request.form.get('password')
        pwd2 =request.form.get('password2')
        nom=request.form.get('name')
        prenom=request.form.get('first_name')
        if verif_password(pwd,pwd2) !='ok':
            return render_template('registration.html', message = verif_password(pwd,pwd2))
        if verif_identity(nom,prenom) !='ok':
            return render_template('registration.html', message = verif_identity(nom,prenom))
        session['user']= {'name' : user, 'email' : mail}   
        lien=lien_unique()
        #ici enregistre le lien et la fiche membre en non actif
        ft_send(lien,'registration')
        return redirect(url_for('accueil'))
    else:
        return render_template('registration.html')

@app.route('/forgot/',methods=['GET', 'POST'])
def forgot():
    try:
        user=session['user']['name']
    except:
        user=''
    if request.method=="POST":
        user=request.form.get('login')
        users = USERS_MANAGER().get_users()
        mail = rep =''
        for u in users:
            if u[3] == user:
                mail=u[6]
                session['user']= {'name' : user, 'email' : mail}
        if mail =='':
            rep='Utilisateur inconnu !'
            return render_template('forgot_password.html',rep=rep)
        else :
            lien=lien_unique()
            nature='password'
            #ici enregistre le lien dans la fiche membre
            ft_send(lien, nature)
            return redirect(url_for('logout')) 
    return render_template('forgot_password.html',user=user)

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('homepage'))
    
@app.route('/validation/<code>')
def validation(code):
    users = USERS_MANAGER().get_users()
    #for u in users:
        #if u[8]==code:
            #passer l'utilisateur en mode actif
            #supprimer confirm  
            #return redirect(url_for('logout'))        
    return render_template('validation.html', code = code)

@app.route('/newpassword/<code>', methods=['GET','POST'])
def newpassword(code):
    users = USERS_MANAGER().get_users()
    for u in users:
        if u[8]==code:
            login=u[3]
    if request.method=="POST":
        pwd=request.form.get('password')
        pwd2=request.form.get('password2')
        if verif_password(pwd,pwd2) !='ok':
            return render_template('newpassword.html', message = verif_password(pwd,pwd2))
        else:
            #hash=hash_pwd(pwd,login)
            #sauvegarder ce pwd hashé
            #supprimer confirm
            return redirect(url_for('logout'))
    return render_template('newpassword.html', code =code)

@app.route('/profilmodif/',methods=['GET', 'POST'])
def profilmodif():
    if "user" not in session:
        return redirect(url_for('homepage')) 
    users = USERS_MANAGER().get_users()
    user = session['user']['name']
    ph1="/static/photo/"+session['user']['name']+"1.jpg"
    for u in users:
        if u[3] == user:
            nom = u[2]
            login =u[3]
            prenom = u[1]
            bio= u[5]
            orientation = u[10]
            email=u[6]
            sexe=u[9]
            b=str(u[11]) #champ date transformé en texte
            naissance=b[8:]+'/'+b[5:7]+'/'+b[:4] #conversion date americaine en europeene
    if request.method=="POST":
        return redirect(url_for('profil'))
    return render_template('profilmodif.html',nom=nom,prenom=prenom,bio=bio,orientation=orientation,email=email,naissance=naissance)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# Temps réel avec socketio
@socketio.on('message')
def message(data):
    # print(f"\n\n{data}\n\n")
    send({'msg': data['msg'], 'username': data['username'], 
    'time_stamp': strftime('%d-%b %I:%M%p', localtime())}, room=data['room'])
    

@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'msg': data['username'] + " has join the " + data['room'] + " room."}, room=data['room'])


@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + " has left the " + data['room'] + " room."}, room=data['room'])


@socketio.on('like') #l'evenement 'like'  arrive ici
def like(data):
    # find users id
    user1 = DataAccess().find('Users', conditions=('user_name', data['username']))
    user2 = DataAccess().find('Users', conditions=('user_name','LaBombe'))
    # print(f"\n\n{user1.id}\n\n") 
    # print(f"\n\n{user2.id}\n\n")
    print(f"\n\n{data}\n\n")
    
    #search if room already exists
    # users_room = DataAccess().find('Users_room', conditions=[('master_id', user1.id),('slave_id', user2.id)], joins=[('room_id')])
    # print("users_room : ", users_room.room_id, users_room.master_id, users_room.slave_id )
    
    # create new room
    newroom = Room()
    newroom.users_ids = [user1.id, user2.id]
    newroom.active = False
    DataAccess().persist(newroom)
    print("newroom_id : ",newroom.id)

    # join the newroom
    join_room(newroom)

    emit("afterlike", {'username': data['username']}, room=newroom) # renvoie un evenement 'afterlike' 


# @ socketio.on('create')
# def create(data):
# username = data['username']
# room = data['room_name']
# join_room(data[room])
# send(username + ' has left the room.', room=room)


# Lance les serveurs
if __name__ == '__main__':
    socketio.run(app)