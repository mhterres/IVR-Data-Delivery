--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.2
-- Dumped by pg_dump version 9.5.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: ivrdatadelivery_id_customer; Type: SEQUENCE; Schema: public; Owner: ivrdatadelivery
--

CREATE SEQUENCE ivrdatadelivery_id_customer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 1000000
    CACHE 1;


ALTER TABLE ivrdatadelivery_id_customer OWNER TO ivrdatadelivery;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: customer; Type: TABLE; Schema: public; Owner: ivrdatadelivery
--

CREATE TABLE customer (
    id bigint DEFAULT nextval('ivrdatadelivery_id_customer'::regclass) NOT NULL,
    name character varying(100) NOT NULL,
    code character(4) NOT NULL
);


ALTER TABLE customer OWNER TO ivrdatadelivery;

--
-- Name: ivrdatadelivery_id_queue; Type: SEQUENCE; Schema: public; Owner: ivrdatadelivery
--

CREATE SEQUENCE ivrdatadelivery_id_queue
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 1000000
    CACHE 1;


ALTER TABLE ivrdatadelivery_id_queue OWNER TO ivrdatadelivery;

--
-- Name: ivrdatadelivery_id_queuesip; Type: SEQUENCE; Schema: public; Owner: ivrdatadelivery
--

CREATE SEQUENCE ivrdatadelivery_id_queuesip
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 1000000
    CACHE 1;


ALTER TABLE ivrdatadelivery_id_queuesip OWNER TO ivrdatadelivery;

--
-- Name: ivrdatadelivery_id_sip; Type: SEQUENCE; Schema: public; Owner: ivrdatadelivery
--

CREATE SEQUENCE ivrdatadelivery_id_sip
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 1000000
    CACHE 1;


ALTER TABLE ivrdatadelivery_id_sip OWNER TO ivrdatadelivery;

--
-- Name: queue; Type: TABLE; Schema: public; Owner: ivrdatadelivery
--

CREATE TABLE queue (
    id bigint DEFAULT nextval('ivrdatadelivery_id_queue'::regclass) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE queue OWNER TO ivrdatadelivery;

--
-- Name: queue_sip; Type: TABLE; Schema: public; Owner: ivrdatadelivery
--

CREATE TABLE queue_sip (
    id bigint DEFAULT nextval('ivrdatadelivery_id_queuesip'::regclass) NOT NULL,
    queue_id bigint NOT NULL,
    sip_id bigint NOT NULL,
    logged boolean DEFAULT false NOT NULL,
    lasthangup timestamp without time zone
);


ALTER TABLE queue_sip OWNER TO ivrdatadelivery;

--
-- Name: sip; Type: TABLE; Schema: public; Owner: ivrdatadelivery
--

CREATE TABLE sip (
    id bigint DEFAULT nextval('ivrdatadelivery_id_sip'::regclass) NOT NULL,
    extension character varying(10) NOT NULL,
    jid character varying(100) NOT NULL
);


ALTER TABLE sip OWNER TO ivrdatadelivery;

--
-- Name: customer_name_key; Type: CONSTRAINT; Schema: public; Owner: ivrdatadelivery
--

ALTER TABLE ONLY customer
    ADD CONSTRAINT customer_name_key UNIQUE (name);


--
-- Name: customer_pkey; Type: CONSTRAINT; Schema: public; Owner: ivrdatadelivery
--

ALTER TABLE ONLY customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (id);


--
-- Name: queue_pkey; Type: CONSTRAINT; Schema: public; Owner: ivrdatadelivery
--

ALTER TABLE ONLY queue
    ADD CONSTRAINT queue_pkey PRIMARY KEY (id);


--
-- Name: queue_sip_pkey; Type: CONSTRAINT; Schema: public; Owner: ivrdatadelivery
--

ALTER TABLE ONLY queue_sip
    ADD CONSTRAINT queue_sip_pkey PRIMARY KEY (id);


--
-- Name: sip_pkey; Type: CONSTRAINT; Schema: public; Owner: ivrdatadelivery
--

ALTER TABLE ONLY sip
    ADD CONSTRAINT sip_pkey PRIMARY KEY (id);


--
-- Name: ivrdatadelivery_sip_extension; Type: INDEX; Schema: public; Owner: ivrdatadelivery
--

CREATE UNIQUE INDEX ivrdatadelivery_sip_extension ON sip USING btree (extension);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

