drop table if exists CONNECTION;
drop table if exists VISIT;
drop table if exists USERS_TAG;
drop table if exists TAG;
drop table if exists USERS_ROOM;
drop table if exists ROOM;
drop table if exists MESSAGE;
drop table if exists USERS;

drop sequence if exists USERS_ID_SEQ;
drop sequence if exists ROOM_ID_SEQ;
drop sequence if exists MESSAGE_ID_SEQ;
drop sequence if exists TAG_ID_SEQ;
drop sequence if exists VISIT_ID_SEQ;
drop sequence if exists CONNECTION_ID_SEQ;

drop type if exists mpaa_gender;
drop type if exists mpaa_orientation;
