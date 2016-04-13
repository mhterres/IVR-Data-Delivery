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

SET search_path = public, pg_catalog;

--
-- Data for Name: customer; Type: TABLE DATA; Schema: public; Owner: ivrdatadelivery
--

COPY customer (id, name, code) FROM stdin;
1	Company 1	1111
2	Company 2	2222
\.


--
-- Name: ivrdatadelivery_id_customer; Type: SEQUENCE SET; Schema: public; Owner: ivrdatadelivery
--

SELECT pg_catalog.setval('ivrdatadelivery_id_customer', 2, true);


--
-- Name: ivrdatadelivery_id_queue; Type: SEQUENCE SET; Schema: public; Owner: ivrdatadelivery
--

SELECT pg_catalog.setval('ivrdatadelivery_id_queue', 1, true);


--
-- Data for Name: queue; Type: TABLE DATA; Schema: public; Owner: ivrdatadelivery
--

COPY queue (id, name) FROM stdin;
1	support
\.


--
-- PostgreSQL database dump complete
--

