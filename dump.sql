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
-- Name: trigger_room(); Type: FUNCTION; Schema: public; Owner: lwiller
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


ALTER FUNCTION public.trigger_room() OWNER TO lwiller;

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
    popularity numeric(3,0),
    created timestamp without time zone DEFAULT now() NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.users OWNER TO matchaadmin;

--
-- Name: users_recommendation_id_seq; Type: SEQUENCE; Schema: public; Owner: matchaadmin
--

CREATE SEQUENCE public.users_recommendation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_recommendation_id_seq OWNER TO matchaadmin;

--
-- Name: users_recommendation; Type: TABLE; Schema: public; Owner: matchaadmin
--

CREATE TABLE public.users_recommendation (
    id integer DEFAULT nextval('public.users_recommendation_id_seq'::regclass) NOT NULL,
    sender_id integer NOT NULL,
    receiver_id integer NOT NULL,
    age_diff numeric(4,2),
    distance numeric(9,2),
    dist_ratio numeric(2,0),
    topics_ratio numeric(9,2),
    last_consult timestamp without time zone,
    is_rejected boolean DEFAULT false NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.users_recommendation OWNER TO matchaadmin;

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
INSERT INTO public.connection VALUES (7, 1, '127.0.0.1', '2021-04-27 08:08:03.727825', NULL);
INSERT INTO public.connection VALUES (8, 1, '127.0.0.1', '2021-04-27 08:28:40.16837', NULL);
INSERT INTO public.connection VALUES (9, 1, '127.0.0.1', '2021-04-27 08:31:17.642127', NULL);
INSERT INTO public.connection VALUES (10, 2, '127.0.0.1', '2021-04-27 08:37:50.82491', NULL);
INSERT INTO public.connection VALUES (11, 2, '127.0.0.1', '2021-04-27 08:39:35.641497', NULL);
INSERT INTO public.connection VALUES (12, 1, '127.0.0.1', '2021-04-27 08:39:53.620055', NULL);
INSERT INTO public.connection VALUES (13, 1, '127.0.0.1', '2021-04-27 09:19:39.064281', NULL);
INSERT INTO public.connection VALUES (14, 1, '127.0.0.1', '2021-04-27 09:22:23.006975', NULL);
INSERT INTO public.connection VALUES (15, 2, '127.0.0.1', '2021-04-27 09:31:40.990347', '2021-04-27 09:36:26.787138');
INSERT INTO public.connection VALUES (16, 2, '127.0.0.1', '2021-04-27 10:08:56.591334', NULL);
INSERT INTO public.connection VALUES (17, 2, '127.0.0.1', '2021-04-27 11:11:31.9416', NULL);
INSERT INTO public.connection VALUES (18, 2, '127.0.0.1', '2021-04-27 11:17:44.446439', NULL);
INSERT INTO public.connection VALUES (19, 1, '127.0.0.1', '2021-04-27 11:23:21.204711', NULL);
INSERT INTO public.connection VALUES (20, 2, '127.0.0.1', '2021-04-27 11:23:26.395646', NULL);
INSERT INTO public.connection VALUES (21, 2, '127.0.0.1', '2021-04-27 11:47:52.95894', NULL);
INSERT INTO public.connection VALUES (22, 2, '127.0.0.1', '2021-04-27 12:55:44.748047', NULL);
INSERT INTO public.connection VALUES (23, 2, '127.0.0.1', '2021-04-27 12:57:25.762286', NULL);
INSERT INTO public.connection VALUES (24, 2, '127.0.0.1', '2021-04-27 12:59:10.809104', NULL);
INSERT INTO public.connection VALUES (25, 2, '127.0.0.1', '2021-04-27 13:02:32.351', '2021-04-27 13:03:37.201721');
INSERT INTO public.connection VALUES (26, 2, '127.0.0.1', '2021-04-27 13:05:28.374036', NULL);
INSERT INTO public.connection VALUES (27, 2, '127.0.0.1', '2021-04-28 09:41:40.010985', NULL);
INSERT INTO public.connection VALUES (28, 1, '127.0.0.1', '2021-04-28 09:48:07.500345', NULL);
INSERT INTO public.connection VALUES (29, 1, '127.0.0.1', '2021-04-28 09:56:02.098804', NULL);
INSERT INTO public.connection VALUES (30, 1, '127.0.0.1', '2021-04-28 10:53:52.135853', NULL);
INSERT INTO public.connection VALUES (31, 2, '127.0.0.1', '2021-04-28 13:59:22.424741', NULL);
INSERT INTO public.connection VALUES (32, 2, '127.0.0.1', '2021-05-04 09:15:12.238992', NULL);
INSERT INTO public.connection VALUES (33, 2, '127.0.0.1', '2021-05-04 09:20:03.856365', NULL);
INSERT INTO public.connection VALUES (34, 2, '127.0.0.1', '2021-05-04 09:21:09.018561', NULL);
INSERT INTO public.connection VALUES (35, 2, '127.0.0.1', '2021-05-04 09:27:51.894223', NULL);
INSERT INTO public.connection VALUES (36, 2, '127.0.0.1', '2021-05-04 14:28:56.0011', NULL);
INSERT INTO public.connection VALUES (37, 2, '127.0.0.1', '2021-05-05 09:36:07.532398', NULL);
INSERT INTO public.connection VALUES (38, 2, '127.0.0.1', '2021-05-05 13:54:32.317211', NULL);
INSERT INTO public.connection VALUES (39, 2, '127.0.0.1', '2021-05-06 07:36:48.733418', NULL);
INSERT INTO public.connection VALUES (40, 1, '127.0.0.1', '2021-05-06 07:38:58.74627', NULL);
INSERT INTO public.connection VALUES (41, 3, '127.0.0.1', '2021-05-06 08:03:09.623698', NULL);
INSERT INTO public.connection VALUES (42, 2, '127.0.0.1', '2021-05-06 13:43:21.834685', NULL);
INSERT INTO public.connection VALUES (43, 1, '127.0.0.1', '2021-05-06 13:48:03.573179', NULL);
INSERT INTO public.connection VALUES (44, 3, '127.0.0.1', '2021-05-06 16:01:22.509284', NULL);
INSERT INTO public.connection VALUES (45, 2, '127.0.0.1', '2021-05-07 07:42:08.086763', NULL);
INSERT INTO public.connection VALUES (46, 1, '127.0.0.1', '2021-05-07 08:08:41.527024', NULL);
INSERT INTO public.connection VALUES (47, 3, '127.0.0.1', '2021-05-07 08:09:40.274397', NULL);
INSERT INTO public.connection VALUES (79, 1, '127.0.0.1', '2021-05-07 11:08:21.299661', NULL);
INSERT INTO public.connection VALUES (80, 1, '127.0.0.1', '2021-05-07 13:32:00.503054', NULL);
INSERT INTO public.connection VALUES (81, 1, '127.0.0.1', '2021-05-07 14:20:50.464327', '2021-05-07 14:33:34.679621');
INSERT INTO public.connection VALUES (82, 2, '127.0.0.1', '2021-05-07 14:33:39.732091', NULL);
INSERT INTO public.connection VALUES (83, 2, '127.0.0.1', '2021-05-07 14:37:49.179903', NULL);
INSERT INTO public.connection VALUES (84, 3, '127.0.0.1', '2021-05-07 15:22:14.566552', NULL);
INSERT INTO public.connection VALUES (85, 2, '127.0.0.1', '2021-05-10 10:02:30.030988', NULL);
INSERT INTO public.connection VALUES (86, 1, '127.0.0.1', '2021-05-10 10:09:01.902077', NULL);
INSERT INTO public.connection VALUES (87, 2, '127.0.0.1', '2021-05-11 08:04:58.640542', NULL);
INSERT INTO public.connection VALUES (88, 1, '127.0.0.1', '2021-05-11 08:05:25.802601', NULL);
INSERT INTO public.connection VALUES (89, 3, '127.0.0.1', '2021-05-11 08:39:56.749291', NULL);
INSERT INTO public.connection VALUES (90, 2, '127.0.0.1', '2021-05-12 07:50:14.64477', NULL);
INSERT INTO public.connection VALUES (91, 1, '127.0.0.1', '2021-05-12 07:50:53.773299', NULL);
INSERT INTO public.connection VALUES (92, 2, '127.0.0.1', '2021-05-12 10:36:01.977768', NULL);
INSERT INTO public.connection VALUES (93, 2, '127.0.0.1', '2021-05-12 13:12:18.616846', NULL);
INSERT INTO public.connection VALUES (94, 1, '127.0.0.1', '2021-05-12 13:13:57.997785', NULL);
INSERT INTO public.connection VALUES (95, 3, '127.0.0.1', '2021-05-12 13:59:27.754714', '2021-05-12 14:01:17.523981');
INSERT INTO public.connection VALUES (96, 3, '127.0.0.1', '2021-05-12 14:08:49.79592', NULL);
INSERT INTO public.connection VALUES (97, 2, '127.0.0.1', '2021-05-17 08:46:58.750715', NULL);
INSERT INTO public.connection VALUES (98, 2, '127.0.0.1', '2021-05-17 11:34:30.595074', NULL);
INSERT INTO public.connection VALUES (99, 2, '127.0.0.1', '2021-05-17 11:41:12.486294', NULL);
INSERT INTO public.connection VALUES (101, 4, '127.0.0.1', '2021-05-17 13:36:16.012143', NULL);
INSERT INTO public.connection VALUES (102, 4, '127.0.0.1', '2021-05-17 13:36:50.100048', NULL);
INSERT INTO public.connection VALUES (103, 4, '127.0.0.1', '2021-05-17 13:37:20.496348', NULL);
INSERT INTO public.connection VALUES (104, 4, '127.0.0.1', '2021-05-17 13:47:37.572506', NULL);
INSERT INTO public.connection VALUES (100, 2, '127.0.0.1', '2021-05-17 13:22:06.928749', '2021-05-17 13:47:48.699365');
INSERT INTO public.connection VALUES (105, 2, '127.0.0.1', '2021-05-17 13:47:53.099033', NULL);
INSERT INTO public.connection VALUES (106, 1, '127.0.0.1', '2021-05-17 13:48:34.610468', '2021-05-17 13:48:42.915518');
INSERT INTO public.connection VALUES (107, 4, '127.0.0.1', '2021-05-17 13:48:53.674523', NULL);
INSERT INTO public.connection VALUES (108, 1, '127.0.0.1', '2021-05-17 13:50:39.441722', NULL);
INSERT INTO public.connection VALUES (109, 4, '127.0.0.1', '2021-05-17 15:00:33.768494', NULL);
INSERT INTO public.connection VALUES (110, 1, '127.0.0.1', '2021-05-17 15:01:03.021881', '2021-05-17 15:01:30.718196');
INSERT INTO public.connection VALUES (111, 5, '127.0.0.1', '2021-05-17 15:01:43.935203', NULL);
INSERT INTO public.connection VALUES (112, 5, '127.0.0.1', '2021-05-17 15:03:45.84625', NULL);
INSERT INTO public.connection VALUES (113, 5, '127.0.0.1', '2021-05-17 15:04:24.230437', NULL);
INSERT INTO public.connection VALUES (114, 5, '127.0.0.1', '2021-05-17 15:05:56.478475', NULL);
INSERT INTO public.connection VALUES (115, 5, '127.0.0.1', '2021-05-17 15:08:10.391201', NULL);
INSERT INTO public.connection VALUES (118, 4, '127.0.0.1', '2021-05-18 08:02:40.37895', NULL);
INSERT INTO public.connection VALUES (116, 2, '127.0.0.1', '2021-05-18 08:00:42.513601', '2021-05-18 08:11:34.060552');
INSERT INTO public.connection VALUES (119, 2, '127.0.0.1', '2021-05-18 08:11:38.588964', NULL);
INSERT INTO public.connection VALUES (120, 3, '127.0.0.1', '2021-05-18 08:25:18.605921', '2021-05-18 08:26:13.557761');
INSERT INTO public.connection VALUES (121, 4, '127.0.0.1', '2021-05-18 08:26:43.175109', NULL);
INSERT INTO public.connection VALUES (117, 1, '127.0.0.1', '2021-05-18 08:01:20.736508', '2021-05-18 10:18:32.42917');
INSERT INTO public.connection VALUES (123, 3, '127.0.0.1', '2021-05-18 10:25:09.746257', NULL);
INSERT INTO public.connection VALUES (124, 3, '127.0.0.1', '2021-05-18 10:45:38.330948', NULL);
INSERT INTO public.connection VALUES (122, 2, '127.0.0.1', '2021-05-18 08:44:50.643446', '2021-05-18 11:25:03.813894');
INSERT INTO public.connection VALUES (125, 3, '127.0.0.1', '2021-05-18 12:38:44.275069', NULL);
INSERT INTO public.connection VALUES (126, 4, '127.0.0.1', '2021-05-18 12:39:01.192558', '2021-05-18 14:24:03.170055');
INSERT INTO public.connection VALUES (127, 2, '127.0.0.1', '2021-05-18 14:24:09.614692', '2021-05-18 14:26:48.458686');
INSERT INTO public.connection VALUES (128, 2, '127.0.0.1', '2021-05-18 14:26:52.34257', NULL);
INSERT INTO public.connection VALUES (129, 2, '127.0.0.1', '2021-05-19 08:08:03.236784', NULL);
INSERT INTO public.connection VALUES (130, 4, '127.0.0.1', '2021-05-19 08:29:18.785879', NULL);
INSERT INTO public.connection VALUES (131, 3, '127.0.0.1', '2021-05-19 08:30:19.473563', NULL);
INSERT INTO public.connection VALUES (132, 2, '127.0.0.1', '2021-05-19 14:34:33.670277', NULL);
INSERT INTO public.connection VALUES (133, 4, '127.0.0.1', '2021-05-19 14:53:06.775004', NULL);
INSERT INTO public.connection VALUES (134, 2, '127.0.0.1', '2021-05-20 08:40:13.269258', '2021-05-20 11:37:34.806012');
INSERT INTO public.connection VALUES (136, 2, '127.0.0.1', '2021-05-20 11:42:24.847402', '2021-05-20 11:47:14.104717');
INSERT INTO public.connection VALUES (137, 2, '127.0.0.1', '2021-05-20 11:47:18.505665', '2021-05-20 12:19:37.066088');
INSERT INTO public.connection VALUES (135, 1, '127.0.0.1', '2021-05-20 11:42:07.586858', '2021-05-20 12:57:40.629532');
INSERT INTO public.connection VALUES (138, 2, '127.0.0.1', '2021-05-20 12:19:41.826397', '2021-05-20 13:50:08.444833');
INSERT INTO public.connection VALUES (140, 2, '127.0.0.1', '2021-05-20 13:50:12.80561', '2021-05-20 14:01:25.822665');
INSERT INTO public.connection VALUES (141, 2, '127.0.0.1', '2021-05-20 14:01:29.714479', NULL);
INSERT INTO public.connection VALUES (139, 4, '127.0.0.1', '2021-05-20 12:58:02.324672', '2021-05-20 15:52:35.892078');
INSERT INTO public.connection VALUES (142, 2, '127.0.0.1', '2021-05-25 07:38:57.536826', '2021-05-25 07:40:10.941762');
INSERT INTO public.connection VALUES (144, 4, '127.0.0.1', '2021-05-25 08:02:54.978658', '2021-05-25 08:45:41.371449');
INSERT INTO public.connection VALUES (143, 2, '127.0.0.1', '2021-05-25 07:40:16.285908', '2021-05-25 14:11:25.839572');
INSERT INTO public.connection VALUES (146, 2, '127.0.0.1', '2021-05-25 14:11:31.03054', '2021-05-25 14:11:59.166819');
INSERT INTO public.connection VALUES (145, 4, '127.0.0.1', '2021-05-25 08:47:20.560993', '2021-05-25 14:13:52.057012');
INSERT INTO public.connection VALUES (147, 2, '127.0.0.1', '2021-05-25 14:12:04.033845', '2021-05-25 14:20:03.452644');
INSERT INTO public.connection VALUES (149, 2, '127.0.0.1', '2021-05-25 14:20:08.466759', '2021-05-25 14:25:28.865156');
INSERT INTO public.connection VALUES (150, 2, '127.0.0.1', '2021-05-25 14:25:33.054575', '2021-05-25 14:29:25.97352');
INSERT INTO public.connection VALUES (148, 4, '127.0.0.1', '2021-05-25 14:14:03.478511', '2021-05-25 14:30:08.876683');
INSERT INTO public.connection VALUES (151, 2, '127.0.0.1', '2021-05-25 14:29:30.432264', '2021-05-25 14:31:28.160943');
INSERT INTO public.connection VALUES (153, 2, '127.0.0.1', '2021-05-25 14:31:32.568977', '2021-05-25 14:34:14.480872');
INSERT INTO public.connection VALUES (154, 2, '127.0.0.1', '2021-05-25 14:34:20.151017', '2021-05-25 14:35:08.751149');
INSERT INTO public.connection VALUES (155, 2, '127.0.0.1', '2021-05-25 14:35:13.154246', '2021-05-25 14:38:35.734891');
INSERT INTO public.connection VALUES (156, 2, '127.0.0.1', '2021-05-25 14:38:40.486431', '2021-05-25 14:43:59.871506');
INSERT INTO public.connection VALUES (152, 4, '127.0.0.1', '2021-05-25 14:30:28.568887', '2021-05-25 14:44:38.697205');
INSERT INTO public.connection VALUES (158, 4, '127.0.0.1', '2021-05-25 14:44:48.568463', NULL);
INSERT INTO public.connection VALUES (157, 2, '127.0.0.1', '2021-05-25 14:44:03.589407', '2021-05-25 15:05:36.738914');
INSERT INTO public.connection VALUES (159, 2, '127.0.0.1', '2021-05-25 15:05:40.906904', NULL);
INSERT INTO public.connection VALUES (160, 2, '127.0.0.1', '2021-05-26 08:05:37.316426', '2021-05-26 08:16:51.130049');
INSERT INTO public.connection VALUES (161, 2, '127.0.0.1', '2021-05-26 08:16:56.855895', NULL);
INSERT INTO public.connection VALUES (162, 4, '127.0.0.1', '2021-05-26 08:18:46.666492', NULL);
INSERT INTO public.connection VALUES (163, 3, '127.0.0.1', '2021-05-26 10:54:01.946192', NULL);


--
-- Data for Name: message; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.message VALUES (1, 1, 3, 'Que dois-je faire pour l''Astra-Zeneca', '2021-04-26 16:40:13.761518');
INSERT INTO public.message VALUES (2, 1, 2, 'Faut faire gaffe', '2021-04-26 16:40:13.761518');
INSERT INTO public.message VALUES (3, 1, 3, 'Zut, mon PM a dit hier que c''etait OK', '2021-04-26 16:40:13.761518');
INSERT INTO public.message VALUES (4, 1, 2, 'T''as plus qu''a le contredire!', '2021-04-26 16:40:13.761518');
INSERT INTO public.message VALUES (5, 1, 2, 'Ce ne sera qu''une fois de plus!!!!', '2021-04-26 16:40:13.761518');
INSERT INTO public.message VALUES (6, 2, 2, 'hi', '2021-04-27 11:23:26.410094');
INSERT INTO public.message VALUES (7, 2, 1, 'hohoh', '2021-04-27 11:24:01.237463');
INSERT INTO public.message VALUES (8, 2, 1, 'fffff', '2021-04-27 11:24:08.012348');
INSERT INTO public.message VALUES (9, 2, 2, 'gogogo', '2021-04-27 11:24:18.09347');
INSERT INTO public.message VALUES (10, 2, 2, 'lili', '2021-04-27 11:24:27.1251');
INSERT INTO public.message VALUES (11, 2, 2, 'jjjj', '2021-04-27 11:24:40.485089');
INSERT INTO public.message VALUES (12, 2, 1, 'ffrr', '2021-04-27 11:24:56.187936');
INSERT INTO public.message VALUES (13, 2, 2, 'hhhh', '2021-04-27 11:25:15.356857');
INSERT INTO public.message VALUES (14, 2, 2, 'gggg', '2021-05-05 13:54:32.402616');
INSERT INTO public.message VALUES (15, 2, 2, 'nnnn', '2021-05-05 13:58:03.934796');
INSERT INTO public.message VALUES (16, 2, 2, 'dddd', '2021-05-05 14:09:00.505143');
INSERT INTO public.message VALUES (17, 2, 2, 'dd', '2021-05-05 14:10:49.733786');
INSERT INTO public.message VALUES (18, 2, 2, 'sssss', '2021-05-05 14:11:32.752013');
INSERT INTO public.message VALUES (19, 2, 2, 'zzzz', '2021-05-05 14:13:02.878745');
INSERT INTO public.message VALUES (20, 2, 2, 'aaaa', '2021-05-05 14:14:04.299435');
INSERT INTO public.message VALUES (21, 2, 2, 'ddddd', '2021-05-05 14:19:22.665099');
INSERT INTO public.message VALUES (22, 2, 2, 'www', '2021-05-05 14:20:35.083936');
INSERT INTO public.message VALUES (23, 2, 2, 'eee', '2021-05-05 14:20:46.704239');
INSERT INTO public.message VALUES (24, 2, 2, 'tttt', '2021-05-05 14:26:30.243573');
INSERT INTO public.message VALUES (25, 2, 2, 'ooo', '2021-05-05 14:28:43.249095');
INSERT INTO public.message VALUES (26, 2, 2, 'kkkk', '2021-05-05 14:29:48.006431');
INSERT INTO public.message VALUES (27, 2, 2, 'nbnb', '2021-05-05 14:36:18.668773');
INSERT INTO public.message VALUES (28, 2, 2, 'mnmn', '2021-05-05 14:41:09.365391');
INSERT INTO public.message VALUES (29, 2, 2, 'ppp', '2021-05-05 14:44:19.459292');
INSERT INTO public.message VALUES (30, 2, 2, 'fff', '2021-05-05 14:45:55.960859');
INSERT INTO public.message VALUES (31, 2, 2, 'bbbb', '2021-05-06 08:01:08.256395');
INSERT INTO public.message VALUES (32, 2, 1, 'ghgh', '2021-05-06 08:03:09.672415');
INSERT INTO public.message VALUES (33, 2, 1, 'hjhj', '2021-05-06 08:06:29.014107');
INSERT INTO public.message VALUES (34, 2, 2, 'ghgh', '2021-05-06 08:08:02.983226');
INSERT INTO public.message VALUES (35, 2, 2, 'rrrr', '2021-05-06 08:16:39.285752');
INSERT INTO public.message VALUES (36, 2, 2, 'ssss', '2021-05-06 08:22:45.253104');
INSERT INTO public.message VALUES (37, 2, 1, 'eee', '2021-05-06 08:30:27.907736');
INSERT INTO public.message VALUES (38, 2, 2, 'yyy', '2021-05-06 08:31:22.216142');
INSERT INTO public.message VALUES (39, 2, 2, 'ffff', '2021-05-06 08:32:20.009323');
INSERT INTO public.message VALUES (40, 2, 1, 'kkkk', '2021-05-06 08:33:03.287051');
INSERT INTO public.message VALUES (41, 2, 1, 'kjjj', '2021-05-06 09:15:28.539796');
INSERT INTO public.message VALUES (42, 2, 2, 'momo', '2021-05-06 09:20:27.334003');
INSERT INTO public.message VALUES (43, 2, 1, 'vivi', '2021-05-06 09:21:22.53864');
INSERT INTO public.message VALUES (44, 2, 2, 'titi', '2021-05-06 09:22:51.56102');
INSERT INTO public.message VALUES (45, 2, 2, 'toto', '2021-05-06 09:24:56.114347');
INSERT INTO public.message VALUES (46, 2, 2, 'dudud', '2021-05-06 09:27:33.566885');
INSERT INTO public.message VALUES (47, 2, 2, 'hihih', '2021-05-06 09:40:08.934939');
INSERT INTO public.message VALUES (48, 2, 2, 'rtrt', '2021-05-06 09:49:53.437349');
INSERT INTO public.message VALUES (49, 2, 1, 'bnbn', '2021-05-06 09:50:40.159661');
INSERT INTO public.message VALUES (50, 2, 1, 'hjhj', '2021-05-06 09:51:10.983504');
INSERT INTO public.message VALUES (51, 2, 2, 'hkhk', '2021-05-06 09:55:05.328838');
INSERT INTO public.message VALUES (52, 2, 2, 'liili', '2021-05-06 10:03:07.880372');
INSERT INTO public.message VALUES (53, 2, 2, 'hkhk', '2021-05-06 10:06:45.67228');
INSERT INTO public.message VALUES (54, 2, 1, 'kjkjk', '2021-05-06 10:38:53.78976');
INSERT INTO public.message VALUES (55, 2, 2, 'lolo', '2021-05-06 10:40:42.812268');
INSERT INTO public.message VALUES (56, 2, 2, 'hghg', '2021-05-06 10:49:29.105618');
INSERT INTO public.message VALUES (57, 2, 1, 'nnn', '2021-05-06 11:00:39.169442');
INSERT INTO public.message VALUES (58, 2, 1, 'vvv', '2021-05-06 11:01:29.297582');
INSERT INTO public.message VALUES (59, 2, 1, 'ghgh', '2021-05-06 11:02:02.680298');
INSERT INTO public.message VALUES (60, 2, 2, 'nbnb', '2021-05-06 11:05:56.613438');
INSERT INTO public.message VALUES (61, 2, 1, 'hjhj', '2021-05-06 11:07:39.075947');
INSERT INTO public.message VALUES (62, 2, 1, 'erer', '2021-05-06 13:48:03.620323');
INSERT INTO public.message VALUES (63, 2, 2, 'thth', '2021-05-06 15:41:48.831048');
INSERT INTO public.message VALUES (64, 2, 2, 'jhjh', '2021-05-06 15:59:40.86259');
INSERT INTO public.message VALUES (65, 2, 2, 'khkhk', '2021-05-06 15:59:46.776444');
INSERT INTO public.message VALUES (66, 1, 3, 'nmnmn', '2021-05-06 16:01:54.940286');
INSERT INTO public.message VALUES (67, 1, 3, 'ffff', '2021-05-06 16:01:59.372265');
INSERT INTO public.message VALUES (68, 2, 1, 'bvbv', '2021-05-06 16:02:11.167347');
INSERT INTO public.message VALUES (69, 1, 3, 'bbblll', '2021-05-07 08:09:53.897837');
INSERT INTO public.message VALUES (70, 2, 1, 'rtrt', '2021-05-07 08:10:07.185756');
INSERT INTO public.message VALUES (71, 2, 1, 'hghg', '2021-05-07 08:10:12.625133');
INSERT INTO public.message VALUES (102, 2, 1, 'vbvbv', '2021-05-07 09:20:04.955672');
INSERT INTO public.message VALUES (103, 2, 1, 'nnn', '2021-05-07 09:20:09.826981');
INSERT INTO public.message VALUES (104, 1, 3, 'wewe', '2021-05-07 09:20:17.875666');
INSERT INTO public.message VALUES (105, 1, 3, 'hghg', '2021-05-07 11:02:19.15187');
INSERT INTO public.message VALUES (106, 2, 1, 'jkjk', '2021-05-07 11:08:34.774258');
INSERT INTO public.message VALUES (107, 2, 1, 'lll', '2021-05-07 11:08:39.237737');
INSERT INTO public.message VALUES (108, 1, 3, 'ggg', '2021-05-07 11:08:46.582981');
INSERT INTO public.message VALUES (109, 1, 3, 'ss', '2021-05-07 11:09:11.934372');
INSERT INTO public.message VALUES (110, 1, 3, 'rrrr', '2021-05-07 11:09:52.614822');
INSERT INTO public.message VALUES (111, 2, 1, 'sss', '2021-05-07 14:21:03.346479');
INSERT INTO public.message VALUES (112, 2, 1, 'vbvb', '2021-05-07 15:19:42.067679');
INSERT INTO public.message VALUES (113, 2, 1, 'ghgh', '2021-05-07 15:19:50.069176');
INSERT INTO public.message VALUES (114, 1, 3, 'kklkl', '2021-05-07 15:22:22.113598');
INSERT INTO public.message VALUES (115, 1, 3, 'mnmnm', '2021-05-07 15:22:25.357307');
INSERT INTO public.message VALUES (116, 1, 3, 'mnmn', '2021-05-07 15:32:06.271483');
INSERT INTO public.message VALUES (117, 1, 3, 'nbnb', '2021-05-07 15:33:18.309147');
INSERT INTO public.message VALUES (118, 2, 1, 'xxx', '2021-05-10 10:09:11.798431');
INSERT INTO public.message VALUES (119, 2, 1, 'cc', '2021-05-10 10:09:12.611412');
INSERT INTO public.message VALUES (120, 2, 2, 'klkl', '2021-05-10 10:54:20.962796');
INSERT INTO public.message VALUES (121, 2, 2, 'jkjk', '2021-05-10 10:54:33.671592');
INSERT INTO public.message VALUES (122, 2, 2, 'popo', '2021-05-10 10:54:49.670238');
INSERT INTO public.message VALUES (123, 2, 2, 'jkjk', '2021-05-10 11:36:42.958081');
INSERT INTO public.message VALUES (124, 2, 2, 'nbnb', '2021-05-11 08:10:56.097718');
INSERT INTO public.message VALUES (125, 2, 1, 'hjhj', '2021-05-11 08:12:43.331131');
INSERT INTO public.message VALUES (126, 2, 1, 'dddd', '2021-05-11 08:12:51.332451');
INSERT INTO public.message VALUES (127, 2, 1, 'gfgf', '2021-05-11 08:27:24.16106');
INSERT INTO public.message VALUES (128, 1, 3, 'gffg', '2021-05-11 08:40:03.557812');
INSERT INTO public.message VALUES (129, 1, 3, 'nbnb', '2021-05-11 11:07:53.591536');
INSERT INTO public.message VALUES (130, 2, 1, 'hkhk', '2021-05-11 11:20:35.022518');
INSERT INTO public.message VALUES (131, 2, 1, 'ddd', '2021-05-11 11:20:43.024844');
INSERT INTO public.message VALUES (132, 2, 1, 'dddd', '2021-05-12 07:51:02.700137');
INSERT INTO public.message VALUES (133, 2, 1, 'mnmn', '2021-05-12 07:51:05.436655');
INSERT INTO public.message VALUES (134, 2, 1, 'hjhj', '2021-05-12 10:28:02.568288');
INSERT INTO public.message VALUES (135, 2, 1, 'ghgh', '2021-05-12 10:31:30.63666');
INSERT INTO public.message VALUES (136, 2, 1, 'rtrttr', '2021-05-12 13:22:29.540789');
INSERT INTO public.message VALUES (137, 2, 2, 'lkkl', '2021-05-12 13:22:37.543408');
INSERT INTO public.message VALUES (138, 2, 2, 'hjhj', '2021-05-12 13:22:49.365347');
INSERT INTO public.message VALUES (139, 2, 2, 'ghghgh', '2021-05-12 13:23:13.375826');
INSERT INTO public.message VALUES (140, 2, 2, 'jkjk', '2021-05-12 13:27:42.575721');
INSERT INTO public.message VALUES (141, 2, 2, 'jkjk', '2021-05-12 13:29:59.910606');
INSERT INTO public.message VALUES (142, 2, 2, 'jkjkll', '2021-05-12 13:30:15.918301');
INSERT INTO public.message VALUES (143, 2, 2, 'pppp', '2021-05-12 13:31:03.933722');
INSERT INTO public.message VALUES (144, 2, 2, 'jjjj', '2021-05-12 13:32:09.294829');
INSERT INTO public.message VALUES (145, 2, 2, 'ghghgh', '2021-05-12 13:33:14.916103');
INSERT INTO public.message VALUES (146, 2, 2, 'gggg', '2021-05-12 13:36:47.814255');
INSERT INTO public.message VALUES (147, 2, 2, 'klkllk', '2021-05-12 13:36:55.816432');
INSERT INTO public.message VALUES (148, 2, 2, 'iiii', '2021-05-12 13:38:14.149665');
INSERT INTO public.message VALUES (149, 2, 2, 'rtrtr', '2021-05-12 13:40:35.91906');
INSERT INTO public.message VALUES (150, 2, 2, 'ttt', '2021-05-12 13:41:34.478955');
INSERT INTO public.message VALUES (151, 2, 2, 'yyyy', '2021-05-12 13:41:51.909704');
INSERT INTO public.message VALUES (152, 2, 2, 'lklk', '2021-05-12 13:46:41.219655');
INSERT INTO public.message VALUES (153, 2, 2, 'lklkl', '2021-05-12 13:57:09.433073');
INSERT INTO public.message VALUES (154, 2, 1, 'yuyuu', '2021-05-12 13:59:58.929596');
INSERT INTO public.message VALUES (155, 2, 1, 'ioio', '2021-05-12 14:00:05.790675');
INSERT INTO public.message VALUES (156, 2, 1, 'ptpt', '2021-05-12 14:00:06.932576');
INSERT INTO public.message VALUES (157, 1, 3, 'ioio', '2021-05-12 14:00:09.833808');
INSERT INTO public.message VALUES (158, 2, 1, 'hjhj', '2021-05-12 14:06:06.025671');
INSERT INTO public.message VALUES (159, 2, 1, 'eeee', '2021-05-12 14:06:22.03229');
INSERT INTO public.message VALUES (160, 2, 1, 'jkjkj', '2021-05-12 14:07:04.912819');
INSERT INTO public.message VALUES (161, 2, 1, 'llll', '2021-05-12 14:07:45.515056');
INSERT INTO public.message VALUES (162, 1, 3, 'lkklkl', '2021-05-12 14:08:54.695738');
INSERT INTO public.message VALUES (163, 2, 1, 'www', '2021-05-12 14:09:23.403916');
INSERT INTO public.message VALUES (164, 2, 1, 'ghghg', '2021-05-12 14:22:33.70993');
INSERT INTO public.message VALUES (165, 1, 3, 'llll', '2021-05-12 14:22:43.716401');
INSERT INTO public.message VALUES (166, 1, 3, 'oo', '2021-05-12 14:22:50.025677');
INSERT INTO public.message VALUES (167, 1, 3, 'yy', '2021-05-12 14:22:53.723447');
INSERT INTO public.message VALUES (168, 1, 3, 'jkjk', '2021-05-12 14:23:43.420461');
INSERT INTO public.message VALUES (169, 1, 3, 'lkkl', '2021-05-12 14:23:54.074902');
INSERT INTO public.message VALUES (170, 3, 3, 'fffff', '2021-05-18 13:13:56.116627');
INSERT INTO public.message VALUES (171, 3, 4, 'kjkjk', '2021-05-18 13:14:08.282399');
INSERT INTO public.message VALUES (172, 3, 3, 'jkjk', '2021-05-18 13:15:31.148118');
INSERT INTO public.message VALUES (173, 3, 4, 'jkjkj', '2021-05-18 13:15:36.150339');
INSERT INTO public.message VALUES (174, 3, 3, 'fffff', '2021-05-18 13:16:45.056259');
INSERT INTO public.message VALUES (175, 3, 4, 'kljh', '2021-05-18 13:17:01.413728');
INSERT INTO public.message VALUES (176, 3, 3, 'fffff', '2021-05-18 13:17:24.370265');
INSERT INTO public.message VALUES (177, 3, 4, 'kkk', '2021-05-18 13:17:34.371605');
INSERT INTO public.message VALUES (178, 3, 3, 'qqq', '2021-05-18 13:17:54.378724');
INSERT INTO public.message VALUES (179, 3, 4, 'yuyu', '2021-05-18 13:17:56.198184');
INSERT INTO public.message VALUES (180, 3, 3, 'qa', '2021-05-18 13:18:49.397445');
INSERT INTO public.message VALUES (181, 3, 3, 'rtrt', '2021-05-18 13:18:56.228408');
INSERT INTO public.message VALUES (182, 3, 4, 'jjj', '2021-05-18 13:36:36.652812');
INSERT INTO public.message VALUES (183, 3, 4, 'www', '2021-05-18 13:37:07.992326');
INSERT INTO public.message VALUES (184, 3, 4, 'ooo', '2021-05-18 13:37:11.66656');
INSERT INTO public.message VALUES (185, 3, 4, 'nbjkfjbknpfnpbknnbjnbngkbnnbnbntbnpbninbinbitnitnbinti', '2021-05-18 13:37:36.676908');
INSERT INTO public.message VALUES (186, 3, 3, 'gfgfgfg', '2021-05-18 13:43:36.559421');
INSERT INTO public.message VALUES (187, 3, 4, 'ghhghgh', '2021-05-18 13:44:15.270553');
INSERT INTO public.message VALUES (188, 3, 4, 'ooo', '2021-05-18 13:44:25.273321');
INSERT INTO public.message VALUES (189, 3, 4, 'kkmjkmh', '2021-05-19 08:41:13.706778');
INSERT INTO public.message VALUES (190, 3, 4, 'khkhjk', '2021-05-19 08:41:43.71718');
INSERT INTO public.message VALUES (191, 3, 4, 'hjhj', '2021-05-19 09:10:59.114521');
INSERT INTO public.message VALUES (192, 3, 4, 'kiki', '2021-05-19 09:11:43.877208');
INSERT INTO public.message VALUES (193, 3, 4, 'hjhjhj', '2021-05-19 09:31:20.610779');
INSERT INTO public.message VALUES (194, 3, 4, 'jkjkjk', '2021-05-19 09:37:06.76296');
INSERT INTO public.message VALUES (195, 3, 4, 'ioioi', '2021-05-19 09:37:47.36791');
INSERT INTO public.message VALUES (196, 3, 4, 'klkllk', '2021-05-19 09:38:16.102976');


--
-- Data for Name: notification; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.notification VALUES (2, 2, 1, 'Message', true, '2021-05-05 14:46:03.091857');
INSERT INTO public.notification VALUES (32, 2, 1, 'Message', true, '2021-05-06 11:07:06.585404');
INSERT INTO public.notification VALUES (34, 1, 2, 'Message', true, '2021-05-06 13:48:22.449024');
INSERT INTO public.notification VALUES (1, 2, 1, 'Message', true, '2021-05-05 14:44:28.410349');
INSERT INTO public.notification VALUES (3, 2, 1, 'Message', true, '2021-05-06 08:01:50.255995');
INSERT INTO public.notification VALUES (6, 2, 1, 'Message', true, '2021-05-06 08:08:40.09372');
INSERT INTO public.notification VALUES (7, 2, 1, 'Message', true, '2021-05-06 08:17:00.17215');
INSERT INTO public.notification VALUES (8, 2, 1, 'Message', true, '2021-05-06 08:23:01.699244');
INSERT INTO public.notification VALUES (10, 2, 1, 'Message', true, '2021-05-06 08:31:22.217617');
INSERT INTO public.notification VALUES (11, 2, 1, 'Message', true, '2021-05-06 08:32:39.77762');
INSERT INTO public.notification VALUES (14, 2, 1, 'Message', true, '2021-05-06 09:20:41.06749');
INSERT INTO public.notification VALUES (16, 2, 1, 'Message', true, '2021-05-06 09:23:14.754864');
INSERT INTO public.notification VALUES (17, 2, 1, 'Message', true, '2021-05-06 09:25:13.562852');
INSERT INTO public.notification VALUES (18, 2, 1, 'Message', true, '2021-05-06 09:27:46.306232');
INSERT INTO public.notification VALUES (19, 2, 1, 'Message', true, '2021-05-06 09:40:22.462472');
INSERT INTO public.notification VALUES (20, 2, 1, 'Message', true, '2021-05-06 09:50:24.324681');
INSERT INTO public.notification VALUES (23, 2, 1, 'Message', true, '2021-05-06 09:55:21.733638');
INSERT INTO public.notification VALUES (24, 2, 1, 'Message', true, '2021-05-06 10:03:36.635343');
INSERT INTO public.notification VALUES (25, 2, 1, 'Message', true, '2021-05-06 10:06:45.673717');
INSERT INTO public.notification VALUES (27, 2, 1, 'Message', true, '2021-05-06 10:41:11.486048');
INSERT INTO public.notification VALUES (28, 2, 1, 'Message', true, '2021-05-06 10:49:44.509252');
INSERT INTO public.notification VALUES (4, 1, 2, 'Message', true, '2021-05-06 08:04:08.110746');
INSERT INTO public.notification VALUES (5, 1, 2, 'Message', true, '2021-05-06 08:06:56.54163');
INSERT INTO public.notification VALUES (9, 1, 2, 'Message', true, '2021-05-06 08:30:49.074552');
INSERT INTO public.notification VALUES (12, 1, 2, 'Message', true, '2021-05-06 08:33:03.288757');
INSERT INTO public.notification VALUES (13, 1, 2, 'Message', true, '2021-05-06 09:15:51.530123');
INSERT INTO public.notification VALUES (15, 1, 2, 'Message', true, '2021-05-06 09:21:36.275452');
INSERT INTO public.notification VALUES (21, 1, 2, 'Message', true, '2021-05-06 09:50:51.711162');
INSERT INTO public.notification VALUES (22, 1, 2, 'Message', true, '2021-05-06 09:51:21.446677');
INSERT INTO public.notification VALUES (26, 1, 2, 'Message', true, '2021-05-06 10:39:09.596471');
INSERT INTO public.notification VALUES (29, 1, 2, 'Message', true, '2021-05-06 11:00:57.090854');
INSERT INTO public.notification VALUES (30, 1, 2, 'Message', true, '2021-05-06 11:01:42.370141');
INSERT INTO public.notification VALUES (31, 1, 2, 'Message', true, '2021-05-06 11:02:11.673452');
INSERT INTO public.notification VALUES (33, 1, 2, 'Message', true, '2021-05-06 11:07:46.736578');
INSERT INTO public.notification VALUES (35, 2, 1, 'Message', true, '2021-05-06 15:41:48.847409');
INSERT INTO public.notification VALUES (36, 2, 1, 'Message', true, '2021-05-06 15:59:40.876638');
INSERT INTO public.notification VALUES (37, 2, 1, 'Message', true, '2021-05-06 16:00:19.52623');
INSERT INTO public.notification VALUES (38, 3, 2, 'Message', true, '2021-05-06 16:01:54.941933');
INSERT INTO public.notification VALUES (39, 3, 2, 'Message', true, '2021-05-06 16:01:59.37434');
INSERT INTO public.notification VALUES (40, 1, 2, 'Message', true, '2021-05-06 16:02:19.542697');
INSERT INTO public.notification VALUES (42, 1, 2, 'Message', true, '2021-05-07 08:10:07.192556');
INSERT INTO public.notification VALUES (43, 1, 2, 'Message', true, '2021-05-07 08:10:12.627453');
INSERT INTO public.notification VALUES (41, 3, 2, 'Message', true, '2021-05-07 08:09:53.918429');
INSERT INTO public.notification VALUES (74, 1, 2, 'Message', true, '2021-05-07 09:20:04.984613');
INSERT INTO public.notification VALUES (75, 1, 2, 'Message', true, '2021-05-07 09:20:09.830614');
INSERT INTO public.notification VALUES (76, 3, 2, 'Message', true, '2021-05-07 09:20:17.877384');
INSERT INTO public.notification VALUES (77, 3, 2, 'Message', true, '2021-05-07 11:02:26.682611');
INSERT INTO public.notification VALUES (80, 3, 2, 'Message', true, '2021-05-07 11:08:46.584657');
INSERT INTO public.notification VALUES (81, 3, 2, 'Message', true, '2021-05-07 11:09:11.935972');
INSERT INTO public.notification VALUES (78, 1, 2, 'Message', true, '2021-05-07 11:08:34.776927');
INSERT INTO public.notification VALUES (79, 1, 2, 'Message', true, '2021-05-07 11:08:39.239826');
INSERT INTO public.notification VALUES (83, 1, 2, 'Message', true, '2021-05-07 14:21:03.363525');
INSERT INTO public.notification VALUES (84, 1, 2, 'Message', true, '2021-05-07 15:19:46.563333');
INSERT INTO public.notification VALUES (85, 1, 2, 'Message', true, '2021-05-07 15:20:18.33288');
INSERT INTO public.notification VALUES (82, 3, 2, 'Message', true, '2021-05-07 11:09:59.754027');
INSERT INTO public.notification VALUES (86, 3, 2, 'Message', true, '2021-05-07 15:22:25.053222');
INSERT INTO public.notification VALUES (87, 3, 2, 'Message', true, '2021-05-07 15:24:48.860231');
INSERT INTO public.notification VALUES (88, 3, 2, 'Message', true, '2021-05-07 15:32:17.412811');
INSERT INTO public.notification VALUES (89, 3, 2, 'Message', true, '2021-05-07 15:33:35.20357');
INSERT INTO public.notification VALUES (90, 1, 2, 'Message', true, '2021-05-10 10:09:11.815889');
INSERT INTO public.notification VALUES (91, 1, 2, 'Message', true, '2021-05-10 10:09:35.944125');
INSERT INTO public.notification VALUES (92, 2, 1, 'Message', true, '2021-05-10 10:54:29.129375');
INSERT INTO public.notification VALUES (93, 2, 1, 'Message', true, '2021-05-10 10:54:48.955018');
INSERT INTO public.notification VALUES (94, 2, 1, 'Message', true, '2021-05-10 10:56:03.258804');
INSERT INTO public.notification VALUES (95, 2, 1, 'Message', true, '2021-05-10 11:36:46.949217');
INSERT INTO public.notification VALUES (96, 2, 1, 'Message', true, '2021-05-11 08:11:03.909228');
INSERT INTO public.notification VALUES (97, 1, 2, 'Message', true, '2021-05-11 08:12:48.725711');
INSERT INTO public.notification VALUES (100, 3, 2, 'Message', true, '2021-05-11 08:40:07.927643');
INSERT INTO public.notification VALUES (101, 3, 2, 'Message', true, '2021-05-11 11:07:57.41967');
INSERT INTO public.notification VALUES (98, 1, 2, 'Message', true, '2021-05-11 08:13:03.08536');
INSERT INTO public.notification VALUES (99, 1, 2, 'Message', true, '2021-05-11 08:31:42.260336');
INSERT INTO public.notification VALUES (102, 1, 2, 'Message', true, '2021-05-11 11:20:41.201332');
INSERT INTO public.notification VALUES (103, 1, 2, 'Message', true, '2021-05-11 11:21:44.032195');
INSERT INTO public.notification VALUES (104, 1, 2, 'Message', true, '2021-05-12 07:51:05.307544');
INSERT INTO public.notification VALUES (105, 1, 2, 'Message', true, '2021-05-12 08:02:35.873278');
INSERT INTO public.notification VALUES (106, 1, 2, 'Message', true, '2021-05-12 10:28:06.909435');
INSERT INTO public.notification VALUES (107, 1, 2, 'Message', true, '2021-05-12 10:31:57.898477');
INSERT INTO public.notification VALUES (108, 1, 2, 'Message', true, '2021-05-12 13:22:35.926142');
INSERT INTO public.notification VALUES (109, 2, 1, 'Message', true, '2021-05-12 13:22:46.470982');
INSERT INTO public.notification VALUES (110, 2, 1, 'Message', true, '2021-05-12 13:23:00.998343');
INSERT INTO public.notification VALUES (111, 2, 1, 'Message', true, '2021-05-12 13:26:16.045987');
INSERT INTO public.notification VALUES (112, 2, 1, 'Message', true, '2021-05-12 13:29:07.648174');
INSERT INTO public.notification VALUES (113, 2, 1, 'Message', true, '2021-05-12 13:30:03.285665');
INSERT INTO public.notification VALUES (114, 2, 1, 'Message', true, '2021-05-12 13:31:02.662917');
INSERT INTO public.notification VALUES (115, 2, 1, 'Message', true, '2021-05-12 13:31:43.389749');
INSERT INTO public.notification VALUES (116, 2, 1, 'Message', true, '2021-05-12 13:32:28.501099');
INSERT INTO public.notification VALUES (117, 2, 1, 'Message', true, '2021-05-12 13:35:23.773225');
INSERT INTO public.notification VALUES (118, 2, 1, 'Message', true, '2021-05-12 13:36:49.052589');
INSERT INTO public.notification VALUES (119, 2, 1, 'Message', true, '2021-05-12 13:38:04.180034');
INSERT INTO public.notification VALUES (120, 2, 1, 'Message', true, '2021-05-12 13:39:46.771548');
INSERT INTO public.notification VALUES (121, 2, 1, 'Message', true, '2021-05-12 13:41:31.115747');
INSERT INTO public.notification VALUES (122, 2, 1, 'Message', true, '2021-05-12 13:41:44.852936');
INSERT INTO public.notification VALUES (123, 2, 1, 'Message', true, '2021-05-12 13:43:25.01949');
INSERT INTO public.notification VALUES (124, 2, 1, 'Message', true, '2021-05-12 13:48:45.387464');
INSERT INTO public.notification VALUES (125, 2, 1, 'Message', true, '2021-05-12 13:57:17.881555');
INSERT INTO public.notification VALUES (129, 3, 2, 'Message', true, '2021-05-12 14:00:27.080248');
INSERT INTO public.notification VALUES (126, 1, 2, 'Message', true, '2021-05-12 14:00:03.601513');
INSERT INTO public.notification VALUES (127, 1, 2, 'Message', true, '2021-05-12 14:00:05.793382');
INSERT INTO public.notification VALUES (128, 1, 2, 'Message', true, '2021-05-12 14:00:07.632185');
INSERT INTO public.notification VALUES (130, 1, 2, 'Message', true, '2021-05-12 14:06:13.216679');
INSERT INTO public.notification VALUES (131, 1, 2, 'Message', true, '2021-05-12 14:06:43.838983');
INSERT INTO public.notification VALUES (132, 1, 2, 'Message', true, '2021-05-12 14:07:44.351035');
INSERT INTO public.notification VALUES (133, 1, 2, 'Message', true, '2021-05-12 14:07:57.382669');
INSERT INTO public.notification VALUES (134, 3, 2, 'Message', true, '2021-05-12 14:09:02.095512');
INSERT INTO public.notification VALUES (135, 1, 2, 'Message', true, '2021-05-12 14:09:26.870762');
INSERT INTO public.notification VALUES (136, 1, 2, 'Message', true, '2021-05-12 14:22:40.880747');
INSERT INTO public.notification VALUES (137, 3, 2, 'Message', true, '2021-05-12 14:22:49.189862');
INSERT INTO public.notification VALUES (138, 3, 2, 'Message', true, '2021-05-12 14:22:51.189406');
INSERT INTO public.notification VALUES (139, 3, 2, 'Message', true, '2021-05-12 14:23:08.917252');
INSERT INTO public.notification VALUES (140, 3, 2, 'Message', true, '2021-05-12 14:23:47.337393');
INSERT INTO public.notification VALUES (141, 3, 2, 'Message', true, '2021-05-12 14:24:16.077394');
INSERT INTO public.notification VALUES (142, 2, 10, 'Visit', false, '2021-05-17 11:05:57.147959');
INSERT INTO public.notification VALUES (143, 2, 5, 'Visit', false, '2021-05-17 11:06:14.772374');
INSERT INTO public.notification VALUES (144, 2, 4, 'Visit', false, '2021-05-17 11:06:18.630573');
INSERT INTO public.notification VALUES (145, 2, 4, 'Visit', false, '2021-05-17 11:42:04.169931');
INSERT INTO public.notification VALUES (146, 2, 4, 'Visit', false, '2021-05-17 11:42:51.780718');
INSERT INTO public.notification VALUES (147, 2, 4, 'Like', false, '2021-05-17 11:42:51.785489');
INSERT INTO public.notification VALUES (148, 2, 4, 'Visit', false, '2021-05-17 11:44:08.133183');
INSERT INTO public.notification VALUES (149, 2, 4, 'Visit', false, '2021-05-17 13:22:33.40242');
INSERT INTO public.notification VALUES (150, 2, 4, 'Visit', false, '2021-05-17 13:24:43.14985');
INSERT INTO public.notification VALUES (151, 2, 4, 'Visit', false, '2021-05-17 13:26:34.045245');
INSERT INTO public.notification VALUES (152, 2, 4, 'Visit', false, '2021-05-17 13:26:39.653969');
INSERT INTO public.notification VALUES (153, 2, 4, 'Dislike', false, '2021-05-17 13:26:39.658846');
INSERT INTO public.notification VALUES (154, 2, 4, 'Visit', false, '2021-05-17 13:27:19.909215');
INSERT INTO public.notification VALUES (155, 2, 4, 'Like', false, '2021-05-17 13:27:19.913316');
INSERT INTO public.notification VALUES (156, 2, 4, 'Visit', false, '2021-05-17 13:29:49.509769');
INSERT INTO public.notification VALUES (157, 2, 4, 'Dislike', false, '2021-05-17 13:29:49.514048');
INSERT INTO public.notification VALUES (158, 2, 4, 'Visit', false, '2021-05-17 13:30:04.458723');
INSERT INTO public.notification VALUES (159, 2, 4, 'Like', false, '2021-05-17 13:30:04.461403');
INSERT INTO public.notification VALUES (160, 2, 4, 'Visit', false, '2021-05-17 14:49:17.743439');
INSERT INTO public.notification VALUES (161, 2, 4, 'Visit', false, '2021-05-17 14:49:21.361275');
INSERT INTO public.notification VALUES (162, 2, 4, 'Dislike', false, '2021-05-17 14:49:21.365067');
INSERT INTO public.notification VALUES (163, 2, 4, 'Visit', false, '2021-05-17 14:53:11.984715');
INSERT INTO public.notification VALUES (164, 2, 4, 'Like', false, '2021-05-17 14:53:11.992058');
INSERT INTO public.notification VALUES (165, 2, 4, 'Visit', false, '2021-05-17 14:55:56.10207');
INSERT INTO public.notification VALUES (166, 1, 2, 'Visit', false, '2021-05-18 08:01:40.280915');
INSERT INTO public.notification VALUES (167, 3, 4, 'Visit', false, '2021-05-18 08:26:04.080644');
INSERT INTO public.notification VALUES (168, 2, 5, 'Visit', false, '2021-05-18 10:10:55.434511');
INSERT INTO public.notification VALUES (169, 2, 5, 'Visit', false, '2021-05-18 10:11:46.758699');
INSERT INTO public.notification VALUES (170, 2, 4, 'Visit', false, '2021-05-18 10:12:39.168427');
INSERT INTO public.notification VALUES (171, 2, 4, 'Visit', false, '2021-05-18 10:12:44.164408');
INSERT INTO public.notification VALUES (172, 2, 4, 'Dislike', false, '2021-05-18 10:12:44.170316');
INSERT INTO public.notification VALUES (173, 2, 4, 'Visit', false, '2021-05-18 10:12:49.432251');
INSERT INTO public.notification VALUES (174, 2, 4, 'Like', false, '2021-05-18 10:12:49.435747');
INSERT INTO public.notification VALUES (175, 2, 4, 'Visit', false, '2021-05-18 10:14:17.244122');
INSERT INTO public.notification VALUES (176, 2, 4, 'Dislike', false, '2021-05-18 10:14:17.247838');
INSERT INTO public.notification VALUES (177, 2, 4, 'Visit', false, '2021-05-18 10:14:28.866908');
INSERT INTO public.notification VALUES (178, 2, 4, 'Like', false, '2021-05-18 10:14:28.870083');
INSERT INTO public.notification VALUES (179, 2, 4, 'Visit', false, '2021-05-18 10:15:25.635655');
INSERT INTO public.notification VALUES (180, 2, 4, 'Dislike', false, '2021-05-18 10:15:25.641499');
INSERT INTO public.notification VALUES (181, 2, 4, 'Visit', false, '2021-05-18 10:15:34.254315');
INSERT INTO public.notification VALUES (182, 2, 4, 'Like', false, '2021-05-18 10:15:34.257064');
INSERT INTO public.notification VALUES (183, 4, 3, 'Visit', false, '2021-05-18 10:19:33.530498');
INSERT INTO public.notification VALUES (184, 4, 3, 'Visit', false, '2021-05-18 10:30:17.610817');
INSERT INTO public.notification VALUES (185, 3, 4, 'Visit', false, '2021-05-18 11:08:58.713762');
INSERT INTO public.notification VALUES (186, 3, 4, 'Visit', false, '2021-05-18 11:09:53.431756');
INSERT INTO public.notification VALUES (187, 3, 4, 'Like', false, '2021-05-18 11:09:53.43467');
INSERT INTO public.notification VALUES (188, 3, 4, 'Visit', false, '2021-05-18 11:09:57.360118');
INSERT INTO public.notification VALUES (189, 4, 3, 'Visit', false, '2021-05-18 11:12:25.228259');
INSERT INTO public.notification VALUES (190, 4, 3, 'Visit', false, '2021-05-18 11:12:37.039803');
INSERT INTO public.notification VALUES (191, 4, 3, 'Like', false, '2021-05-18 11:12:37.042791');
INSERT INTO public.notification VALUES (192, 3, 4, 'Visit', false, '2021-05-18 11:22:16.711721');
INSERT INTO public.notification VALUES (193, 3, 4, 'Dislike', false, '2021-05-18 11:22:16.717525');
INSERT INTO public.notification VALUES (194, 3, 4, 'Visit', false, '2021-05-18 11:22:25.526862');
INSERT INTO public.notification VALUES (195, 3, 4, 'Like', false, '2021-05-18 11:22:25.531084');
INSERT INTO public.notification VALUES (196, 3, 4, 'Visit', false, '2021-05-18 11:23:06.117724');
INSERT INTO public.notification VALUES (197, 3, 4, 'Visit', false, '2021-05-18 11:24:03.136506');
INSERT INTO public.notification VALUES (198, 3, 4, 'Visit', false, '2021-05-18 11:24:09.189924');
INSERT INTO public.notification VALUES (199, 3, 4, 'Dislike', false, '2021-05-18 11:24:09.193492');
INSERT INTO public.notification VALUES (200, 3, 4, 'Visit', false, '2021-05-18 11:24:18.973488');
INSERT INTO public.notification VALUES (201, 3, 4, 'Like', false, '2021-05-18 11:24:18.975971');
INSERT INTO public.notification VALUES (202, 3, 4, 'Visit', false, '2021-05-18 11:24:31.603015');
INSERT INTO public.notification VALUES (203, 3, 4, 'Visit', false, '2021-05-18 11:24:37.638075');
INSERT INTO public.notification VALUES (204, 3, 4, 'Dislike', false, '2021-05-18 11:24:37.642577');
INSERT INTO public.notification VALUES (205, 3, 4, 'Visit', false, '2021-05-18 11:25:30.406676');
INSERT INTO public.notification VALUES (206, 3, 4, 'Like', false, '2021-05-18 11:25:30.409209');
INSERT INTO public.notification VALUES (207, 3, 4, 'Visit', false, '2021-05-18 11:26:18.094237');
INSERT INTO public.notification VALUES (208, 3, 4, 'Visit', false, '2021-05-18 11:26:24.554979');
INSERT INTO public.notification VALUES (209, 3, 4, 'Visit', false, '2021-05-18 11:31:41.150814');
INSERT INTO public.notification VALUES (210, 3, 4, 'Dislike', false, '2021-05-18 11:31:41.154963');
INSERT INTO public.notification VALUES (211, 3, 4, 'Visit', false, '2021-05-18 11:31:51.939583');
INSERT INTO public.notification VALUES (212, 3, 4, 'Like', false, '2021-05-18 11:31:51.943179');
INSERT INTO public.notification VALUES (213, 3, 4, 'Visit', false, '2021-05-18 11:33:18.113525');
INSERT INTO public.notification VALUES (214, 3, 4, 'Visit', false, '2021-05-18 11:33:28.030835');
INSERT INTO public.notification VALUES (215, 3, 4, 'Dislike', false, '2021-05-18 11:33:28.036567');
INSERT INTO public.notification VALUES (216, 3, 4, 'Visit', false, '2021-05-18 11:33:31.634831');
INSERT INTO public.notification VALUES (217, 3, 4, 'Like', false, '2021-05-18 11:33:31.637776');
INSERT INTO public.notification VALUES (218, 3, 4, 'Visit', false, '2021-05-18 11:35:48.959496');
INSERT INTO public.notification VALUES (219, 3, 4, 'Visit', false, '2021-05-18 11:35:56.747956');
INSERT INTO public.notification VALUES (220, 3, 4, 'Visit', false, '2021-05-18 11:36:26.764317');
INSERT INTO public.notification VALUES (221, 3, 4, 'Dislike', false, '2021-05-18 11:36:26.767812');
INSERT INTO public.notification VALUES (222, 3, 4, 'Visit', false, '2021-05-18 11:36:30.067182');
INSERT INTO public.notification VALUES (223, 3, 4, 'Like', false, '2021-05-18 11:36:30.069916');
INSERT INTO public.notification VALUES (224, 4, 3, 'Visit', false, '2021-05-18 11:39:38.694414');
INSERT INTO public.notification VALUES (225, 4, 3, 'Visit', false, '2021-05-18 11:42:31.898646');
INSERT INTO public.notification VALUES (226, 4, 3, 'Dislike', false, '2021-05-18 11:42:31.902702');
INSERT INTO public.notification VALUES (227, 4, 3, 'Visit', false, '2021-05-18 11:42:34.977143');
INSERT INTO public.notification VALUES (228, 4, 3, 'Like', false, '2021-05-18 11:42:34.980239');
INSERT INTO public.notification VALUES (229, 4, 3, 'Visit', false, '2021-05-18 12:39:34.507424');
INSERT INTO public.notification VALUES (230, 4, 3, 'Visit', false, '2021-05-18 12:39:39.536772');
INSERT INTO public.notification VALUES (231, 4, 3, 'Dislike', false, '2021-05-18 12:39:39.5396');
INSERT INTO public.notification VALUES (232, 4, 3, 'Visit', false, '2021-05-18 12:40:10.471961');
INSERT INTO public.notification VALUES (233, 4, 3, 'Like', false, '2021-05-18 12:40:10.477828');
INSERT INTO public.notification VALUES (234, 4, 3, 'Visit', false, '2021-05-18 12:42:38.281928');
INSERT INTO public.notification VALUES (235, 4, 3, 'Visit', false, '2021-05-18 12:43:25.5278');
INSERT INTO public.notification VALUES (236, 4, 3, 'Dislike', false, '2021-05-18 12:43:25.532706');
INSERT INTO public.notification VALUES (237, 4, 3, 'Visit', false, '2021-05-18 12:43:30.332763');
INSERT INTO public.notification VALUES (238, 4, 3, 'Like', false, '2021-05-18 12:43:30.334992');
INSERT INTO public.notification VALUES (239, 4, 3, 'Visit', false, '2021-05-18 12:44:13.454945');
INSERT INTO public.notification VALUES (240, 4, 3, 'Visit', false, '2021-05-18 12:50:26.898682');
INSERT INTO public.notification VALUES (241, 4, 3, 'Visit', false, '2021-05-18 12:50:34.807711');
INSERT INTO public.notification VALUES (242, 4, 3, 'Dislike', false, '2021-05-18 12:50:34.810864');
INSERT INTO public.notification VALUES (243, 4, 3, 'Visit', false, '2021-05-18 12:50:37.999275');
INSERT INTO public.notification VALUES (244, 4, 3, 'Like', false, '2021-05-18 12:50:38.002821');
INSERT INTO public.notification VALUES (245, 4, 3, 'Visit', false, '2021-05-18 12:51:24.634517');
INSERT INTO public.notification VALUES (246, 4, 3, 'Visit', false, '2021-05-18 12:51:28.654652');
INSERT INTO public.notification VALUES (247, 4, 3, 'Dislike', false, '2021-05-18 12:51:28.657059');
INSERT INTO public.notification VALUES (248, 4, 3, 'Visit', false, '2021-05-18 12:51:32.447159');
INSERT INTO public.notification VALUES (249, 4, 3, 'Like', false, '2021-05-18 12:51:32.449724');
INSERT INTO public.notification VALUES (250, 3, 4, 'Message', true, '2021-05-18 13:14:01.098525');
INSERT INTO public.notification VALUES (251, 4, 3, 'Message', true, '2021-05-18 13:14:14.260118');
INSERT INTO public.notification VALUES (253, 4, 3, 'Message', true, '2021-05-18 13:15:48.059731');
INSERT INTO public.notification VALUES (252, 3, 4, 'Message', true, '2021-05-18 13:15:34.860204');
INSERT INTO public.notification VALUES (254, 3, 4, 'Message', true, '2021-05-18 13:16:47.340999');
INSERT INTO public.notification VALUES (255, 4, 3, 'Message', true, '2021-05-18 13:17:09.97202');
INSERT INTO public.notification VALUES (256, 3, 4, 'Message', true, '2021-05-18 13:17:31.227333');
INSERT INTO public.notification VALUES (257, 4, 3, 'Message', true, '2021-05-18 13:17:45.923888');
INSERT INTO public.notification VALUES (258, 3, 4, 'Message', true, '2021-05-18 13:17:56.027618');
INSERT INTO public.notification VALUES (259, 4, 3, 'Message', true, '2021-05-18 13:18:42.579369');
INSERT INTO public.notification VALUES (260, 3, 4, 'Message', true, '2021-05-18 13:18:55.415179');
INSERT INTO public.notification VALUES (261, 3, 4, 'Message', true, '2021-05-18 13:21:51.619181');
INSERT INTO public.notification VALUES (262, 4, 3, 'Message', true, '2021-05-18 13:36:41.763586');
INSERT INTO public.notification VALUES (263, 4, 3, 'Message', true, '2021-05-18 13:37:11.306023');
INSERT INTO public.notification VALUES (264, 4, 3, 'Message', true, '2021-05-18 13:37:28.170192');
INSERT INTO public.notification VALUES (265, 4, 3, 'Message', true, '2021-05-18 13:38:49.425029');
INSERT INTO public.notification VALUES (266, 3, 4, 'Message', true, '2021-05-18 13:43:50.608923');
INSERT INTO public.notification VALUES (267, 4, 3, 'Message', true, '2021-05-18 13:44:22.425059');
INSERT INTO public.notification VALUES (268, 4, 3, 'Message', true, '2021-05-18 13:47:58.64125');
INSERT INTO public.notification VALUES (269, 4, 3, 'Message', true, '2021-05-19 08:41:19.542192');
INSERT INTO public.notification VALUES (270, 4, 3, 'Message', true, '2021-05-19 08:41:49.820259');
INSERT INTO public.notification VALUES (271, 4, 3, 'Message', true, '2021-05-19 09:11:04.771342');
INSERT INTO public.notification VALUES (272, 4, 3, 'Message', true, '2021-05-19 09:11:46.954556');
INSERT INTO public.notification VALUES (273, 4, 3, 'Message', true, '2021-05-19 09:31:25.709796');
INSERT INTO public.notification VALUES (274, 4, 3, 'Message', true, '2021-05-19 09:37:11.87792');
INSERT INTO public.notification VALUES (275, 4, 3, 'Message', true, '2021-05-19 09:37:54.404571');
INSERT INTO public.notification VALUES (276, 4, 3, 'Message', false, '2021-05-19 09:38:19.852224');
INSERT INTO public.notification VALUES (277, 2, 5, 'Visit', false, '2021-05-25 07:40:05.018258');
INSERT INTO public.notification VALUES (278, 2, 3, 'Visit', false, '2021-05-26 10:54:56.095256');
INSERT INTO public.notification VALUES (279, 2, 1, 'Visit', false, '2021-05-26 10:56:06.583634');
INSERT INTO public.notification VALUES (280, 2, 5, 'Visit', false, '2021-05-26 10:57:45.278582');


--
-- Data for Name: room; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.room VALUES (1, '{2,3}', false, '2021-04-26 16:40:13.761518', '2021-04-26 16:40:13.761518');
INSERT INTO public.room VALUES (3, '{4,3}', true, '2021-05-18 12:51:32.452186', '2021-05-18 12:51:32.452186');
INSERT INTO public.room VALUES (2, '{2,1}', true, '2021-04-26 16:40:13.761518', '2021-04-26 16:40:13.761518');


--
-- Data for Name: topic; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.topic VALUES ('Piscine', '2021-04-26 16:40:13.761518');
INSERT INTO public.topic VALUES ('Peluche', '2021-04-26 16:40:13.761518');
INSERT INTO public.topic VALUES ('Gerontologie', '2021-04-26 16:40:13.761518');
INSERT INTO public.topic VALUES ('Manipulation', '2021-04-26 16:40:13.761518');
INSERT INTO public.topic VALUES ('Blitz', '2021-04-26 16:40:13.761518');
INSERT INTO public.topic VALUES ('Mercedes', '2021-04-26 16:40:13.761518');


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.users VALUES (1, 'Donald', 'Trump', 'Duck', '3c4d8ef0fbafbff632cb3b7368825ca2285dcac1', 'Blond au tweet feroce', 'donald@duck.us', true, NULL, 'Male', 'Hetero', '1946-06-14', 38.89783, -77.03650, 1, '2021-04-26 16:40:13.761518', '2021-05-26 10:56:06.584756');
INSERT INTO public.users VALUES (5, 'Elric', 'De Melnibonnée', 'elric', 'bca2cb7e710dcb7dd23437f268b38d482555d7a5', 'Du sang et des âmes pour mon seigneur Arioch !', 'matcha@ik.me', true, '', 'Male', 'Hetero', '1967-12-05', 45.78777, 4.73096, 1, '2021-04-07 12:24:59.79232', '2021-05-26 10:57:45.281335');
INSERT INTO public.users VALUES (6, 'Pol', 'Gara', 'Pol', 'a4811333da7b59d6b65d98720a7cd91ba2cd741f', 'Puissante sorcière aux pouvoirs aussi ravageurs que son humour !', 'matcha@ik.me', true, '', 'Female', 'Hetero', NULL, 59.93222, 30.35308, NULL, '2021-04-07 12:25:21.768918', '2021-04-07 12:25:21.768918');
INSERT INTO public.users VALUES (7, 'Henri', 'de Toulouse Lautrec', 'lautrec', '0d85a07eacf2cd451a21c4eaff29ed1bf658480f', 'Peintre, amateur de bordels', 'matcha@ik.me', true, '', 'Male', 'Hetero', '1864-11-24', 0.00000, 0.00000, NULL, '2021-04-06 13:20:19.89491', '2021-04-06 13:20:19.89491');
INSERT INTO public.users VALUES (8, 'Misse', 'Ara', 'Aramis', 'd87ddca6e3f4fea34dc5611e5e7a384c68ef5746', '', 'matcha@ik.me', true, '', NULL, NULL, NULL, NULL, NULL, NULL, '2021-04-08 11:45:05.188755', '2021-04-08 11:45:05.188755');
INSERT INTO public.users VALUES (9, 'LaFronde', 'Thierry', 'Thierry', 'b0695c170a3b7c482516ff93e95b042d33caf106', '', 'matcha@ik.me', true, '', NULL, NULL, NULL, NULL, NULL, NULL, '2021-04-08 12:40:38.403396', '2021-04-08 12:40:38.403396');
INSERT INTO public.users VALUES (10, 'Olivier', 'Gasnier', 'pegase7', 'db2c2e5e6d6aca34c822150bae61bfef5f31b623', '""', 'matcha@ik.me', true, '', 'Male', 'Hetero', '1967-09-18', 46.10904, 3.46268, 1, '2021-04-09 07:25:20.498829', '2021-05-17 11:05:57.164736');
INSERT INTO public.users VALUES (4, 'Fogiel', 'Marc-Olivier', 'marcopapolo', '69e26107900f42acf218eb925b8d366bd4d44f92', 'Ouvert a toute les promotions', 'mo-fogiel@tetu.fr', true, NULL, 'Male', 'Homo', '1969-07-05', 48.83636, 2.27387, 2, '2021-04-26 16:40:13.761518', '2021-05-18 11:36:30.068507');
INSERT INTO public.users VALUES (2, 'Angela', 'Merkel', 'LaBombe', '1a5c00f684afd4b983e037403c843346b63e93e0', 'Mon serieux est mon principal atout', 'angela@frech.de', true, NULL, 'Female', 'Hetero', '1954-07-17', 52.52021, 13.36924, 1, '2021-04-26 16:40:13.761518', '2021-05-18 08:01:40.298591');
INSERT INTO public.users VALUES (3, 'Emmanuel', 'Macron', 'LeKiki', '2ce2ff46f219286e08cf551b217d198a91d11912', 'Passionne des antiquites', 'manu@narcisse.com', true, NULL, 'Male', 'Bi', '1977-12-21', 48.87120, 2.31650, 2, '2021-04-26 16:40:13.761518', '2021-05-26 10:54:56.121347');


--
-- Data for Name: users_recommendation; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--



--
-- Data for Name: users_room; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.users_room VALUES (1, 2, 3);
INSERT INTO public.users_room VALUES (1, 3, 2);
INSERT INTO public.users_room VALUES (2, 2, 1);
INSERT INTO public.users_room VALUES (2, 1, 2);
INSERT INTO public.users_room VALUES (3, 4, 3);
INSERT INTO public.users_room VALUES (3, 3, 4);


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


--
-- Data for Name: visit; Type: TABLE DATA; Schema: public; Owner: matchaadmin
--

INSERT INTO public.visit VALUES (1, 10, 2, 1, false, false, '2021-05-17 11:03:57.807165', '2021-05-17 11:03:57.807165', false);
INSERT INTO public.visit VALUES (6, 3, 4, 20, true, false, '2021-05-18 10:18:34.931058', '2021-05-18 12:51:32.450984', false);
INSERT INTO public.visit VALUES (7, 3, 2, 1, false, false, '2021-05-26 10:54:02.100627', '2021-05-26 10:54:02.100627', false);
INSERT INTO public.visit VALUES (8, 1, 2, 1, false, false, '2021-05-26 10:55:05.59699', '2021-05-26 10:55:05.59699', false);
INSERT INTO public.visit VALUES (2, 5, 2, 5, false, false, '2021-05-17 11:05:57.997522', '2021-05-26 10:57:45.235569', false);
INSERT INTO public.visit VALUES (4, 2, 1, 1, false, false, '2021-05-18 08:01:20.78046', '2021-05-18 08:01:20.78046', false);
INSERT INTO public.visit VALUES (5, 4, 3, 24, true, false, '2021-05-18 08:25:18.655287', '2021-05-18 11:36:30.07133', false);
INSERT INTO public.visit VALUES (3, 4, 2, 23, true, false, '2021-05-17 11:06:14.940808', '2021-05-18 10:15:34.258296', false);


--
-- Name: connection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.connection_id_seq', 163, true);


--
-- Name: message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.message_id_seq', 196, true);


--
-- Name: notification_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.notification_id_seq', 280, true);


--
-- Name: room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.room_id_seq', 3, true);


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.tag_id_seq', 6, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- Name: users_recommendation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.users_recommendation_id_seq', 1, false);


--
-- Name: visit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: matchaadmin
--

SELECT pg_catalog.setval('public.visit_id_seq', 8, true);


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
-- Name: users_recommendation users_recommendation_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.users_recommendation
    ADD CONSTRAINT users_recommendation_tag_pkey PRIMARY KEY (id);


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
-- Name: users_recommendation_receiver_fk; Type: INDEX; Schema: public; Owner: matchaadmin
--

CREATE INDEX users_recommendation_receiver_fk ON public.users_recommendation USING btree (receiver_id);


--
-- Name: users_recommendation_sender_receiver_unq; Type: INDEX; Schema: public; Owner: matchaadmin
--

CREATE UNIQUE INDEX users_recommendation_sender_receiver_unq ON public.users_recommendation USING btree (sender_id, receiver_id);


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
-- Name: users_recommendation users_recommendation_receiver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.users_recommendation
    ADD CONSTRAINT users_recommendation_receiver_id_fkey FOREIGN KEY (receiver_id) REFERENCES public.users(id);


--
-- Name: users_recommendation users_recommendation_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: matchaadmin
--

ALTER TABLE ONLY public.users_recommendation
    ADD CONSTRAINT users_recommendation_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public.users(id);


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

