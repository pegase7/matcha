window.onload = function() {
    setTimeout(refresh_page, 8000);
}

function refresh_page() {

    let xhr = new XMLHttpRequest();
    let nb_mess = document.getElementById("nb_messages");
    xhr.onreadystatechange = function() {
        console.log(xhr.readyState);
        if (xhr.readyState == 4) {
            console.log(xhr.status);
            if (xhr.status != 200) {
                nb_mess.innerHTML = '?';
            } else {
                nb_mess.innerHTML = xhr.responseText;
            }

        }
    }
    xhr.open('GET', '/ajax');
    // xhr.setRequestHeader("content-type", "application/x-www-form-urlencoded;charset=UTF-8");
    xhr.send();



    setTimeout(refresh_page, 8000);
}