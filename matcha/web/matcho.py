from matcha.web.util1 import *
from flask import *
from PIL import Image  
import os
import psycopg2
from datetime import datetime,timedelta
from random import *
from flask_socketio import SocketIO, join_room, send, emit, leave_room
from time import localtime, strftime
from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
from matcha.model.Visit import Visit
from matcha.model.Connection import Connection
import logging
from matcha.model.Room import Room
from matcha.model.Message import Message
from matcha.model.Users_room import Users_room
from matcha.model.Notification import Notification 
from matcha.orm.reflection import dispatcher
from matcha.web.util2 import *
from matcha.web.notification_cache import NotificationCache
import urllib
# import threading
#from matcha.web.thread.disconnect import DisconnectInactiveUsersThread


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'd66HR8dç"f_-àgjYYic*dh'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=6000)  # definie une duree au cookie de session
app.debug = True  # a supprimer en production
# SESSION_COOKIE_SECURE=True,
# SESSION_COOKIE_HTTPONLY=True,
# SESSION_COOKIE_SAMESITE='Strict'
socketio = SocketIO(app)
# diut = DisconnectInactiveUsersThread()

notif_cache = NotificationCache()
notif_cache.init()

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
        connect=Connection()
        connect.users_id=us.id
        connect.connect_date=datetime.now()
        connect.ip=request.remote_addr
        connect.disconnect_date=None
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
    if "user" in session:
        username = session['user']['name']
        us = DataAccess().find('Users', conditions=('user_name', username))
        visits = DataAccess().fetch('Visit', conditions=('visited_id', us.id), joins=('visitor_id', 'V2'),
                                             orderby='v.last_update desc', limit='3')
        visits_made = DataAccess().fetch('Visit', conditions=[('visitor_id', us.id)], joins=('visited_id', 'V3'), 
                                                  orderby='v.last_update desc', limit='3')
        likes = DataAccess().fetch('Visit', conditions=[('visited_id', us.id),('islike', True)])
        matchs = DataAccess().fetch('Users_room', conditions=[('master_id', us.id), ('R.active', True)], joins=('room_id', 'R'))
        like = 0
        match = 0
        for l in likes:
            like = like + 1
            
        for m in matchs:
            match = match + 1
        
        visitors = []
        visited_infos = []
        matching = True
        if us.gender == None or us.description == None or us.orientation == None or us.birthday == None:
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
        print('visitor : ', *visitors)
            
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
        print('visited_infos : ', visited_infos)
        return render_template('accueil.html', match = match, like = like, visited_infos = visited_infos, username=username, visitors=visitors, pop=us.popularity, matching=matching)
    else:
        return redirect(url_for('homepage'))   

@app.route('/visites/')
def visites():
    like = request.args['like']
    if "user" in session:
        username = session['user']['name']
        us = DataAccess().find('Users', conditions=('user_name', username))
        visits=DataAccess().fetch('Visit', conditions=('visited_id',us.id), joins=('visitor_id', 'V2'))
        visitors=[]
        for visit in visits:
            info={}
            info["pseudo"]=visit.visitor_id.user_name
            info["sex"]=visit.visitor_id.gender
            info["popul"]=visit.visitor_id.popularity
            info["distance"]=int(distanceGPS(us.latitude,us.longitude,visit.visitor_id.latitude,visit.visitor_id.longitude))
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
            if(visit.isblocked==False and visit.isfake==False):
                if like=='no':
                    visitors.append(info)
                elif visit.islike==True:
                    visitors.append(info)
        if like=='yes':
            message="Qui m'a liké ?"
        else:
            message='Qui a consulté mon profil ?'
        if visitors:
            return render_template('visites.html', username=username, visitors=visitors, pop=us.popularity, message=message)
        else:
            return redirect(url_for('accueil'))
    else:
        return redirect(url_for('homepage'))


@app.route('/consultation/<login>/',methods=['GET', 'POST'])
def consultation(login):
    if "user" not in session:
        return redirect(url_for('homepage'))
    user = session['user']['name']
    dataAccess = DataAccess()
    visitor = dataAccess.find('Users', conditions=('user_name', user))
    us = dataAccess.find('Users', conditions=('user_name', login))
    tag = dataAccess.fetch('Users_topic', conditions=('users_id',us.id))
    date_connect=dataAccess.fetch('Connection', conditions=('users_id',us.id))
    dates_c=[]
    for da in date_connect:
        dates_c.append(da.connect_date)
    if len(dates_c)>0 :
        b=str(max(dates_c).date().isoformat()) #champ date transformé en texte
        last_connection=b[8:]+'/'+b[5:7]+'/'+b[:4] #conversion date americaine en europeene
    else:
        last_connection=0
    visit = DataAccess().find('Visit', conditions=[('visited_id', us.id), ('visitor_id', visitor.id)])
    visited =DataAccess().find('Visit', conditions=[('visited_id', visitor.id), ('visitor_id', us.id)])
    liked=fake=False
    if visited:
        liked=visited.islike
    if visit:
        visit.visits_number = visit.visits_number + 1
        dataAccess.merge(visit)
        fake=visit.isfake
    else:
        visit = Visit()
        visit.visited_id = us.id
        visit.visitor_id = visitor.id
        visit.visits_number = 1
        visit.islike=False
        visit.isblocked=False
        visit.isfake=False
        dataAccess.persist(visit)
    visits = DataAccess().fetch('Visit', conditions=('visited_id', us.id))
    ############## Notification de la visite ###################
    notif(visitor.id,us.id,'Visit')
    us.popularity=calculPopularite(us.id)
    DataAccess().merge(us)
    ###########
    tags=[]
   
    for t in tag:
        tags.append(t.tag)
    liste_photo=listePhoto(us.user_name)
    nb_photo = 5 - liste_photo.count('/static/nophoto.jpg')
    b=str(us.birthday) #champ date transformé en texte
    naissance=b[8:]+'/'+b[5:7]+'/'+b[:4] #conversion date americaine en europeene
    if us.birthday ==None:
        naissance=''
    if request.method=="POST":
        like=request.form.get('like')
        block=request.form.get('block')
        fake=request.form.get('fake')
        if like:
            like=True
        else:
            like=False
        if block:
            block=True
        else:
            block=False
        if fake:
            fake=True
        else:
            fake=False
        if like != visit.islike:
            if like==False and liked==True:
                notif(visitor.id,us.id,'Dislike')
                closeRoom(visitor.id,us.id)
            else:
                if like==True:
                    notif(visitor.id,us.id,'Like')
            visit.islike = like #modifier le score popularité 
        if block != visit.isblocked:
            visit.isblocked=block
        if fake != visit.isfake:
            visit.isfake=fake
            if fake==True:
                ft_send(login,'fake')
        dataAccess.merge(visit)
        us.popularity=calculPopularite(us.id)
        DataAccess().merge(us)
        ##### creation de la room si necessaire ######
        if visit.islike == True:
            #visited = DataAccess().find('Visit', conditions=[('visited_id', visit.visitor_id), ('visitor_id', visit.visited_id)])
            if visited:
                if visited.islike == True and visited.isblocked == False and visited.isfake == False:
                    room = DataAccess().find('Users_room', conditions=[('master_id', visited.visited_id), ('slave_id', visited.visitor_id)])
                    if room == None:
                        new_room = Room()
                        new_room.users_ids = [visited.visited_id, visited.visitor_id]
                        new_room.active  = True
                        DataAccess().persist(new_room)
                    else:
                        openRoom(visitor.id,us.id)

        #################################
    return render_template('consultation.html',profil=us,photos=liste_photo,naissance=naissance,tags=tags,last_connection=last_connection,visit=visit,nb_photo=nb_photo,liked=liked,fake=fake)


@app.route('/profil/')
def profil():
    if "user" not in session:
        return redirect(url_for('homepage')) 
    user = session['user']['name']
    if os.path.isfile("./static/photo/"+session['user']['name']+"1.jpg"):
        ph1="/static/photo/"+session['user']['name']+"1.jpg"
    else:
        ph1='/static/nophoto.jpg'
    us = DataAccess().find('Users', conditions=('user_name', user))
    tag = DataAccess().fetch('Users_topic', conditions=('users_id',us.id))    
    tags=[]
    for t in tag:
        tags.append(t.tag)
    b=str(us.birthday) #champ date transformé en texte
    naissance=b[8:]+'/'+b[5:7]+'/'+b[:4] #conversion date americaine en europeene
    if us.birthday ==None:
        naissance=''
    latitude=us.latitude
    longitude=us.longitude
    return render_template('profil.html',ph1=ph1, profil=us,naissance=naissance,tags=tags)


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
        if (coordonnee):
            latitude=coordonnees(coordonnee)[0]
            longitude=coordonnees(coordonnee)[1]
        else:
            latitude=us.latitude
            longitude=us.longitude
        criteres={}
        criteres['sexe']=request.form.get('sexe')
        if us.orientation:
            criteres['orientation']=us.orientation
        else:
            criteres['orientation']='Bi'
        criteres['sexe_chercheur']=us.gender
        criteres['latitude']=latitude
        criteres['longitude']=longitude
        if request.form.get('km'):
            criteres['dist_max']=request.form.get('km')
        else:
            criteres['dist_max']=20000
        if request.form.get('agemin'):
            criteres['age_min']=request.form.get('agemin')
        else:
            criteres['age_min']=18
        if request.form.get('agemax'):
            criteres['age_max']=request.form.get('agemax')
        else:
            criteres['age_max']=110
        if request.form.get('popmin'):
            criteres['pop_min']=request.form.get('popmin')
        else:
            criteres['pop_min']=0
        if request.form.get('popmax'):
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
    last_connect=connections[0]
    last_connect.disconnect_date=datetime.now()
    DataAccess().merge(last_connect)
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
        if (coordonnee):
            us.latitude=coordonnees(coordonnee)[0]
            us.longitude=coordonnees(coordonnee)[1]
        interets=request.form.getlist('interest')
        dataAccess.call_procedure('INSERT_TOPICS', parameters=[us.id, interets])
        us.first_name=request.form.get('first_name')
        us.last_name=request.form.get('name')
        us.gender=request.form.get('sexe')
        us.orientation=request.form.get('orientation')
        us.description=request.form.get('bio')
        if not(request.form.get('birthday')==''):
            us.birthday=request.form.get('birthday')
        DataAccess().merge(us)
        tagset = set()
        if (request.form.get('interet')):
            tagset.add(request.form.get('interet'))
        for inte in interets:
            tagset.add(inte)
        dataAccess.call_procedure(procedure='insert_topics', parameters=(us.id, list(tagset)))
        return redirect(url_for('profil'))
    return render_template('profilmodif.html',profil=us,naissance=naissance,tags=tags,topics=topics)


@app.route('/chat/')
def chat():
    if "user" in session:
        username = session['user']['name']
        user = DataAccess().find('Users', conditions=('user_name', username))
        room_list = DataAccess().fetch('Users_room', 
                                       conditions=[('R.active', True), ('U.slave_id', user.id)], 
                                       joins=[('master_id', 'US'), ('room_id', 'R')])
        return render_template('chat.html',
                                username=username,
                                user_id=user.id, 
                                rooms=room_list
                                )
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

###### mise à jour asynchrone des notifications ##########
@app.route("/ajax/")
def refresh_notif():
   # print("ajax")
    if "user" in session:
        username = session['user']['name']
        us = DataAccess().find('Users', conditions=[('user_name', username)])
        (like, msg, visit, dislike) = notif_cache.get_unread(us.id)
        print('like : ', like)
        list_notifs = {'like': like, 'msg': msg, 'visit': visit, 'dislike': dislike}
        json_notif = json.dumps(list_notifs, default=dispatcher.encoder_default)
        return json_notif



################################################
########## Temps réel avec socketio  ###########
################################################

# Connexions des users
@socketio.on('connect_user')
def login_connect(data):
    pass
    #print('login-connect = ', data['msg'])


############# Chat  ###################

#receive and send message
@socketio.on('message')
def message(data):
    # print(f"\n\n{data}\n\n")
    msg = Message()
    msg.chat = data['msg']
    msg.room_id = data['room']
    msg.sender_id = data['user_id']
    receiver = DataAccess().find('Users', conditions=('user_name', data['receiver']))
    notif = Notification()
    notif.sender_id = data['user_id']
    notif.receiver_id = receiver.id
    notif.notif_type = 'Message'
    notif.is_read = False
    DataAccess().persist(msg)
    # DataAccess().persist(notif)
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
    
    
#test receiver connection
@socketio.on('receiver_connect')
def test_connect(data):
    if data['test'] == True:
        notif = DataAccess().find('Notification', conditions=('id', data['notif']))
        notif.is_read = True
        # DataAccess().merge(notif)
        notif_cache.merge(notif)
        
        
#join room
@socketio.on('join')
def join(data):
    join_room(data['room'])
    msgs = DataAccess().fetch("Message", conditions=('room_id', data['room']))
    user = DataAccess().find('Users', conditions=('user_name', data['username']))
    room_data = DataAccess().find('Users_room', conditions=('room_id', data['room']))
    print('room = ',data['room'])
    receiver_id = room_data.slave_id
    sender_id = room_data.master_id
    if room_data.slave_id == user.id:
        receiver_id = room_data.master_id
        sender_id = room_data.slave_id
    # print('receiver_id = ', receiver_id)
    receiver = DataAccess().find('Users', conditions=('id', receiver_id))
    # print('receiver = ', receiver.user_name)
    # print('sender_id = ', sender_id)
    # print(data['username'])
    # print(user.id)
    # print("list msgs = ")
    msgs_json = json.dumps(msgs, default=dispatcher.encoder_default)
    # mise a jour des notifs 'message' a true (concernant cette room)
    notif_list = DataAccess().fetch('Notification', conditions=[
                                                                ('sender_id', receiver_id),
                                                                ('receiver_id', sender_id),
                                                                ('notif_type', 'Message'),
                                                                ('is_read', False)
                                                                ])
    print(notif_list)
    for notif in notif_list:
        notif.is_read = True
        # DataAccess().merge(notif, autocommit=False)
        notif_cache.merge(notif, autocommit=False)
    # DataAccess().commit()
    notif_cache.commit()
        
    emit('display_old_messages', {
           'username': data['username'],
           'msgs_list': msgs_json,
           'user_id': user.id,  # voir dans template si on peut l'enlever
           'receiver': receiver.user_name,
           'receiver_id': receiver.id,
          },
        room=data['room']
        )
          
   
#leave room       
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