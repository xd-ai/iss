--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2
-- Dumped by pg_dump version 14.1 (Ubuntu 14.1-2.pgdg20.04+1)

-- Started on 2022-03-03 17:43:30 +04

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
-- TOC entry 210 (class 1255 OID 16990)
-- Name: psa_new_valid(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.psa_new_valid() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        PERFORM pg_notify('new_row', '' || NEW.id);
        RETURN NULL;
    END;
$$;


ALTER FUNCTION public.psa_new_valid() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 209 (class 1259 OID 16500)
-- Name: raw; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.raw (
    id bigint NOT NULL,
    response text
);


ALTER TABLE public.raw OWNER TO postgres;

--
-- TOC entry 3169 (class 2606 OID 16506)
-- Name: raw raw_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.raw
    ADD CONSTRAINT raw_pkey PRIMARY KEY (id);


--
-- TOC entry 3170 (class 2620 OID 16991)
-- Name: raw psa_valid_trig; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER psa_valid_trig AFTER INSERT ON public.raw FOR EACH ROW EXECUTE FUNCTION public.psa_new_valid();


-- Completed on 2022-03-03 17:43:30 +04

--
-- PostgreSQL database dump complete
--

