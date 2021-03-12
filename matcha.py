from flask import *
from PIL import Image  
import os
from flask_mail import Mail, Message
from config import ConfigMail

app = Flask(__name__)
app.config.from_object(ConfigMail)
mail = Mail(app)
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
        #size = os.path.getsize(f)
        return f.filename
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
        session['user']= {'name' : user}   
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
    msg=Message("confirmation d'inscription",recipients=['ogasnier@gmail.com'])
    msg.body="Bravo vous venez de vous inscrire !"
    mail.send(msg)
    return redirect(url_for('accueil'))
