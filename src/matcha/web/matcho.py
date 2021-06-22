from flask import *
from PIL import Image  
# import os
import psycopg2
from datetime import datetime, timedelta
from random import *
from flask_socketio import SocketIO, join_room, send, emit, leave_room
from time import localtime, strftime
from matcha.web.util1 import *
from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
from matcha.model.Connection import Connection
import logging
from matcha.model.Visit import Visit
from matcha.model.Room import Room
from matcha.model.Message import Message
from matcha.model.Users_room import Users_room
from matcha.model.Notification import Notification
from matcha.orm.reflection import dispatcher
from matcha.web.util2 import *
from matcha.web.util3 import *
from matcha.web.notification_cache import NotificationCache
import urllib
from email.mime import text

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'd66HR8dç"f_-àgjYYic*dh'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=600)  # definie une duree au cookie de session
app.debug = True  # a supprimer en production
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict',
    )
socketio = SocketIO(app)

dict_users_ids = {}

notif_cache = NotificationCache()
notif_cache.init()

def get_user_id(user_name):
        if user_name not in dict_users_ids:
            us = DataAccess().find('Users', conditions=('user_name', user_name))
            dict_users_ids[user_name] = us.id
            return us.id
        return dict_users_ids[user_name]


@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == "POST":
        login = request.form.get('login')
        pwd = request.form.get('password')
        if login ==None  or pwd ==None:
            return render_template('home.html')
        us = DataAccess().find('Users', conditions=('user_name', login))
        if us == None:
            rep = 'Utilisateur inconnu, merci de vous inscrire'
            return  render_template('home.html', rep=rep)
        if  not (us.password == hash_pwd(pwd, login)):
            rep = "Mauvais mot de passe, merci de réessayer"
            return  render_template('home.html', rep=rep)
        if us.active == False:
            rep = "Vous n'avez pas confirmé votre inscription, veuillez consulter vos mails."
            return  render_template('home.html', rep=rep)
        session['user'] = {'name': login}
        session.permanent = True  # le cookie a la duree definie plus haut
        connect = Connection()
        connect.users_id = us.id
        connect.connect_date = datetime.now()
        connect.ip = request.remote_addr
        connect.disconnect_date = None
        DataAccess().persist(connect)
        return redirect(url_for('accueil'))                      
    else: 
        return render_template('home.html')
    

@app.route('/photo/',methods=['GET', 'POST'])
def photo():
    if "user" not in session:
        return redirect(url_for('homepage')) 
    if request.method=="POST":
        path = 'static/photo'
        f = request.files['maphoto']
        num = request.form.get('numphoto')
        photo_name = session['user']['name'] + num + '.jpg'
        if request.form.get('raz')!=None:
            liste_photo=listePhoto(session['user']['name'])
            photo_name2 = '/static/photo/'+photo_name
            if photo_name2 in liste_photo:
                os.remove('static/photo/'+photo_name)  
                liste_photo=listePhoto(session['user']['name'])
            return render_template('photo.html',photos=liste_photo)
        if f:# verification de la présence d'un fichier
            if extension_ok(f.filename): # on vérifie que son extension est valide 
                f.save(os.path.join(path, photo_name))
            else:
                flash('Seuls les fichier JPG ou JPEG sont autorisés !')
        else:
                flash('Aucun fichier choisi !')
    liste_photo=listePhoto(session['user']['name'])
    return render_template('photo.html',photos=liste_photo)


@app.route('/accueil/')
def accueil():
    if "user" not in session:
        return redirect(url_for('homepage'))
    username = session['user']['name']
    us = DataAccess().find('Users', conditions=('user_name', username),joins='topics')
    visits = DataAccess().fetch('Visit', conditions=('visited_id', us.id), joins=('visitor_id', 'V2'),
                                         orderby='v.last_update desc', limit='3')
    visits_made = DataAccess().fetch('Visit', conditions=[('visitor_id', us.id)], joins=('visited_id', 'V3'), 
                                              orderby='v.last_update desc', limit='3')
    likes = DataAccess().fetch('Visit', conditions=[('visited_id', us.id),('islike', True)])
    matchs = DataAccess().fetch('Users_room', conditions=[('master_id', us.id), ('R.active', True)], joins=('room_id', 'R'))


    #######################  recommandations  ###########################
    reco =DataAccess().fetch('Users_recommendation', conditions=[('sender_id', us.id),('is_rejected',False)],joins='receiver_id', limit='3')
    
    if not reco:
        compute_recommendations(us)
        reco =DataAccess().fetch('Users_recommendation', conditions=[('sender_id', us.id),('is_rejected',False)],joins='receiver_id', limit='3')
    suggest=[]
    for rec in reco:
        info = {
            "pseudo": rec.receiver_id.user_name,
            "popul": rec.receiver_id.popularity,
            "id":rec.receiver_id.id
        }

        if (rec.receiver_id.birthday):
            info["age"] = calculate_age(rec.receiver_id.birthday)
        else:
            info["age"] = 0
        
        if os.path.isfile("./static/photo/" + rec.receiver_id.user_name + '1' + ".jpg"):
            info['photo'] = ("/static/photo/" + rec.receiver_id.user_name + '1' + ".jpg")
        else:
            info['photo'] = ('/static/nophoto.jpg')
        suggest.append(info)
        #####################################################################
    like = sum(1 for _ in likes)
    match = sum(1 for _ in matchs)
    visitors = []
    visited_infos = []
    matching = True
    if (
        us.gender is None
        or us.description is None
        or us.orientation is None
        or us.birthday is None
    ):
        matching = False
    for visit in visits:
        info = {}
        info["pseudo"] = visit.visitor_id.user_name
        info["popul"] = visit.visitor_id.popularity
        if (visit.visitor_id.birthday):
            info["age"] = calculate_age(visit.visitor_id.birthday)
        else:
            info["age"] = 0
        info["date"] = visit.last_update.date().isoformat()
        if os.path.isfile("./static/photo/" + visit.visitor_id.user_name + '1' + ".jpg"):
            info['photo'] = ("/static/photo/" + visit.visitor_id.user_name + '1' + ".jpg")
        else:
            info['photo'] = ('/static/nophoto.jpg')
        if(visit.isblocked == False and visit.isfake == False):
            visitors.append(info)

    for visited in visits_made:
        info = {}
        info['age'] = calculate_age(visited.visited_id.birthday)
        info['date'] = visited.visited_id.last_update.date().isoformat()
        info['popul'] = visited.visited_id.popularity
        info['pseudo'] = visited.visited_id.user_name
        print('visited-username : ', visited.visited_id.user_name)
        if os.path.isfile("./static/photo/" + visited.visited_id.user_name + '1' + ".jpg"):
            info['photo'] = ("/static/photo/" + visited.visited_id.user_name + '1' + ".jpg")
        else:
            info['photo'] = ('/static/nophoto.jpg')
        visited_infos.append(info)
    return render_template('accueil.html', match = match, like = like, visited_infos = visited_infos, username=username, visitors=visitors, pop=us.popularity, matching=matching, suggest=suggest, userid=us.id)   


@app.route('/visites/')
def visites():
    if "user" not in session:
        return redirect(url_for('homepage'))
    username = session['user']['name']
    us = DataAccess().find('Users', conditions=('user_name', username))
    visits=DataAccess().fetch('Visit', conditions=('visited_id',us.id), joins=('visitor_id', 'V2'))
    visitors=[]
    like = request.args['like']
    for visit in visits:
        info = {
            "pseudo": visit.visitor_id.user_name,
            "sex": visit.visitor_id.gender,
            "popul": visit.visitor_id.popularity,
            "distance": int(
                distanceGPS(
                    us.latitude,
                    us.longitude,
                    visit.visitor_id.latitude,
                    visit.visitor_id.longitude,
                )
            ),
        }

        info["like"]=visit.islike
        if (visit.visitor_id.birthday):
            info["age"]=calculate_age(visit.visitor_id.birthday)
        else:
            info["age"]=0
        info["date"]=visit.last_update.date().isoformat()
        if os.path.isfile("./static/photo/"+visit.visitor_id.user_name+'1'+".jpg"):
            photo="/static/photo/"+visit.visitor_id.user_name+'1'+".jpg"
        else:
            photo='/static/nophoto.jpg'
        info["photo"]=photo
        if (visit.isblocked == False and visit.isfake == False) and (
            like == 'no' or visit.islike == True
        ):
            visitors.append(info)
        ############# update notification table and cached file ##############
        notifs = DataAccess().fetch('Notification', conditions=[('receiver_id', us.id),
                                                                ('notif_type', 'Visit'),
                                                                ('is_read', False)])
        for n in notifs:
            n.is_read = True
            notif_cache.merge(n, autocommit=False)
        DataAccess().commit()
        ######################################################################
        
        if visitors:
            message = "Qui m'a liké ?" if like=='yes' else 'Qui a consulté mon profil ?'
            return render_template('visites.html', username=username, visitors=visitors, pop=us.popularity, message=message)
        else:
            return redirect(url_for('accueil'))
    else:
        return redirect(url_for('homepage'))
    

@app.route('/recalcul')
def recalculsuggest():
    if "user" not in session:
        return redirect(url_for('homepage'))
    username = session['user']['name']
    us = DataAccess().find('Users', conditions=('user_name', username),joins='topics')
    print('user :::', us)
    compute_recommendations(us)
    return redirect(url_for('accueil'))


@app.route('/suggestions/',methods=['GET', 'POST'])
def suggestions():  # sourcery skip: last-if-guard, merge-dict-assign
    if "user" not in session:
        return redirect(url_for('homepage'))

    username = session['user']['name']
    us = DataAccess().find('Users', conditions=('user_name', username),joins='topics')
    reco =DataAccess().fetch('Users_recommendation', conditions=[('sender_id', us.id),('is_rejected',False)],joins=['receiver_id', 'topics'])

    liste_topics = [topic.tag for topic in us.topics]
    suggests=[]
    for suggest in reco:
        liste_tag = [rec_topi.tag for rec_topi in suggest.topics]
        info={}
        info["tag"]=liste_tag
        info["pseudo"]=suggest.receiver_id.user_name
        info["sex"]=suggest.receiver_id.gender
        info["popul"]=suggest.receiver_id.popularity
        info["distance"]=int(distanceGPS(us.latitude,us.longitude,suggest.receiver_id.latitude,suggest.receiver_id.longitude))
        if (suggest.receiver_id.birthday):
            info["age"]=calculate_age(suggest.receiver_id.birthday)
        else:
           info["age"]=0
        if os.path.isfile("./static/photo/"+suggest.receiver_id.user_name+'1'+".jpg"):
            photo="/static/photo/"+suggest.receiver_id.user_name+'1'+".jpg"
        else:
            photo='/static/nophoto.jpg'
        info["photo"]=photo
        info['id']=suggest.receiver_id.id
        suggests.append(info)
    if request.method=="POST":
        if request.form.get('sexe') and request.form.get('sexe') in['Male','Female']:
            sex=request.form.get('sexe')
        else:
            sex= None
        if request.form.get('agemin') and verifInt(request.form.get('agemin')):
            agemin=request.form.get('agemin')
        else:
            agemin=0
        if request.form.get('agemax') and verifInt(request.form.get('agemax')):
            agemax=request.form.get('agemax')
        else:
            agemax=110
        if request.form.get('popmax') and verifInt(request.form.get('popmax')):
            popmax=request.form.get('popmax')
        else:
            popmax=100
        if request.form.get('popmin') and verifInt(request.form.get('popmin')):
            popmin=request.form.get('popmin')
        else:
            popmin=0
        if request.form.get('dist') and verifInt(request.form.get('dist')):
            dist=request.form.get('dist')
        else:
            dist=None
        if  request.form.getlist('interest') and verifInput(request.form.getlist('interest'),list) != None:  
            interest=request.form.getlist('interest')
        else:
            interest=[]
        filtered=[]
        for sug in suggests:
            if sex != None and sug['sex'] != sex:
                continue
            if agemin and sug['age'] < int(agemin):
                continue
            if agemax and sug['age'] > int(agemax):
                continue
            if popmax and sug['popul'] > int(popmax):
                continue
            if popmin and sug['popul'] < int(popmin):
                continue
            if dist and sug['distance'] > int(dist):
                continue
            if len(interest) >0:
                to_remove=0
                for topic in interest:
                    for tag in sug['tag']:
                        if tag == topic:
                            to_remove += 1
                if to_remove==0:
                    continue
            filtered.append(sug)
        return render_template('suggestions.html', username=username, suggests=filtered, liste_topics=liste_topics)
    if suggests:
        return render_template('suggestions.html', username=username, suggests=suggests, liste_topics=liste_topics)
    else:
        return redirect(url_for('accueil'))
    

@app.route('/rejection/<reject>/',methods=['GET', 'POST'])
def rejection(reject):
    if "user" not in session:
        return redirect(url_for('homepage'))
    username = session['user']['name']
    us = DataAccess().find('Users', conditions=('user_name', username))
    rejected =DataAccess().find('Users_recommendation', conditions=[('sender_id',us.id), ('receiver_id', reject)])
    rejected.is_rejected=True
    DataAccess().merge(rejected)
    return redirect(url_for('accueil'))


@app.route('/consultation/<login>/', methods=['GET', 'POST'])
def consultation(login):
    if "user" not in session:
        return redirect(url_for('homepage'))
    user = session['user']['name']
    dataAccess = DataAccess()
    visitor = dataAccess.find('Users', conditions=('user_name', user))
    us = dataAccess.find('Users', conditions=('user_name', login))
    tag = dataAccess.fetch('Users_topic', conditions=('users_id', us.id))
    date_connect = dataAccess.fetch('Connection', conditions=('users_id', us.id))
    dates_c = []
    for da in date_connect:
        dates_c.append(da.connect_date)
    if len(dates_c) > 0:
        b = str(max(dates_c).date().isoformat())  # champ date transformé en texte
        last_connection = b[8:] + '/' + b[5:7] + '/' + b[:4]  # conversion date americaine en europeene
    else:
        last_connection = 0
    visit = DataAccess().find('Visit', conditions=[('visited_id', us.id), ('visitor_id', visitor.id)])
    visited = DataAccess().find('Visit', conditions=[('visited_id', visitor.id), ('visitor_id', us.id)])
    liked = fake = False
    if visited:
        liked = visited.islike
    if visit:
        visit.visits_number = visit.visits_number + 1
        dataAccess.merge(visit)
        fake = visit.isfake
    else:
        visit = Visit()
        visit.visited_id = us.id
        visit.visitor_id = visitor.id
        visit.visits_number = 1
        visit.islike = False
        visit.isblocked = False
        visit.isfake = False
        dataAccess.persist(visit)
    visits = DataAccess().fetch('Visit', conditions=('visited_id', us.id))
    ############## Notification de la visite ###################
    notif(visitor.id,us.id,'Visit', notif_cache)
    ############################################################
    us.popularity=calculPopularite(us.id)
    DataAccess().merge(us)
    ###########
    tags = []
   
    for t in tag:
        tags.append(t.tag)
    liste_photo = listePhoto(us.user_name)
    nb_photo = 5 - liste_photo.count('/static/nophoto.jpg')
    b = str(us.birthday)  # champ date transformé en texte
    naissance = b[8:] + '/' + b[5:7] + '/' + b[:4]  # conversion date americaine en europeene
    if us.birthday == None:
        naissance = ''
    if request.method == "POST":
        like = request.form.get('like')
        block = request.form.get('block')
        fake = request.form.get('fake')
        if like:
            like = True
        else:
            like = False
        if block:
            block = True
        else:
            block = False
        if fake:
            fake = True
        else:
            fake = False
        if like != visit.islike:
            if like == False and liked==True:
                notif(visitor.id, us.id, 'Dislike', notif_cache)
                closeRoom(visitor.id,us.id, notif_cache)
            else:
                if like==True:
                    notif(visitor.id, us.id, 'Like', notif_cache)
            visit.islike = like  # modifier le score popularité et envoyer une notification
        if block != visit.isblocked:
            visit.isblocked = block
        if fake != visit.isfake:
            visit.isfake = fake
            if fake == True:
                ft_send(login, 'fake')
        dataAccess.merge(visit)
        us.popularity=calculPopularite(us.id)
        DataAccess().merge(us)
        
        ##### creation de la room  ######
        
        if visit.islike == True:
            # visited = DataAccess().find('Visit', conditions=[('visited_id', visit.visitor_id), ('visitor_id', visit.visited_id)])
            if visited:
                if visited.islike == True and visited.isblocked == False and visited.isfake == False:
                    room = DataAccess().find('Users_room', conditions=[('master_id', visited.visited_id), ('slave_id', visited.visitor_id)])
                    if room == None:
                        new_room = Room()
                        new_room.users_ids = [visited.visited_id, visited.visitor_id]
                        new_room.active = True
                        DataAccess().persist(new_room)
                    else:
                        openRoom(visitor.id,us.id)
                    
        #################################
    return render_template('consultation.html', profil=us, photos=liste_photo, naissance=naissance, tags=tags, last_connection=last_connection, visit=visit, nb_photo=nb_photo, liked=liked, fake=fake)


@app.route('/profil/')
def profil():
    if "user" not in session:
        return redirect(url_for('homepage')) 
    user = session['user']['name']
    if os.path.isfile("./static/photo/" + session['user']['name'] + "1.jpg"):
        ph1 = "/static/photo/" + session['user']['name'] + "1.jpg"
    else:
        ph1 = '/static/nophoto.jpg'  
    us = DataAccess().find('Users', conditions=('user_name', user))
    tag = DataAccess().fetch('Users_topic', conditions=('users_id', us.id))    
    tags = []
    for t in tag:
        tags.append(t.tag)
    b = str(us.birthday)  # champ date transformé en texte
    naissance = b[8:] + '/' + b[5:7] + '/' + b[:4]  # conversion date americaine en europeene
    if us.birthday == None:
        naissance = ''
    latitude = us.latitude
    longitude = us.longitude
    return render_template('profil.html', ph1=ph1, profil=us, naissance=naissance, tags=tags)


@app.route('/recherche/',methods=['GET', 'POST'])
def recherche():
    if "user" not in session:
        return redirect(url_for('homepage')) 
    user = session['user']['name']
    us = DataAccess().find('Users', conditions=('user_name', user))
    tops = DataAccess().fetch('Topic')
    topics=[]
    for topic in tops:
        topics.append(topic.tag)
    if us.gender==None or us.description==None or us.orientation==None or us.birthday==None:
        msg = 'Merci de bien remplir votre fiche avant de chercher un profil compatible'
        return render_template('alerte.html',msg=msg)
    if us.orientation != "Hetero":
        sex_to_find=us.gender
    else:
        if us.gender=="Male":
            sex_to_find="Female"
        else:
            sex_to_find="Male"
    latitude=us.latitude
    longitude=us.longitude
    ##### Criteres de recherches
    if request.method=="POST":
        coordonnee=request.form.get('longlat')
        if (coordonnee) and verifCoor(coordonnee):
            latitude=coordonnees(coordonnee)[0]
            longitude=coordonnees(coordonnee)[1]
        else:
            latitude=us.latitude
            longitude=us.longitude
        criteres={}
        if request.form.get('sexe') and request.form.get('sexe') in ['Male','Female']:
            criteres['sexe']=request.form.get('sexe')
        if us.orientation:
            criteres['orientation']=us.orientation
        else:
            criteres['orientation']='Bi'
        criteres['sexe_chercheur']=us.gender
        criteres['latitude']=latitude
        criteres['longitude']=longitude
        if request.form.get('km') and verifInt(request.form.get('km')):
            criteres['dist_max']=request.form.get('km')
        else:
            criteres['dist_max']=20000
        if request.form.get('agemin') and verifInt(request.form.get('agemin')):
            criteres['age_min']=int(request.form.get('agemin'))
        else:
            criteres['age_min']=18
        if request.form.get('agemax') and verifInt(request.form.get('agemax')):
            criteres['age_max']=int(request.form.get('agemax'))
        else:
            criteres['age_max']=110
        if request.form.get('popmin') and verifInt(request.form.get('popmin')):
            criteres['pop_min']=request.form.get('popmin')
        else:
            criteres['pop_min']=0
        if request.form.get('popmax') and verifInt(request.form.get('popmax')):
            criteres['pop_max']=request.form.get('popmax')
        else:
            criteres['pop_max']=100
        criteres['interets']=request.form.getlist('interest')
        criteres['id']=us.id
        return render_template('resultats.html',candidats=find_profil(criteres))
    return render_template('recherche.html',topics=topics, sex_to_find=sex_to_find, latitude=latitude,longitude=longitude)


@app.route('/registration/',methods=['GET', 'POST'])
def registration():
    if request.method=="POST":
        login=verifInput(request.form.get('login'),str)
        mail=verifInput(request.form.get('courriel'),str)
        pwd=verifInput(request.form.get('password'),str)
        pwd2 =verifInput(request.form.get('password2'),str)
        nom=verifInput(request.form.get('name'),str)
        prenom=verifInput(request.form.get('first_name'),str)
        if login==None or mail== None or pwd==None or pwd2==None or nom==None or prenom==None:
            return render_template('registration.html', message = "Merci de remplir tous les champs")
        if verif_login(login) !='ok':
            return render_template('registration.html', message = verif_login(login))
        if verif_password(pwd,pwd2) !='ok':
            return render_template('registration.html', message = verif_password(pwd,pwd2))
        if verif_identity(nom,prenom) !='ok':
            return render_template('registration.html', message = verif_identity(nom,prenom))
        if verifMail(mail) ==False:
            return render_template('registration.html', message = "email invalide")
        session['user']= {'name' : login, 'email' : mail}   
        lien=lien_unique()
        new = Users()
        new.first_name = prenom
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
        new.is_recommendable = False
        new.latitude = request.form.get('latitude')
        new.longitude = request.form.get('longitude')
        new.popularity = 0
        DataAccess().persist(new)
        ft_send(lien,'registration')
        session.clear()
        return redirect(url_for('homepage'))
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
        if user:
            mail = rep =''
            us = DataAccess().find('Users', conditions=('user_name', user))
            if us == None:
                rep='Utilisateur inconnu !'
                return render_template('forgot_password.html',rep=rep)
            else :
                lien=lien_unique()
                mail=us.email
                session['user']= {'name' : user, 'email' : mail}
                nature='password'
                us.confirm=lien
                DataAccess().merge(us)  
                ft_send(lien, nature)
                return redirect(url_for('logout')) 
    return render_template('forgot_password.html',user=user)


@app.route('/logout/')
def logout():
    login = session['user']['name']
    us = DataAccess().find('Users', conditions=('user_name', login))
    connections = DataAccess().fetch('Connection', conditions=('users_id', us.id), orderby='connect_date desc')
    last_connect = connections[0]
    last_connect.disconnect_date = datetime.now()
    DataAccess().merge(last_connect)
    # enregistrer deconnexion pour room du chat et autres notifs
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
    session.clear()     
    return redirect(url_for('homepage'))        


@app.route('/newpassword/<code>', methods=['GET','POST'])
def newpassword(code):
    us = DataAccess().find('Users', conditions=('confirm', code))
    if us==None:
        rep="ce lien n'est pas valable !"
        return render_template('newpasswordfalse.html', rep =rep)
    session['user']= {'name' : us.user_name}
    if request.method=="POST":
        pwd=request.form.get('password')
        pwd2=request.form.get('password2')
        if pwd == None or pwd2 == None:
            return render_template('newpassword.html', login=us.user_name)
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
    if "user" not in session:
        return redirect(url_for('homepage'))
    dataAccess = DataAccess()
    user = session['user']['name']
    us = dataAccess.find('Users', conditions=('user_name', user))
    tops = dataAccess.fetch('Topic')
    tag = dataAccess.fetch('Users_topic', conditions=('users_id',us.id))
    topics=[]
    tags=[]
    for topic in tops:
        topics.append(topic.tag)
    for t in tag:
        tags.append(t.tag)
    naissance=(us.birthday)
    latitude=us.latitude
    if latitude == None:
        latitude=0
    longitude=us.longitude
    if longitude == None:
        longitude=0
    if request.method=="POST":
        coordonnee=request.form.get('longlat')
        if verifInput(coordonnee,str) != None:
            if verifCoor(coordonnee):
                us.latitude=coordonnees(coordonnee)[0]
                us.longitude=coordonnees(coordonnee)[1]
        interets=request.form.getlist('interest')
        if verifInput(interets,list) == None:
            return render_template('profilmodif.html',profil=us,naissance=naissance,tags=tags,topics=topics)
        dataAccess.call_procedure('INSERT_TOPICS', parameters=[us.id, interets])
        if request.form.get('first_name'):
            us.first_name=request.form.get('first_name')
        if request.form.get('courriel'):   
            if verifMail(request.form.get('courriel')):
                us.email=request.form.get('courriel')
        
        if request.form.get('name'):   
            us.last_name=request.form.get('name')
        if request.form.get('sexe') and request.form.get('sexe') in ['Male','Female']:
            us.gender=request.form.get('sexe')
        if request.form.get('orientation') and request.form.get('orientation') in ['Bi','Homo','Hetero']:
            us.orientation=request.form.get('orientation')
        if request.form.get('bio'):
            us.description=request.form.get('bio')
        if not(request.form.get('birthday')==''):
            if verifDate(request.form.get('birthday')):
                us.birthday=request.form.get('birthday')
        DataAccess().merge(us)
        tagset = set()
        if (request.form.get('interet')):
            new_tag = request.form.get('interet')
            if verif_word(new_tag):
                new_tag = format_word(new_tag)                
                tagset.add(new_tag)
        for inte in interets:
            tagset.add(inte)
        dataAccess.call_procedure(procedure='insert_topics', parameters=(us.id, list(tagset)))
        return redirect(url_for('profil'))
    return render_template('profilmodif.html', profil=us, naissance=naissance, tags=tags, topics=topics)


@app.route('/chat/')
def chat():
    if "user" in session:
        username = session['user']['name']
        us_id = get_user_id(username)
        room_list = DataAccess().fetch('Users_room',
                                       conditions=[('R.active', True), ('U.slave_id', us_id)],
                                       joins=[('master_id', 'US'), ('room_id', 'R')])
        messages_list = DataAccess().fetch('Notification', conditions=[('receiver_id', us_id), 
                                                                        ('notif_type', 'Message'),
                                                                        ('is_read', False)])
        msgs = {}
        for m in messages_list:
            if m.sender_id in msgs:
                msgs[m.sender_id] += 1
            else:
                msgs[m.sender_id] = 1
        return render_template('chat.html',
                                username=username,
                                user_id=us_id,
                                rooms=room_list,
                                msgs=msgs
                                )
    else:
        return redirect(url_for('homepage'))


@app.route('/like')
def like():
    if "user" not in session:
        return redirect(url_for('homepage'))
    username = session['user']['name']
    us_id = get_user_id(username)
    like_list = DataAccess().fetch('Visit', conditions=[('visited_id', us_id),
                                                               ('islike', True)],
                                                   joins=('visitor_id', 'V2'), 
                                                   orderby='V.last_update desc')
    ############# update notification table and cache file #########
    like_list2 = DataAccess().fetch('Notification', conditions=[('receiver_id', us_id),
                                                                ('notif_type', 'Like'),
                                                                ('is_read', False)])
    new_like = []
    for l in like_list2:
        if l.sender_id not in new_like:
            new_like.append(l.sender_id)
        l.is_read = True
        notif_cache.merge(l, autocommit=False)
    DataAccess().commit()
        ###############################################################
    like_infos = []
    for l in like_list:
        info = {}
        info['username'] = l.visitor_id.user_name
        info['date'] = l.last_update.date().isoformat()
        info['is_read'] = True
        if l.visitor_id.id in new_like:   
            info['is_read'] = False
        if os.path.isfile("./static/photo/" + l.visitor_id.user_name + '1' + ".jpg"):
            info['photo'] = ("/static/photo/" + l.visitor_id.user_name + '1' + ".jpg")
        else:
            info['photo'] = ('/static/nophoto.jpg')
        like_infos.append(info)
        
       
    return render_template('like.html', liste = like_infos)
        

@app.route('/dislike')
def dislike():
    if "user" not in session:
        return redirect(url_for('homepage'))
    username = session['user']['name']
    us_id = get_user_id(username)
    dislike_list = DataAccess().fetch('Notification', 
                                      conditions=[('receiver_id', us_id),
                                                  ('notif_type', 'Dislike')], 
                                      joins=('sender_id', 'S'),
                                      orderby='N.id desc')
    
    dislike_infos = []
    test_duplicate = {}
    for d in dislike_list:
        if not d.sender_id.user_name in test_duplicate:
            test_duplicate[d.sender_id.user_name] = 1
            info = {}
            info['username'] = d.sender_id.user_name
            info['date'] = d.created.date().isoformat()
            info['is_read'] = d.is_read
            if os.path.isfile("./static/photo/" + d.sender_id.user_name + '1' + ".jpg"):
                info['photo'] = ("/static/photo/" + d.sender_id.user_name + '1' + ".jpg")
            else:
                info['photo'] = ('/static/nophoto.jpg')
            dislike_infos.append(info)
        
        ######## update notification table and cache file #######
    dislike_list2 = DataAccess().fetch('Notification', conditions=[('receiver_id', us_id), 
                                                                   ('notif_type', 'Dislike'), 
                                                                   ('is_read', False)])
    for d in dislike_list2:
        d.is_read = True 
        notif_cache.merge(d, autocommit=False) 
    DataAccess().commit()
        #########################################################
    return render_template('dislike.html', liste = dislike_infos)
    

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


###### mise à jour asynchrone des notifications ##########
@app.route("/ajax/")
def refresh_notif():
    print("ajax")
    if "user" in session:
        username = session['user']['name']
        (like, msg, visit, dislike) = notif_cache.get_unread(username)
        list_notifs = {'like': like, 'msg': msg, 'visit': visit, 'dislike': dislike}
        json_notif = json.dumps(list_notifs, default=dispatcher.encoder_default)
        return json_notif
    
################################################
########## Temps réel avec socketio  ###########
################################################


########### profil consult connect #############

# receive consult page infos
@socketio.on('profil_user')
def profil_user(data):
    socketio.emit('visited_profil', data, broadcast=True)


# visited page response
@socketio.on('visited_response')
def visited_response(data):
    socketio.emit('visitor_reception', data, broadcast=True)


############## Connect users ###########
@socketio.on('login')
def login(data):
    print('login = ', data['msg'])

# Connexions des users
@socketio.on('connect_user')
def login_connect(data):
    print('login-connect = ', data['msg'])

############# Chat  ###################


# receive and send message
@socketio.on('message')
def message(data):
    # print(f"\n\n{data}\n\n")
    msg = Message()
    msg.chat = data['msg']
    msg.room_id = data['room']
    msg.sender_id = data['user_id']
    receiver_id = get_user_id(data['receiver'])
    notif = Notification()
    notif.sender_id = data['user_id']
    notif.receiver_id = receiver_id
    notif.notif_type = 'Message'
    notif.is_read = False
    DataAccess().persist(msg)
    notif_cache.persist(notif)
    # print('notif_cache.cache : ', *notif_cache.cache)
    send({
          'msg': data['msg'],
          'sender': data['sender'],
          'receiver': data['receiver'],
          'room': data['room'], 'notif': notif.id,
          'time_stamp': strftime('%d-%b %H:%M', localtime())
          },
          room=data['room']
        )
    
    
# test receiver connection
@socketio.on('receiver_connect')
def test_connect(data):
    if data['test'] == True:
        notif = DataAccess().find('Notification', conditions=('id', data['notif']))
        notif.is_read = True
        notif_cache.merge(notif)
        
        
# join room
@socketio.on('join')
def join(data):
    join_room(data['room'])
    msgs = DataAccess().fetch("Message", conditions=('room_id', data['room']))
    user = DataAccess().find('Users', conditions=('user_name', data['username']))
    room_data = DataAccess().find('Users_room', conditions=('room_id', data['room']))
    # print('room = ',data['room'])
    receiver_id = room_data.slave_id
    sender_id = room_data.master_id
    if room_data.slave_id == user.id:
        receiver_id = room_data.master_id
        sender_id = room_data.slave_id
    receiver = notif_cache.get_user_name(receiver_id)
    
    msgs_json = json.dumps(msgs, default=dispatcher.encoder_default)
    
    ###### mise a jour des notifs 'message' a true (concernant cette room) ##########
    notif_list = DataAccess().fetch('Notification', conditions=[
                                                                ('sender_id', receiver_id),
                                                                ('receiver_id', sender_id),
                                                                ('notif_type', 'Message'),
                                                                ('is_read', False)
                                                                ])
    for notif in notif_list:
        notif.is_read = True
        notif_cache.merge(notif, autocommit=False)
    DataAccess().commit()
    #################################################################################
    emit('display_old_messages', {
           'username': data['username'],
           'msgs_list': msgs_json,
           'user_id': user.id,
           'receiver': receiver,
           'receiver_id': receiver_id,
          },
        room=data['room']
        )
          
   
# leave room       
@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    ########## si on veut ajouter un message de deconnection  ##############
    # msg = ""
    # msg_json = json.dumps(msg, default=dispatcher.encoder_default)
    # enregistrer la date de deconnexion pour les notifications
    # send({msg}, room=data['room'])  # msg optionnel
    
    
# Lance les serveurs
if __name__ == '__main__':
    socketio.run(app)
    
