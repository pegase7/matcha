from flask import *
from PIL import Image  
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import psycopg2
from UserManager import USERS_MANAGER
from datetime import datetime
from random import *

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'd66HR8dç"f_-àgjYYic*dh'
app.debug = True # a supprimer en production

def send(unique, nature):
    lien = 'http://127.0.0.1:5000/validation/'+unique
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

@app.route('/',methods=['GET', 'POST'])
def homepage():
    users = USERS_MANAGER().get_users()
    if request.method=="POST":
        user=request.form.get('login')
        pwd=request.form.get('password')
        rep='Utilisateur inconnu, merci de vous inscrire'
        for u in users:
            if u[3] == user:
                if u[4] == pwd:
                    if u[7]:#verifier si l'utilisateur est actif
                        session['user']= {'name' : user}
                        date_connexion = datetime.now()# rajouter cette info dans la fiche user a ce moment
                        return redirect(url_for('accueil'))
                    else:
                        rep = "vous n'avez pas encore confirmé votre inscription"
                else:
                    rep = "Mauvais mot de passe, merci de réessayer"
        return  render_template('home.html', rep = rep)
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
        path = 'static/photo'
        f.save(os.path.join(path, photo_name))
        
        return redirect(url_for('okphoto'))
    else:
        return render_template('photo.html',ph1 = ph1, ph2=ph2,ph3=ph3,ph4=ph4,ph5=ph5)

@app.route('/accueil/')
def accueil():
    if "user" in session:
        return render_template('accueil.html')
    else:
        return redirect(url_for('homepage'))   

@app.route('/test/')
def test():
    return render_template('test.html')

@app.route('/profil/')
def profil():
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

    return render_template('profil.html',ph1=ph1, nom = nom, prenom = prenom, sexe=sexe, orientation=orientation,bio=bio,email =email, naissance=naissance)

@app.route('/recherche/',methods=['GET', 'POST'])
def recherche():
    if "user" not in session:
        return redirect(url_for('homepage')) 
    return render_template('recherche.html')

@app.route('/registration/',methods=['GET', 'POST'])
def registration():
    if request.method=="POST":
        user=request.form.get('login')
        mail=request.form.get('courriel')
        session['user']= {'name' : user, 'email' : mail}   
        lien=lien_unique()
        #ici enregistre le lien dans la fiche membre
        send(lien,'registration')
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
            send(lien, 'nature')
            return redirect(url_for('logout')) 
    return render_template('forgot_password.html',user=user)

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('homepage'))
    
@app.route('/okphoto')
def okphoto():
    if "user" not in session:
        return redirect(url_for('homepage')) 
    #os.remove('static/photo/temp.jpg')
    return render_template('okphoto.html')

@app.route('/validation/<code>')
def validation(code):
    return render_template('validation.html', code =code)

@app.route('/newpassword/<code>', methods=['GET','POST'])
def newpassword(code):
    return render_template('newpassword.html', code =code)