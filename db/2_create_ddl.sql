---
--- type mpaa_gender
---
create type mpaa_gender as enum (
    'Female',
    'Male'
);
alter type mpaa_gender owner to MATCHAADMIN;

---
--- type mpaa_orientation
---
create type mpaa_orientation as enum (
    'Hetero',
    'Homo',
    'Bi'
);
alter type mpaa_orientation owner to MATCHAADMIN;


---
--- sequence USERS_ID_SEQ
---
create sequence USERS_ID_SEQ increment by 1 cache 1;
alter table USERS_ID_SEQ owner to MATCHAADMIN;

---
--- table USERS
---
create table USERS (
    id			integer DEFAULT nextval('USERS_ID_SEQ'::regclass) NOT NULL,
    first_name	character varying(45) NOT NULL,
    last_name	character varying(45) NOT NULL,
    user_name	character varying(45) NOT NULL,
    password	character varying(45) NOT NULL,
    description text,
    email		character varying(45),
    active		boolean DEFAULT False NOT NULL,
    confirm		character varying(20),
    gender		mpaa_gender DEFAULT 'Female'::mpaa_gender,
    orientation	mpaa_orientation  DEFAULT 'Hetero'::mpaa_orientation,
    birthday	date,
    latitude	numeric(7,5),
    longitude 	numeric(7,5),
    last_update timestamp without time zone DEFAULT now() NOT NULL
);
alter table USERS owner to MATCHAADMIN;




---
--- sequence ROOM_ID_SEQ
---
create sequence ROOM_ID_SEQ increment by 1 cache 1;
alter table ROOM_ID_SEQ owner to MATCHAADMIN;

---
--- table ROOM
---
create table ROOM (
    id			integer DEFAULT nextval('ROOM_ID_SEQ'::regclass) NOT NULL,
    users_ids	integer[2] NOT NULL,
    active		boolean DEFAULT False NOT NULL
);
alter table ROOM owner to MATCHAADMIN;




---
--- table USERS_ROOM
---		insert/delete recors are automatic on this table.
---		Triggers on table ROOM are used to insert/delete automatically record in this link table.
---		when inserting/deleting a ROOM record, 2 records are inserted/deleted in this table.
---		So 'select r.* from USERS_ROOM as UR  left outer join ROOM as R on R.id = UR.room_id where master_id = ?' gives all rooms accessible for a specific user.
---
create table USERS_ROOM (
    room_id		integer DEFAULT nextval('ROOM_ID_SEQ'::regclass) NOT NULL,
    master_id	integer NOT NULL,
    slave_id	integer NOT NULL
);
alter table USERS_ROOM owner to MATCHAADMIN;



---
--- sequence MESSAGE_ID_SEQ
---
create sequence MESSAGE_ID_SEQ increment by 1 cache 1;
alter table MESSAGE_ID_SEQ owner to MATCHAADMIN;

---
--- table MESSAGE
---
create table MESSAGE (
    id			integer DEFAULT nextval('MESSAGE_ID_SEQ'::regclass) NOT NULL,
    room_id		integer NOT NULL,
    sender_id	integer NOT NULL,
    receiver_id	integer NOT NULL,
    chat		text,
    last_update timestamp without time zone DEFAULT now() NOT NULL
);
alter table MESSAGE owner to MATCHAADMIN;


  


---
--- sequence TAG_ID_SEQ
---
create sequence TAG_ID_SEQ increment by 1 cache 1;
alter table TAG_ID_SEQ owner to MATCHAADMIN;

---
--- table TAG
---
create table TAG(
    id		integer DEFAULT nextval('TAG_ID_SEQ'::regclass) NOT NULL,
    wording	character varying(45) NOT NULL
);
alter table TAG owner to MATCHAADMIN;


---
--- table USERS_TAG
---
create table USERS_TAG(
    users_id	integer NOT NULL,
    tag_id		integer NOT NULL
);
alter table USERS_TAG owner to MATCHAADMIN;


---
--- sequence VISIT_ID_SEQ
---
create sequence VISIT_ID_SEQ increment by 1 cache 1;
alter table VISIT_ID_SEQ owner to MATCHAADMIN;

---
--- table VISIT
---
create table VISIT (
    id				integer DEFAULT nextval('VISIT_ID_SEQ'::regclass) NOT NULL,
    visited_id		integer not null,
    visitor_id		integer not null,
    is_like			boolean DEFAULT False NOT NULL,
    last_visit		timestamp,
    visit_number	int
);
alter table VISIT_ID_SEQ owner to MATCHAADMIN;

---
--- sequence CONNECTION_ID_SEQ
---
create sequence CONNECTION_ID_SEQ increment by 1 cache 1;
alter table CONNECTION_ID_SEQ owner to MATCHAADMIN;

---
--- table CONNECTION
---
create table CONNECTION (
    id				integer DEFAULT nextval('CONNECTION_ID_SEQ'::regclass) NOT NULL,
    users_id		integer not null,
    ip				character varying(45) NOT NULL,
    connect_date	timestamp without time zone NOT NULL,
    disconnect_date	timestamp without time zone
);
alter table CONNECTION owner to MATCHAADMIN;

---
--- Create Trigger on ROOM to automatically insert/delete rows in USERS_ROOM when inserting/deleting rows
---
create or replace function trigger_room() returns trigger as $$
begin
  IF TG_OP = 'INSERT' THEN
  	insert into USERS_ROOM(room_id, master_id, slave_id) values (new.id, new.users_ids[1], new.users_ids[2]);
  	insert into USERS_ROOM(room_id, master_id, slave_id) values (new.id, new.users_ids[2], new.users_ids[1]);
  ELSIF TG_OP = 'DELETE' THEN
  	delete from USERS_ROOM where room_id = old.id;
  END IF;
  return null;
end;
$$ language PLPGSQL;


create trigger TRIGGER_ROOM after insert or delete on ROOM
for each row execute function trigger_room(); 
