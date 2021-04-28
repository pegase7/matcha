-- password is unique = PasseMot0
insert into USERS (first_name, last_name, user_name, password, description, email, active, confirm, gender, orientation, birthday, latitude, longitude) values ('Donald', 'Trump', 'Duck', '8408ff8b4eb12ae70bb99055a571586620be97f5', 'Blond au tweet feroce', 'donald@duck.us', true, null, 'Male', 'Hetero', '1946-06-14', 38.89783, -77.03650);
insert into USERS (first_name, last_name, user_name, password, description, email, active, confirm, gender, orientation, birthday, latitude, longitude) values ('Angela', 'Merkel', 'LaBombe', 'b051e9143c2bbe4cb2e0f797ef0e60aefe2e2283', 'Mon serieux est mon principal atout', 'angela@frech.de', true, null, 'Female', 'Hetero', '1954-07-17', 52.52021, 13.36924);
insert into USERS (first_name, last_name, user_name, password, description, email, active, confirm, gender, orientation, birthday, latitude, longitude) values ('Emmanuel', 'Macron', 'Le Kiki', '2b912813da1e65a92c56b8505847ea3ed4c5ea61', 'Passionne des antiquites', 'manu@narcisse.com', true, null, 'Male', 'Bi', '1977-12-21', 48.87120, 2.31650);
insert into USERS (first_name, last_name, user_name, password, description, email, active, confirm, gender, orientation, birthday, latitude, longitude) values ('Fogiel', 'Marc-Olivier', 'marcopapolo', '2dc3f30fd6e5cf6120d948b6ec00b462ea92ff31', 'Ouvert a toute les promotions', 'mo-fogiel@tetu.fr', true, null, 'Male', 'Homo', '1969-07-05', 48.83636, 2.27387);

insert into USERS (first_name, last_name, user_name, password, description, email, active, confirm, gender, orientation, birthday, latitude, longitude, created, last_update) values ('Elric', 'De Melnibonnée', 'elric', '9d16f572d8ec4336f5121de759fd1ee9c7f2f314', 'Du sang et des âmes pour mon seigneur Arioch !', 'matcha@ik.me', true, '',  'Male',  'Hetero',  '1967-12-05',  '45.78777',  '4.73096', '2021-04-07 12:24:59.79232', '2021-04-07 12:24:59.79232');
insert into USERS (first_name, last_name, user_name, password, description, email, active, confirm, gender, orientation, birthday, latitude, longitude, created, last_update) values ('Pol', 'Gara', 'Pol', '8f4ec6f891bc405e799d549c413057c2d52bca2c', 'Puissante sorcière aux pouvoirs aussi ravageurs que son humour !', 'matcha@ik.me', true, '',  'Female',  'Hetero',  null,  '59.93222',  '30.35308', '2021-04-07 12:25:21.768918', '2021-04-07 12:25:21.768918');
insert into USERS (first_name, last_name, user_name, password, description, email, active, confirm, gender, orientation, birthday, latitude, longitude, created, last_update) values ('Henri', 'de Toulouse Lautrec', 'lautrec', 'fc29eb7bc0fdf107a70a3f9fc3b13a247ccd9d34', 'Peintre, amateur de bordels', 'matcha@ik.me', true, '',  'Male',  'Hetero',  '1864-11-24',  '0.00000',  '0.00000', '2021-04-06 13:20:19.89491', '2021-04-06 13:20:19.89491');
insert into USERS (first_name, last_name, user_name, password, description, email, active, confirm, gender, orientation, birthday, latitude, longitude, created, last_update) values ('Misse', 'Ara', 'Aramis', '828b7f73e3287dc5c3aa9ec8c8d8fecd983a2443', '', 'matcha@ik.me', true, '',  null,  null,  null,  null,  null, '2021-04-08 11:45:05.188755', '2021-04-08 11:45:05.188755');
insert into USERS (first_name, last_name, user_name, password, description, email, active, confirm, gender, orientation, birthday, latitude, longitude, created, last_update) values ('LaFronde', 'Thierry', 'Thierry', '1a40e05434d2d1a26885569d8fb3bd888473500f', '', 'matcha@ik.me', true, '',  null,  null,  null,  null,  null, '2021-04-08 12:40:38.403396', '2021-04-08 12:40:38.403396');
insert into USERS (first_name, last_name, user_name, password, description, email, active, confirm, gender, orientation, birthday, latitude, longitude, created, last_update) values ('Olivier', 'Gasnier', 'pegase7', '5ae518a42d43a56d2edb4f36fb96874ac8baae37', '""', 'matcha@ik.me', true, '',  'Male',  'Hetero',  '1967-09-18',  '46.10904',  '3.46268', '2021-04-09 07:25:20.498829', '2021-04-09 07:25:20.498829');



insert into topic(tag) values ('Piscine');
insert into topic(tag) values ('Peluche');
insert into topic(tag) values ('Gerontologie');
insert into topic(tag) values ('Manipulation');
insert into topic(tag) values ('Blitz');
insert into topic(tag) values ('Mercedes');

insert into users_topic(users_id, tag) values (1, 'Piscine'); 
insert into users_topic(users_id, tag) values (1, 'Manipulation');
insert into users_topic(users_id, tag) values (2, 'Blitz');
insert into users_topic(users_id, tag) values (2, 'Mercedes');
insert into users_topic(users_id, tag) values (3, 'Peluche');
insert into users_topic(users_id, tag) values (3, 'Gerontologie');
insert into users_topic(users_id, tag) values (3, 'Manipulation');
insert into users_topic(users_id, tag) values (4, 'Piscine');
insert into users_topic(users_id, tag) values (4, 'Mercedes');

insert into room(id, users_ids) values (1, '{2,3}');
insert into room(id, users_ids) values (2,	'{2,1}');


insert into message(room_id, sender_id, chat) values (1,3, 'Que dois-je faire pour l''Astra-Zeneca');
insert into message(room_id, sender_id, chat) values (1,2, 'Faut faire gaffe');
insert into message(room_id, sender_id, chat) values (1,3, 'Zut, mon PM a dit hier que c''etait OK');
insert into message(room_id, sender_id, chat) values (1,2, 'T''as plus qu''a le contredire!');
insert into message(room_id, sender_id, chat) values (1,2, 'Ce ne sera qu''une fois de plus!!!!');

insert into connection (users_id, ip, connect_date) values(1, '192.0.0.1', TIMESTAMP '2021-03-17 09:09:12');
insert into connection (users_id, ip, connect_date) values(2, '192.0.0.1', TIMESTAMP '2021-03-17 11:30:34');
insert into connection (users_id, ip, connect_date) values(3, '192.0.0.1', TIMESTAMP '2021-03-17 16:16:56');
insert into connection (users_id, ip, connect_date, disconnect_date) values(1, '192.0.0.1', TIMESTAMP '2021-03-16 09:34:31', TIMESTAMP '2021-03-16 10:10:09');
insert into connection (users_id, ip, connect_date, disconnect_date) values(2, '192.0.0.1', TIMESTAMP '2021-03-16 08:14:12', TIMESTAMP '2021-03-16 09:02:26');
insert into connection (users_id, ip, connect_date, disconnect_date) values(3, '192.0.0.1', TIMESTAMP '2021-03-16 11:21:45', TIMESTAMP '2021-03-16 12:01:34');

insert into visit(visited_id, visitor_id, visits_number) values (1, 4, 2);
insert into visit(visited_id, visitor_id, visits_number) values (1, 5, 6);
insert into visit(visited_id, visitor_id, visits_number) values (2, 4, 7);
insert into visit(visited_id, visitor_id, visits_number) values (2, 5, 1);
