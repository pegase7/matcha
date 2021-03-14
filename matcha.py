from flask import *
from PIL import Image  
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'd66HR8dç"f_-àgjYYic*dh'
app.debug = True # a supprimer en production

@app.route('/',methods=['GET', 'POST'])
def homepage():
    if request.method=="POST":
        user=request.form.get('login')
        session['user']= {'name' : user}
        return redirect(url_for('accueil'))
    else:   
        return render_template('home.html')

@app.route('/photo/',methods=['GET', 'POST'])
def photo():
    if request.method=="POST":
        f = request.files['maphoto']
        b=f.filename
        path = 'static/photo'
        f.save(os.path.join(path, 'temp.jpg'))
        
        return redirect(url_for('okphoto'))
    else:
        return render_template('photo.html')

@app.route('/accueil/')
def accueil():
    return render_template('accueil.html')

@app.route('/test/')
def test():
    return render_template('test.html')

@app.route('/profil/')
def profil():
    return render_template('profil.html')

@app.route('/recherche/')
def recherche():
    return render_template('recherche.html')

@app.route('/registration/',methods=['GET', 'POST'])
def registration():
    if request.method=="POST":
        user=request.form.get('login')
        mail=request.form.get('courriel')
        session['user']= {'name' : user, 'email' : mail}   
        return redirect(url_for('send'))
    else:
        return render_template('registration.html')

@app.route('/forgot/')
def forgot():
    return render_template('forgot_password.html')

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('homepage'))

@app.route('/send/')
def send():
    Fromadd = "matcha@ik.me"
    Toadd = session['user']['email']   ##  Spécification du destinataire
    message = MIMEMultipart()    
    message['From'] = Fromadd   
    message['To'] = Toadd   
    message['Subject'] = "inscription" 
    msg = "Bravo, " + session['user']['name'] +" vous êtes maintenant inscrit"    
    message.attach(MIMEText(msg.encode('utf-8'), 'plain', 'utf-8'))  
    serveur = smtplib.SMTP('mail.infomaniak.com', 587)  ## Connexion au serveur sortant 
    serveur.starttls()    ## Spécification de la sécurisation
    serveur.login(Fromadd, "42Flask@lyon")    ## Authentification
    texte= message.as_string().encode('utf-8')    
    Toadds = [Toadd]
    serveur.sendmail(Fromadd, Toadds, texte)    ## Envoi du mail
    serveur.quit() 
    return redirect(url_for('accueil'))
    
@app.route('/okphoto')
def okphoto():
    os.remove('static/photo/temp.jpg')
    return render_template('okphoto.html')