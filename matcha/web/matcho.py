from flask import *
from PIL import Image  
import os
import psycopg2
from datetime import datetime
from random import *
from flask_socketio import SocketIO, join_room, send, emit, leave_room
from util1 import *
from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
from matcha.model.Connection import Connection
import logging
from pickle import NONE

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'd66HR8dç"f_-àgjYYic*dh'
app.debug = True # a supprimer en production

socketio = SocketIO(app)
ROOMS = ["lounge", "news", "games", "coding"]


@app.route('/',methods=['GET', 'POST'])
def homepage():
    if request.method=="POST":
        login=request.form.get('login')
        pwd=request.form.get('password')
        us = DataAccess().find('Users', conditions=('user_name', login))
        if us==None:
            rep='Utilisateur inconnu, merci de vous inscrire'
            return  render_template('home.html', rep = rep)
        if  not (us.password == hash_pwd(pwd,login)):
            rep = "Mauvais mot de passe, merci de réessayer"
            return  render_template('home.html', rep = rep)
        if us.active==False:
            rep = "Vous n'avez pas confirmé votre inscription, veuillez consulter vos mails."
            return  render_template('home.html', rep = rep)
        session['user']= {'name' : login}
        return redirect(url_for('accueil'))
                 #               date_connexion = datetime.now()# rajouter cette info dans la fiche user a ce moment           
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
        num = request.form.get('numphoto')
        photo_name = session['user']['name'] + num + '.jpg'
        if request.form.get('bou')=='raz':
            os.remove('matcha/web/static/photo/'+photo_name)
            return render_template('photo.html',ph1 = ph1, ph2=ph2,ph3=ph3,ph4=ph4,ph5=ph5)
        path = 'static/photo'
        f.save(os.path.join(path, photo_name))     
    return render_template('photo.html',ph1 = ph1, ph2=ph2,ph3=ph3,ph4=ph4,ph5=ph5)
    

@app.route('/accueil/')
def accueil():
    if "user" in session:
        username = session['user']['name']
        return render_template('accueil.html', username=username, rooms=ROOMS)
    else:
        return redirect(url_for('homepage'))   


@app.route('/consultation/<login>/')
def consultation(login):
    if "user" not in session:
        return redirect(url_for('homepage'))
    us = DataAccess().find('Users', conditions=('user_name', login))
    ph1="/static/photo/"+us.user_name+"1.jpg"
    ph2="/static/photo/"+us.user_name+"2.jpg"
    ph3="/static/photo/"+us.user_name+"3.jpg"
    ph4="/static/photo/"+us.user_name+"4.jpg"
    ph5="/static/photo/"+us.user_name+"5.jpg"
    b=str(us.birthday) #champ date transformé en texte
    naissance=b[8:]+'/'+b[5:7]+'/'+b[:4] #conversion date americaine en europeene
    if us.birthday ==None:
        naissance=''
    return render_template('consultation.html',profil=us,ph1=ph1,ph2=ph2,ph3=ph3,ph4=ph4,ph5=ph5,naissance=naissance)

@app.route('/test/')
def test():
    return render_template('test.html')


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
    if us.birthday ==None:
        naissance=''
    latitude=us.latitude
    longitude=us.longitude
    return render_template('profil.html',ph1=ph1, profil=us,naissance=naissance )


@app.route('/recherche/',methods=['GET', 'POST'])
def recherche():
    if "user" not in session:
        return redirect(url_for('homepage')) 
    user = session['user']['name']
    us = DataAccess().find('Users', conditions=('user_name', user))
    if us.gender==None or us.description==None or us.orientation==None or us.birthday==None:
        msg = 'Merci de bien remplir votre fiche avant de chercher un profil compatible'
        return redirect(url_for('profilmodif',msg=msg))
    return render_template('recherche.html')


@app.route('/registration/',methods=['GET', 'POST'])
def registration():
    if request.method=="POST":
        login=request.form.get('login')
        if verif_login(login) !='ok':
            return render_template('registration.html', message = verif_login(login))
        mail=request.form.get('courriel')
        pwd=request.form.get('password')
        pwd2 =request.form.get('password2')
        nom=request.form.get('name')
        prenom=request.form.get('first_name')
        if verif_password(pwd,pwd2) !='ok':
            return render_template('registration.html', message = verif_password(pwd,pwd2))
        if verif_identity(nom,prenom) !='ok':
            return render_template('registration.html', message = verif_identity(nom,prenom))
        session['user']= {'name' : login, 'email' : mail}   
        lien=lien_unique()
        new = Users()
        print('Prenom '+prenom)
        new.first_name = prenom
        print("nom"+nom)
        new.last_name = nom
        new.user_name = login
        new.password = hash_pwd(pwd,login)
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
        mail = rep =''
        us = DataAccess().find('Users', conditions=('user_name', user))
        mail=us.email
        session['user']= {'name' : user, 'email' : mail}
        if us == None:
            rep='Utilisateur inconnu !'
            return render_template('forgot_password.html',rep=rep)
        else :
            lien=lien_unique()
            nature='password'
            us.confirm=lien
            DataAccess().merge(us)  
            ft_send(lien, nature)
            return redirect(url_for('logout')) 
    return render_template('forgot_password.html',user=user)

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('homepage'))
    
@app.route('/validation/<code>')
def validation(code):
    us = DataAccess().find('Users', conditions=('confirm', code))
    if us==None:
        rep="ce lien n'est pas valable !"
        return render_template('validation.html', rep=rep)
    us.active=True
    us.confirm=None
    DataAccess().merge(us)       
    return redirect(url_for('logout'))        


@app.route('/newpassword/<code>', methods=['GET','POST'])
def newpassword(code):
    us = DataAccess().find('Users', conditions=('confirm', code))
    if us==None:
        rep="ce lien n'est pas valable !"
        return render_template('newpasswordfalse.html', rep =rep)
    if request.method=="POST":
        pwd=request.form.get('password')
        pwd2=request.form.get('password2')
        if verif_password(pwd,pwd2) !='ok':
            return render_template('newpassword.html', message = verif_password(pwd,pwd2))
        else:
            hash=hash_pwd(pwd,us.user_name)
            us.confirm=None
            us.password=hash
            DataAccess().merge(us)
            return redirect(url_for('logout'))
    return render_template('newpassword.html', login=us.user_name)

@app.route('/profilmodif/',methods=['GET', 'POST'])
def profilmodif():
    try:
        msg = request.args['msg']
    except:
        msg=''
    if "user" not in session:
        return redirect(url_for('homepage')) 
    user = session['user']['name']
    us = DataAccess().find('Users', conditions=('user_name', user))
    ph1="/static/photo/"+session['user']['name']+"1.jpg"
    nom = us.last_name
    login = us.user_name
    prenom = us.first_name
    bio= us.description
    sexe= us.gender
    if bio==None:
        bio=""
    orientation = us.orientation
    email= us.email
    sexe=us.gender
    
    naissance=(us.birthday)
    latitude=us.latitude
    if latitude == None:
        latitude=0
    longitude=us.longitude
    if longitude == None:
        longitude=0
    if request.method=="POST":
        coordonnee=request.form.get('longlat')
        if (coordonnee):
            us.latitude=coordonnees(coordonnee)[0]
            us.longitude=coordonnees(coordonnee)[1]
        us.first_name=request.form.get('first_name')
        us.last_name=request.form.get('name')
        us.gender=request.form.get('sexe')
        us.orientation=request.form.get('orientation')
        us.description=request.form.get('bio')
        if not(request.form.get('birthday')==''):
            us.birthday=request.form.get('birthday')
        DataAccess().merge(us)
        return redirect(url_for('profil'))
    return render_template('profilmodif.html',nom=nom,prenom=prenom,bio=bio,orientation=orientation,email=email,naissance=naissance,latitude=latitude,longitude=longitude,msg=msg,sexe=sexe)

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

if __name__ =="__main__":
    app.run()
