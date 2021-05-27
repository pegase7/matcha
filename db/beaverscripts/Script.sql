select * from users as u
 where not exists ( select null from users_topic ut where ut.users_id= u.id )
 

select * from users_topic ut where ut.users_id = 1

select  U.id, U.first_name, U.last_name, U.user_name, U.password, U.description, U.email, U.active, U.is_recommendable, U.confirm, U.gender, U.orientation, U.birthday, U.latitude, U.longitude, U.popularity, U.created, U.last_update from Users U where user_name='Duck'

SELECT nextval('CONNECTION_ID_SEQ');