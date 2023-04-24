--
-- PostgreSQL database dump
--

-- Dumped from database version 12.9 (Ubuntu 12.9-2.pgdg20.04+1)
-- Dumped by pg_dump version 14.1 (Ubuntu 14.1-2.pgdg20.04+1)

-- Started on 2022-02-21 10:17:21 +04

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
-- TOC entry 2 (class 3079 OID 16959)
-- Name: dblink; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS dblink WITH SCHEMA public;


--
-- TOC entry 3016 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION dblink; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION dblink IS 'connect to other PostgreSQL databases from within a database';


--
-- TOC entry 259 (class 1255 OID 17006)
-- Name: sync_iss_visibility(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.sync_iss_visibility() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
        insert_statement TEXT;
        table_name TEXT;
        res TEXT;
    BEGIN
        perform dblink_connect('iss_visibility', 'dbname=iss_visibility host=localhost user=postgres password=postgres');
        table_name := NEW.visibility;
        insert_statement = 'insert into '||table_name||'(id, latitude, longitude, timestamp)' ||
                           'values ('''||NEW.id||''','''||NEW.latitude||''','''||NEW.longitude||''','''||NEW.timestamp||''');';
        res := dblink_exec('iss_visibility', insert_statement);
        RAISE INFO '%', res;
        perform dblink_disconnect('iss_visibility');
        RETURN NEW;
    END
$$;


ALTER FUNCTION public.sync_iss_visibility() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 204 (class 1259 OID 16897)
-- Name: iss25544; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.iss25544 (
    id bigint NOT NULL,
    latitude numeric,
    longitude numeric,
    altitude numeric,
    velocity_km numeric,
    visibility text,
    footprint numeric,
    "timestamp" timestamp without time zone,
    daynum numeric,
    solar_lat numeric,
    solar_lon numeric
);


ALTER TABLE public.iss25544 OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 16895)
-- Name: iss25544_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.iss25544_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.iss25544_id_seq OWNER TO postgres;

--
-- TOC entry 3017 (class 0 OID 0)
-- Dependencies: 203
-- Name: iss25544_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.iss25544_id_seq OWNED BY public.iss25544.id;


--
-- TOC entry 2881 (class 2604 OID 16900)
-- Name: iss25544 id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.iss25544 ALTER COLUMN id SET DEFAULT nextval('public.iss25544_id_seq'::regclass);


--
-- TOC entry 2883 (class 2606 OID 16905)
-- Name: iss25544 iss25544_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.iss25544
    ADD CONSTRAINT iss25544_pkey PRIMARY KEY (id);


--
-- TOC entry 2884 (class 2620 OID 17013)
-- Name: iss25544 visibility_mart_trig; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER visibility_mart_trig AFTER INSERT ON public.iss25544 FOR EACH ROW EXECUTE FUNCTION public.sync_iss_visibility();


-- Completed on 2022-02-21 10:17:21 +04

--
-- PostgreSQL database dump complete
--

