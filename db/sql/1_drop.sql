drop table if exists MESSAGE;
drop table if exists VISIT;
drop table if exists NOTIFICATION;
drop table if exists CONNECTION;
drop table if exists RECOMMENDATION_TOPIC;
drop table if exists USERS_RECOMMENDATION;
drop table if exists USERS_TOPIC;
drop table if exists TOPIC;
drop table if exists USERS_ROOM;
drop table if exists ROOM;
drop table if exists USERS;

drop sequence if exists NOTIFICATION_ID_SEQ;
drop sequence if exists USERS_ID_SEQ;
drop sequence if exists ROOM_ID_SEQ;
drop sequence if exists MESSAGE_ID_SEQ;
drop sequence if exists VISIT_ID_SEQ;
drop sequence if exists CONNECTION_ID_SEQ;
drop sequence if exists USERS_RECOMMENDATION_ID_SEQ;

drop type if exists mpaa_gender;
drop type if exists mpaa_orientation;
drop type if exists mpaa_notif_type;

drop procedure if exists INSERT_TOPICS;
drop function if exists ON_ROOM_DML;

commit;