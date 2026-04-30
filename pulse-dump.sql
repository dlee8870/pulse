--
-- PostgreSQL database dump
--

\restrict 6hSDlTsjqyn7qrt4xH0BR7LOfx9U78AXAGpRaTpOJdYMOqdRzvT6ILef6vfhaU2

-- Dumped from database version 16.13 (Debian 16.13-1.pgdg13+1)
-- Dumped by pg_dump version 16.13 (Debian 16.13-1.pgdg13+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alert_rules; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alert_rules (
    id uuid NOT NULL,
    name character varying(120) NOT NULL,
    category character varying(50) NOT NULL,
    subcategory character varying(100),
    threshold_count integer NOT NULL,
    time_window_hours integer NOT NULL,
    severity_level character varying(20) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone
);


--
-- Name: alerts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alerts (
    id uuid NOT NULL,
    rule_id uuid NOT NULL,
    triggered_at timestamp with time zone,
    current_count integer NOT NULL,
    message text NOT NULL,
    acknowledged boolean NOT NULL
);


--
-- Name: api_users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.api_users (
    id uuid NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: ingestion_logs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ingestion_logs (
    id uuid NOT NULL,
    source character varying(50) NOT NULL,
    subreddit character varying(100),
    posts_fetched integer,
    posts_new integer,
    posts_duplicate integer,
    status character varying(20),
    error_message text,
    started_at timestamp with time zone,
    completed_at timestamp with time zone
);


--
-- Name: issue_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.issue_events (
    id uuid NOT NULL,
    issue_id uuid NOT NULL,
    event_type character varying(30) NOT NULL,
    message text NOT NULL,
    created_at timestamp with time zone
);


--
-- Name: issue_posts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.issue_posts (
    id uuid NOT NULL,
    issue_id uuid NOT NULL,
    processed_post_id uuid NOT NULL,
    linked_at timestamp with time zone
);


--
-- Name: issues; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.issues (
    id uuid NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    category character varying(50) NOT NULL,
    subcategory character varying(100),
    status character varying(20) NOT NULL,
    severity character varying(20) NOT NULL,
    post_count integer NOT NULL,
    avg_sentiment double precision NOT NULL,
    avg_severity double precision NOT NULL,
    first_reported_at timestamp with time zone NOT NULL,
    last_activity_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone,
    updated_at timestamp with time zone
);


--
-- Name: patches; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.patches (
    id uuid NOT NULL,
    created_at timestamp(6) with time zone,
    notes character varying(255),
    release_date date NOT NULL,
    version character varying(255) NOT NULL
);


--
-- Name: processed_posts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.processed_posts (
    id uuid NOT NULL,
    raw_post_id uuid NOT NULL,
    category character varying(50) NOT NULL,
    subcategory character varying(100),
    sentiment_score double precision NOT NULL,
    severity_score double precision NOT NULL,
    processed_at timestamp with time zone NOT NULL,
    keywords jsonb
);


--
-- Name: raw_posts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_posts (
    id uuid NOT NULL,
    title text NOT NULL,
    body text,
    source character varying(50) NOT NULL,
    subreddit character varying(100),
    score integer,
    comment_count integer,
    posted_at timestamp with time zone NOT NULL,
    author character varying(255),
    flair character varying(255),
    ingested_at timestamp(6) with time zone,
    processed boolean NOT NULL,
    source_id character varying(255),
    url character varying(255)
);


--
-- Data for Name: alert_rules; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alert_rules (id, name, category, subcategory, threshold_count, time_window_hours, severity_level, is_active, created_at) FROM stdin;
\.


--
-- Data for Name: alerts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alerts (id, rule_id, triggered_at, current_count, message, acknowledged) FROM stdin;
\.


--
-- Data for Name: api_users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.api_users (id, username, password_hash, is_active, created_at) FROM stdin;
2295c54c-d3ef-41ec-845c-2833e4a82ec8	pulse_admin	pbkdf2_sha256$600000$vdvGTmFKWvF6KoE3TkKj9w==$SKkzsGAVqdjPKePodKy0QjIm3xgzVLbaMV_YNodaf20=	t	2026-04-17 20:42:37.207497+00
\.


--
-- Data for Name: ingestion_logs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.ingestion_logs (id, source, subreddit, posts_fetched, posts_new, posts_duplicate, status, error_message, started_at, completed_at) FROM stdin;
40ccfc2f-0c8a-4e00-8abe-4a4710c862b1	seed	seed_data	30	30	0	completed	\N	2026-04-17 21:03:53.893006+00	2026-04-17 21:03:53.935335+00
\.


--
-- Data for Name: issue_events; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.issue_events (id, issue_id, event_type, message, created_at) FROM stdin;
a654392a-9baf-4440-84ba-7157cb7c7a10	422c6d1b-34b8-4fcb-9cc3-88cb1f5b323e	auto_created	Issue auto-created from 2 clustered posts (all time).	2026-04-17 21:03:55.298092+00
45339d75-63a7-43e6-a8ce-2787f5db68ce	cb7a7190-a0a1-4eda-9f79-67e7273c64bc	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.301101+00
71200149-5df8-439c-9847-91f098c45989	f26218d9-02d0-4fca-ba5d-7cf00c5e9a7b	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.302484+00
3e72e653-850d-48cb-95f7-cc1d0837f57f	e989a3e2-fbed-4350-8590-2c1945d5ce6b	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.303918+00
398549e6-7711-479a-a876-ceeb81e78ca5	254eb5a5-8e4f-4357-a0e4-a01fb55fb6bf	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.305278+00
20fd1a91-aa8d-4134-b4f9-701dd4c7b440	a88a03cd-b8a0-4906-bca6-d59b7b4f1164	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.306759+00
38def3d2-6476-45d9-94c7-2d9a85c17bc7	8c89ddd8-a0c6-44cd-a9f7-a017fbebc35e	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.308199+00
f7eaba43-5c09-4ce7-8498-009771fe21ad	058c8d8a-0a0a-4c07-923e-c2f551d13542	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.309635+00
10dee36f-c48f-4375-bf22-a5afe6cf5bd7	e238bf4c-575f-4213-976c-84d11bac713b	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.311032+00
fc93a70e-38e5-4574-9381-fa3bf03fcfa9	d16e2344-1f52-4199-8f85-edc0d824f6b0	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.312293+00
830069aa-dfe5-4898-97a0-68b37d67baac	fa7c69b3-ecce-4981-af82-b170805a0f15	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.313348+00
f951fe34-fb23-4163-83ca-1d4afc07bb3e	32ddbe84-3776-4350-b40c-9c819e34030c	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.314566+00
9f9c5c5c-74e8-43b2-9086-9304d622dca7	bd27c1bb-324e-4672-bc02-9437c8e7b66c	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.315951+00
4582ba0c-3ed7-4f60-92ed-153c1135d6b0	761cf8de-4271-4cd7-b208-c71fe6eeca9c	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.317257+00
fb35904f-f7b5-40aa-b17f-6b84f72349ed	e68aae15-599d-435f-a496-137932642a4d	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.318423+00
34fbe7a7-5814-41b8-ab37-2ef2a7070ce6	c4b2d833-3100-4aa1-8638-de6ea132515a	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.319511+00
98ad4dd0-b8a7-4a49-82ac-07deb3a2db19	f08abf86-a0e2-4248-8f68-5f808def8fab	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.320517+00
9a818218-33a6-424d-b883-7c06bcec87d7	e1e12737-9d10-4466-865f-7d27a5b3dbee	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.321821+00
369ada1b-cadf-4109-b2c4-312bc952e327	742b6a87-4b52-48b8-baf5-fe88ace38eec	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.322928+00
65c5b094-8595-403f-ba87-bd159fc27abc	d08de825-0e1c-4d82-a73a-a15f5f93db6e	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.324205+00
90542153-7772-4693-b09f-71eb921743b4	7f90d916-5e66-4766-b41e-4a4a9e952280	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.325335+00
d9d1d26f-433d-4b7e-915f-f2780a23ae7d	12316ab3-a340-485d-946b-2c28424179ac	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.326466+00
e34d1901-1954-4658-a6d6-ce9644635532	6b968a04-1d4f-4574-bade-fc5534a32e21	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.327795+00
a81177ed-c342-4b67-9486-7d3dfd694a3f	7ac43e08-6c6f-424b-8873-daef3a519456	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.329049+00
b370e468-3143-42a2-9349-dea373eb09a3	cf3c83c0-2be3-4ba3-a98f-9556a9c59642	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.330419+00
b5e43821-dccf-4308-b2df-2ecb78b23b2e	4f6723c0-1f2b-4205-a599-3eb1d38c988f	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.331885+00
4ae133c9-0f83-405d-b9bb-da21c31121f5	893c0729-63c0-49bf-9873-121f2731fb4f	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.333224+00
e2ae10f5-daab-4fa5-8a46-73309cb48969	0dea3aba-c75b-47f6-8854-e1078f75084e	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.334466+00
cdb3da8a-cdcb-4cd3-8b63-db013a14ab80	aad5b09a-c301-4e50-bd9f-f8281f9ec726	auto_created	Issue auto-created from 1 clustered posts (all time).	2026-04-17 21:03:55.335789+00
\.


--
-- Data for Name: issue_posts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.issue_posts (id, issue_id, processed_post_id, linked_at) FROM stdin;
b2e90df0-ed92-4e06-8280-180efcf700b3	422c6d1b-34b8-4fcb-9cc3-88cb1f5b323e	c951e9ef-ff2e-4d92-9291-bbbe25ec5424	2026-04-17 21:03:55.299455+00
f8fb9cf5-85c7-483f-a9ec-65215cc68870	422c6d1b-34b8-4fcb-9cc3-88cb1f5b323e	dd0a0de2-0d0f-4002-8c35-35d631f8d823	2026-04-17 21:03:55.299459+00
c4c6c096-53c6-487e-8adb-dae072fe3ee1	cb7a7190-a0a1-4eda-9f79-67e7273c64bc	c825fe19-ede2-4e97-a0a8-08c4a049bcf1	2026-04-17 21:03:55.301409+00
26ec8322-3282-48ee-864c-8bf9b63577a1	f26218d9-02d0-4fca-ba5d-7cf00c5e9a7b	b74cdf69-8dca-42d5-857f-cda8954b6e1e	2026-04-17 21:03:55.302781+00
bea39d75-a8cc-40fc-8060-35e761fc65fe	e989a3e2-fbed-4350-8590-2c1945d5ce6b	3c882253-32d7-45ae-8b8e-cabbb99ca1a3	2026-04-17 21:03:55.304145+00
dbc2555c-1b3b-4a39-96bc-fce440997e87	254eb5a5-8e4f-4357-a0e4-a01fb55fb6bf	993aed28-1c2c-47c2-a70d-3b69f1be44bc	2026-04-17 21:03:55.305553+00
8d935087-e5aa-4c2f-8f76-409f865366ee	a88a03cd-b8a0-4906-bca6-d59b7b4f1164	15a6f5c1-e08d-441b-9cb7-7c145b31fb38	2026-04-17 21:03:55.307044+00
9f983004-c16d-4bbd-a6e4-81478b84e350	8c89ddd8-a0c6-44cd-a9f7-a017fbebc35e	687a3f3e-2b8d-4165-af9f-8adb6eee6710	2026-04-17 21:03:55.308451+00
89bc4918-3163-4f77-923c-15bddd8b6cef	058c8d8a-0a0a-4c07-923e-c2f551d13542	92198035-7c27-4839-a86f-82b28cc376cf	2026-04-17 21:03:55.3099+00
2532e237-7139-4073-8aab-d71d0b804657	e238bf4c-575f-4213-976c-84d11bac713b	df2fc0c1-71f8-446f-b7d9-675067020290	2026-04-17 21:03:55.311256+00
c10edb93-4c7d-4ecc-b52a-d4c4fe61ae90	d16e2344-1f52-4199-8f85-edc0d824f6b0	d54d0271-7dce-4edd-a990-752b3f943246	2026-04-17 21:03:55.312443+00
4a65c164-7596-4226-ad93-f2c2b7632d4c	fa7c69b3-ecce-4981-af82-b170805a0f15	85abd69e-96fa-48ae-b935-a0cc946b86be	2026-04-17 21:03:55.313495+00
2b7492fb-58bf-49af-9d05-6f3d28e258fa	32ddbe84-3776-4350-b40c-9c819e34030c	27c69a3e-ab24-43c9-ac2a-0ddb3c889b56	2026-04-17 21:03:55.314789+00
5cc5bbc2-440d-4ffe-bf71-69a592915730	bd27c1bb-324e-4672-bc02-9437c8e7b66c	dc86c25b-75ed-4dd9-a83a-8ff7e587fb61	2026-04-17 21:03:55.316156+00
ae3a3f8a-42cd-4a37-ba10-67deff83334a	761cf8de-4271-4cd7-b208-c71fe6eeca9c	8c659964-6a04-4227-96e6-8826d878e262	2026-04-17 21:03:55.317435+00
d1e11784-fe28-46f5-a005-12d4db8f1b3d	e68aae15-599d-435f-a496-137932642a4d	ff4a8b41-1c9f-4074-9464-56433eb6cc83	2026-04-17 21:03:55.318599+00
a61d8dbe-e597-46c4-9904-1f7dddb5d9a5	c4b2d833-3100-4aa1-8638-de6ea132515a	99f7df0b-9f73-4d0f-88e4-01998baada01	2026-04-17 21:03:55.319675+00
23535091-f2e4-4788-a762-c525b3824d7d	f08abf86-a0e2-4248-8f68-5f808def8fab	82ce3d72-e96c-4b8a-ba29-8781f6288461	2026-04-17 21:03:55.320721+00
6e816bfe-dc59-4b8d-bddf-7cf2697c9c7a	e1e12737-9d10-4466-865f-7d27a5b3dbee	e9b2df05-55d8-4cff-98e9-f9287ff5c151	2026-04-17 21:03:55.321976+00
426d7344-1d3a-449e-82ad-b77653b7e26a	742b6a87-4b52-48b8-baf5-fe88ace38eec	5cbd3b25-8c93-40e9-bdc1-2f04b573597c	2026-04-17 21:03:55.323142+00
3034015b-06c3-40f6-a65e-899c4d1b99ac	d08de825-0e1c-4d82-a73a-a15f5f93db6e	93f6631c-4e2f-412b-879a-6eac2870c54e	2026-04-17 21:03:55.324355+00
ff1728c6-443b-485b-8ec0-9ece9e47d998	7f90d916-5e66-4766-b41e-4a4a9e952280	c89cdcf9-8aa6-4d0b-88e6-407a20e1381e	2026-04-17 21:03:55.325486+00
b889b4c8-e022-4596-acee-37ab9386a1ee	12316ab3-a340-485d-946b-2c28424179ac	a5ea8dff-4c34-4989-8bb9-653cb8b55919	2026-04-17 21:03:55.326646+00
ce8a72e2-d025-4042-a8b2-1a74dc860d75	6b968a04-1d4f-4574-bade-fc5534a32e21	d60f11ff-ce33-4d2e-8c1c-25973063ba35	2026-04-17 21:03:55.328001+00
4c9ecdb1-e877-42cf-94ef-a8dac8d301f8	7ac43e08-6c6f-424b-8873-daef3a519456	b682fd03-2324-4019-8316-780d009e4307	2026-04-17 21:03:55.329318+00
4a561cbd-0268-481a-97b6-37ea540823fb	cf3c83c0-2be3-4ba3-a98f-9556a9c59642	38861171-08ea-4e71-abcd-cbf5b38892f5	2026-04-17 21:03:55.33073+00
fc3d9b6f-f201-4e55-bb4b-7a66cee45de1	4f6723c0-1f2b-4205-a599-3eb1d38c988f	7667ab66-73cd-4528-ba75-a802b76eab69	2026-04-17 21:03:55.332107+00
4ef6e16c-4c9e-48b1-90ac-8a3dd3f8d763	893c0729-63c0-49bf-9873-121f2731fb4f	5fbbf7e9-26a4-4998-bc0e-733b6d7f0a0f	2026-04-17 21:03:55.333413+00
bdd231bc-9d70-458e-8493-0d7b8e1afa29	0dea3aba-c75b-47f6-8854-e1078f75084e	3716f649-f3b9-43e7-b2f9-d8e9c023bbb0	2026-04-17 21:03:55.33465+00
8b46180f-77b3-4929-bea6-010f4b708714	aad5b09a-c301-4e50-bd9f-f8281f9ec726	9a489009-84dc-41a3-bf4f-95817e42d88b	2026-04-17 21:03:55.33597+00
\.


--
-- Data for Name: issues; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.issues (id, title, description, category, subcategory, status, severity, post_count, avg_sentiment, avg_severity, first_reported_at, last_activity_at, created_at, updated_at) FROM stdin;
422c6d1b-34b8-4fcb-9cc3-88cb1f5b323e	Goalkeeper AI and Positioning Issues	Auto-generated from clustered community complaints.	gameplay-bug	goalkeeper-logic	open	high	2	-0.7995	0.8	2025-01-18 09:15:00+00	2025-01-26 13:00:00+00	2026-04-17 21:03:55.295549+00	2026-04-17 21:03:55.295552+00
cb7a7190-a0a1-4eda-9f79-67e7273c64bc	Body Type Matters More Than Ratings	Auto-generated from clustered community complaints.	balance	body-type	open	medium	1	-0.3092	0.582	2025-02-16 10:45:00+00	2025-02-16 10:45:00+00	2026-04-17 21:03:55.297534+00	2026-04-17 21:03:55.297537+00
f26218d9-02d0-4fca-ba5d-7cf00c5e9a7b	Pace Dominates All Other Attributes	Auto-generated from clustered community complaints.	balance	pace-meta	open	high	1	-0.6199	0.694	2025-01-28 10:30:00+00	2025-01-28 10:30:00+00	2026-04-17 21:03:55.300826+00	2026-04-17 21:03:55.300827+00
e989a3e2-fbed-4350-8590-2c1945d5ce6b	PlayStyles Override Base Stats	Auto-generated from clustered community complaints.	balance	playstyle-dependency	open	high	1	-0.8679	0.788	2025-01-20 18:45:00+00	2025-01-20 18:45:00+00	2026-04-17 21:03:55.302231+00	2026-04-17 21:03:55.302232+00
254eb5a5-8e4f-4357-a0e4-a01fb55fb6bf	Career Mode Transfer Logic Overhaul	Auto-generated from clustered community complaints.	feature-request	career-mode	open	high	1	-0.8772	0.679	2025-01-29 08:00:00+00	2025-01-29 08:00:00+00	2026-04-17 21:03:55.303697+00	2026-04-17 21:03:55.303698+00
a88a03cd-b8a0-4906-bca6-d59b7b4f1164	Add Proper Training and Practice Mode	Auto-generated from clustered community complaints.	feature-request	practice-mode	open	medium	1	-0.2287	0.523	2025-02-20 16:45:00+00	2025-02-20 16:45:00+00	2026-04-17 21:03:55.305034+00	2026-04-17 21:03:55.305035+00
8c89ddd8-a0c6-44cd-a9f7-a017fbebc35e	Add Option to Skip Celebrations and Replays	Auto-generated from clustered community complaints.	feature-request	skip-cutscenes	open	high	1	-0.7701	0.714	2025-02-11 17:30:00+00	2025-02-11 17:30:00+00	2026-04-17 21:03:55.306473+00	2026-04-17 21:03:55.306474+00
058c8d8a-0a0a-4c07-923e-c2f551d13542	Unwanted Auto-Lunge Tackles	Auto-generated from clustered community complaints.	gameplay-bug	auto-lunge	open	high	1	-0.8586	0.786	2025-02-02 15:30:00+00	2025-02-02 15:30:00+00	2026-04-17 21:03:55.307941+00	2026-04-17 21:03:55.307943+00
e238bf4c-575f-4213-976c-84d11bac713b	Corner Kick Balancing Issues	Auto-generated from clustered community complaints.	gameplay-bug	corners	open	high	1	-0.8749	0.781	2025-02-18 12:15:00+00	2025-02-18 12:15:00+00	2026-04-17 21:03:55.309361+00	2026-04-17 21:03:55.309362+00
d16e2344-1f52-4199-8f85-edc0d824f6b0	First Touch Quality Not Matching Stats	Auto-generated from clustered community complaints.	gameplay-bug	first-touch	open	high	1	-0.7297	0.766	2025-02-10 09:00:00+00	2025-02-10 09:00:00+00	2026-04-17 21:03:55.310713+00	2026-04-17 21:03:55.310714+00
fa7c69b3-ecce-4981-af82-b170805a0f15	Fullback Defensive Tracking Failures	Auto-generated from clustered community complaints.	gameplay-bug	fullback-tracking	open	high	1	-0.67	0.72	2025-01-15 14:30:00+00	2025-01-15 14:30:00+00	2026-04-17 21:03:55.312076+00	2026-04-17 21:03:55.312077+00
32ddbe84-3776-4350-b40c-9c819e34030c	Heading Accuracy Not Reflecting Stats	Auto-generated from clustered community complaints.	gameplay-bug	heading	open	high	1	-0.7718	0.763	2025-02-01 12:00:00+00	2025-02-01 12:00:00+00	2026-04-17 21:03:55.313157+00	2026-04-17 21:03:55.313158+00
bd27c1bb-324e-4672-bc02-9437c8e7b66c	Kick-Off Goal Exploit	Auto-generated from clustered community complaints.	gameplay-bug	kickoff-goals	open	high	1	-0.8864	0.825	2025-02-04 22:00:00+00	2025-02-04 22:00:00+00	2026-04-17 21:03:55.314318+00	2026-04-17 21:03:55.31432+00
761cf8de-4271-4cd7-b208-c71fe6eeca9c	Offside Detection Inaccuracy	Auto-generated from clustered community complaints.	gameplay-bug	offside-logic	open	high	1	-0.8197	0.772	2025-02-06 11:30:00+00	2025-02-06 11:30:00+00	2026-04-17 21:03:55.3157+00	2026-04-17 21:03:55.315702+00
e68aae15-599d-435f-a496-137932642a4d	Passing Goes to Wrong Player	Auto-generated from clustered community complaints.	gameplay-bug	passing-accuracy	open	high	1	-0.6292	0.722	2025-02-13 14:00:00+00	2025-02-13 14:00:00+00	2026-04-17 21:03:55.316987+00	2026-04-17 21:03:55.316988+00
c4b2d833-3100-4aa1-8638-de6ea132515a	Player Switching Inconsistency	Auto-generated from clustered community complaints.	gameplay-bug	player-switching	open	high	1	-0.8629	0.827	2025-02-08 20:15:00+00	2025-02-08 20:15:00+00	2026-04-17 21:03:55.318178+00	2026-04-17 21:03:55.318179+00
f08abf86-a0e2-4248-8f68-5f808def8fab	Inconsistent Referee Decisions	Auto-generated from clustered community complaints.	gameplay-bug	referee-logic	open	high	1	-0.909	0.812	2025-02-09 13:45:00+00	2025-02-09 13:45:00+00	2026-04-17 21:03:55.319308+00	2026-04-17 21:03:55.31931+00
e1e12737-9d10-4466-865f-7d27a5b3dbee	Transfer Market Price Instability	Auto-generated from clustered community complaints.	market	price-crash	open	high	1	-0.8959	0.725	2025-02-07 16:00:00+00	2025-02-07 16:00:00+00	2026-04-17 21:03:55.320327+00	2026-04-17 21:03:55.320328+00
742b6a87-4b52-48b8-baf5-fe88ace38eec	Chemistry System Praise	Auto-generated from clustered community complaints.	positive	chemistry-system	open	low	1	0.95	0.145	2025-02-14 11:30:00+00	2025-02-14 11:30:00+00	2026-04-17 21:03:55.321607+00	2026-04-17 21:03:55.321608+00
d08de825-0e1c-4d82-a73a-a15f5f93db6e	Content Quality Praise	Auto-generated from clustered community complaints.	positive	content-quality	open	low	1	0.9667	0.147	2025-02-19 09:30:00+00	2025-02-19 09:30:00+00	2026-04-17 21:03:55.322636+00	2026-04-17 21:03:55.322638+00
7f90d916-5e66-4766-b41e-4a4a9e952280	Evolution System Praise	Auto-generated from clustered community complaints.	positive	evolution-system	open	low	1	0.9666	0.147	2025-02-05 14:15:00+00	2025-02-05 14:15:00+00	2026-04-17 21:03:55.324001+00	2026-04-17 21:03:55.324002+00
12316ab3-a340-485d-946b-2c28424179ac	Rush Mode Praise	Auto-generated from clustered community complaints.	positive	rush-mode	open	low	1	0.9766	0.148	2025-02-17 15:30:00+00	2025-02-17 15:30:00+00	2026-04-17 21:03:55.325122+00	2026-04-17 21:03:55.325124+00
6b968a04-1d4f-4574-bade-fc5534a32e21	Server Disconnections Causing Losses	Auto-generated from clustered community complaints.	server-issue	disconnection	open	high	1	-0.8779	0.804	2025-02-15 19:00:00+00	2025-02-15 19:00:00+00	2026-04-17 21:03:55.326251+00	2026-04-17 21:03:55.326252+00
7ac43e08-6c6f-424b-8873-daef3a519456	Server Lag and Input Delay	Auto-generated from clustered community complaints.	server-issue	lag-delay	open	high	1	-0.8916	0.822	2025-01-31 19:45:00+00	2025-01-31 19:45:00+00	2026-04-17 21:03:55.327528+00	2026-04-17 21:03:55.32753+00
cf3c83c0-2be3-4ba3-a98f-9556a9c59642	Companion App Crashes and Bugs	Auto-generated from clustered community complaints.	ui-bug	companion-app	open	high	1	-0.9152	0.725	2025-02-03 07:45:00+00	2025-02-03 07:45:00+00	2026-04-17 21:03:55.328764+00	2026-04-17 21:03:55.328765+00
4f6723c0-1f2b-4205-a599-3eb1d38c988f	SBC Menu Filter Broken	Auto-generated from clustered community complaints.	ui-bug	sbc-interface	open	high	1	-0.8395	0.695	2025-01-22 11:00:00+00	2025-01-22 11:00:00+00	2026-04-17 21:03:55.330181+00	2026-04-17 21:03:55.330182+00
893c0729-63c0-49bf-9873-121f2731fb4f	Scoreboard Overlay Stuck on Screen	Auto-generated from clustered community complaints.	ui-bug	scoreboard-overlay	open	high	1	-0.757	0.661	2025-01-23 20:30:00+00	2025-01-23 20:30:00+00	2026-04-17 21:03:55.331607+00	2026-04-17 21:03:55.331608+00
0dea3aba-c75b-47f6-8854-e1078f75084e	AI Difficulty Scaling Feels Unfair	Auto-generated from clustered community complaints.	balance	ai-difficulty	open	medium	1	-0.15	0.518	2025-02-12 08:15:00+00	2025-02-12 08:15:00+00	2026-04-17 21:03:55.332936+00	2026-04-17 21:03:55.332937+00
aad5b09a-c301-4e50-bd9f-f8281f9ec726	Ui Bug	Auto-generated from clustered community complaints.	ui-bug	\N	open	medium	1	-0.5749	0.63	2025-01-25 16:15:00+00	2025-01-25 16:15:00+00	2026-04-17 21:03:55.334209+00	2026-04-17 21:03:55.33421+00
\.


--
-- Data for Name: patches; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.patches (id, created_at, notes, release_date, version) FROM stdin;
85d1ad87-2612-4e9d-aaa8-0fb81c3f6ffe	2026-04-17 21:09:42.483097+00	Mid-cycle balance and bug fixes	2025-01-28	Title Update 7
3483c022-a69d-4d29-828d-1fa8d74c1af2	2026-04-17 21:09:49.114938+00	Major gameplay update	2025-01-14	Title Update 6
363b3e75-336f-4dc5-883e-a511bf766827	2026-04-17 21:09:53.78814+00	Server stability patch	2025-02-10	Title Update 8
\.


--
-- Data for Name: processed_posts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.processed_posts (id, raw_post_id, category, subcategory, sentiment_score, severity_score, processed_at, keywords) FROM stdin;
85abd69e-96fa-48ae-b935-a0cc946b86be	1a8bb75d-15bb-4909-a301-c4307b2a6d9a	gameplay-bug	fullback-tracking	-0.67	0.72	2026-04-17 21:03:55.247541+00	["fullbacks", "past", "anyone", "runs"]
c951e9ef-ff2e-4d92-9291-bbbe25ec5424	91983ef9-679f-493a-a40c-7df7aeee47ef	gameplay-bug	goalkeeper-logic	-0.7474	0.769	2026-04-17 21:03:55.247549+00	["keeper", "rivals", "toty", "gk", "rated", "logic"]
3c882253-32d7-45ae-8b8e-cabbb99ca1a3	aff08ef6-4b94-485f-8cd3-a9d13ed9badb	balance	playstyle-dependency	-0.8679	0.788	2026-04-17 21:03:55.247553+00	["playstyles", "playstyle", "passing", "legend", "pass", "without", "incisive"]
7667ab66-73cd-4528-ba75-a802b76eab69	b7e1982b-66cc-4eea-8487-e819ebed680a	ui-bug	sbc-interface	-0.8395	0.695	2026-04-17 21:03:55.247557+00	["sbc", "gk", "position", "filter", "patch", "broken", "latest", "months"]
5fbbf7e9-26a4-4998-bc0e-733b6d7f0a0f	5a5bedf0-53e5-469a-a227-55e81adede46	ui-bug	scoreboard-overlay	-0.757	0.661	2026-04-17 21:03:55.24756+00	["substitution", "screen", "entire", "second", "half"]
9a489009-84dc-41a3-bf4f-95817e42d88b	31abcc73-37d8-45f1-bacb-4cfb56122a7f	ui-bug	\N	-0.5749	0.63	2026-04-17 21:03:55.247562+00	["goal", "center"]
dd0a0de2-0d0f-4002-8c35-35d631f8d823	f5293757-a107-4245-85f2-22fb171d39fa	gameplay-bug	goalkeeper-logic	-0.8516	0.831	2026-04-17 21:03:55.247564+00	["keeper", "gk", "manual", "fix", "movement", "reducing", "problem"]
b74cdf69-8dca-42d5-857f-cda8954b6e1e	3e54e07a-3c17-432c-ba17-c372a7dd4c63	balance	pace-meta	-0.6199	0.694	2026-04-17 21:03:55.247567+00	["dribbling", "physical", "passing", "pace", "matters", "team", "rated"]
993aed28-1c2c-47c2-a70d-3b69f1be44bc	53aec566-7512-4b1d-9433-5494fc571466	feature-request	career-mode	-0.8772	0.679	2026-04-17 21:03:55.247569+00	["career mode", "striker", "rated", "transfer"]
b682fd03-2324-4019-8316-780d009e4307	aaacf357-1093-492d-a076-43afc5530c89	server-issue	lag-delay	-0.8916	0.822	2026-04-17 21:03:55.247572+00	["weekend league", "input delay", "server", "rivals", "lag", "unplayable"]
27c69a3e-ab24-43c9-ac2a-0ddb3c889b56	7a52f6ee-8dd8-4b0c-993b-0bbe7594d091	gameplay-bug	heading	-0.7718	0.763	2026-04-17 21:03:55.247574+00	["playstyles", "playstyle", "fullback", "heading", "aerial", "accuracy"]
92198035-7c27-4839-a86f-82b28cc376cf	0f4867af-1a67-4d1c-8142-523b7bf5be30	gameplay-bug	auto-lunge	-0.8586	0.786	2026-04-17 21:03:55.247576+00	["champs", "auto", "lunge"]
38861171-08ea-4e71-abcd-cbf5b38892f5	7cfa7270-8c6d-470d-a252-da81880d18d7	ui-bug	companion-app	-0.9152	0.725	2026-04-17 21:03:55.247579+00	["transfer market", "companion app", "sbc"]
dc86c25b-75ed-4dd9-a83a-8ff7e587fb61	1d0cecce-c21e-4a0c-9c5f-a5c7224abc52	gameplay-bug	kickoff-goals	-0.8864	0.825	2026-04-17 21:03:55.247581+00	["kick"]
c89cdcf9-8aa6-4d0b-88e6-407a20e1381e	501c840b-d126-426d-a306-97a3d35908c4	positive	evolution-system	0.9666	0.147	2026-04-17 21:03:55.247583+00	["evolution", "evo", "system", "actually", "cards"]
8c659964-6a04-4227-96e6-8826d878e262	73a54a34-9ee0-48fc-8e62-4f9909e1420e	gameplay-bug	offside-logic	-0.8197	0.772	2026-04-17 21:03:55.247586+00	["offside", "striker", "calls"]
e9b2df05-55d8-4cff-98e9-f9287ff5c151	59a9bdaa-0879-40b9-a75e-1c48b12ba640	market	price-crash	-0.8959	0.725	2026-04-17 21:03:55.247588+00	["transfer market", "promo", "sbc", "card", "crashes", "within", "hours"]
99f7df0b-9f73-4d0f-88e4-01998baada01	8a121b2a-5297-4fd1-8de1-8fd2ae3617e9	gameplay-bug	player-switching	-0.8629	0.827	2026-04-17 21:03:55.24759+00	["fullback", "cdm", "cb", "pressed", "switching", "mechanic", "switches"]
82ce3d72-e96c-4b8a-ba29-8781f6288461	5e3433a2-bb9a-41a6-a00b-5f869795800c	gameplay-bug	referee-logic	-0.909	0.812	2026-04-17 21:03:55.247593+00	["advantage"]
d54d0271-7dce-4edd-a990-752b3f943246	24054e45-2a2d-4ea1-bd42-c63281c28b83	gameplay-bug	first-touch	-0.7297	0.766	2026-04-17 21:03:55.247595+00	["toty", "touch", "ball", "control"]
687a3f3e-2b8d-4165-af9f-8adb6eee6710	5b9ec625-38d9-4cc5-a390-59847e932545	feature-request	skip-cutscenes	-0.7701	0.714	2026-04-17 21:03:55.247597+00	["skip", "minutes"]
3716f649-f3b9-43e7-b2f9-d8e9c023bbb0	71ccc9f5-f748-418a-bbff-6e66ca81a12a	balance	ai-difficulty	-0.15	0.518	2026-04-17 21:03:55.2476+00	["squad battles", "defending", "passing", "rivals", "perfect", "world", "class"]
ff4a8b41-1c9f-4074-9464-56433eb6cc83	d24d33d7-dffd-4fe8-880c-0fb0332f9540	gameplay-bug	passing-accuracy	-0.6292	0.722	2026-04-17 21:03:55.247602+00	["passing", "striker", "goes"]
5cbd3b25-8c93-40e9-bdc1-2f04b573597c	6ef761bb-53db-41ac-97a2-cce0928eeace	positive	chemistry-system	0.95	0.145	2026-04-17 21:03:55.247604+00	["chemistry", "system", "actually", "good", "use", "without"]
d60f11ff-ce33-4d2e-8c1c-25973063ba35	8fb06b2d-c56a-4c14-b072-5bf35c06d386	server-issue	disconnection	-0.8779	0.804	2026-04-17 21:03:55.247607+00	["disconnect", "division", "server", "rivals", "side", "loss"]
c825fe19-ede2-4e97-a0a8-08c4a049bcf1	bbd8fb15-80ff-4533-8168-963459335391	balance	body-type	-0.3092	0.582	2026-04-17 21:03:55.247609+00	["body", "stats", "type", "types", "unique", "lower"]
a5ea8dff-4c34-4989-8bb9-653cb8b55919	26ddd99f-904f-4c50-b642-0c5b3771a660	positive	rush-mode	0.9766	0.148	2026-04-17 21:03:55.247611+00	["rush mode", "new", "fun"]
df2fc0c1-71f8-446f-b7d9-675067020290	57d9d14c-a95e-4791-b143-45fbde5f4394	gameplay-bug	corners	-0.8749	0.781	2026-04-17 21:03:55.247613+00	["corner", "corners", "patch"]
93f6631c-4e2f-412b-879a-6eac2870c54e	acb0ba78-50c9-4298-ad1d-1fdff5b1efd0	positive	content-quality	0.9667	0.147	2026-04-17 21:03:55.247616+00	["promo", "content", "sbcs"]
15a6f5c1-e08d-441b-9cb7-7c145b31fb38	5bb62511-5c14-47a4-8060-0d85ef12ddc5	feature-request	practice-mode	-0.2287	0.523	2026-04-17 21:03:55.247618+00	["practice", "proper", "training", "match"]
\.


--
-- Data for Name: raw_posts; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.raw_posts (id, title, body, source, subreddit, score, comment_count, posted_at, author, flair, ingested_at, processed, source_id, url) FROM stdin;
0f4867af-1a67-4d1c-8142-523b7bf5be30	Why do defenders auto-lunge when I'm not pressing tackle?	My CBs keep doing auto-lunge tackles that I never triggered. Im holding jockey and they just decide to stick a leg out at the worst possible time, leaving a gap in my defense. This needs to be something the player controls, not the AI deciding for me. Its cost me so many goals in Champs.	seed	EAFC	1789	398	2025-02-02 15:30:00+00	manual_defending_please	GAMEPLAY	2026-04-17 21:03:53.93099+00	t	seed_012	https://reddit.com/r/EAFC/comments/seed012
1a8bb75d-15bb-4909-a301-c4307b2a6d9a	Fullbacks literally jogging while attackers sprint past them	Is anyone else noticing that fullbacks just stop tracking runs this year? In FC 24 they would actually follow wingers on overlapping runs. Now my Robertson just stands there watching Salah run past him. This is genuinely game breaking for anyone trying to play a high line. The AI defensive awareness for fullbacks has completely regressed.	seed	EAFC	1847	342	2025-01-15 14:30:00+00	tactical_masterclass	GAMEPLAY	2026-04-17 21:03:53.930963+00	t	seed_001	https://reddit.com/r/EAFC/comments/seed001
1d0cecce-c21e-4a0c-9c5f-a5c7224abc52	Kick off goals are still a thing in 2025. Embarrassing.	Conceded directly from kick off for the third time today. Opponent just sprints straight through the middle and my entire team parts like the Red Sea. Kick off boost has been a known issue since FIFA 17 and here we are 8 years later with the same problem. This should be priority number one to fix.	seed	EAFC	2567	723	2025-02-04 22:00:00+00	scripting_believer	GAMEPLAY	2026-04-17 21:03:53.930994+00	t	seed_014	https://reddit.com/r/EAFC/comments/seed014
24054e45-2a2d-4ea1-bd42-c63281c28b83	First touch is unbelievably bad for elite players	My TOTY Messi with 99 ball control takes a first touch that sends the ball 3 meters away from him. Meanwhile a 78 rated midfielder on the other team controls everything perfectly. First touch should directly correlate with ball control stats but it feels completely random. Is there a hidden momentum mechanic affecting this?	seed	EAFC	2789	634	2025-02-10 09:00:00+00	first_touch_merchant	GAMEPLAY	2026-04-17 21:03:53.931002+00	t	seed_020	https://reddit.com/r/EAFC/comments/seed020
26ddd99f-904f-4c50-b642-0c5b3771a660	Love the new Rush mode - most fun Ive had in FC in years	Rush mode with friends is genuinely incredible. Quick matches, smaller pitch, less sweaty than regular UT. This is what EA should focus on - fun social modes that dont require you to grind for 40 hours a week. Please keep supporting this mode with new content and dont let it die.	seed	EAFC	3678	567	2025-02-17 15:30:00+00	rush_is_goated	POSITIVE	2026-04-17 21:03:53.931011+00	t	seed_027	https://reddit.com/r/EAFC/comments/seed027
31abcc73-37d8-45f1-bacb-4cfb56122a7f	Goal replays showing the center circle instead of the actual goal	Scored a banger from outside the box and the instant replay just showed the grass at the center line. No angle of the goal, no celebration, just a random camera shot of midfield. This has been happening since Title Update 3 and somehow still isnt fixed. Anyone else getting this?	seed	EAFC	1245	289	2025-01-25 16:15:00+00	replay_watcher	BUG	2026-04-17 21:03:53.930979+00	t	seed_006	https://reddit.com/r/EAFC/comments/seed006
3e54e07a-3c17-432c-ba17-c372a7dd4c63	Pace is still the only stat that matters in this game	Built a full team of high-rated technical players. Got destroyed by a team of 82-rated pacey wingers. Dribbling, passing, physical - none of it matters if the opponent just sprints past your defense. We need a genuine pace nerf or at least make other attributes competitive. Its been like this for years.	seed	EAFC	2876	654	2025-01-28 10:30:00+00	skills_over_speed	GAMEPLAY	2026-04-17 21:03:53.930983+00	t	seed_008	https://reddit.com/r/EAFC/comments/seed008
501c840b-d126-426d-a306-97a3d35908c4	Props to EA for the new Evo system - actually a good addition	I know we complain a lot here but credit where its due. The Evolution system this year is genuinely fun. Being able to upgrade lower rated players you actually like into usable cards is a great concept. My evolved Ollie Watkins is one of my favorite cards this year. More of this kind of content please EA.	seed	EAFC	4123	534	2025-02-05 14:15:00+00	positive_vibes_fc	POSITIVE	2026-04-17 21:03:53.930995+00	t	seed_015	https://reddit.com/r/EAFC/comments/seed015
53aec566-7512-4b1d-9433-5494fc571466	Career Mode transfers are completely unrealistic	Liverpool just offered me 12M for my 89 rated striker in Career Mode. Meanwhile the AI buys 76 rated players for 45M. The transfer logic has always been rough but this year its genuinely broken. Release clauses, contract negotiations, and AI transfer behavior all need a complete overhaul.	seed	EAFC	1654	312	2025-01-29 08:00:00+00	career_mode_addict	CAREER MODE	2026-04-17 21:03:53.930984+00	t	seed_009	https://reddit.com/r/EAFC/comments/seed009
57d9d14c-a95e-4791-b143-45fbde5f4394	Corners are either completely useless or broken OP depending on the patch	Before the last patch corners were impossible to score from. Now after the patch every other corner goes in. There is no middle ground. EA seems to only know how to swing between extremes. Can we just have corners that reward good delivery and positioning without being automatic goals?	seed	EAFC	1432	312	2025-02-18 12:15:00+00	corner_flag_pain	GAMEPLAY	2026-04-17 21:03:53.931014+00	t	seed_028	https://reddit.com/r/EAFC/comments/seed028
59a9bdaa-0879-40b9-a75e-1c48b12ba640	Market is dead - every card crashes within hours of release	Packed a promo card worth 400k, listed it, and by the time it sold the price had dropped to 280k. Every single promo crashes the market within hours now. The supply is too high and the SBC requirements dont create enough demand. The entire transfer market economy needs rebalancing.	seed	EAFC	1567	423	2025-02-07 16:00:00+00	market_crash_survivor	ULTIMATE TEAM	2026-04-17 21:03:53.930998+00	t	seed_017	https://reddit.com/r/EAFC/comments/seed017
5a5bedf0-53e5-469a-a227-55e81adede46	Substitution graphic stuck on screen for entire second half	Made a sub at halftime and the substitution overlay on the scoreboard never went away. It stayed on screen the entire second half covering part of my view. Had to play around it. This has happened three times this week. Small bug but incredibly annoying when it happens in a close WL match.	seed	EAFC	987	178	2025-01-23 20:30:00+00	weekend_league_warrior	BUG	2026-04-17 21:03:53.930977+00	t	seed_005	https://reddit.com/r/EAFC/comments/seed005
5b9ec625-38d9-4cc5-a390-59847e932545	How is there still no way to skip celebrations and cutscenes?	I just want to play football. I dont want to watch my opponents celebration, the walk back to the center circle, the camera pan, the replay from three angles. A single match takes 15+ minutes but only 6 minutes of that is actual gameplay. Give us a skip all option. Respect peoples time.	seed	EAFC	5432	1456	2025-02-11 17:30:00+00	skip_please	FEATURE REQUEST	2026-04-17 21:03:53.931003+00	t	seed_021	https://reddit.com/r/EAFC/comments/seed021
5bb62511-5c14-47a4-8060-0d85ef12ddc5	This game needs a proper training/practice mode	Want to practice skill moves? Go into a match. Want to practice set pieces? Go into a match. Want to practice new tactics? Go into a match and risk your rank. Every competitive game has a proper training ground with drills and scenarios. Rocket League has custom training, Valorant has the range. FC has nothing useful. Build a proper practice arena.	seed	EAFC	3234	756	2025-02-20 16:45:00+00	practice_makes_perfect	FEATURE REQUEST	2026-04-17 21:03:53.931016+00	t	seed_030	https://reddit.com/r/EAFC/comments/seed030
5e3433a2-bb9a-41a6-a00b-5f869795800c	Refs in this game are absolutely clueless	Got a red card for a clean standing tackle but my opponent slide tackled from behind with studs up and got nothing. The referee logic this year is the worst its ever been. Fouls are completely random with no consistency between what gets called and what doesnt. Even advantage play is broken - ref plays advantage when I dont want it and stops play when I do.	seed	EAFC	2234	512	2025-02-09 13:45:00+00	ref_needs_var	GAMEPLAY	2026-04-17 21:03:53.931+00	t	seed_019	https://reddit.com/r/EAFC/comments/seed019
6ef761bb-53db-41ac-97a2-cce0928eeace	Chemistry system actually feels good this year - nice change	Hot take but the chemistry system this year is the best its ever been. Being able to use players from different leagues without being punished too hard makes squad building actually fun. I can use my favorite players together without worrying about perfect links. Good job on this one EA.	seed	EAFC	2345	345	2025-02-14 11:30:00+00	chemistry_enjoyer	POSITIVE	2026-04-17 21:03:53.931007+00	t	seed_024	https://reddit.com/r/EAFC/comments/seed024
71ccc9f5-f748-418a-bbff-6e66ca81a12a	AI defending in squad battles is absurdly perfect on World Class	Playing Squad Battles on World Class and the AI defense is literally perfect. Every tackle timed perfectly, every passing lane covered, zero mistakes. Then you go to Rivals and real players leave gaps everywhere. The difficulty scaling isnt about smarter AI, its about giving the CPU perfect execution which feels unfair rather than challenging.	seed	EAFC	1234	267	2025-02-12 08:15:00+00	squad_battles_only	GAMEPLAY	2026-04-17 21:03:53.931004+00	t	seed_022	https://reddit.com/r/EAFC/comments/seed022
73a54a34-9ee0-48fc-8e62-4f9909e1420e	Can we talk about how broken the offside line is?	The offside calls this year are absurd. Clear onside runs being called off, and blatant offsides being allowed. The margin of error is way too wide. Instant replay shows my striker is clearly behind the last defender but the game calls it offside. If VAR exists in real football to fix this, surely the game engine can get it right.	seed	EAFC	1876	389	2025-02-06 11:30:00+00	offside_trap_victim	GAMEPLAY	2026-04-17 21:03:53.930996+00	t	seed_016	https://reddit.com/r/EAFC/comments/seed016
7a52f6ee-8dd8-4b0c-993b-0bbe7594d091	Heading is completely useless without Aerial PlayStyle+	Tried crossing to Haaland in the box. Man is 6'4 with 90 heading accuracy but cant win a header against a 5'8 fullback because he doesnt have Aerial+. PlayStyles have created a two-tier system where base stats are meaningless. A 90 heading accuracy should mean something on its own.	seed	EAFC	2134	445	2025-02-01 12:00:00+00	cross_and_pray	GAMEPLAY	2026-04-17 21:03:53.930987+00	t	seed_011	https://reddit.com/r/EAFC/comments/seed011
7cfa7270-8c6d-470d-a252-da81880d18d7	The companion app is more broken than the actual game	Tried to list a player on the transfer market from the companion app and it crashed three times. SBC solutions dont load, player search randomly resets filters, and notifications are delayed by hours. If youre going to have an app that people use daily at least make it functional.	seed	EAFC	1432	267	2025-02-03 07:45:00+00	companion_app_pain	BUG	2026-04-17 21:03:53.930992+00	t	seed_013	https://reddit.com/r/EAFC/comments/seed013
8a121b2a-5297-4fd1-8de1-8fd2ae3617e9	Player switching is the most frustrating mechanic in this game	Pressed L1 to switch to my CB. Game switches to my CDM. Pressed again, switches to my fullback. Pressed again, back to CDM. Meanwhile the attacker is through on goal. Right stick switching isnt any better - its inconsistent and laggy. This single mechanic has cost me more games than anything else.	seed	EAFC	3456	945	2025-02-08 20:15:00+00	switch_to_the_right_player	GAMEPLAY	2026-04-17 21:03:53.930999+00	t	seed_018	https://reddit.com/r/EAFC/comments/seed018
8fb06b2d-c56a-4c14-b072-5bf35c06d386	Disconnection losses in Rivals need to be addressed	I was winning 3-0 in the 80th minute and got disconnected. Server side disconnect, not my internet. Got handed the loss. No compensation, no replay, just a loss that affects my division. If EA can detect that a disconnect was server-side they should nullify the match, not punish the player.	seed	EAFC	2876	678	2025-02-15 19:00:00+00	disconnected_rage	SERVERS	2026-04-17 21:03:53.931008+00	t	seed_025	https://reddit.com/r/EAFC/comments/seed025
91983ef9-679f-493a-a40c-7df7aeee47ef	GK logic is completely broken - 73 rated keepers save the same as 90 rated	Just played a Rivals match where my TOTY Courtois performed identically to a 73 rated gold keeper my opponent had. Same animations, same positioning, same reaction saves. What is the point of spending coins on a top keeper if the GK logic treats them all the same? Tested this in friendlies with my friend and confirmed it. Keeper rating seems to have zero impact on actual performance.	seed	EAFC	2341	567	2025-01-18 09:15:00+00	fut_economist_99	GAMEPLAY	2026-04-17 21:03:53.930968+00	t	seed_002	https://reddit.com/r/EAFC/comments/seed002
aaacf357-1093-492d-a076-43afc5530c89	Servers are unplayable during Weekend League - 100ms+ delay	Every single Weekend League I get speed up lag and input delay that makes the game unplayable. During the week Rivals is fine, maybe 20-30ms. But as soon as WL starts its 80-120ms consistently. My internet is 500mbps wired. This is a server capacity issue and its been the same for 3 years running.	seed	EAFC	3245	876	2025-01-31 19:45:00+00	lag_ruins_everything	SERVERS	2026-04-17 21:03:53.930985+00	t	seed_010	https://reddit.com/r/EAFC/comments/seed010
acb0ba78-50c9-4298-ad1d-1fdff5b1efd0	Content this year has been the best ever. SBCs and objectives are great.	Say what you want about gameplay but the content team is killing it. Daily SBCs, good objective players that are actually usable, interesting promo concepts. The grind feels rewarding this year compared to last year where everything was overpriced and underwhelming. Keep this energy for the rest of the cycle.	seed	EAFC	2567	423	2025-02-19 09:30:00+00	content_is_king	POSITIVE	2026-04-17 21:03:53.931015+00	t	seed_029	https://reddit.com/r/EAFC/comments/seed029
aff08ef6-4b94-485f-8cd3-a9d13ed9badb	PlayStyles are ruining this game. An 85+ passing legend cant pass without Incisive Pass+	Why does my 92 Zidane with 89 passing feel like a bronze player just because he doesnt have Incisive Pass or Tiki Taka? PlayStyles should ENHANCE players, not be a requirement for basic functionality. A legend with 85+ passing should be able to make a simple through ball without needing a specific PlayStyle. This system is fundamentally flawed.	seed	EAFC	3102	891	2025-01-20 18:45:00+00	legends_deserve_better	GAMEPLAY	2026-04-17 21:03:53.930973+00	t	seed_003	https://reddit.com/r/EAFC/comments/seed003
b7e1982b-66cc-4eea-8487-e819ebed680a	SBC position filter is completely broken after latest patch	The square button filter on the SBC menu used to let you filter by position when hovering over a slot. First it broke for GK a few months ago, and now after the latest patch it doesnt work for ANY position. This is a basic UI function that worked fine for months. How does this get broken in a patch that was supposed to fix other things?	seed	EAFC	1523	234	2025-01-22 11:00:00+00	sbc_grinder_daily	BUG	2026-04-17 21:03:53.930976+00	t	seed_004	https://reddit.com/r/EAFC/comments/seed004
bbd8fb15-80ff-4533-8168-963459335391	Body types matter more than stats and that needs to change	Tried using a player with average body type and high stats vs a player with unique body type and lower stats. The unique body type player felt 10x better. Body types creating such a massive gap in feel despite lower stats is terrible design. If Im picking players based on body type over their actual ratings something is wrong.	seed	EAFC	1654	389	2025-02-16 10:45:00+00	stats_should_matter	GAMEPLAY	2026-04-17 21:03:53.93101+00	t	seed_026	https://reddit.com/r/EAFC/comments/seed026
d24d33d7-dffd-4fe8-880c-0fb0332f9540	Passing accuracy needs a complete rework	Aimed a pass to my right winger. Ball goes to my striker who is 45 degrees in the opposite direction. Passing assistance is supposed to help but it feels like it actively fights against your input. Either give us true manual passing that goes exactly where we aim, or fix assisted passing so it actually goes to the player were targeting.	seed	EAFC	1987	445	2025-02-13 14:00:00+00	where_did_that_pass_go	GAMEPLAY	2026-04-17 21:03:53.931006+00	t	seed_023	https://reddit.com/r/EAFC/comments/seed023
f5293757-a107-4245-85f2-22fb171d39fa	Manual GK movement nerf was the wrong fix	So EA decided to fix GK issues by reducing manual GK movement range. That was never the problem. The problem is that keeper AI and logic is broken. They dont position correctly, they dont come out for crosses, they dont react to near post shots. Reducing manual control just removed the only workaround we had for bad AI. Fix the root cause EA.	seed	EAFC	4521	1203	2025-01-26 13:00:00+00	gk_needs_rework	GAMEPLAY	2026-04-17 21:03:53.930981+00	t	seed_007	https://reddit.com/r/EAFC/comments/seed007
\.


--
-- Name: alert_rules alert_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alert_rules
    ADD CONSTRAINT alert_rules_pkey PRIMARY KEY (id);


--
-- Name: alerts alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_pkey PRIMARY KEY (id);


--
-- Name: api_users api_users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.api_users
    ADD CONSTRAINT api_users_pkey PRIMARY KEY (id);


--
-- Name: ingestion_logs ingestion_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ingestion_logs
    ADD CONSTRAINT ingestion_logs_pkey PRIMARY KEY (id);


--
-- Name: issue_events issue_events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.issue_events
    ADD CONSTRAINT issue_events_pkey PRIMARY KEY (id);


--
-- Name: issue_posts issue_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.issue_posts
    ADD CONSTRAINT issue_posts_pkey PRIMARY KEY (id);


--
-- Name: issue_posts issue_posts_processed_post_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.issue_posts
    ADD CONSTRAINT issue_posts_processed_post_id_key UNIQUE (processed_post_id);


--
-- Name: issues issues_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.issues
    ADD CONSTRAINT issues_pkey PRIMARY KEY (id);


--
-- Name: patches patches_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patches
    ADD CONSTRAINT patches_pkey PRIMARY KEY (id);


--
-- Name: processed_posts processed_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.processed_posts
    ADD CONSTRAINT processed_posts_pkey PRIMARY KEY (id);


--
-- Name: processed_posts processed_posts_raw_post_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.processed_posts
    ADD CONSTRAINT processed_posts_raw_post_id_key UNIQUE (raw_post_id);


--
-- Name: raw_posts raw_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_posts
    ADD CONSTRAINT raw_posts_pkey PRIMARY KEY (id);


--
-- Name: ix_alert_rules_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_alert_rules_category ON public.alert_rules USING btree (category);


--
-- Name: ix_alert_rules_subcategory; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_alert_rules_subcategory ON public.alert_rules USING btree (subcategory);


--
-- Name: ix_alerts_rule_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_alerts_rule_id ON public.alerts USING btree (rule_id);


--
-- Name: ix_api_users_username; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_api_users_username ON public.api_users USING btree (username);


--
-- Name: ix_issue_events_issue_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_issue_events_issue_id ON public.issue_events USING btree (issue_id);


--
-- Name: ix_issue_posts_issue_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_issue_posts_issue_id ON public.issue_posts USING btree (issue_id);


--
-- Name: ix_issues_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_issues_category ON public.issues USING btree (category);


--
-- Name: ix_issues_severity; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_issues_severity ON public.issues USING btree (severity);


--
-- Name: ix_issues_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_issues_status ON public.issues USING btree (status);


--
-- Name: ix_issues_subcategory; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_issues_subcategory ON public.issues USING btree (subcategory);


--
-- Name: ix_processed_posts_category; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_processed_posts_category ON public.processed_posts USING btree (category);


--
-- Name: ix_processed_posts_severity_score; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_processed_posts_severity_score ON public.processed_posts USING btree (severity_score);


--
-- Name: ix_processed_posts_subcategory; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_processed_posts_subcategory ON public.processed_posts USING btree (subcategory);


--
-- Name: ix_raw_posts_subreddit; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_raw_posts_subreddit ON public.raw_posts USING btree (subreddit);


--
-- Name: alerts alerts_rule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_rule_id_fkey FOREIGN KEY (rule_id) REFERENCES public.alert_rules(id) ON DELETE CASCADE;


--
-- Name: processed_posts fk3k9p3hx0fydv0xbjxu4udbovi; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.processed_posts
    ADD CONSTRAINT fk3k9p3hx0fydv0xbjxu4udbovi FOREIGN KEY (raw_post_id) REFERENCES public.raw_posts(id);


--
-- Name: issue_events issue_events_issue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.issue_events
    ADD CONSTRAINT issue_events_issue_id_fkey FOREIGN KEY (issue_id) REFERENCES public.issues(id) ON DELETE CASCADE;


--
-- Name: issue_posts issue_posts_issue_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.issue_posts
    ADD CONSTRAINT issue_posts_issue_id_fkey FOREIGN KEY (issue_id) REFERENCES public.issues(id) ON DELETE CASCADE;


--
-- Name: issue_posts issue_posts_processed_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.issue_posts
    ADD CONSTRAINT issue_posts_processed_post_id_fkey FOREIGN KEY (processed_post_id) REFERENCES public.processed_posts(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 6hSDlTsjqyn7qrt4xH0BR7LOfx9U78AXAGpRaTpOJdYMOqdRzvT6ILef6vfhaU2

