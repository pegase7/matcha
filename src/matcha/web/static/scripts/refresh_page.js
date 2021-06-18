const socket = io.connect('http://' + document.domain + ':' + location.port);


window.onload = function() {
    display_notifs();
    connected_consult();
}

function connected_consult() {
    if (document.getElementById('profil-consult')) {
        let profil_consult_tag = document.getElementById('profil-consult');
        let nav_username_tag = document.getElementById('nav-username');
        let profil_visited = profil_consult_tag.firstChild.data;
        let visitor = nav_username_tag.firstChild.data;
        // console.log('profil visited :', profil_visited);
        // console.log('visitor :', visitor);

        socket.emit('profil_user', { 'visitor': visitor, 'visited': profil_visited });
    }
}

socket.on('visited_profil', data => {
    let visited_page_tag = document.getElementById('nav-username');
    let visited_usr = visited_page_tag.firstChild.data;
    // console.log('data-visited :', data.visited);
    // console.log('visitor page :', visited_usr);
   
    if (data.visited == visited_usr) {
        socket.emit('visited_response', data);
    }
});

socket.on('visitor_reception', data => {
    console.log('reception data :', data);
    let visitor_page_tag = document.getElementById('nav-username');
    let visitor_usr = visitor_page_tag.firstChild.data;

    if (data.visitor == visitor_usr) {
        console.log('connecté !!');
        let state_connect = document.getElementById('consult-profil-connect-state');
        state_connect.innerHTML = 'connecté !!';
        state_connect.className = 'state-connect';
    }

});

let notifs = new Array();

function display_notifs() {

    let xhr = new XMLHttpRequest();
    let nb_mess_dom_element = document.getElementById("nb_messages");
    let nb_like_dom_element = document.getElementById("nb_likes");
    let nb_visit_dom_element = document.getElementById("nb_visites");
    let nb_dislikes_dom_element = document.getElementById("nb_dislikes");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if (xhr.status != 200) {
                nb_mess_dom_element.innerHTML = '?';
                nb_like_dom_element.innerHTML = '?';
                nb_visit_dom_element.innerHTML = '?';
                nb_dislikes_dom_element.innerHTML = '?';
            } else {

                notifs = JSON.parse(xhr.responseText);

                let nb_like = notifs.like;
                let nb_mess = notifs.msg;
                let nb_visit = notifs.visit;
                let nb_dislike = notifs.dislike;
                // console.log("nb_like : ", nb_like);
                // console.log("nb_mess : ", nb_mess);
                // console.log("nb_visit : ", nb_visit);
                // console.log("nb_dislike : ", nb_dislike);


                // affichage des notifications //
                // affiche nb total de messages
                nb_mess_dom_element.innerHTML = nb_mess;
                if (nb_mess === 0) {
                    nb_mess_dom_element.style.display = "none";
                } else {
                    nb_mess_dom_element.style.display = "inline-block";
                }

                // affiche nb total likes
                if (nb_like > 0) {
                    nb_like_dom_element.innerHTML = nb_like;
                    nb_like_dom_element.style.display = "inline-block";
                } else {
                    nb_like_dom_element.style.display = "none";
                }

                // affiche nb total visites
                if (nb_visit > 0) {
                    nb_visit_dom_element.innerHTML = nb_visit;
                    nb_visit_dom_element.style.display = "inline-block";
                } else {
                    nb_visit_dom_element.style.display = "none";
                }

                // affiche nb total dislikes
                if (nb_dislike > 0) {
                    nb_dislikes_dom_element.innerHTML = nb_dislike;
                    nb_dislikes_dom_element.style.display = "inline-block";
                } else {
                    nb_dislikes_dom_element.style.display = "none";
                }
            }
        }
    }
    xhr.open('GET', '/ajax');
    // xhr.setRequestHeader("content-type", "application/x-www-form-urlencoded;charset=UTF-8");
    xhr.send();
    setTimeout(display_notifs, 5000);
}