---
--- type mpaa_notif_type
---
create type mpaa_notif_type as enum (
	'Like',
	'Visit',
	'Message',
	'Like_too',
	'Dislike'
	);
alter type mpaa_notif_type owner to MATCHAADMIN;

---
--- sequence NOTIFICATION_ID_SEQ
---
create sequence NOTIFICATION_ID_SEQ increment by 1 cache 1;
alter table NOTIFICATION_ID_SEQ owner to MATCHAADMIN;

---
--- table NOTIFICATION
---
create table NOTIFICATION (
	id          integer DEFAULT nextval('NOTIFICATION_ID_SEQ'::regclass) NOT NULL,
	sender_id   integer NOT NULL,
	receiver_id integer NOT NULL,
	notif_type  mpaa_notif_type  NOT NULL,
	read_notif  boolean DEFAULT False NOT NULL,
	created     timestamp without time zone DEFAULT now() NOT NULL
);
alter table NOTIFICATION owner to MATCHAADMIN;
