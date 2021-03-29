document.addEventListener('DOMContentLoaded', () => {var socket = io.connect('http://' + document.domain + ':' + location.port);
    let room = "Lounge";
    joinRoom("Lounge");

    // display incomming message
    socket.on('message', data => {
        const p = document.createElement('p');
        p.className = "chat_p";
        const span_username = document.createElement('span');
        const span_timestamp = document.createElement('span');
        span_username.className = "span_username";
        span_timestamp.className = "span_timestamp";
        const br = document.createElement('br');

        if (data.username) {
            if (data.username == sessionStorage.getItem("current_user")) {
                p.className = "current";
                data.username = "Moi";
            }
            span_username.innerHTML = data.username;
            span_timestamp.innerHTML = data.time_stamp;
            p.innerHTML = span_username.outerHTML + br.outerHTML + data.msg +
                br.outerHTML + span_timestamp.outerHTML;
            document.querySelector('#display-message-section').append(p);
            document.getElementById("rigthside-pannel").scrollTop;
        } else {
            printSysMsg(data.msg);
        }
    });

    // display like
    socket.on('like', data => {
        const p = document.createElement('p');
        p.innerHTML = "vous avez un like";
        document.querySelector('#display-like-section').append(p);
    });
    //voir comment recuperer l'evenement 'like' envoyé par le serveur


    // Send message
    document.querySelector('#send_message').onclick = () => {
        console.log('chat');
        socket.send({
            'msg': document.querySelector('#user_message').value,
            'username': username,
            'room': room
        });
        // Clear input area
        document.querySelector('#user_message').value = '';
    }

    //send like
    document.querySelector('#send_like').onclick = () => {
        console.log('like');
        sendLike(room);
    }

    // Room selection
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;
            if (newRoom == room) {
                msg = `You are already in ${room} room.`;
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
        socket.emit('like', { 'username': username, 'room': room })
    }

    // Leave room
    function leaveRoom(room) {
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
    