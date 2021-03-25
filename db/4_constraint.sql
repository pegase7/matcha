alter table USERS add constraint USERS_PKEY primary key (id);
alter table TAG add constraint TAG_PKEY primary key (id);
alter table ROOM add constraint ROOM_TAG_PKEY primary key (id);
alter table USERS_ROOM add constraint USERS_ROOM_TAG_PKEY primary key (room_id, master_id);
alter table MESSAGE add constraint MESSAGE_TAG_PKEY primary key (id);
alter table USERS_TAG add constraint USERS_TAG_PKEY primary key (users_id, tag_id);
alter table VISIT add constraint VISIT_PKEY primary key (id);
alter table CONNECTION add constraint CONNECTION_PKEY primary key (id);

alter table USERS_TAG add foreign key (users_id) references USERS;
alter table USERS_TAG add foreign key (tag_id) references TAG;
create index USERS_TAG_USERS_FK on USERS_TAG using btree(users_id);
create index USERS_TAG_TAG_FK on USERS_TAG using btree(tag_id);


alter table USERS_ROOM add foreign key (master_id) references USERS;
alter table USERS_ROOM add foreign key (room_id) references ROOM;
alter table USERS_ROOM add foreign key (slave_id) references USERS;
create index USERS_ROOM_MASTER_FK on USERS_ROOM using btree(master_id);
create index USERS_ROOM_ROOM_FK on USERS_ROOM using btree(room_id);

alter table MESSAGE add foreign key (sender_id) references USERS;
alter table MESSAGE add foreign key (receiver_id) references USERS;
create index MESSAGE_SENDER_FK on MESSAGE using btree(sender_id);
create index MESSAGE_RECEIVER_FK on MESSAGE using btree(receiver_id);

alter table VISIT add foreign key (visited_id) references USERS;
alter table VISIT add foreign key (visitor_id) references USERS;
create index VISIT_VISITED_FK on VISIT using btree(visited_id);
create index VISIT_VISITOR_FK on VISIT using btree(visitor_id);

alter table CONNECTION add foreign key (users_id) references USERS;
create index CONNECTION_USERS_FK on CONNECTION using btree(users_id);

