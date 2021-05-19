window.onload = function() {
    refresh_nb_message();
    // setTimeout(refresh_page, 8000);
}

function refresh_nb_message() {

    let xhr = new XMLHttpRequest();
    let nb_mess_dom_element = document.getElementById("nb_messages");
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if (xhr.status != 200) {
                nb_mess_dom_element.innerHTML = '?';
            } else {
                notifs = JSON.parse(xhr.responseText);
                console.log(notifs);
                let nb_mess = 0;
                const notifs_map = new Map(); // Map(key, value) pour compter, dans la boucle, le nombre de messages par sender
                // boucle sur le tableau de notifs
                notifs.forEach(notif => {
                    if (notif.notif_type === "Message") {
                        // nb total de messages
                        nb_mess++;

                        // nb de messages par sender
                        if (!notifs_map.has(notif.sender_id)) {
                            notifs_map.set(notif.sender_id, 1);
                        } else {
                            let val;
                            val = notifs_map.get(notif.sender_id);
                            val++;
                            notifs_map.set(notif.sender_id, val);
                        }
                    }
                });
                // if (nb_mess > 0) {
                nb_mess_dom_element.innerHTML = nb_mess; //affiche nb total de messages
                // }
                for (const key of notifs_map.keys()) { //récupère les key de la Map

                    if (document.getElementById("chat-room-receiver-" + key)) {
                        let input_nb = document.getElementById("chat-room-receiver-" + key);
                        if (notifs_map.get(key) != 0) {
                            input_nb.innerHTML = notifs_map.get(key); // affiche le nb de message non lu par room s'il y en a.
                        }

                    }
                }

            }
        }
    }
    xhr.open('GET', '/ajax');
    // xhr.setRequestHeader("content-type", "application/x-www-form-urlencoded;charset=UTF-8");
    xhr.send();
    setTimeout(refresh_nb_message, 5000);
}