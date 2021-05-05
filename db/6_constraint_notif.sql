alter table NOTIFICATION add constraint NOTIFICATION_PKEY primary key (id);

alter table NOTIFICATION add foreign key (sender_id) references USERS;
alter table NOTIFICATION add foreign key (receiver_id) references USERS;
create index NOTIFICATION_SENDER_ID_FK on NOTIFICATION using btree(sender_id);
create index NOTIFICATION_RECEIVER_ID_FK on NOTIFICATION using btree(receiver_id);
