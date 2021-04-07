alter table USERS add constraint USERS_PKEY primary key (id);
alter table TOPIC add constraint TOPIC_PKEY primary key (tag);
alter table ROOM add constraint ROOM_PKEY primary key (id);
alter table USERS_ROOM add constraint USERS_ROOM_TAG_PKEY primary key (room_id, master_id);
alter table MESSAGE add constraint MESSAGE_TAG_PKEY primary key (id);
alter table USERS_TOPIC add constraint USERS_TOPIC_PKEY primary key (users_id, tag);
alter table VISIT add constraint VISIT_PKEY primary key (id);
alter table CONNECTION add constraint CONNECTION_PKEY primary key (id);

create unique index USERS_USER_NAME_UNQ ON USERS (user_name);

alter table USERS_TOPIC add foreign key (users_id) references USERS;
alter table USERS_TOPIC add foreign key (tag) references TOPIC;
create index USERS_TOPIC_USERS_FK on USERS_TOPIC using btree(users_id);
create index USERS_TOPIC_TAG_FK on USERS_TOPIC using btree(tag);


alter table USERS_ROOM add foreign key (master_id) references USERS;
alter table USERS_ROOM add foreign key (room_id) references ROOM;
alter table USERS_ROOM add foreign key (slave_id) references USERS;
create index USERS_ROOM_MASTER_FK on USERS_ROOM using btree(master_id);
create index USERS_ROOM_ROOM_FK on USERS_ROOM using btree(room_id);

alter table MESSAGE add foreign key (sender_id) references USERS;
create index MESSAGE_SENDER_FK on MESSAGE using btree(sender_id);

alter table VISIT add foreign key (visited_id) references USERS;
alter table VISIT add foreign key (visitor_id) references USERS;
create index VISIT_VISITED_FK on VISIT using btree(visited_id);
create index VISIT_VISITOR_FK on VISIT using btree(visitor_id);

alter table CONNECTION add foreign key (users_id) references USERS;
create index CONNECTION_USERS_FK on CONNECTION using btree(users_id);

