insert into USERS (first_name, last_name, user_name, password, description, email, active, confirm, gender, orientation, birthday, latitude, longitude) values ('Donald', 'Trump', 'Duck', 'MyPassword', 'Blond au tweet feroce', 'donald@duck.us', true, null, 'Male', 'Hetero', '1946-06-14', 38.89783, -77.03650);
insert into USERS (first_name, last_name, user_name, password, description, email, active, confirm, gender, orientation, birthday, latitude, longitude) values ('Angela', 'Merkel', 'LaBombe', 'MyPassword', 'Mon serieux est mon principal atout', 'angela@frech.de', true, null, 'Female', 'Hetero', '1954-07-17', 52.52021, 13.36924);
insert into USERS (first_name, last_name, user_name, password, description, email, active, confirm, gender, orientation, birthday, latitude, longitude) values ('Emmanuel', 'Macron', 'Le Kiki', 'MyPassword', 'Passionne des antiquites', 'manu@narcisse.com', true, null, 'Male', 'Bi', '1977-12-21', 48.87120, 2.31650);
insert into USERS (first_name, last_name, user_name, password, description, email, active, confirm, gender, orientation, birthday, latitude, longitude) values ('Fogiel', 'Marc-Olivier', 'marcopapolo', 'MyPassword', 'Ouvert a toute les promotions', 'mo-fogiel@tetu.fr', true, null, 'Male', 'Homo', '1969-07-05', 48.83636, 2.27387);

insert into tag(wording) values ('Piscine');
insert into tag(wording) values ('Peluche');
insert into tag(wording) values ('Gerontologie');
insert into tag(wording) values ('Manipulation');
insert into tag(wording) values ('Blitz');
insert into tag(wording) values ('Mercedes');

insert into users_tag(users_id, tag_id) values (1,1);
insert into users_tag(users_id, tag_id) values (1,4);
insert into users_tag(users_id, tag_id) values (2,5);
insert into users_tag(users_id, tag_id) values (2,6);
insert into users_tag(users_id, tag_id) values (3,2);
insert into users_tag(users_id, tag_id) values (3,3);
insert into users_tag(users_id, tag_id) values (3,4);
insert into users_tag(users_id, tag_id) values (4,1);
insert into users_tag(users_id, tag_id) values (4,6);

insert into room(id, users_ids) values (1, '{2,3}');
insert into room(id, users_ids) values (2,	'{2,1}');


insert into message(room_id, sender_id, receiver_id, chat) values (1,3,2, 'Que dois-je faire pour l''Astra-Zeneca');
insert into message(room_id, sender_id, receiver_id, chat) values (1,2,3, 'Faut faire gaffe');
insert into message(room_id, sender_id, receiver_id, chat) values (1,3,2, 'Zut, mon PM a dit hier que c''etait OK');
insert into message(room_id, sender_id, receiver_id, chat) values (1,2,3, 'T''as plus qu''a le contredire!');
insert into message(room_id, sender_id, receiver_id, chat) values (1,2,3, 'Ce ne sera qu''une fois de plus!!!!');

insert into connection (users_id, ip, connect_date) values(1, '192.0.0.1', TIMESTAMP '2021-03-17 09:09:12');
insert into connection (users_id, ip, connect_date) values(2, '192.0.0.1', TIMESTAMP '2021-03-17 11:30:34');
insert into connection (users_id, ip, connect_date) values(3, '192.0.0.1', TIMESTAMP '2021-03-17 16:16:56');
insert into connection (users_id, ip, connect_date, disconnect_date) values(1, '192.0.0.1', TIMESTAMP '2021-03-16 09:34:31', TIMESTAMP '2021-03-16 10:10:09');
insert into connection (users_id, ip, connect_date, disconnect_date) values(2, '192.0.0.1', TIMESTAMP '2021-03-16 08:14:12', TIMESTAMP '2021-03-16 09:02:26');
insert into connection (users_id, ip, connect_date, disconnect_date) values(3, '192.0.0.1', TIMESTAMP '2021-03-16 11:21:45', TIMESTAMP '2021-03-16 12:01:34');
