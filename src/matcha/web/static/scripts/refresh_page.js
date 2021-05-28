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

                let nb_like = notifs.like;
                let nb_mess = notifs.msg;
                let nb_visit = notifs.visit;
                let nb_dislike = notifs.dislike;
                console.log("nb_like : ", nb_like);
                console.log("nb_mess : ", nb_mess);
                console.log("nb_visit : ", nb_visit);
                console.log("nb_dislike : ", nb_dislike);

                // affichage des notifications //
                //affiche nb total de messages
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
            }
        }
    }
    xhr.open('GET', '/ajax');
    // xhr.setRequestHeader("content-type", "application/x-www-form-urlencoded;charset=UTF-8");
    xhr.send();
    setTimeout(display_notifs, 5000);
}