document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    let room = "";
    // joinRoom("Lounge");

    // display incomming message
    socket.on('message', data => {
        console.log(data);
        const current_user = sessionStorage.getItem("current_user");
        const p = document.createElement('p');
        p.className = "msg_p";
        const span_sender = document.createElement('span');
        const span_timestamp = document.createElement('span');
        span_sender.className = "span_sender";
        span_timestamp.className = "span_timestamp";
        const br = document.createElement('br');

        if (data.sender) {
            // console.log('data.username');
            if (data.sender == current_user) {
                p.className = "current";
                data.sender = "Moi";
            }
            span_sender.innerHTML = data.sender;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = data.msg +
                br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-message-section').append(p);
            document.getElementById("rigthside-pannel").scrollTop;
            if (current_user == data.receiver) {
                socket.emit('receiver_connect', { 'msg': 'receiver connect', 'test': true, 'notif': data.notif })
                    // } else {
                    //     socket.emit('receiver_connect', {'msg': 'receiver non-connect', 'test': false})
            }

        } else {
            printSysMsg(data.msg);
        }
    });

    // Send message
    document.querySelector('#send_message').onclick = () => {

        console.log('receiver :' + document.getElementById('chat-receiver-name').innerHTML);
        socket.send({
            'msg': document.querySelector('#user_message').value,
            'sender': username,
            'receiver': document.getElementById('chat-receiver-name').innerHTML,
            'room': room,
            'user_id': document.querySelector("#input-area").className
        });
        // Clear input area
        document.querySelector('#user_message').value = '';
    }

    // test receiver connection
    socket.on('test_receiver', data => {
        console.log('user = ' + sessionStorage.getItem("current_user"));
        console.log(data);
        sender = data.username;
        current_user = sessionStorage.getItem("current_user");
        if (sender != current_user) {
            socket.emit('receiver_ok', {
                'msg': data.msg,
                'sender': data.sender,
                'receiver': data.receiver,
                'room': data.room,
                'time_stamp': data.time_stamp,
            })
        }
    });

    //display old message
    socket.on('display_old_messages', data => {
        console.log('1 ' + data.username);
        console.log('2 ' + data.user_id);
        console.log('3 ' + sessionStorage.getItem("current_user"));
        console.log('4 ' + data.receiver);
        console.log('5 ' + data.receiver_id);

        // met le nb de message non lu à 0
        if (document.getElementById("chat-room-receiver-" + data.receiver_id)) {
            nb_mess = document.getElementById("chat-room-receiver-" + data.receiver_id);
            nb_mess.innerHTML = 0;
        }

        //envoie la liste des messages à l'utilisateur qui a rejoint la room
        if (sessionStorage.getItem("current_user") == data.username) {
            const h3 = document.createElement('h3');
            h3.id = "chat-receiver-name"
            h3.innerHTML = data.receiver;
            document.getElementById('chat-message-area').append(h3)
                //display old messages
            list = JSON.parse(data.msgs_list)
                // console.log(list)
            list.forEach(
                msg => {
                    // console.log(msg)
                    const p = document.createElement('p');
                    p.className = "msg_p";
                    const span_username = document.createElement('span');
                    const span_timestamp = document.createElement('span');
                    span_username.className = "span_sender";
                    span_timestamp.className = "span_timestamp";
                    const br = document.createElement('br');
                    if (data.username) {
                        // console.log('data.username');
                        if (data.user_id == msg.sender_id) {
                            p.className = "current";
                            data.username = "Moi";
                        }
                        span_username.innerHTML = data.username;
                        span_timestamp.innerHTML = msg.created;
                        p.innerHTML = msg.chat +
                            br.outerHTML + span_timestamp.outerHTML;
                        document.querySelector('#display-message-section').append(p);
                    }
                },
                document.getElementById("rigthside-pannel").scrollTop
            )
        }
    });

    // display like, recupere l'evenement 'afterlike' envoye du server
    socket.on('afterlike', data => {
        const username = data['username'];
        console.log(data['username']);
        console.log('toto');
        console.log(sessionStorage.getItem("current_user"))
        if (sessionStorage.getItem("current_user") != username) {
            const p = document.createElement('p');
            const btn = document.createElement('button');
            const btn_text = document.createTextNode("Repondre au like");
            btn.appendChild(btn_text);
            // btn.value = 'like_response';
            p.innerHTML = username + " vous a envoye un like";
            document.querySelector('#display-like-section').append(p);
            document.querySelector('#display-like-section').append(btn); //remplacer le btn like par ce nouveau btn
        }
    });
    //voir comment recuperer l'evenement 'like' envoyé par le serveur


    socket.on('login', data => {
        console.log('socket login : ' + data['msg'])
    });


    //send like
    const buttons = document.querySelectorAll('.send_like');
    for (const button of buttons) {
        button.onclick = () => {
            console.log('send like');
            console.log(button.value);
            console.log(username);
            socket.emit('like', { 'user1': username, 'user2': button.value })
        }
    }


    // Room selection
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.value.toString();
            let node = p;
            // console.log("room = " + newRoom);
            // console.log("username = " + username)
            if (newRoom == room) {
                msg = `Vous êtes déjà connecté à cette discussion.`;
                printSysMsg(msg);
            } else {

                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    });


    // Send like
    function sendLike(room) {
        ///socket.emit('like', { 'username': username, 'room': room })
    }

    // Leave room
    function leaveRoom(room) {
        old_receiver = document.getElementById('chat-receiver-name');
        document.getElementById('chat-message-area').removeChild(old_receiver);
        socket.emit('leave', { 'username': username, 'room': room });
    }

    // Join room
    function joinRoom(room) {
        socket.emit('join', { 'username': username, 'room': room });
        //Clear message area
        document.querySelector('#display-message-section').innerHTML = ''
            // Autofocus on text box
        document.querySelector('#user_message').focus();
    }

    // Print system message
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
    }

    //Print like message
    function printLikeMsg(msg) {
        const p = document.createElement('p');
        p.innerHTML = msg;
        document.querySelector("#display-like-section").append(p);
    }
})