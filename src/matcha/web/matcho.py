from flask import *
from PIL import Image  
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import psycopg2
from datetime import datetime
from random import *
from flask_socketio import SocketIO, join_room, send, emit, leave_room
from time import localtime, strftime
from matcha.web.hashage import *
from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
from matcha.model.Connection import Connection
import logging
from pickle import NONE
from matcha.model.Room import Room
from matcha.model.Message import Message
from matcha.model.Users_room import Users_room
from matcha.config import FlaskEncoder, MyEncoder


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'd66HR8dç"f_-àgjYYic*dh'
app.debug = True  # a supprimer en production
socketio = SocketIO(app)
ROOMS = ["lounge", "news", "games", "coding"]


def ft_send(unique, nature):
    if nature == 'registration':
        lien = 'http://127.0.0.1:5000/validation/' + unique
    elif nature == 'password':
        lien = 'http://127.0.0.1:5000/newpassword/' + unique
    f_time = time.asctime(time.localtime(time.time())).split()
    
    Fromadd = "matcha@ik.me"
    Toadd = session['user']['email']  # #  Spécification du destinataire
    message = MIMEMultipart()    
    message['From'] = Fromadd   
    message['To'] = Toadd 
    message['Date'] = f_time[0] + ', ' + f_time[2] + ' ' + f_time[1] + ' ' + f_time[4] + ' ' + f_time[3] + ' +0100' + '\r\n'
    if nature == 'registration':
        message['Subject'] = "inscription"
        msg = "Bomjour, " + session['user']['name'] + " merci de valider votre inscription  en cliquant sur  ce lien " + lien 
    elif nature == 'password':
        message['Subject'] = "Reinitialisation du mot de passe" 
        msg = "Bomjour, merci de suivre ce lien pour réinitialiser votre mot de passe " + lien
    message.attach(MIMEText(msg.encode('utf-8'), 'plain', 'utf-8'))  
    serveur = smtplib.SMTP('mail.infomaniak.com', 587)  # # Connexion au serveur sortant 
    serveur.starttls()  # # Spécification de la sécurisation
    serveur.login(Fromadd, "42Flask@lyon")  # # Authentification
    texte = message.as_string().encode('utf-8')  
    Toadds = [Toadd]
    serveur.sendmail(Fromadd, Toadds, texte)  # # Envoi du mail
    serveur.quit() 


def coordonnees(c):
    debut = c.find('(')
    virgule = c.find(',')
    fin = c.find(')')
    lat = c[debut + 1:virgule]
    lon = c[virgule + 1:fin]
    coor = (lat, lon)
    return (coor)


def lien_unique():
    a = ''
    for i in range(17):  # compose une chaine aleatoire de lettres et de chiffres
        ok = False
        while ok == False:
            x = randint(48, 122)
            if (x >= 58 and x <= 64) or (x >= 91 and x <= 96):
                ok = False
            else:
                ok = True
        a = a + chr(x)
    return(a)


def verif_login(login):
    message = 'ok'
    if len(login) < 3:
        message = 'Le login doit comporter au moins 3 caractéres et etre uniquement compose de lettres et chiffres'
    for letter in login:
        if not(letter >= 'a' and letter <= 'z' or letter >= 'A' and letter <= 'Z' or letter >= '0' and letter <= '9'): 
         message = 'Le login doit comporter au moins 3 caractéres et etre uniquement compose de lettres et chiffres'
    if 0 != len(DataAccess().fetch("Users", conditions=('user_name', login))):
         message = 'Le login ' + login + " est deja utilisé, merci d'en choisir un autre !"
    return message 


def verif_password(pwd, pwd2):
    message = 'ok'
    if len(pwd) < 8:
        message = 'Le mot de passe doit avoir au moins 8 caracteres !!!'
    if pwd != pwd2:
        message = 'Les 2 mots de passe ne sont pas vraiment identiques !!!'
    maj = min = nbr = 0
    for letter in pwd:
        if letter >= 'a' and letter <= 'z':
            min = min + 1
        if letter >= 'A' and letter <= 'Z':
            maj = maj + 1
        if letter >= '0' and letter <= '9':
            nbr = nbr + 1
    if maj == 0 or min == 0 or nbr == 0:
        message = 'Votre mot de passe doit comporter au moins une minuscule, une majuscule et un chiffre'
    return message


def verif_identity(nom, prenom):
    message = 'ok'
    if len(nom) < 2 or len(prenom) < 2:
        message = "Nom et prénom doivent obligatoirement comporter au moins 2 caracteres"
    return message


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == "POST":
        login = request.form.get('login')
        pwd = request.form.get('password')
        us = DataAccess().find('Users', conditions=('user_name', login))
        if us == None:
            rep = 'Utilisateur inconnu, merci de vous inscrire'
            return  render_template('home.html', rep=rep)
        # if  not (us.password == hash_pwd(pwd, login)):
            # rep = "Mauvais mot de passe, merci de réessayer"
            return  render_template('home.html', rep=rep)
        if us.active == False:
            rep = "Vous n'avez pas confirmé votre inscription, veuillez consulter vos mails."
            return  render_template('home.html', rep=rep)
        session['user'] = {'name': login}
        return redirect(url_for('accueil'))
        
        # date_connexion = datetime.now()# rajouter cette info dans la fiche user a ce moment           
    else: 
        return render_template('home.html')
    

@app.route('/photo/', methods=['GET', 'POST'])
def photo():
    if "user" not in session:
        return redirect(url_for('homepage')) 
    ph1 = "/static/photo/" + session['user']['name'] + "1.jpg"
    ph2 = "/static/photo/" + session['user']['name'] + "2.jpg"
    ph3 = "/static/photo/" + session['user']['name'] + "3.jpg"
    ph4 = "/static/photo/" + session['user']['name'] + "4.jpg"
    ph5 = "/static/photo/" + session['user']['name'] + "5.jpg"
    if request.method == "POST":
        f = request.files['maphoto']
        b = f.filename
        num = request.form.get('numphoto')
        photo_name = session['user']['name'] + num + '.jpg'
        if request.form.get('bou') == 'raz':
            os.remove('static/photo/' + photo_name)
            return render_template('photo.html', ph1=ph1, ph2=ph2, ph3=ph3, ph4=ph4, ph5=ph5)
        path = 'static/photo'
        f.save(os.path.join(path, photo_name))     
    return render_template('photo.html', ph1=ph1, ph2=ph2, ph3=ph3, ph4=ph4, ph5=ph5)
    
    
@app.route('/accueil/')
def accueil():
    if "user" in session:
        username = session['user']['name']
        
        # list sera le resultat de la recherche
        list = DataAccess().fetch('Users')
        print('list = ',list)
        # ipExterne = urlopen("https://ip.lafibre.info/ip.php").read()
        # print('ip = ',ipExterne.decode('ascii'))
        # request.remodeaddr recupere adresse ip
        return render_template('accueil.html', username=username, rooms=ROOMS, list=list)
    else:
        return redirect(url_for('homepage'))   


@app.route('/consultation/<login>/')
def consultation(login):
    if "user" not in session:
        return redirect(url_for('homepage'))
    us = DataAccess().find('Users', conditions=('user_name', login))
    ph1 = "/static/photo/" + us.user_name + "1.jpg"
    ph2 = "/static/photo/" + us.user_name + "2.jpg"
    ph3 = "/static/photo/" + us.user_name + "3.jpg"
    ph4 = "/static/photo/" + us.user_name + "4.jpg"
    ph5 = "/static/photo/" + us.user_name + "5.jpg"
    b = str(us.birthday)  # champ date transformé en texte
    naissance = b[8:] + '/' + b[5:7] + '/' + b[:4]  # conversion date americaine en europeene
    if us.birthday == None:
        naissance = ''
    return render_template('consultation.html', profil=us, ph1=ph1, ph2=ph2, ph3=ph3, ph4=ph4, ph5=ph5, naissance=naissance)


@app.route('/test/')
def test():
    return render_template('test.html')


@app.route('/test2/', methods=['GET', 'POST'])
def test2():
    if request.method == "POST":
        a = request.form.get('bou')
        return a
    return render_template('test2.html')


@app.route('/profil/')
def profil():
    if "user" not in session:
        return redirect(url_for('homepage')) 
    # users = USERS_MANAGER().get_users()
    user = session['user']['name']
    ph1 = "/static/photo/" + session['user']['name'] + "1.jpg"
    us = DataAccess().find('Users', conditions=('user_name', user))
    nom = us.last_name
    login = us.user_name
    prenom = us.first_name
    bio = us.description
    orientation = us.orientation
    email = us.email
    sexe = us.gender
    b = str(us.birthday)  # champ date transformé en texte
    if us.birthday == None:
        naissance = ''
    naissance = b[8:] + '/' + b[5:7] + '/' + b[:4]  # conversion date americaine en europeene
    latitude = us.latitude
    longitude = us.longitude
    return render_template('profil.html', ph1=ph1, nom=nom, prenom=prenom, sexe=sexe, orientation=orientation, bio=bio, email=email, naissance=naissance, latitude=latitude, longitude=longitude)


@app.route('/recherche/', methods=['GET', 'POST'])
def recherche():
    if "user" not in session:
        return redirect(url_for('homepage')) 
    return render_template('recherche.html')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if request.method == "POST":
        login = request.form.get('login')
        # if verif_login(login) != 'ok':
            # return render_template('registration.html', message=verif_login(user))
        mail = request.form.get('courriel')
        pwd = request.form.get('password')
        pwd2 = request.form.get('password2')
        nom = request.form.get('name')
        prenom = request.form.get('first_name')
        if verif_password(pwd, pwd2) != 'ok':
            return render_template('registration.html', message=verif_password(pwd, pwd2))
        if verif_identity(nom, prenom) != 'ok':
            return render_template('registration.html', message=verif_identity(nom, prenom))
        session['user'] = {'name': login, 'email': mail}   
        lien = lien_unique()
        new = Users()
        print('Prenom ' + prenom)
        new.first_name = prenom
        print("nom" + nom)
        new.last_name = nom
        new.user_name = login
        new.password = hash_pwd(pwd, login)
        new.description = None
        new.email = mail
        new.active = False
        new.confirm = lien
        new.gender = None
        new.orientation = None
        new.birthday = None
        new.latitude = None
        new.longitude = None
        DataAccess().persist(new)

        ft_send(lien, 'registration')
        return redirect(url_for('accueil'))
    else:
        return render_template('registration.html')


@app.route('/forgot/', methods=['GET', 'POST'])
def forgot():
    try:
        user = session['user']['name']
    except:
        user = ''
    if request.method == "POST":
        user = request.form.get('login')
        mail = rep = ''
        us = DataAccess().find('Users', conditions=('user_name', user))
        mail = us.email
        session['user'] = {'name': user, 'email': mail}
        if us == None:
            rep = 'Utilisateur inconnu !'
            return render_template('forgot_password.html', rep=rep)
        else:
            lien = lien_unique()
            nature = 'password'
            us.confirm = lien
            DataAccess().merge(us)  
            ft_send(lien, nature)
            return redirect(url_for('logout')) 
    return render_template('forgot_password.html', user=user)


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('homepage'))

    
@app.route('/validation/<code>')
def validation(code):
    us = DataAccess().find('Users', conditions=('confirm', code))
    if us == None:
        rep = "ce lien n'est pas valable !"
        return render_template('validation.html', rep=rep)
    us.active = True
    us.confirm = None
    DataAccess().merge(us)       
    return redirect(url_for('logout'))        


@app.route('/newpassword/<code>', methods=['GET', 'POST'])
def newpassword(code):
    us = DataAccess().find('Users', conditions=('confirm', code))
    if us == None:
        rep = "ce lien n'est pas valable !"
        return render_template('newpasswordfalse.html', rep=rep)
    if request.method == "POST":
        pwd = request.form.get('password')
        pwd2 = request.form.get('password2')
        if verif_password(pwd, pwd2) != 'ok':
            return render_template('newpassword.html', message=verif_password(pwd, pwd2))
        else:
            hash = hash_pwd(pwd, us.user_name)
            us.confirm = None
            us.password = hash
            DataAccess().merge(us)
            return redirect(url_for('logout'))
    return render_template('newpassword.html', login=us.user_name)


@app.route('/profilmodif/', methods=['GET', 'POST'])
def profilmodif():
    try:
        msg = request.args['msg']
    except:
        msg = ''
    if "user" not in session:
        return redirect(url_for('homepage')) 
    user = session['user']['name']
    us = DataAccess().find('Users', conditions=('user_name', user))
    ph1 = "/static/photo/" + session['user']['name'] + "1.jpg"
    nom = us.last_name
    login = us.user_name
    prenom = us.first_name
    bio = us.description
    sexe = us.gender
    if bio == None:\
        bio = ""
    orientation = us.orientation
    email = us.email
    sexe = us.gender
    
    naissance = (us.birthday)
    latitude = us.latitude
    if latitude == None:
        latitude = 0
    longitude = us.longitude
    if longitude == None:
        longitude = 0
    if request.method == "POST":
        coordonnee = request.form.get('longlat')
        if (coordonnee):
            us.latitude = coordonnees(coordonnee)[0]
            us.longitude = coordonnees(coordonnee)[1]
        us.first_name = request.form.get('first_name')
        us.last_name = request.form.get('name')
        us.gender = request.form.get('sexe')
        us.orientation = request.form.get('orientation')
        us.description = request.form.get('bio')
        if not(request.form.get('birthday') == ''):
            us.birthday = request.form.get('birthday')
        DataAccess().merge(us)
        return redirect(url_for('profil'))
    return render_template('profilmodif.html', nom=nom, prenom=prenom, bio=bio, orientation=orientation, email=email, naissance=naissance, latitude=latitude, longitude=longitude, msg=msg, sexe=sexe)


@app.route('/chat/')
def chat():
    if "user" in session:
        username = session['user']['name']
        user = DataAccess().find('Users', conditions=('user_name', username))
        print(user)
        # msgs = DataAccess()fetch('Message',)
        # print(f"\n\n{username}\n\n")
        # print(f"\n\n{session}\n\n")
        liste = DataAccess().fetch('Users_room', joins=[('master_id', 'US')])
        # print("liste : ", liste)
        print("\n\n")
        return render_template('chat.html',
                                username=username,
                                user_id=user.id, 
                                rooms=liste)
    else:
        return redirect(url_for('homepage'))  


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


# # Temps réel avec socketio
@socketio.on('message')
def message(data):
    # print(f"\n\n{data}\n\n")
    msg = Message()
    msg.chat = data['msg']
    msg.room_id = data['room']
    msg.sender_id = data['user_id']
    DataAccess().persist(msg)
    send({'msg': data['msg'], 'username': data['username'],
    'time_stamp': strftime('%d-%b %I:%M%p', localtime())}, room=data['room'])
    
    
@socketio.on('join')
def join(data):
    join_room(data['room'])
    msgs = DataAccess().fetch("Message", conditions=('room_id', data['room']))
    user = DataAccess().find('Users', conditions=('user_name', data['username']))
    room_data = DataAccess().find('Users_room', conditions=('room_id', data['room']))
    print('room = ',data['room'])
    receiver_id = 0
    if room_data.slave_id == user.id:
        receiver_id = room_data.master_id
    else:
        receiver_id = room_data.slave_id
    print('receiver_id = ', receiver_id)
    receiver = DataAccess().find('Users', conditions=('id', receiver_id))
    print('receiver = ', receiver.user_name)
    # print(data['username'])
    # print(user.id)
    # print("list msgs = ")
    msgs_json = json.dumps(msgs)
    emit('old_messages', {
        'username': data['username'],
        'msgs_list': msgs_json,
        'user_id': user.id,
        'receiver': receiver.user_name,
          },
          room=data['room']
          )
          
          
@socketio.on('leave')
def leave(data):
    # print("leave : ",data)
    leave_room(data['room'])
    send({'msg': data['username'] + " a quitté cette discussion."}, room=data['room'])
    
    
@socketio.on('like')  # l'evenement 'like'  arrive ici
def like(data):
    # find users id
    user1 = DataAccess().find('Users', conditions=('user_name', data['user1']))
    user2 = DataAccess().find('Users', conditions=('user_name', data['user2']))
    print(f"\n\n{user1.id}\n\n") 
    print(f"\n\n{user2.id}\n\n")
    print(f"\n\n{data}\n\n")
    
    # search if room already exists
    # users_room = DataAccess().find('Users_room', conditions=[('master_id', user1.id),('slave_id', user2.id)], joins=[('room_id')])
    # print("users_room : ", users_room.room_id, users_room.master_id, users_room.slave_id )
    
    # create new room
    # newroom = Room()
    # newroom.users_ids = [user1.id, user2.id]
    # newroom.active = False
    # DataAccess().persist(newroom)
    # print("newroom_id : ",newroom.id)
    
    # join the newroom
    # user1.join_room(newroom)
    # user2.join_room(newroom)
    # emit("afterlike", {'username': data['username']}, room=newroom) # renvoie un evenement 'afterlike' 
    
# @ socketio.on('create')
# def create(data):
# username = data['username']
# room = data['room_name']
# join_room(data[room])
# send(username + ' has left the room.', room=room)


# Lance les serveurs
if __name__ == '__main__':
    socketio.run(app)
