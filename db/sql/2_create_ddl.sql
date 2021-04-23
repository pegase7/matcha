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
    latitude	numeric(8,5),
    longitude 	numeric(8,5),
    popularity	numeric(3),
    created		timestamp without time zone DEFAULT now() NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
);
alter table USERS owner to MATCHAADMIN;


---
--- sequence USERS_RECOMMANDATION_ID_SEQ
---
create sequence USERS_RECOMMANDATION_ID_SEQ increment by 1 cache 1;
alter table USERS_RECOMMANDATION_ID_SEQ owner to MATCHAADMIN;

---
--- table USERS_RECOMMANDATION
---
create table USERS_RECOMMANDATION (
    id              integer DEFAULT nextval('USERS_RECOMMANDATION_ID_SEQ'::regclass) NOT NULL,
    sender_id		integer NOT NULL,
    receiver_id		integer NOT NULL,
    age_diff		numeric(4,2),
    distance		numeric(9,2),
    dist_ratio		numeric(2),
    topics_ratio	numeric(9,2),
    last_consult 	timestamp,    
    created         timestamp without time zone DEFAULT now() NOT NULL,
    last_update 	timestamp without time zone DEFAULT now() NOT NULL
);
alter table USERS_RECOMMANDATION owner to MATCHAADMIN;



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
    active		boolean DEFAULT False NOT NULL,
    created		timestamp without time zone DEFAULT now() NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
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
    chat		text,
    created		timestamp without time zone DEFAULT now() NOT NULL
);
alter table MESSAGE owner to MATCHAADMIN;


  


---
--- table TOPIC
---
create table TOPIC(
    tag		character varying(45) NOT NULL,
    created		timestamp without time zone DEFAULT now() NOT NULL
);
alter table TOPIC owner to MATCHAADMIN;


---
--- table USERS_TOPIC
---
create table USERS_TOPIC(
    users_id	integer NOT NULL,
    tag			character varying(45) NOT NULL
);
alter table USERS_TOPIC owner to MATCHAADMIN;


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
    visits_number	int,
    islike          boolean DEFAULT FALSE,
    isblocked       boolean DEFAULT FALSE,
    created		timestamp without time zone DEFAULT now() NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
);
alter table VISIT owner to MATCHAADMIN;

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
create or replace function ON_ROOM_DML() returns trigger as $$
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
alter function ON_ROOM_DML owner to MATCHAADMIN;


create trigger TRIGGER_ROOM after insert or delete on ROOM
for each row execute function on_room_dml(); 



---
--- Create procedure INSERT_TOPICS
---		Reintialize list of topic for userid.
---		if topic does not exist, insert it.
---
create or replace procedure INSERT_TOPICS(usersid int, topic_array  text[]) AS $$
	declare
            topic_element  text;
	begin
		delete from USERS_TOPIC where users_id = usersid;
		foreach topic_element in array topic_array
		loop
			insert into topic(tag)
			select topic_element
			 where not exists ( select 1 from TOPIC where tag = topic_element);
			insert into USERS_TOPIC(users_id, tag) values (usersid, topic_element);
		end loop;
	end;
    $$ language plpgsql;
alter procedure INSERT_TOPICS owner to MATCHAADMIN;
