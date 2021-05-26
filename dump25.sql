--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: mpaa_gender; Type: TYPE; Schema: public; Owner: matchaadmin
--

CREATE TYPE public.mpaa_gender AS ENUM (
    'Female',
    'Male'
);


ALTER TYPE public.mpaa_gender OWNER TO matchaadmin;

--
-- Name: mpaa_notif_type; Type: TYPE; Schema: public; Owner: matchaadmin
--

CREATE TYPE public.mpaa_notif_type AS ENUM (
    'Like',
    'Visit',
    'Message',
    'Like_too',
    'Dislike'
);


ALTER TYPE public.mpaa_notif_type OWNER TO matchaadmin;

--
-- Name: mpaa_orientation; Type: TYPE; Schema: public; Owner: matchaadmin
--

CREATE TYPE public.mpaa_orientation AS ENUM (
    'Hetero',
    'Homo',
    'Bi'
);


ALTER TYPE public.mpaa_orientation OWNER TO matchaadmin;

--
-- Name: insert_topics(integer, text[]); Type: PROCEDURE; Schema: public; Owner: matchaadmin
--

CREATE PROCEDURE public.insert_topics(usersid integer, topic_array text[])
    LANGUAGE plpgsql
    AS $$
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
    $$;


ALTER PROCEDURE public.insert_topics(usersid integer, topic_array text[]) OWNER TO matchaadmin;

--
-- Name: on_room_dml(); Type: FUNCTION; Schema: public; Owner: matchaadmin
--

CREATE FUNCTION public.on_room_dml() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
  IF TG_OP = 'INSERT' THEN
  	insert into USERS_ROOM(room_id, master_id, slave_id) values (new.id, new.users_ids[1], new.users_ids[2]);
  	insert into USERS_ROOM(room_id, master_id, slave_id) values (new.id, new.users_ids[2], new.users_ids[1]);
  ELSIF TG_OP = 'DELETE' THEN
  	delete from USERS_ROOM where room_id = old.id;
  END IF;
  return null;
end;
$$;


ALTER FUNCTION public.on_room_dml() OWNER TO matchaadmin;

--
-- Name: trigger_room(); Type: FUNCTION; Schema: public; Owner: ogasnier
--

CREATE FUNCTION public.trigger_room() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
begin
  IF TG_OP = 'INSERT' THEN
  	insert into USERS_ROOM(room_id, master_id, slave_id) values (new.id, new.users_ids[1], new.users_ids[2]);
  	insert into USERS_ROOM(room_id, master_id, slave_id) values (new.id, new.users_ids[2], new.users_ids[1]);
  ELSIF TG_OP = 'DELETE' THEN
  	delete from USERS_ROOM where room_id = old.id;
  END IF;
  return null;
end;
$$;


ALTER FUNCTION public.trigger_room() OWNER TO ogasnier;

--
-- Name: connection_id_seq; Type: SEQUENCE; Schema: public; Owner: matchaadmin
--

CREATE SEQUENCE public.connection_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.connection_id_seq OWNER TO matchaadmin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: connection; Type: TABLE; Schema: public; Owner: matchaadmin
--

CREATE TABLE public.connection (
    id integer DEFAULT nextval('public.connection_id_seq'::regclass) NOT NULL,
    users_id integer NOT NULL,
    ip character varying(45) NOT NULL,
    connect_date timestamp without time zone NOT NULL,
    disconnect_date timestamp without time zone
);


ALTER TABLE public.connection OWNER TO matchaadmin;

--
-- Name: message_id_seq; Type: SEQUENCE; Schema: public; Owner: matchaadmin
--

CREATE SEQUENCE public.message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.message_id_seq OWNER TO matchaadmin;

--
-- Name: message; Type: TABLE; Schema: public; Owner: matchaadmin
--

CREATE TABLE public.message (
    id integer DEFAULT nextval('public.message_id_seq'::regclass) NOT NULL,
    room_id integer NOT NULL,
    sender_id integer NOT NULL,
    chat text,
    created timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.message OWNER TO matchaadmin;

--
-- Name: notification_id_seq; Type: SEQUENCE; Schema: public; Owner: matchaadmin
--

CREATE SEQUENCE public.notification_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notification_id_seq OWNER TO matchaadmin;

--
-- Name: notification; Type: TABLE; Schema: public; Owner: matchaadmin
--

CREATE TABLE public.notification (
    id integer DEFAULT nextval('public.notification_id_seq'::regclass) NOT NULL,
    sender_id integer NOT NULL,
    receiver_id integer NOT NULL,
    notif_type public.mpaa_notif_type NOT NULL,
    is_read boolean DEFAULT false NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.notification OWNER TO matchaadmin;

--
-- Name: room_id_seq; Type: SEQUENCE; Schema: public; Owner: matchaadmin
--

CREATE SEQUENCE public.room_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.room_id_seq OWNER TO matchaadmin;

--
-- Name: room; Type: TABLE; Schema: public; Owner: matchaadmin
--

CREATE TABLE public.room (
    id integer DEFAULT nextval('public.room_id_seq'::regclass) NOT NULL,
    users_ids integer[] NOT NULL,
    active boolean DEFAULT false NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.room OWNER TO matchaadmin;

--
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: matchaadmin
--

CREATE SEQUENCE public.tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_id_seq OWNER TO matchaadmin;

--
-- Name: topic; Type: TABLE; Schema: public; Owner: matchaadmin
--

CREATE TABLE public.topic (
    tag character varying(45) NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.topic OWNER TO matchaadmin;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: matchaadmin
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO matchaadmin;

--
-- Name: users; Type: TABLE; Schema: public; Owner: matchaadmin
--

CREATE TABLE public.users (
    id integer DEFAULT nextval('public.users_id_seq'::regclass) NOT NULL,
    first_name character varying(45) NOT NULL,
    last_name character varying(45) NOT NULL,
    user_name character varying(45) NOT NULL,
    password character varying(45) NOT NULL,
    description text,
    email character varying(45),
    active boolean DEFAULT false NOT NULL,
    confirm character varying(20),
    gender public.mpaa_gender DEFAULT 'Female'::public.mpaa_gender,
    orientation public.mpaa_orientation DEFAULT 'Hetero'::public.mpaa_orientation,
    birthday date,
    latitude numeric(8,5),
    longitude numeric(8,5),
    created timestamp without time zone DEFAULT now() NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL,
    popularity numeric(3,0)
);


ALTER TABLE public.users OWNER TO matchaadmin;

--
-- Name: users_recommandation; Type: TABLE; Schema: public; Owner: matchaadmin
--

CREATE TABLE public.users_recommandation (
    sender_id integer NOT NULL,
    receiver_id integer NOT NULL,
    islike boolean,
    isblocked boolean,
    age_diff numeric(4,2),
    distance numeric(9,2),
    dist_ratio numeric(2,0),
    topics_ratio numeric(9,2),
    nb_consult numeric(9,0),
    created timestamp without time zone DEFAULT now() NOT NULL,
    last_consult timestamp without time zone DEFAULT now() NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.users_recommandation OWNER TO matchaadmin;

--
-- Name: users_room; Type: TABLE; Schema: public; Owner: matchaadmin
--

CREATE TABLE public.users_room (
    room_id integer DEFAULT nextval('public.room_id_seq'::regclass) NOT NULL,
    master_id integer NOT NULL,
    slave_id integer NOT NULL
);


ALTER TABLE public.users_room OWNER TO matchaadmin;

--
-- Name: users_suggest; Type: TABLE; Schema: public; Owner: matchaadmin
--

CREATE TABLE public.users_suggest (
    sender_id integer NOT NULL,
    receiver_id integer NOT NULL,
    islike boolean,
    isblocked boolean,
    created timestamp without time zone DEFAULT now() NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.users_suggest OWNER TO matchaadmin;

--
-- Name: users_topic; Type: TABLE; Schema: public; Owner: matchaadmin
--

CREATE TABLE public.users_topic (
    users_id integer NOT NULL,
    tag character varying(45) NOT NULL
);


ALTER TABLE public.users_topic OWNER TO matchaadmin;

--
-- Name: visit_id_seq; Type: SEQUENCE; Schema: public; Owner: matchaadmin
--

CREATE SEQUENCE public.visit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.visit_id_seq OWNER TO matchaadmin;

--
-- Name: visit; Type: TABLE; Schema: public; Owner: matchaadmin
--

CREATE TABLE public.visit (
    id integer DEFAULT nextval('public.visit_id_seq'::regclass) NOT NULL,
    visited_id integer NOT NULL,
    visitor_id integer NOT NULL,
    visits_number integer,
    islike boolean DEFAULT false,
    isblocked boolean DEFAULT false,
    created timestamp without time zone DEFAULT now() NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL,
    isfake boolean DEFAULT false
);


ALTER TABLE public.visit OWNER TO matchaadmin;

--
-- Data for Name: connection; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.connection VALUES (1, 1, '192.0.0.1', '2021-03-17 09:09:12', NULL);
INSERT INTO public.connection VALUES (2, 2, '192.0.0.1', '2021-03-17 11:30:34', NULL);
INSERT INTO public.connection VALUES (3, 3, '192.0.0.1', '2021-03-17 16:16:56', NULL);
INSERT INTO public.connection VALUES (4, 1, '192.0.0.1', '2021-03-16 09:34:31', '2021-03-16 10:10:09');
INSERT INTO public.connection VALUES (5, 2, '192.0.0.1', '2021-03-16 08:14:12', '2021-03-16 09:02:26');
INSERT INTO public.connection VALUES (6, 3, '192.0.0.1', '2021-03-16 11:21:45', '2021-03-16 12:01:34');
INSERT INTO public.connection VALUES (7, 10, '127.0.0.1', '2021-04-09 13:38:35.664707', NULL);
INSERT INTO public.connection VALUES (8, 5, '127.0.0.1', '2021-04-09 13:43:54.571734', NULL);
INSERT INTO public.connection VALUES (9, 10, '127.0.0.1', '2021-04-09 13:58:22.518929', '2021-04-09 13:58:34.917987');
INSERT INTO public.connection VALUES (156, 7, '127.0.0.1', '2021-04-16 11:15:46.453228', '2021-04-16 13:17:46.832144');
INSERT INTO public.connection VALUES (10, 11, '127.0.0.1', '2021-04-09 14:07:14.759588', '2021-04-09 14:07:31.604203');
INSERT INTO public.connection VALUES (11, 11, '127.0.0.1', '2021-04-09 14:07:40.868267', NULL);
INSERT INTO public.connection VALUES (12, 10, '127.0.0.1', '2021-04-09 14:21:23.555068', '2021-04-09 14:34:50.344027');
INSERT INTO public.connection VALUES (13, 7, '127.0.0.1', '2021-04-09 14:35:12.315964', '2021-04-10 08:21:13.835185');
INSERT INTO public.connection VALUES (14, 5, '127.0.0.1', '2021-04-10 08:21:26.587258', '2021-04-10 13:39:37.716384');
INSERT INTO public.connection VALUES (15, 10, '127.0.0.1', '2021-04-10 13:39:44.288743', '2021-04-10 13:39:54.683864');
INSERT INTO public.connection VALUES (16, 7, '127.0.0.1', '2021-04-10 13:40:03.341918', '2021-04-10 13:42:11.692324');
INSERT INTO public.connection VALUES (17, 5, '127.0.0.1', '2021-04-10 13:42:19.309226', '2021-04-10 14:40:04.645748');
INSERT INTO public.connection VALUES (50, 7, '127.0.0.1', '2021-04-10 14:40:11.965752', '2021-04-10 14:40:35.460149');
INSERT INTO public.connection VALUES (51, 5, '127.0.0.1', '2021-04-10 14:40:56.429697', '2021-04-10 15:12:17.832717');
INSERT INTO public.connection VALUES (52, 7, '127.0.0.1', '2021-04-10 15:12:28.185955', '2021-04-10 15:12:59.031504');
INSERT INTO public.connection VALUES (53, 5, '127.0.0.1', '2021-04-10 15:13:09.193894', NULL);
INSERT INTO public.connection VALUES (54, 7, '127.0.0.1', '2021-04-10 15:32:18.513136', '2021-04-10 15:32:29.671325');
INSERT INTO public.connection VALUES (55, 5, '127.0.0.1', '2021-04-10 15:32:40.280982', '2021-04-12 12:45:30.409489');
INSERT INTO public.connection VALUES (87, 10, '127.0.0.1', '2021-04-12 12:45:45.645675', '2021-04-12 13:00:16.807699');
INSERT INTO public.connection VALUES (88, 10, '127.0.0.1', '2021-04-12 13:09:34.802036', '2021-04-13 08:12:03.558215');
INSERT INTO public.connection VALUES (89, 5, '127.0.0.1', '2021-04-13 08:12:12.493594', '2021-04-13 08:51:29.598237');
INSERT INTO public.connection VALUES (90, 10, '127.0.0.1', '2021-04-13 08:51:41.297319', '2021-04-13 08:52:18.846314');
INSERT INTO public.connection VALUES (91, 11, '127.0.0.1', '2021-04-13 08:52:30.112342', '2021-04-13 08:53:21.910883');
INSERT INTO public.connection VALUES (92, 5, '127.0.0.1', '2021-04-13 08:53:41.383837', NULL);
INSERT INTO public.connection VALUES (93, 5, '127.0.0.1', '2021-04-13 09:02:30.709666', '2021-04-13 09:18:49.496513');
INSERT INTO public.connection VALUES (95, 10, '127.0.0.1', '2021-04-13 09:20:57.544856', '2021-04-13 09:27:43.591091');
INSERT INTO public.connection VALUES (96, 7, '127.0.0.1', '2021-04-13 09:27:51.255378', '2021-04-13 09:27:58.533573');
INSERT INTO public.connection VALUES (97, 6, '127.0.0.1', '2021-04-13 09:28:19.406853', '2021-04-13 09:28:37.629229');
INSERT INTO public.connection VALUES (98, 10, '127.0.0.1', '2021-04-13 09:28:46.670907', '2021-04-13 09:28:58.447933');
INSERT INTO public.connection VALUES (99, 6, '127.0.0.1', '2021-04-13 09:29:07.086593', '2021-04-13 09:48:17.775665');
INSERT INTO public.connection VALUES (100, 7, '127.0.0.1', '2021-04-13 09:48:26.218012', '2021-04-13 10:24:53.663931');
INSERT INTO public.connection VALUES (101, 5, '127.0.0.1', '2021-04-13 10:25:06.345709', '2021-04-13 10:26:37.103939');
INSERT INTO public.connection VALUES (102, 10, '127.0.0.1', '2021-04-13 10:26:48.265738', '2021-04-13 10:28:28.839395');
INSERT INTO public.connection VALUES (103, 8, '127.0.0.1', '2021-04-13 10:28:54.008168', '2021-04-13 11:24:06.833981');
INSERT INTO public.connection VALUES (104, 10, '127.0.0.1', '2021-04-13 11:24:37.568732', '2021-04-13 11:30:39.465051');
INSERT INTO public.connection VALUES (105, 8, '127.0.0.1', '2021-04-13 11:30:49.265373', NULL);
INSERT INTO public.connection VALUES (106, 10, '127.0.0.1', '2021-04-13 12:38:43.822637', '2021-04-13 12:48:39.523149');
INSERT INTO public.connection VALUES (107, 8, '127.0.0.1', '2021-04-13 12:48:51.180363', '2021-04-13 12:56:06.063498');
INSERT INTO public.connection VALUES (108, 10, '127.0.0.1', '2021-04-13 12:56:15.400867', '2021-04-14 11:12:33.775144');
INSERT INTO public.connection VALUES (109, 5, '127.0.0.1', '2021-04-14 11:12:46.145278', '2021-04-14 12:54:52.879201');
INSERT INTO public.connection VALUES (110, 6, '127.0.0.1', '2021-04-14 12:55:02.957671', '2021-04-14 12:55:22.036454');
INSERT INTO public.connection VALUES (111, 8, '127.0.0.1', '2021-04-14 12:55:40.189277', '2021-04-14 12:56:13.531722');
INSERT INTO public.connection VALUES (112, 10, '127.0.0.1', '2021-04-14 12:56:20.694522', '2021-04-14 14:54:31.732321');
INSERT INTO public.connection VALUES (113, 5, '127.0.0.1', '2021-04-14 14:55:23.428228', NULL);
INSERT INTO public.connection VALUES (146, 10, '127.0.0.1', '2021-04-15 07:41:19.573007', '2021-04-15 13:01:52.414223');
INSERT INTO public.connection VALUES (147, 10, '127.0.0.1', '2021-04-15 13:02:56.042934', '2021-04-15 14:25:24.425483');
INSERT INTO public.connection VALUES (94, 11, '127.0.0.1', '2021-04-13 09:18:58.898164', '2021-04-15 14:27:22.942417');
INSERT INTO public.connection VALUES (157, 13, '127.0.0.1', '2021-04-16 13:17:58.005438', '2021-04-16 13:24:04.747418');
INSERT INTO public.connection VALUES (148, 13, '127.0.0.1', '2021-04-15 14:27:37.211808', '2021-04-15 14:27:52.133225');
INSERT INTO public.connection VALUES (149, 13, '127.0.0.1', '2021-04-15 14:28:05.509814', '2021-04-15 14:30:02.700457');
INSERT INTO public.connection VALUES (150, 10, '127.0.0.1', '2021-04-15 14:30:12.045559', '2021-04-15 14:31:36.788421');
INSERT INTO public.connection VALUES (151, 13, '127.0.0.1', '2021-04-15 14:31:48.541572', '2021-04-15 14:32:01.09321');
INSERT INTO public.connection VALUES (158, 10, '127.0.0.1', '2021-04-16 13:24:13.108564', NULL);
INSERT INTO public.connection VALUES (159, 5, '127.0.0.1', '2021-04-16 14:40:46.199829', '2021-04-20 10:34:07.573214');
INSERT INTO public.connection VALUES (152, 10, '127.0.0.1', '2021-04-15 14:32:10.30091', '2021-04-16 08:16:54.11787');
INSERT INTO public.connection VALUES (153, 10, '127.0.0.1', '2021-04-16 08:17:00.659327', NULL);
INSERT INTO public.connection VALUES (160, 10, '127.0.0.1', '2021-04-20 10:41:01.12153', '2021-04-20 10:41:55.985741');
INSERT INTO public.connection VALUES (154, 10, '127.0.0.1', '2021-04-16 08:18:11.006784', '2021-04-16 11:13:25.955014');
INSERT INTO public.connection VALUES (155, 10, '127.0.0.1', '2021-04-16 11:13:36.860695', '2021-04-16 11:13:38.628132');
INSERT INTO public.connection VALUES (161, 5, '127.0.0.1', '2021-04-20 10:42:08.53004', '2021-04-20 10:44:01.377067');
INSERT INTO public.connection VALUES (162, 10, '127.0.0.1', '2021-04-20 10:44:10.641893', '2021-04-20 11:10:29.430875');
INSERT INTO public.connection VALUES (182, 5, '127.0.0.1', '2021-04-22 12:42:45.533452', '2021-04-22 12:43:20.037398');
INSERT INTO public.connection VALUES (164, 10, '127.0.0.1', '2021-04-20 11:11:08.079807', '2021-04-20 11:21:03.925715');
INSERT INTO public.connection VALUES (165, 11, '127.0.0.1', '2021-04-20 11:21:15.326292', '2021-04-20 11:21:45.588513');
INSERT INTO public.connection VALUES (166, 7, '127.0.0.1', '2021-04-20 11:21:55.525104', '2021-04-20 11:22:02.844196');
INSERT INTO public.connection VALUES (167, 10, '127.0.0.1', '2021-04-20 11:22:14.918195', NULL);
INSERT INTO public.connection VALUES (163, 5, '127.0.0.1', '2021-04-20 11:10:40.81513', '2021-04-20 14:24:42.583537');
INSERT INTO public.connection VALUES (168, 10, '127.0.0.1', '2021-04-20 14:24:52.00262', '2021-04-21 12:15:17.450256');
INSERT INTO public.connection VALUES (169, 13, '127.0.0.1', '2021-04-21 12:15:29.504109', '2021-04-21 12:28:28.309262');
INSERT INTO public.connection VALUES (170, 10, '127.0.0.1', '2021-04-21 12:28:38.790941', '2021-04-22 07:43:08.7196');
INSERT INTO public.connection VALUES (172, 13, '127.0.0.1', '2021-04-22 07:43:21.114072', '2021-04-22 07:43:42.63869');
INSERT INTO public.connection VALUES (173, 6, '127.0.0.1', '2021-04-22 07:43:54.648283', '2021-04-22 07:44:12.880815');
INSERT INTO public.connection VALUES (174, 10, '127.0.0.1', '2021-04-22 07:44:23.338312', NULL);
INSERT INTO public.connection VALUES (171, 7, '127.0.0.1', '2021-04-21 12:53:48.032358', '2021-04-22 09:04:56.424435');
INSERT INTO public.connection VALUES (175, 11, '127.0.0.1', '2021-04-22 09:05:07.064773', '2021-04-22 09:06:50.950958');
INSERT INTO public.connection VALUES (176, 8, '127.0.0.1', '2021-04-22 09:07:59.800165', '2021-04-22 09:15:13.430321');
INSERT INTO public.connection VALUES (177, 11, '127.0.0.1', '2021-04-22 09:15:22.519383', '2021-04-22 09:16:43.813666');
INSERT INTO public.connection VALUES (178, 8, '127.0.0.1', '2021-04-22 09:16:59.519007', '2021-04-22 09:17:12.834228');
INSERT INTO public.connection VALUES (179, 11, '127.0.0.1', '2021-04-22 09:17:23.038738', '2021-04-22 10:35:38.254489');
INSERT INTO public.connection VALUES (181, 6, '127.0.0.1', '2021-04-22 10:35:49.45193', NULL);
INSERT INTO public.connection VALUES (180, 10, '127.0.0.1', '2021-04-22 09:36:39.574863', '2021-04-22 12:42:36.255176');
INSERT INTO public.connection VALUES (198, 8, '127.0.0.1', '2021-04-26 07:57:52.123864', '2021-04-26 09:19:02.458493');
INSERT INTO public.connection VALUES (184, 10, '127.0.0.1', '2021-04-22 13:06:03.04459', '2021-04-22 13:34:35.958');
INSERT INTO public.connection VALUES (183, 6, '127.0.0.1', '2021-04-22 12:43:30.595384', '2021-04-22 13:37:04.953305');
INSERT INTO public.connection VALUES (185, 14, '127.0.0.1', '2021-04-22 13:37:16.050529', '2021-04-22 13:42:26.571364');
INSERT INTO public.connection VALUES (186, 10, '127.0.0.1', '2021-04-22 13:42:40.69291', '2021-04-23 08:13:51.627854');
INSERT INTO public.connection VALUES (190, 10, '127.0.0.1', '2021-04-23 08:36:20.049922', '2021-04-23 10:41:01.132707');
INSERT INTO public.connection VALUES (187, 14, '127.0.0.1', '2021-04-23 08:14:12.235284', '2021-04-23 08:15:41.742634');
INSERT INTO public.connection VALUES (188, 10, '127.0.0.1', '2021-04-23 08:15:00.044501', '2021-04-23 08:35:59.520409');
INSERT INTO public.connection VALUES (189, 6, '127.0.0.1', '2021-04-23 08:15:52.680207', '2021-04-23 09:44:04.83718');
INSERT INTO public.connection VALUES (191, 13, '127.0.0.1', '2021-04-23 09:44:16.569209', '2021-04-23 09:44:29.828814');
INSERT INTO public.connection VALUES (192, 8, '127.0.0.1', '2021-04-23 09:44:45.686402', NULL);
INSERT INTO public.connection VALUES (193, 10, '127.0.0.1', '2021-04-23 10:41:10.493187', NULL);
INSERT INTO public.connection VALUES (194, 10, '127.0.0.1', '2021-04-23 10:44:18.886854', '2021-04-24 08:58:18.645205');
INSERT INTO public.connection VALUES (195, 7, '127.0.0.1', '2021-04-24 08:58:32.94313', '2021-04-24 08:59:22.31927');
INSERT INTO public.connection VALUES (197, 10, '127.0.0.1', '2021-04-26 07:38:12.758543', '2021-04-26 07:57:40.005897');
INSERT INTO public.connection VALUES (196, 11, '127.0.0.1', '2021-04-24 08:59:33.642148', '2021-04-26 11:45:00.100373');
INSERT INTO public.connection VALUES (200, 14, '127.0.0.1', '2021-04-26 11:45:20.635857', '2021-04-26 13:13:11.381326');
INSERT INTO public.connection VALUES (201, 13, '127.0.0.1', '2021-04-26 13:13:23.157029', '2021-04-26 13:19:51.690812');
INSERT INTO public.connection VALUES (202, 15, '127.0.0.1', '2021-04-26 13:23:00.460514', '2021-04-26 14:04:58.311089');
INSERT INTO public.connection VALUES (199, 10, '127.0.0.1', '2021-04-26 09:19:10.424524', '2021-04-26 14:50:24.077577');
INSERT INTO public.connection VALUES (204, 6, '127.0.0.1', '2021-04-26 14:50:39.846299', '2021-04-26 14:57:53.168623');
INSERT INTO public.connection VALUES (205, 10, '127.0.0.1', '2021-04-26 14:58:02.5898', NULL);
INSERT INTO public.connection VALUES (203, 9, '127.0.0.1', '2021-04-26 14:05:08.694842', '2021-04-27 09:47:43.371453');
INSERT INTO public.connection VALUES (207, 11, '127.0.0.1', '2021-04-27 10:42:22.983177', '2021-04-27 10:42:36.174603');
INSERT INTO public.connection VALUES (208, 17, '127.0.0.1', '2021-04-27 10:49:09.92838', '2021-04-27 10:59:16.824565');
INSERT INTO public.connection VALUES (209, 18, '127.0.0.1', '2021-04-27 11:04:00.696386', '2021-04-27 11:08:04.888658');
INSERT INTO public.connection VALUES (210, 19, '127.0.0.1', '2021-04-27 11:10:30.5769', '2021-04-27 11:15:33.999396');
INSERT INTO public.connection VALUES (206, 10, '127.0.0.1', '2021-04-27 10:41:53.65876', '2021-04-29 07:37:17.425807');
INSERT INTO public.connection VALUES (211, 18, '127.0.0.1', '2021-04-27 11:22:00.456913', '2021-04-28 09:44:28.560617');
INSERT INTO public.connection VALUES (212, 20, '127.0.0.1', '2021-04-28 11:19:25.864614', '2021-04-28 11:21:53.732644');
INSERT INTO public.connection VALUES (213, 21, '127.0.0.1', '2021-04-28 11:24:04.840074', '2021-04-28 11:26:31.830174');
INSERT INTO public.connection VALUES (214, 22, '127.0.0.1', '2021-04-28 11:28:14.896229', NULL);
INSERT INTO public.connection VALUES (215, 21, '127.0.0.1', '2021-04-29 07:37:31.389842', '2021-04-29 07:38:11.014706');
INSERT INTO public.connection VALUES (217, 21, '127.0.0.1', '2021-04-29 08:11:08.195388', NULL);
INSERT INTO public.connection VALUES (218, 21, '127.0.0.1', '2021-04-29 09:22:33.341361', NULL);
INSERT INTO public.connection VALUES (219, 10, '127.0.0.1', '2021-05-02 10:32:09.684875', NULL);
INSERT INTO public.connection VALUES (220, 10, '127.0.0.1', '2021-05-03 09:41:25.59408', '2021-05-04 07:19:51.965699');
INSERT INTO public.connection VALUES (221, 7, '127.0.0.1', '2021-05-04 07:20:18.310689', '2021-05-04 09:17:15.594349');
INSERT INTO public.connection VALUES (222, 13, '127.0.0.1', '2021-05-04 09:17:33.317535', '2021-05-04 09:49:45.442458');
INSERT INTO public.connection VALUES (223, 6, '127.0.0.1', '2021-05-04 09:50:14.294291', '2021-05-04 09:59:38.518577');
INSERT INTO public.connection VALUES (224, 10, '127.0.0.1', '2021-05-04 09:59:47.531402', '2021-05-04 10:17:58.006889');
INSERT INTO public.connection VALUES (225, 11, '127.0.0.1', '2021-05-04 10:18:11.329843', '2021-05-04 10:20:05.062755');
INSERT INTO public.connection VALUES (226, 10, '127.0.0.1', '2021-05-04 10:20:15.951748', '2021-05-04 10:40:33.860262');
INSERT INTO public.connection VALUES (227, 7, '127.0.0.1', '2021-05-04 10:40:46.980311', '2021-05-04 10:48:39.074942');
INSERT INTO public.connection VALUES (228, 11, '127.0.0.1', '2021-05-04 10:48:49.868089', '2021-05-04 11:11:09.806956');
INSERT INTO public.connection VALUES (229, 10, '127.0.0.1', '2021-05-04 11:11:17.404526', '2021-05-04 11:28:44.070093');
INSERT INTO public.connection VALUES (230, 16, '127.0.0.1', '2021-05-04 11:29:47.882027', '2021-05-04 12:19:54.961303');
INSERT INTO public.connection VALUES (216, 22, '127.0.0.1', '2021-04-29 07:38:21.808158', '2021-05-05 08:58:22.924523');
INSERT INTO public.connection VALUES (231, 10, '127.0.0.1', '2021-05-04 12:20:15.844275', '2021-05-12 07:35:57.019996');
INSERT INTO public.connection VALUES (232, 10, '127.0.0.1', '2021-05-12 07:45:45.919412', NULL);
INSERT INTO public.connection VALUES (233, 10, '127.0.0.1', '2021-05-12 08:49:57.993982', NULL);
INSERT INTO public.connection VALUES (234, 10, '127.0.0.1', '2021-05-12 08:55:00.104526', NULL);
INSERT INTO public.connection VALUES (235, 10, '127.0.0.1', '2021-05-12 08:57:26.243216', '2021-05-18 08:10:54.340691');
INSERT INTO public.connection VALUES (237, 10, '127.0.0.1', '2021-05-18 08:24:05.878629', '2021-05-18 08:25:57.254533');
INSERT INTO public.connection VALUES (238, 11, '127.0.0.1', '2021-05-18 08:26:20.831131', NULL);
INSERT INTO public.connection VALUES (236, 15, '127.0.0.1', '2021-05-18 08:11:34.50355', '2021-05-18 08:59:24.022692');
INSERT INTO public.connection VALUES (240, 5, '127.0.0.1', '2021-05-18 09:04:28.049553', '2021-05-18 09:28:12.555808');
INSERT INTO public.connection VALUES (241, 16, '127.0.0.1', '2021-05-18 09:28:53.597256', '2021-05-18 09:33:40.195728');
INSERT INTO public.connection VALUES (242, 21, '127.0.0.1', '2021-05-18 09:33:51.25332', '2021-05-18 09:34:22.212585');
INSERT INTO public.connection VALUES (239, 11, '127.0.0.1', '2021-05-18 08:40:22.902804', '2021-05-18 10:07:14.453157');
INSERT INTO public.connection VALUES (244, 16, '127.0.0.1', '2021-05-18 10:07:26.032338', '2021-05-18 10:08:26.444617');
INSERT INTO public.connection VALUES (245, 22, '127.0.0.1', '2021-05-18 10:08:48.281071', '2021-05-18 10:09:12.420687');
INSERT INTO public.connection VALUES (246, 11, '127.0.0.1', '2021-05-18 10:09:38.694306', '2021-05-18 10:41:39.08261');
INSERT INTO public.connection VALUES (248, 15, '127.0.0.1', '2021-05-18 14:12:32.33169', NULL);
INSERT INTO public.connection VALUES (243, 10, '127.0.0.1', '2021-05-18 09:42:48.127328', '2021-05-19 08:42:19.965835');
INSERT INTO public.connection VALUES (249, 15, '127.0.0.1', '2021-05-19 08:42:35.118358', '2021-05-19 08:42:42.316823');
INSERT INTO public.connection VALUES (250, 22, '127.0.0.1', '2021-05-19 08:43:54.308569', '2021-05-19 08:48:04.693133');
INSERT INTO public.connection VALUES (251, 7, '127.0.0.1', '2021-05-19 08:48:16.509438', '2021-05-19 09:02:53.489305');
INSERT INTO public.connection VALUES (247, 11, '127.0.0.1', '2021-05-18 11:09:22.864425', '2021-05-19 09:29:01.935126');
INSERT INTO public.connection VALUES (253, 22, '127.0.0.1', '2021-05-19 09:29:11.428326', NULL);
INSERT INTO public.connection VALUES (252, 10, '127.0.0.1', '2021-05-19 09:03:01.856754', '2021-05-19 11:23:41.812664');
INSERT INTO public.connection VALUES (255, 21, '127.0.0.1', '2021-05-19 11:38:07.463186', '2021-05-19 11:38:35.903214');
INSERT INTO public.connection VALUES (256, 16, '127.0.0.1', '2021-05-19 11:38:45.596703', '2021-05-19 11:44:48.188066');
INSERT INTO public.connection VALUES (254, 22, '127.0.0.1', '2021-05-19 11:23:51.478321', '2021-05-19 11:45:41.73184');
INSERT INTO public.connection VALUES (258, 11, '127.0.0.1', '2021-05-19 11:45:51.803931', NULL);
INSERT INTO public.connection VALUES (257, 9, '127.0.0.1', '2021-05-19 11:45:17.373862', '2021-05-19 11:49:58.345279');
INSERT INTO public.connection VALUES (259, 6, '127.0.0.1', '2021-05-19 11:50:11.325769', NULL);
INSERT INTO public.connection VALUES (260, 10, '127.0.0.1', '2021-05-25 08:29:55.627968', '2021-05-25 08:30:44.126404');
INSERT INTO public.connection VALUES (261, 10, '127.0.0.1', '2021-05-25 08:31:15.007251', NULL);


--
-- Data for Name: message; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.message VALUES (1, 1, 3, 'Que dois-je faire pour l''Astra-Zeneca', '2021-04-09 09:02:36.549584');
INSERT INTO public.message VALUES (2, 1, 2, 'Faut faire gaffe', '2021-04-09 09:02:36.549584');
INSERT INTO public.message VALUES (3, 1, 3, 'Zut, mon PM a dit hier que c''etait OK', '2021-04-09 09:02:36.549584');
INSERT INTO public.message VALUES (4, 1, 2, 'T''as plus qu''a le contredire!', '2021-04-09 09:02:36.549584');
INSERT INTO public.message VALUES (5, 1, 2, 'Ce ne sera qu''une fois de plus!!!!', '2021-04-09 09:02:36.549584');
INSERT INTO public.message VALUES (6, 3, 11, 'Bonjour', '2021-05-19 09:19:24.84597');
INSERT INTO public.message VALUES (7, 3, 10, 'Salut a toi !', '2021-05-19 09:22:34.930155');
INSERT INTO public.message VALUES (8, 3, 11, 'Comment vas-tu?', '2021-05-19 09:23:24.0248');
INSERT INTO public.message VALUES (9, 4, 9, 'Salut', '2021-05-19 11:46:01.985166');
INSERT INTO public.message VALUES (10, 4, 11, 'Salut ', '2021-05-19 11:46:09.241658');


--
-- Data for Name: notification; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.notification VALUES (1, 10, 13, 'Visit', false, '2021-05-06 08:32:31.804601');
INSERT INTO public.notification VALUES (2, 10, 11, 'Visit', false, '2021-05-06 08:46:01.927191');
INSERT INTO public.notification VALUES (3, 10, 11, 'Visit', false, '2021-05-06 08:46:07.016443');
INSERT INTO public.notification VALUES (4, 10, 11, 'Dislike', false, '2021-05-06 08:46:07.021223');
INSERT INTO public.notification VALUES (5, 10, 11, 'Visit', false, '2021-05-06 08:46:49.329922');
INSERT INTO public.notification VALUES (6, 10, 11, 'Visit', false, '2021-05-06 08:46:52.188223');
INSERT INTO public.notification VALUES (7, 10, 11, 'Like', false, '2021-05-06 08:46:52.191014');
INSERT INTO public.notification VALUES (8, 10, 14, 'Visit', false, '2021-05-06 08:47:46.376529');
INSERT INTO public.notification VALUES (9, 10, 18, 'Visit', false, '2021-05-06 08:47:54.045137');
INSERT INTO public.notification VALUES (10, 10, 11, 'Visit', false, '2021-05-06 09:06:03.023931');
INSERT INTO public.notification VALUES (11, 10, 11, 'Visit', false, '2021-05-06 09:07:22.967233');
INSERT INTO public.notification VALUES (12, 10, 10, 'Visit', false, '2021-05-06 09:07:42.615826');
INSERT INTO public.notification VALUES (13, 10, 10, 'Visit', false, '2021-05-06 09:08:06.551764');
INSERT INTO public.notification VALUES (14, 10, 6, 'Visit', false, '2021-05-06 09:08:27.919037');
INSERT INTO public.notification VALUES (15, 10, 6, 'Visit', false, '2021-05-06 09:09:14.358358');
INSERT INTO public.notification VALUES (16, 10, 14, 'Visit', false, '2021-05-06 09:09:29.455039');
INSERT INTO public.notification VALUES (17, 10, 13, 'Visit', false, '2021-05-06 09:21:51.245217');
INSERT INTO public.notification VALUES (18, 10, 14, 'Visit', false, '2021-05-06 10:02:08.650097');
INSERT INTO public.notification VALUES (19, 10, 18, 'Visit', false, '2021-05-06 10:39:16.537141');
INSERT INTO public.notification VALUES (20, 10, 14, 'Visit', false, '2021-05-06 11:15:19.450451');
INSERT INTO public.notification VALUES (21, 10, 18, 'Visit', false, '2021-05-06 11:42:45.606767');
INSERT INTO public.notification VALUES (22, 10, 6, 'Visit', false, '2021-05-06 12:19:47.119467');
INSERT INTO public.notification VALUES (23, 10, 6, 'Visit', false, '2021-05-06 12:19:54.879668');
INSERT INTO public.notification VALUES (24, 10, 6, 'Visit', false, '2021-05-06 12:26:40.018612');
INSERT INTO public.notification VALUES (25, 10, 6, 'Visit', false, '2021-05-12 07:26:37.922666');
INSERT INTO public.notification VALUES (26, 10, 11, 'Visit', false, '2021-05-12 07:27:04.255278');
INSERT INTO public.notification VALUES (27, 10, 11, 'Visit', false, '2021-05-12 07:46:40.733196');
INSERT INTO public.notification VALUES (28, 10, 11, 'Visit', false, '2021-05-12 09:13:06.725449');
INSERT INTO public.notification VALUES (29, 10, 11, 'Visit', false, '2021-05-12 09:14:18.695954');
INSERT INTO public.notification VALUES (30, 10, 14, 'Visit', false, '2021-05-12 10:44:33.662697');
INSERT INTO public.notification VALUES (31, 10, 14, 'Visit', false, '2021-05-12 10:44:38.538384');
INSERT INTO public.notification VALUES (32, 10, 14, 'Like', false, '2021-05-12 10:44:38.549044');
INSERT INTO public.notification VALUES (33, 10, 14, 'Visit', false, '2021-05-12 10:44:51.679367');
INSERT INTO public.notification VALUES (34, 10, 14, 'Visit', false, '2021-05-12 10:44:54.113646');
INSERT INTO public.notification VALUES (35, 10, 14, 'Dislike', false, '2021-05-12 10:44:54.116833');
INSERT INTO public.notification VALUES (36, 10, 11, 'Visit', false, '2021-05-12 14:30:39.530124');
INSERT INTO public.notification VALUES (37, 10, 13, 'Visit', false, '2021-05-17 08:12:34.414808');
INSERT INTO public.notification VALUES (38, 10, 11, 'Visit', false, '2021-05-17 08:12:39.53567');
INSERT INTO public.notification VALUES (39, 10, 18, 'Visit', false, '2021-05-17 08:13:01.79894');
INSERT INTO public.notification VALUES (40, 10, 11, 'Visit', false, '2021-05-17 13:00:04.944793');
INSERT INTO public.notification VALUES (41, 10, 13, 'Visit', false, '2021-05-17 13:00:10.751764');
INSERT INTO public.notification VALUES (42, 10, 14, 'Visit', false, '2021-05-17 13:01:02.222614');
INSERT INTO public.notification VALUES (43, 10, 13, 'Visit', false, '2021-05-17 13:01:11.40534');
INSERT INTO public.notification VALUES (44, 15, 6, 'Visit', false, '2021-05-18 08:41:31.236612');
INSERT INTO public.notification VALUES (45, 15, 16, 'Visit', false, '2021-05-18 08:58:58.170456');
INSERT INTO public.notification VALUES (46, 15, 16, 'Visit', false, '2021-05-18 08:59:08.338516');
INSERT INTO public.notification VALUES (47, 15, 16, 'Visit', false, '2021-05-18 08:59:16.400007');
INSERT INTO public.notification VALUES (48, 5, 13, 'Visit', false, '2021-05-18 09:07:05.176152');
INSERT INTO public.notification VALUES (49, 5, 2, 'Visit', false, '2021-05-18 09:07:12.190688');
INSERT INTO public.notification VALUES (50, 5, 2, 'Visit', false, '2021-05-18 09:07:27.598383');
INSERT INTO public.notification VALUES (51, 10, 14, 'Visit', false, '2021-05-18 09:42:56.712666');
INSERT INTO public.notification VALUES (52, 10, 11, 'Visit', false, '2021-05-18 09:55:52.179939');
INSERT INTO public.notification VALUES (53, 10, 11, 'Visit', false, '2021-05-18 10:04:58.923595');
INSERT INTO public.notification VALUES (54, 10, 13, 'Visit', false, '2021-05-18 10:05:05.08076');
INSERT INTO public.notification VALUES (55, 10, 6, 'Visit', false, '2021-05-18 10:05:16.103704');
INSERT INTO public.notification VALUES (56, 10, 14, 'Visit', false, '2021-05-18 10:05:27.528217');
INSERT INTO public.notification VALUES (57, 10, 18, 'Visit', false, '2021-05-18 10:05:34.6846');
INSERT INTO public.notification VALUES (58, 10, 10, 'Visit', false, '2021-05-18 10:05:41.939092');
INSERT INTO public.notification VALUES (59, 10, 5, 'Visit', false, '2021-05-18 10:05:48.298379');
INSERT INTO public.notification VALUES (60, 10, 13, 'Visit', false, '2021-05-18 10:05:59.649656');
INSERT INTO public.notification VALUES (61, 10, 14, 'Visit', false, '2021-05-18 10:06:13.752973');
INSERT INTO public.notification VALUES (62, 11, 8, 'Visit', false, '2021-05-18 10:06:32.801671');
INSERT INTO public.notification VALUES (63, 11, 7, 'Visit', false, '2021-05-18 10:06:38.895389');
INSERT INTO public.notification VALUES (64, 11, 10, 'Visit', false, '2021-05-18 10:06:46.432292');
INSERT INTO public.notification VALUES (65, 16, 15, 'Visit', false, '2021-05-18 10:07:35.302561');
INSERT INTO public.notification VALUES (66, 16, 15, 'Visit', false, '2021-05-18 10:07:45.376182');
INSERT INTO public.notification VALUES (67, 16, 15, 'Like', false, '2021-05-18 10:07:45.379359');
INSERT INTO public.notification VALUES (68, 16, 15, 'Visit', false, '2021-05-18 10:07:55.303473');
INSERT INTO public.notification VALUES (69, 11, 3, 'Visit', false, '2021-05-18 10:10:23.784147');
INSERT INTO public.notification VALUES (70, 11, 9, 'Visit', false, '2021-05-18 10:10:55.743725');
INSERT INTO public.notification VALUES (71, 11, 9, 'Visit', false, '2021-05-18 10:11:01.295106');
INSERT INTO public.notification VALUES (72, 11, 9, 'Like', false, '2021-05-18 10:11:01.298811');
INSERT INTO public.notification VALUES (73, 11, 9, 'Visit', false, '2021-05-18 10:11:06.326691');
INSERT INTO public.notification VALUES (74, 11, 19, 'Visit', false, '2021-05-18 10:11:27.415302');
INSERT INTO public.notification VALUES (75, 11, 8, 'Visit', false, '2021-05-18 11:15:19.514825');
INSERT INTO public.notification VALUES (76, 10, 5, 'Visit', false, '2021-05-19 08:11:49.633265');
INSERT INTO public.notification VALUES (77, 10, 13, 'Visit', false, '2021-05-19 08:12:00.064299');
INSERT INTO public.notification VALUES (78, 10, 13, 'Visit', false, '2021-05-19 08:13:44.375032');
INSERT INTO public.notification VALUES (79, 10, 13, 'Visit', false, '2021-05-19 08:13:54.696607');
INSERT INTO public.notification VALUES (80, 10, 13, 'Visit', false, '2021-05-19 08:31:19.443867');
INSERT INTO public.notification VALUES (81, 10, 13, 'Visit', false, '2021-05-19 08:32:29.125746');
INSERT INTO public.notification VALUES (82, 7, 11, 'Visit', false, '2021-05-19 08:49:46.391418');
INSERT INTO public.notification VALUES (83, 7, 13, 'Visit', false, '2021-05-19 08:59:11.418958');
INSERT INTO public.notification VALUES (84, 10, 11, 'Visit', false, '2021-05-19 09:03:09.429489');
INSERT INTO public.notification VALUES (85, 10, 11, 'Visit', false, '2021-05-19 09:03:13.486212');
INSERT INTO public.notification VALUES (86, 10, 11, 'Dislike', false, '2021-05-19 09:03:13.489612');
INSERT INTO public.notification VALUES (87, 10, 11, 'Visit', false, '2021-05-19 09:03:21.811235');
INSERT INTO public.notification VALUES (88, 10, 11, 'Like', false, '2021-05-19 09:03:21.814789');
INSERT INTO public.notification VALUES (89, 10, 11, 'Visit', false, '2021-05-19 09:12:56.383739');
INSERT INTO public.notification VALUES (90, 10, 11, 'Visit', false, '2021-05-19 09:12:59.460988');
INSERT INTO public.notification VALUES (91, 10, 11, 'Dislike', false, '2021-05-19 09:12:59.466147');
INSERT INTO public.notification VALUES (92, 10, 11, 'Visit', false, '2021-05-19 09:13:04.740227');
INSERT INTO public.notification VALUES (93, 10, 11, 'Visit', false, '2021-05-19 09:13:10.348991');
INSERT INTO public.notification VALUES (94, 10, 11, 'Like', false, '2021-05-19 09:13:10.352074');
INSERT INTO public.notification VALUES (95, 10, 11, 'Visit', false, '2021-05-19 09:17:47.842479');
INSERT INTO public.notification VALUES (96, 10, 11, 'Dislike', false, '2021-05-19 09:17:47.849692');
INSERT INTO public.notification VALUES (97, 10, 11, 'Visit', false, '2021-05-19 09:17:50.956428');
INSERT INTO public.notification VALUES (98, 10, 11, 'Like', false, '2021-05-19 09:17:50.960576');
INSERT INTO public.notification VALUES (99, 10, 11, 'Visit', false, '2021-05-19 09:18:08.359821');
INSERT INTO public.notification VALUES (100, 10, 11, 'Dislike', false, '2021-05-19 09:18:08.365027');
INSERT INTO public.notification VALUES (101, 10, 11, 'Visit', false, '2021-05-19 09:18:11.292551');
INSERT INTO public.notification VALUES (102, 10, 11, 'Like', false, '2021-05-19 09:18:11.295887');
INSERT INTO public.notification VALUES (103, 11, 10, 'Message', true, '2021-05-19 09:19:29.83382');
INSERT INTO public.notification VALUES (104, 10, 11, 'Message', true, '2021-05-19 09:23:20.349024');
INSERT INTO public.notification VALUES (105, 11, 10, 'Message', true, '2021-05-19 09:23:53.867794');
INSERT INTO public.notification VALUES (106, 11, 8, 'Visit', false, '2021-05-19 09:28:30.193026');
INSERT INTO public.notification VALUES (107, 10, 13, 'Visit', false, '2021-05-19 10:00:55.654403');
INSERT INTO public.notification VALUES (108, 10, 2, 'Visit', false, '2021-05-19 10:03:18.231013');
INSERT INTO public.notification VALUES (109, 10, 18, 'Visit', false, '2021-05-19 10:03:31.454712');
INSERT INTO public.notification VALUES (110, 10, 13, 'Visit', false, '2021-05-19 11:23:25.544181');
INSERT INTO public.notification VALUES (111, 16, 15, 'Visit', false, '2021-05-19 11:38:49.502854');
INSERT INTO public.notification VALUES (112, 16, 3, 'Visit', false, '2021-05-19 11:44:04.086985');
INSERT INTO public.notification VALUES (113, 16, 4, 'Visit', false, '2021-05-19 11:44:13.717295');
INSERT INTO public.notification VALUES (114, 9, 11, 'Visit', false, '2021-05-19 11:45:26.282083');
INSERT INTO public.notification VALUES (115, 9, 11, 'Visit', false, '2021-05-19 11:45:30.432882');
INSERT INTO public.notification VALUES (116, 9, 11, 'Like', false, '2021-05-19 11:45:30.437022');
INSERT INTO public.notification VALUES (117, 9, 11, 'Message', true, '2021-05-19 11:46:07.511369');
INSERT INTO public.notification VALUES (118, 11, 9, 'Message', true, '2021-05-19 11:46:20.071169');
INSERT INTO public.notification VALUES (119, 9, 6, 'Visit', false, '2021-05-19 11:49:32.173875');
INSERT INTO public.notification VALUES (120, 9, 6, 'Visit', false, '2021-05-19 11:49:40.486833');
INSERT INTO public.notification VALUES (121, 9, 6, 'Like', false, '2021-05-19 11:49:40.490571');
INSERT INTO public.notification VALUES (122, 9, 6, 'Visit', false, '2021-05-19 11:49:53.949978');
INSERT INTO public.notification VALUES (123, 6, 15, 'Visit', false, '2021-05-19 11:50:23.094169');
INSERT INTO public.notification VALUES (156, 10, 6, 'Visit', false, '2021-05-25 08:31:23.76671');
INSERT INTO public.notification VALUES (157, 10, 11, 'Visit', false, '2021-05-25 08:31:35.574405');
INSERT INTO public.notification VALUES (158, 10, 11, 'Visit', false, '2021-05-25 08:36:23.376439');
INSERT INTO public.notification VALUES (159, 10, 6, 'Visit', false, '2021-05-25 08:44:40.458436');


--
-- Data for Name: room; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.room VALUES (1, '{2,3}', false, '2021-04-09 09:02:36.549584', '2021-04-09 09:02:36.549584');
INSERT INTO public.room VALUES (2, '{2,1}', false, '2021-04-09 09:02:36.549584', '2021-04-09 09:02:36.549584');
INSERT INTO public.room VALUES (3, '{10,11}', true, '2021-05-19 09:18:11.297761', '2021-05-19 09:18:11.297761');
INSERT INTO public.room VALUES (4, '{9,11}', true, '2021-05-19 11:45:30.440026', '2021-05-19 11:45:30.440026');


--
-- Data for Name: topic; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.topic VALUES ('Piscine', '2021-04-09 09:02:36.549584');
INSERT INTO public.topic VALUES ('Peluche', '2021-04-09 09:02:36.549584');
INSERT INTO public.topic VALUES ('Gerontologie', '2021-04-09 09:02:36.549584');
INSERT INTO public.topic VALUES ('Manipulation', '2021-04-09 09:02:36.549584');
INSERT INTO public.topic VALUES ('Blitz', '2021-04-09 09:02:36.549584');
INSERT INTO public.topic VALUES ('Mercedes', '2021-04-09 09:02:36.549584');
INSERT INTO public.topic VALUES ('Restaurant', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Concert', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Lecture', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Musée', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Art', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Sports', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Jeu', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Nature', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Voyages', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Jardinage', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Cuisine', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Gastronomie', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Sorties', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Automobile', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Television', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Cinema', '2021-04-11 08:22:46.570159');
INSERT INTO public.topic VALUES ('Bio', '2021-04-11 08:32:57.864048');
INSERT INTO public.topic VALUES ('Geek', '2021-04-11 08:32:57.864048');
INSERT INTO public.topic VALUES ('Piercing', '2021-04-11 08:32:57.864048');
INSERT INTO public.topic VALUES ('Vegan', '2021-04-11 08:32:57.864048');
INSERT INTO public.topic VALUES ('Histoire', '2021-04-11 08:32:57.864048');
INSERT INTO public.topic VALUES ('Architecture', '2021-04-11 08:32:57.864048');
INSERT INTO public.topic VALUES ('Pêche', '2021-04-11 08:32:57.864048');
INSERT INTO public.topic VALUES ('Parachuisme', '2021-04-11 08:32:57.864048');
INSERT INTO public.topic VALUES ('Danse', '2021-04-21 12:21:50.622572');
INSERT INTO public.topic VALUES ('Photographie', '2021-04-21 12:28:20.37701');
INSERT INTO public.topic VALUES ('Peinture', '2021-04-21 12:54:19.732887');
INSERT INTO public.topic VALUES ('Escrime', '2021-04-22 09:08:33.966086');
INSERT INTO public.topic VALUES ('Informatique', '2021-04-26 07:46:33.026781');
INSERT INTO public.topic VALUES ('Randonnées', '2021-04-21 12:29:00.399821');
INSERT INTO public.topic VALUES ('Théatre', '2021-04-27 08:16:24.0213');


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.users VALUES (1, 'Donald', 'Trump', 'Duck', 'MyPassword', 'Blond au tweet feroce', 'donald@duck.us', true, NULL, 'Male', 'Hetero', '1946-06-14', 38.89783, -77.03650, '2021-04-09 09:02:36.549584', '2021-04-09 09:02:36.549584', NULL);
INSERT INTO public.users VALUES (8, 'Misse', 'Ara', 'Aramis', '5acc6c9048803790e46a7a8770b53afef332e379', '', 'matcha@ik.me', true, '', NULL, NULL, NULL, 48.88704, 2.37370, '2021-04-08 11:45:05.188755', '2021-05-19 09:28:30.195188', 0);
INSERT INTO public.users VALUES (12, 'Fred', 'Heric', 'Fred', '71ebe4b7e878004d9228b96801b5a31c0cf464c5', NULL, 'matcha@ik.me', false, '38Kdth1uiyNbUZX1F', NULL, NULL, NULL, 0.00000, 0.00000, '2021-04-09 10:57:00.821599', '2021-04-09 10:57:00.821599', NULL);
INSERT INTO public.users VALUES (2, 'Angela', 'Merkel', 'LaBombe', 'MyPassword', 'Mon serieux est mon principal atout', 'angela@frech.de', true, NULL, 'Female', 'Hetero', '1954-07-17', 52.52021, 13.36924, '2021-04-09 09:02:36.549584', '2021-05-19 10:03:18.233206', 0);
INSERT INTO public.users VALUES (13, 'Peggy', 'Dav', 'peggy', 'e737919d0a4e5aa68bf87896db02ecca0d05b36c', 'None', 'matcha@ik.me', true, NULL, 'Female', 'Hetero', '1968-07-10', 46.12449, 3.44604, '2021-04-15 14:26:48.550652', '2021-05-19 11:23:25.546515', 0);
INSERT INTO public.users VALUES (3, 'Emmanuel', 'Macron', 'Le Kiki', 'MyPassword', 'Passionne des antiquites', 'manu@narcisse.com', true, NULL, 'Male', 'Bi', '1977-12-21', 48.87120, 2.31650, '2021-04-09 09:02:36.549584', '2021-05-19 11:44:04.089081', 0);
INSERT INTO public.users VALUES (7, 'Henri', 'de Toulouse Lautrec', 'lautrec', '7cfd125292c5d44696f61cd5f8df16f34a7cd876', 'Peintre, amateur de bordels', 'matcha@ik.me', true, '', 'Male', 'Hetero', '1864-11-24', 43.92842, 2.14342, '2021-04-06 13:20:19.89491', '2021-05-18 10:06:38.896773', 0);
INSERT INTO public.users VALUES (4, 'Fogiel', 'Marc-Olivier', 'marcopapolo', 'MyPassword', 'Ouvert a toute les promotions', 'mo-fogiel@tetu.fr', true, NULL, 'Male', 'Homo', '1969-07-05', 48.83636, 2.27387, '2021-04-09 09:02:36.549584', '2021-05-19 11:44:13.718757', 0);
INSERT INTO public.users VALUES (9, 'LaFronde', 'Thierry', 'Thierry', 'aef3c2254a2fa7a0f20121be24bdcd4c288bf1b6', '', 'matcha@ik.me', true, '', 'Male', 'Hetero', '1992-04-09', 47.59274, 1.33324, '2021-04-08 12:40:38.403396', '2021-05-18 10:11:06.328244', 50);
INSERT INTO public.users VALUES (5, 'Elric', 'De Melnibonnée', 'elric', '4c4c369a3342b58413d6449a35f26bd06b8498bd', 'Du sang et des âmes pour mon seigneur Arioch !
Pour la preservation de l''antique Melnibonnée
', 'matcha@ik.me', true, '', 'Male', 'Hetero', '1967-12-05', 45.78069, 4.73777, '2021-04-07 12:24:59.79232', '2021-05-19 08:11:49.658714', 0);
INSERT INTO public.users VALUES (11, 'Houmana', 'France', 'Houmana', '4ffd0ddc92356e0334e207d8b6f0e42fea098a30', 'Une fille des iles', 'matcha@ik.me', true, NULL, 'Female', 'Hetero', '1980-07-16', -17.53042, -149.56255, '2021-04-09 10:54:29.381647', '2021-05-25 08:36:23.379766', 75);
INSERT INTO public.users VALUES (6, 'Pol', 'Gara', 'Pol', '23edf5afa212043e1631382e70a8177eae87f224', 'Puissante sorcière aux pouvoirs aussi ravageurs que son humour !', 'matcha@ik.me', true, '', 'Female', 'Hetero', '1980-05-15', 59.93222, 30.35308, '2021-04-07 12:25:21.768918', '2021-05-25 08:44:40.460964', 0);
INSERT INTO public.users VALUES (14, 'Aline', 'Hea', 'aline', 'dd770f000ac9e5b45b8948c426f4cf2fad8f8e80', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Officia, voluptatum iure! Laudantium voluptates odit cumque pariatur, molestiae sunt esse ullam, deleniti minima sit commodi consequuntur eveniet labore velit beatae dicta repellendus magnam animi neque rerum similique sint earum? Neque qui fuga, enim doloribus ex possimus incidunt libero vero iure similique?', 'matcha@ik.me', true, NULL, 'Female', 'Homo', '1974-06-19', 46.13607, 3.38838, '2021-04-22 13:36:53.240225', '2021-05-18 10:06:13.754605', 0);
INSERT INTO public.users VALUES (17, 'Anne', 'Onyme', 'anne', 'e23ce8983fa6bfcc79857d44aa0421862ee9efe6', 'qwertyuioasdfghjklzxcvbnm,', 'matcha@ik.me', true, NULL, 'Female', 'Homo', '1997-01-29', 47.31462, 5.03975, '2021-04-27 10:42:51.757609', '2021-04-27 11:23:09.122691', 1);
INSERT INTO public.users VALUES (21, 'Marlene', 'Attriquoté', 'marlene', '871a61c8ed7f7a469e69ad7e0d72597062f4b545', NULL, 'matcha@ik.me', true, NULL, NULL, NULL, NULL, 48.86023, 2.34107, '2021-04-28 11:22:06.601822', '2021-04-28 11:23:36.191254', 0);
INSERT INTO public.users VALUES (20, 'Xavier', 'Faure', 'xavier', 'be1eaf0d1e5880df8e0fc33c6bfc4efa202e5284', NULL, 'matcha@ik.me', true, NULL, NULL, NULL, NULL, 2.33870, 48.85820, '2021-04-28 11:18:46.809807', '2021-04-28 11:19:03.480638', 0);
INSERT INTO public.users VALUES (22, 'Jade', 'Mear', 'jade', 'b9058cd6474b615d76818735254b615de85e7b44', NULL, 'matcha@ik.me', true, NULL, NULL, NULL, NULL, 48.85820, 2.33870, '2021-04-28 11:27:47.678694', '2021-04-28 11:27:58.740088', 0);
INSERT INTO public.users VALUES (16, 'Paul', 'Hochon', 'paul', '4e9a3d6552bc12380eff954f2c76a3086b873826', 'taga zou', 'matcha@ik.me', true, NULL, 'Male', 'Homo', '1987-06-10', 45.04536, 5.05353, '2021-04-27 09:48:19.363589', '2021-05-18 08:59:16.401597', 1);
INSERT INTO public.users VALUES (19, 'guillian', 'Aplut', 'guillian', '624102147108f6a773567a0282a77bdc21af4963', 'None', 'matcha@ik.me', true, NULL, 'Male', 'Hetero', '1991-05-05', 46.51541, 4.94020, '2021-04-27 11:10:00.592471', '2021-05-18 10:11:27.424041', 0);
INSERT INTO public.users VALUES (18, 'Irene', 'Desnaige', 'irene', '92078f432b7662ac80efeb18b6c63d974cc8ed87', 'ftyftyfffyb.  nkkn jb iuh kh ', 'matcha@ik.me', true, NULL, 'Female', 'Bi', '1996-06-15', 45.45146, 4.40095, '2021-04-27 11:00:46.705133', '2021-05-19 10:03:31.456588', 50);
INSERT INTO public.users VALUES (15, 'Albert', 'Haibask', 'albert', 'decaebb09929f76f8b43b0245b30e15fe9b6c1a6', 'None', 'matcha@ik.me', true, NULL, 'Male', 'Bi', '1984-06-14', 43.41103, -1.58980, '2021-04-26 13:20:52.65997', '2021-05-19 11:50:23.096489', 33);
INSERT INTO public.users VALUES (10, 'Olivier', 'Gasnier', 'pegase7', '657ff497efbe802db68d585a9bf17d4f6fb36530', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Excepturi necessitatibus nihil illo eveniet cumque minus? Voluptatem asperiores earum laudantium voluptatibus fugit aperiam recusandae tempore corporis ad. Dicta veritatis labore beatae et. Dicta sunt, delectus, quo sit quos consequatur at temporibus sequi modi vel perferendis. Ex, neque odit possimus obcaecati nulla mollitia distinctio inventore, maiores esse quisquam nostrum rem reiciendis praesentium provident ut, fugit doloribus iusto molestias tempore! Molestias ab nemo voluptatibus expedita fuga sequi voluptates alias earum laboriosam temporibus repellat et, magnam distinctio dignissimos debitis quidem sed cumque explicabo aliquid saepe ad, facilis neque! Provident dolores, atque architecto doloribus ex eaque. Magni accusantium veniam id a vel! Recusandae ex harum sed facere perferendis. Ad cupiditate officia minus dolorem sed nihil fugit voluptatem pariatur sit id accusamus nesciunt eum dicta aliquid in, totam odit fugiat quas explicabo, iste tempore perspiciatis! Eveniet vitae, rem cupiditate asperiores dolor a esse. Sequi cumque necessitatibus suscipit laudantium, et dicta corporis eligendi facilis! Dolore sequi sed enim facere ipsa est, quidem doloribus ullam error minima veritatis quibusdam provident blanditiis inventore dicta. Dolor sapiente temporibus, nam quam magni nostrum nulla, repellat alias ab beatae veritatis dolorum repudiandae ut perferendis, cum atque aperiam exercitationem dolores. Cumque dolores a consequuntur exercitationem suscipit nemo illo eligendi alias minus provident totam inventore, in neque aliquid vero reprehenderit error dignissimos eum optio repudiandae. Id modi, quos unde facere quo labore laboriosam fugit dicta ea libero assumenda neque. Commodi, deleniti! Animi provident itaque ullam. Unde consequatur saepe expedita tempore fugiat ex. Nam, explicabo.', 'matcha@ik.me', true, NULL, 'Male', 'Hetero', '1967-09-18', 46.10904, 3.46267, '2021-04-09 07:25:20.498829', '2021-05-18 10:06:46.433948', 42);


--
-- Data for Name: users_recommandation; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--



--
-- Data for Name: users_room; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.users_room VALUES (1, 2, 3);
INSERT INTO public.users_room VALUES (1, 3, 2);
INSERT INTO public.users_room VALUES (2, 2, 1);
INSERT INTO public.users_room VALUES (2, 1, 2);
INSERT INTO public.users_room VALUES (3, 10, 11);
INSERT INTO public.users_room VALUES (3, 11, 10);
INSERT INTO public.users_room VALUES (4, 9, 11);
INSERT INTO public.users_room VALUES (4, 11, 9);


--
-- Data for Name: users_suggest; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--



--
-- Data for Name: users_topic; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.users_topic VALUES (1, 'Piscine');
INSERT INTO public.users_topic VALUES (1, 'Manipulation');
INSERT INTO public.users_topic VALUES (2, 'Blitz');
INSERT INTO public.users_topic VALUES (2, 'Mercedes');
INSERT INTO public.users_topic VALUES (3, 'Peluche');
INSERT INTO public.users_topic VALUES (3, 'Gerontologie');
INSERT INTO public.users_topic VALUES (3, 'Manipulation');
INSERT INTO public.users_topic VALUES (4, 'Piscine');
INSERT INTO public.users_topic VALUES (4, 'Mercedes');
INSERT INTO public.users_topic VALUES (5, 'Lecture');
INSERT INTO public.users_topic VALUES (5, 'Musée');
INSERT INTO public.users_topic VALUES (5, 'Art');
INSERT INTO public.users_topic VALUES (5, 'Jeu');
INSERT INTO public.users_topic VALUES (5, 'Nature');
INSERT INTO public.users_topic VALUES (5, 'Gastronomie');
INSERT INTO public.users_topic VALUES (5, 'Histoire');
INSERT INTO public.users_topic VALUES (13, 'Nature');
INSERT INTO public.users_topic VALUES (13, 'Lecture');
INSERT INTO public.users_topic VALUES (13, 'Photographie');
INSERT INTO public.users_topic VALUES (13, 'Danse');
INSERT INTO public.users_topic VALUES (15, 'Danse');
INSERT INTO public.users_topic VALUES (7, 'Art');
INSERT INTO public.users_topic VALUES (7, 'Musée');
INSERT INTO public.users_topic VALUES (7, 'Lecture');
INSERT INTO public.users_topic VALUES (7, 'Gastronomie');
INSERT INTO public.users_topic VALUES (7, 'Peinture');
INSERT INTO public.users_topic VALUES (14, 'Nature');
INSERT INTO public.users_topic VALUES (14, 'Parachuisme');
INSERT INTO public.users_topic VALUES (14, 'Peinture');
INSERT INTO public.users_topic VALUES (14, 'Jeu');
INSERT INTO public.users_topic VALUES (16, 'Television');
INSERT INTO public.users_topic VALUES (16, 'Restaurant');
INSERT INTO public.users_topic VALUES (16, 'Pêche');
INSERT INTO public.users_topic VALUES (6, 'Concert');
INSERT INTO public.users_topic VALUES (6, 'Art');
INSERT INTO public.users_topic VALUES (6, 'Voyages');
INSERT INTO public.users_topic VALUES (6, 'Cuisine');
INSERT INTO public.users_topic VALUES (16, 'Blitz');
INSERT INTO public.users_topic VALUES (15, 'Concert');
INSERT INTO public.users_topic VALUES (15, 'Jeu');
INSERT INTO public.users_topic VALUES (17, 'Vegan');
INSERT INTO public.users_topic VALUES (17, 'Peluche');
INSERT INTO public.users_topic VALUES (17, 'Jeu');
INSERT INTO public.users_topic VALUES (17, 'Nature');
INSERT INTO public.users_topic VALUES (17, 'Voyages');
INSERT INTO public.users_topic VALUES (17, 'Théatre');
INSERT INTO public.users_topic VALUES (17, 'Histoire');
INSERT INTO public.users_topic VALUES (18, 'Peinture');
INSERT INTO public.users_topic VALUES (8, 'Escrime');
INSERT INTO public.users_topic VALUES (18, 'Cinema');
INSERT INTO public.users_topic VALUES (9, 'Escrime');
INSERT INTO public.users_topic VALUES (9, 'Histoire');
INSERT INTO public.users_topic VALUES (9, 'Gastronomie');
INSERT INTO public.users_topic VALUES (18, 'Piscine');
INSERT INTO public.users_topic VALUES (18, 'Musée');
INSERT INTO public.users_topic VALUES (11, 'Piscine');
INSERT INTO public.users_topic VALUES (11, 'Sports');
INSERT INTO public.users_topic VALUES (11, 'Nature');
INSERT INTO public.users_topic VALUES (11, 'Pêche');
INSERT INTO public.users_topic VALUES (19, 'Cuisine');
INSERT INTO public.users_topic VALUES (19, 'Art');
INSERT INTO public.users_topic VALUES (19, 'Mercedes');
INSERT INTO public.users_topic VALUES (19, 'Cinema');
INSERT INTO public.users_topic VALUES (19, 'Randonnées');
INSERT INTO public.users_topic VALUES (10, 'Lecture');
INSERT INTO public.users_topic VALUES (10, 'Gastronomie');
INSERT INTO public.users_topic VALUES (10, 'Photographie');
INSERT INTO public.users_topic VALUES (10, 'Informatique');
INSERT INTO public.users_topic VALUES (10, 'Concert');
INSERT INTO public.users_topic VALUES (10, 'Musée');
INSERT INTO public.users_topic VALUES (10, 'Piscine');
INSERT INTO public.users_topic VALUES (10, 'Jeu');
INSERT INTO public.users_topic VALUES (10, 'Architecture');
INSERT INTO public.users_topic VALUES (10, 'Nature');
INSERT INTO public.users_topic VALUES (10, 'Voyages');
INSERT INTO public.users_topic VALUES (10, 'Théatre');
INSERT INTO public.users_topic VALUES (10, 'Restaurant');
INSERT INTO public.users_topic VALUES (10, 'Cuisine');
INSERT INTO public.users_topic VALUES (10, 'Histoire');
INSERT INTO public.users_topic VALUES (10, 'Art');
INSERT INTO public.users_topic VALUES (10, 'Sorties');


--
-- Data for Name: visit; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.visit VALUES (3, 10, 6, 1, false, false, '2021-04-22 07:43:54.653292', '2021-04-22 07:43:54.653292', false);
INSERT INTO public.visit VALUES (34, 17, 18, 1, false, false, '2021-04-27 11:22:47.160821', '2021-04-27 11:22:47.160821', false);
INSERT INTO public.visit VALUES (35, 14, 18, 1, false, false, '2021-04-27 11:23:13.960314', '2021-04-27 11:23:13.960314', false);
INSERT INTO public.visit VALUES (20, 10, 14, 3, true, false, '2021-04-22 13:40:08.726549', '2021-04-23 08:14:12.269954', false);
INSERT INTO public.visit VALUES (42, 3, 11, 1, false, false, '2021-05-18 10:09:38.700405', '2021-05-18 10:09:38.700405', false);
INSERT INTO public.visit VALUES (33, 19, 18, 2, false, false, '2021-04-27 11:22:00.463517', '2021-04-27 13:54:29.476754', false);
INSERT INTO public.visit VALUES (43, 9, 11, 3, true, false, '2021-05-18 10:10:30.231123', '2021-05-18 10:11:02.249599', false);
INSERT INTO public.visit VALUES (44, 19, 11, 1, false, false, '2021-05-18 10:11:10.255312', '2021-05-18 10:11:10.255312', false);
INSERT INTO public.visit VALUES (13, 11, 8, 2, false, false, '2021-04-22 09:16:59.52434', '2021-04-23 10:37:39.003378', false);
INSERT INTO public.visit VALUES (1, 5, 10, 51, false, false, '2021-04-22 07:42:52.655962', '2021-05-19 07:36:11.430587', true);
INSERT INTO public.visit VALUES (2, 10, 13, 2, false, false, '2021-04-22 07:43:21.130006', '2021-05-04 09:17:33.327898', false);
INSERT INTO public.visit VALUES (37, 6, 13, 1, false, false, '2021-05-04 09:18:30.935782', '2021-05-04 09:18:30.935782', false);
INSERT INTO public.visit VALUES (19, 13, 6, 2, false, false, '2021-04-22 12:55:39.363172', '2021-05-04 09:50:14.301177', false);
INSERT INTO public.visit VALUES (15, 7, 6, 7, false, false, '2021-04-22 10:53:49.819189', '2021-05-04 09:51:34.326443', false);
INSERT INTO public.visit VALUES (8, 11, 7, 6, true, false, '2021-04-22 09:03:54.750822', '2021-05-19 08:48:16.514771', false);
INSERT INTO public.visit VALUES (45, 13, 7, 1, false, false, '2021-05-19 08:49:54.904457', '2021-05-19 08:49:54.904457', false);
INSERT INTO public.visit VALUES (7, 6, 7, 1, false, false, '2021-04-22 08:55:16.991628', '2021-04-22 08:55:16.991628', false);
INSERT INTO public.visit VALUES (16, 8, 6, 11, false, false, '2021-04-22 10:55:26.153082', '2021-04-22 11:14:26.942256', false);
INSERT INTO public.visit VALUES (11, 8, 11, 11, false, false, '2021-04-22 09:06:10.702047', '2021-05-19 09:24:09.966594', false);
INSERT INTO public.visit VALUES (14, 2, 10, 2, false, false, '2021-04-22 10:39:09.452456', '2021-05-19 10:00:56.263637', false);
INSERT INTO public.visit VALUES (36, 18, 10, 16, true, false, '2021-04-27 11:23:37.575976', '2021-05-19 10:03:18.584523', false);
INSERT INTO public.visit VALUES (4, 13, 10, 40, false, false, '2021-04-22 07:44:23.34338', '2021-05-19 11:14:16.932725', false);
INSERT INTO public.visit VALUES (27, 15, 16, 5, true, false, '2021-04-27 09:52:26.771251', '2021-05-19 11:38:45.602793', false);
INSERT INTO public.visit VALUES (28, 3, 16, 2, false, false, '2021-04-27 09:53:21.663945', '2021-05-19 11:38:49.802031', false);
INSERT INTO public.visit VALUES (29, 4, 16, 3, false, false, '2021-04-27 10:00:01.59296', '2021-05-19 11:44:04.32519', false);
INSERT INTO public.visit VALUES (38, 6, 15, 1, false, false, '2021-05-18 08:40:50.016581', '2021-05-18 08:40:50.016581', false);
INSERT INTO public.visit VALUES (17, 10, 5, 1, false, false, '2021-04-22 12:42:45.539918', '2021-04-22 12:42:45.539918', false);
INSERT INTO public.visit VALUES (18, 5, 6, 1, false, false, '2021-04-22 12:43:30.600312', '2021-04-22 12:43:30.600312', false);
INSERT INTO public.visit VALUES (39, 16, 15, 3, false, false, '2021-05-18 08:41:33.492855', '2021-05-18 08:59:14.501565', false);
INSERT INTO public.visit VALUES (40, 13, 5, 1, false, false, '2021-05-18 09:04:28.056538', '2021-05-18 09:04:28.056538', false);
INSERT INTO public.visit VALUES (41, 2, 5, 2, false, false, '2021-05-18 09:07:12.032221', '2021-05-18 09:07:20.380465', false);
INSERT INTO public.visit VALUES (46, 11, 9, 2, true, false, '2021-05-19 11:45:17.379725', '2021-05-19 11:45:30.438586', false);
INSERT INTO public.visit VALUES (22, 8, 8, 2, false, false, '2021-04-23 09:58:19.569623', '2021-04-26 07:57:52.128996', false);
INSERT INTO public.visit VALUES (47, 6, 9, 3, true, false, '2021-05-19 11:48:25.0571', '2021-05-19 11:49:40.49275', false);
INSERT INTO public.visit VALUES (6, 10, 10, 89, true, false, '2021-04-22 07:52:54.433185', '2021-05-18 10:05:34.820714', false);
INSERT INTO public.visit VALUES (26, 15, 6, 2, false, false, '2021-04-26 14:51:17.844505', '2021-05-19 11:50:11.331506', false);
INSERT INTO public.visit VALUES (21, 14, 10, 57, false, false, '2021-04-22 13:42:40.698447', '2021-05-18 10:06:05.901105', false);
INSERT INTO public.visit VALUES (24, 3, 10, 2, false, false, '2021-04-26 14:35:33.034227', '2021-04-26 14:47:00.146585', false);
INSERT INTO public.visit VALUES (23, 15, 10, 2, false, false, '2021-04-26 14:34:44.26462', '2021-04-26 14:50:06.891048', false);
INSERT INTO public.visit VALUES (25, 9, 6, 1, false, false, '2021-04-26 14:50:39.852914', '2021-04-26 14:50:39.852914', false);
INSERT INTO public.visit VALUES (12, 7, 11, 6, false, false, '2021-04-22 09:15:22.5255', '2021-05-18 10:06:36.591823', false);
INSERT INTO public.visit VALUES (9, 10, 11, 7, true, false, '2021-04-22 09:05:07.070761', '2021-05-18 10:06:44.276161', false);
INSERT INTO public.visit VALUES (10, 11, 10, 63, true, false, '2021-04-22 09:05:51.782204', '2021-05-25 08:31:35.793015', false);
INSERT INTO public.visit VALUES (30, 14, 17, 1, false, false, '2021-04-27 10:51:30.118713', '2021-04-27 10:51:30.118713', false);
INSERT INTO public.visit VALUES (31, 10, 18, 1, false, false, '2021-04-27 11:05:16.427444', '2021-04-27 11:05:16.427444', false);
INSERT INTO public.visit VALUES (32, 18, 19, 2, false, false, '2021-04-27 11:13:08.012777', '2021-04-27 11:14:16.398973', false);
INSERT INTO public.visit VALUES (5, 6, 10, 33, false, true, '2021-04-22 07:44:36.31943', '2021-05-25 08:36:23.654932', true);


--
-- Name: connection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.connection_id_seq', 261, true);


--
-- Name: message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.message_id_seq', 10, true);


--
-- Name: notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.notification_id_seq', 159, true);


--
-- Name: room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.room_id_seq', 4, true);


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.tag_id_seq', 6, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.users_id_seq', 22, true);


--
-- Name: visit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.visit_id_seq', 47, true);


--
-- Name: connection connection_pkey; Type: CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.connection
    ADD CONSTRAINT connection_pkey PRIMARY KEY (id);


--
-- Name: message message_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_tag_pkey PRIMARY KEY (id);


--
-- Name: notification notification_pkey; Type: CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_pkey PRIMARY KEY (id);


--
-- Name: room room_pkey; Type: CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_pkey PRIMARY KEY (id);


--
-- Name: topic topic_pkey; Type: CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.topic
    ADD CONSTRAINT topic_pkey PRIMARY KEY (tag);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_room users_room_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.users_room
    ADD CONSTRAINT users_room_tag_pkey PRIMARY KEY (room_id, master_id);


--
-- Name: users_topic users_topic_pkey; Type: CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.users_topic
    ADD CONSTRAINT users_topic_pkey PRIMARY KEY (users_id, tag);


--
-- Name: visit visit_pkey; Type: CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.visit
    ADD CONSTRAINT visit_pkey PRIMARY KEY (id);


--
-- Name: connection_users_fk; Type: INDEX; Schema: public; Owner: matchaadmin
--

CREATE INDEX connection_users_fk ON public.connection USING btree (users_id);


--
-- Name: message_sender_fk; Type: INDEX; Schema: public; Owner: matchaadmin
--

CREATE INDEX message_sender_fk ON public.message USING btree (sender_id);


--
-- Name: notification_receiver_id_fk; Type: INDEX; Schema: public; Owner: matchaadmin
--

CREATE INDEX notification_receiver_id_fk ON public.notification USING btree (receiver_id);


--
-- Name: notification_sender_id_fk; Type: INDEX; Schema: public; Owner: matchaadmin
--

CREATE INDEX notification_sender_id_fk ON public.notification USING btree (sender_id);


--
-- Name: users_room_master_fk; Type: INDEX; Schema: public; Owner: matchaadmin
--

CREATE INDEX users_room_master_fk ON public.users_room USING btree (master_id);


--
-- Name: users_room_room_fk; Type: INDEX; Schema: public; Owner: matchaadmin
--

CREATE INDEX users_room_room_fk ON public.users_room USING btree (room_id);


--
-- Name: users_topic_tag_fk; Type: INDEX; Schema: public; Owner: matchaadmin
--

CREATE INDEX users_topic_tag_fk ON public.users_topic USING btree (tag);


--
-- Name: users_topic_users_fk; Type: INDEX; Schema: public; Owner: matchaadmin
--

CREATE INDEX users_topic_users_fk ON public.users_topic USING btree (users_id);


--
-- Name: users_user_name_unq; Type: INDEX; Schema: public; Owner: matchaadmin
--

CREATE UNIQUE INDEX users_user_name_unq ON public.users USING btree (user_name);


--
-- Name: visit_visited_visitor_unq; Type: INDEX; Schema: public; Owner: matchaadmin
--

CREATE UNIQUE INDEX visit_visited_visitor_unq ON public.visit USING btree (visited_id, visitor_id);


--
-- Name: visit_visitor_fk; Type: INDEX; Schema: public; Owner: matchaadmin
--

CREATE INDEX visit_visitor_fk ON public.visit USING btree (visitor_id);


--
-- Name: room trigger_room; Type: TRIGGER; Schema: public; Owner: matchaadmin
--

CREATE TRIGGER trigger_room AFTER INSERT OR DELETE ON public.room FOR EACH ROW EXECUTE FUNCTION public.on_room_dml();


--
-- Name: connection connection_users_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.connection
    ADD CONSTRAINT connection_users_id_fkey FOREIGN KEY (users_id) REFERENCES public.users(id);


--
-- Name: message message_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id);


--
-- Name: notification notification_receiver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_receiver_id_fkey FOREIGN KEY (receiver_id) REFERENCES public.users(id);


--
-- Name: notification notification_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.notification
    ADD CONSTRAINT notification_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id);


--
-- Name: users_room users_room_master_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.users_room
    ADD CONSTRAINT users_room_master_id_fkey FOREIGN KEY (master_id) REFERENCES public.users(id);


--
-- Name: users_room users_room_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.users_room
    ADD CONSTRAINT users_room_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room(id);


--
-- Name: users_room users_room_slave_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.users_room
    ADD CONSTRAINT users_room_slave_id_fkey FOREIGN KEY (slave_id) REFERENCES public.users(id);


--
-- Name: users_topic users_topic_tag_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.users_topic
    ADD CONSTRAINT users_topic_tag_fkey FOREIGN KEY (tag) REFERENCES public.topic(tag);


--
-- Name: users_topic users_topic_users_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.users_topic
    ADD CONSTRAINT users_topic_users_id_fkey FOREIGN KEY (users_id) REFERENCES public.users(id);


--
-- Name: visit visit_visited_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.visit
    ADD CONSTRAINT visit_visited_id_fkey FOREIGN KEY (visited_id) REFERENCES public.users(id);


--
-- Name: visit visit_visitor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.visit
    ADD CONSTRAINT visit_visitor_id_fkey FOREIGN KEY (visitor_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

