--
-- PostgreSQL database dump
--

-- Dumped from database version 12.9 (Ubuntu 12.9-2.pgdg20.04+1)
-- Dumped by pg_dump version 14.1 (Ubuntu 14.1-2.pgdg20.04+1)

-- Started on 2022-02-21 10:22:17 +04

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
-- TOC entry 2 (class 3079 OID 16907)
-- Name: dblink; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS dblink WITH SCHEMA public;


--
-- TOC entry 3014 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION dblink; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION dblink IS 'connect to other PostgreSQL databases from within a database';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 204 (class 1259 OID 16953)
-- Name: daylight; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.daylight (
    id bigint,
    latitude numeric,
    longitude numeric,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.daylight OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 17025)
-- Name: eclipsed; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.eclipsed (
    id bigint NOT NULL,
    latitude numeric,
    longitude numeric,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.eclipsed OWNER TO postgres;

-- Completed on 2022-02-21 10:22:17 +04

--
-- PostgreSQL database dump complete
--

