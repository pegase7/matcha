window.onload = function() {
    display_notifs();
}

let notifs = new Array();

function display_notifs() {

    let xhr = new XMLHttpRequest();
    let nb_mess_dom_element = document.getElementById("nb_messages");
    let nb_like_dom_element = document.getElementById("nb_likes");
    let nb_visit_dom_element = document.getElementById("nb_visites");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if (xhr.status != 200) {
                nb_mess_dom_element.innerHTML = '?';
                nb_like_dom_element.innerHTML = '?';
                nb_visit_dom_element.innerHTML = '?';
            } else {

                notifs = JSON.parse(xhr.responseText);
                console.log("notifs : ", notifs);
                console.log("notifs : ", typeof(notifs));


                let nb_mess = 0;
                let nb_like = 0;
                let nb_visit = 0;
                let nb_dislike = 0;
                const notifs_map = new Map(); // Map(key, value) pour compter, dans la boucle, le nombre de messages par sender
                // boucle sur le tableau de notifs
                // notifs.forEach(notif => {
                //     // notif type Message
                //     if (notif.notif_type === "Message") {
                //         // nb total de messages
                //         nb_mess++;

                //         // nb de messages par sender
                //         if (!notifs_map.has(notif.sender_id)) {
                //             notifs_map.set(notif.sender_id, 1);
                //         } else {
                //             let val;
                //             val = notifs_map.get(notif.sender_id);
                //             val++;
                //             notifs_map.set(notif.sender_id, val);
                //         }
                //     }
                //     // notif type Like
                //     if (notif.notif_type === "Like") {
                //         nb_like++;

                //     }

                //     // notif type Visite
                //     if (notif.notif_type === "Visit") {
                //         nb_visit++;
                //     }
                // })
                nb_like = notifs.like;
                nb_mess = notifs.msg;
                nb_visit = notifs.visit;
                nb_dislike = notifs.dislike;
                console.log("nb_like : ", nb_like);




                // affichage notifications
                nb_mess_dom_element.innerHTML = nb_mess; //affiche nb total de messages
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

                // affiche le nb de message non lu par room s'il y en a.
                for (const key of notifs_map.keys()) { //récupère les key de la Map

                    if (document.getElementById("chat-room-receiver-" + key)) {
                        let input_nb = document.getElementById("chat-room-receiver-" + key);
                        if (notifs_map.get(key) > 0) {
                            input_nb.innerHTML = notifs_map.get(key);
                            input_nb.style.display = "inline-block";
                        } else {
                            input_nb.style.display = "none";
                        }
                    }
                }
            }
        }
    }
    xhr.open('GET', '/ajax');
    // xhr.setRequestHeader("content-type", "application/x-www-form-urlencoded;charset=UTF-8");
    xhr.send();
    // setTimeout(display_notifs, 5000);
}

document.addEventListener('DOMContentLoaded', () => {

    // affiche menu déroulant des likes
    document.querySelector("#like-deroulant").onclick = () => {
        notifs.forEach(notif => {
            if (notif.notif_type === 'Like') {
                a_elem = document.createElement('a');
                a_elem.className = "dropdown-item";
                a_elem.innerHTML = notif.sender_id.user_name;
                document.querySelector("#like-menu").append(a_elem);
            }
        });
    }
});