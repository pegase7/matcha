const socket_conn = io.connect('http://' + document.domain + ':' + location.port);


function user_connect() {
    console.log("connect");
    socket_conn.emit('connect_user', { 'msg': 'je suis connecté :)' }, )
}
user_connect()