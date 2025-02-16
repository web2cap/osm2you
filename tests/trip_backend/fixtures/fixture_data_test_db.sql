

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;



CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO DB_USER;


ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO DB_USER;


ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO DB_USER;


ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO DB_USER;


CREATE TABLE public.core_kind (
    id bigint NOT NULL,
    kind_class character varying(32) NOT NULL,
    priority smallint NOT NULL,
    value character varying(255) NOT NULL,
    kind_group_id bigint NOT NULL,
    tag_id bigint NOT NULL
);


ALTER TABLE public.core_kind OWNER TO DB_USER;


ALTER TABLE public.core_kind ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_kind_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.core_kindgroup (
    id bigint NOT NULL,
    name character varying(128) NOT NULL,
    descriptive_name character varying(128),
    icon character varying(100) NOT NULL,
    color character varying(20) NOT NULL
);


ALTER TABLE public.core_kindgroup OWNER TO DB_USER;


ALTER TABLE public.core_kindgroup ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_kindgroup_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.core_marker (
    id bigint NOT NULL,
    name character varying(255),
    location public.geometry(Point,4326) NOT NULL,
    osm_id bigint,
    add_date timestamp with time zone NOT NULL,
    author_id bigint
);


ALTER TABLE public.core_marker OWNER TO DB_USER;


ALTER TABLE public.core_marker ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_marker_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.core_markercluster (
    id bigint NOT NULL,
    location public.geometry(Point,4326) NOT NULL,
    square_size double precision NOT NULL,
    markers_count integer NOT NULL,
    update_date timestamp with time zone NOT NULL,
    CONSTRAINT core_markercluster_markers_count_check CHECK ((markers_count >= 0))
);


ALTER TABLE public.core_markercluster OWNER TO DB_USER;


ALTER TABLE public.core_markercluster ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_markercluster_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.core_markerkind (
    id bigint NOT NULL,
    kind_id bigint NOT NULL,
    marker_id bigint NOT NULL
);


ALTER TABLE public.core_markerkind OWNER TO DB_USER;


ALTER TABLE public.core_markerkind ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_markerkind_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.core_relatedmarkerscrap (
    id bigint NOT NULL,
    marker_id bigint NOT NULL,
    pack_index integer,
    CONSTRAINT core_relatedmarkerscrap_pack_index_check CHECK ((pack_index >= 0))
);


ALTER TABLE public.core_relatedmarkerscrap OWNER TO DB_USER;


ALTER TABLE public.core_relatedmarkerscrap ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_relatedmarkerscrap_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.core_story (
    id bigint NOT NULL,
    created timestamp with time zone NOT NULL,
    text text NOT NULL,
    author_id bigint NOT NULL,
    marker_id bigint NOT NULL,
    CONSTRAINT text_min_length CHECK ((length(text) >= 10))
);


ALTER TABLE public.core_story OWNER TO DB_USER;


ALTER TABLE public.core_story ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_story_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.core_tag (
    id bigint NOT NULL,
    created timestamp with time zone NOT NULL,
    name character varying(255) NOT NULL,
    display_name character varying(255),
    CONSTRAINT name_min_length CHECK ((length((name)::text) >= 1))
);


ALTER TABLE public.core_tag OWNER TO DB_USER;


ALTER TABLE public.core_tag ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.core_tagvalue (
    id bigint NOT NULL,
    created timestamp with time zone NOT NULL,
    value character varying(255),
    marker_id bigint NOT NULL,
    tag_id bigint NOT NULL,
    CONSTRAINT value_min_length CHECK ((length((value)::text) >= 1))
);


ALTER TABLE public.core_tagvalue OWNER TO DB_USER;


ALTER TABLE public.core_tagvalue ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_tagvalue_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.core_updatedmarkercluster (
    id bigint NOT NULL,
    location public.geometry(Point,4326) NOT NULL,
    square_size double precision NOT NULL,
    markers_count integer NOT NULL,
    update_date timestamp with time zone NOT NULL,
    CONSTRAINT core_updatedmarkercluster_markers_count_check CHECK ((markers_count >= 0))
);


ALTER TABLE public.core_updatedmarkercluster OWNER TO DB_USER;


ALTER TABLE public.core_updatedmarkercluster ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_updatedmarkercluster_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.core_user (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    last_name character varying(150) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    email character varying(254) NOT NULL,
    username character varying(150),
    first_name character varying(150) NOT NULL,
    bio text,
    instagram character varying(64),
    telegram character varying(64),
    facebook character varying(254)
);


ALTER TABLE public.core_user OWNER TO DB_USER;


CREATE TABLE public.core_user_groups (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.core_user_groups OWNER TO DB_USER;


ALTER TABLE public.core_user_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



ALTER TABLE public.core_user ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.core_user_user_permissions (
    id bigint NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.core_user_user_permissions OWNER TO DB_USER;


ALTER TABLE public.core_user_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.core_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO DB_USER;


ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.django_celery_beat_clockedschedule (
    id integer NOT NULL,
    clocked_time timestamp with time zone NOT NULL
);


ALTER TABLE public.django_celery_beat_clockedschedule OWNER TO DB_USER;


ALTER TABLE public.django_celery_beat_clockedschedule ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_celery_beat_clockedschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.django_celery_beat_crontabschedule (
    id integer NOT NULL,
    minute character varying(240) NOT NULL,
    hour character varying(96) NOT NULL,
    day_of_week character varying(64) NOT NULL,
    day_of_month character varying(124) NOT NULL,
    month_of_year character varying(64) NOT NULL,
    timezone character varying(63) NOT NULL
);


ALTER TABLE public.django_celery_beat_crontabschedule OWNER TO DB_USER;


ALTER TABLE public.django_celery_beat_crontabschedule ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_celery_beat_crontabschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.django_celery_beat_intervalschedule (
    id integer NOT NULL,
    every integer NOT NULL,
    period character varying(24) NOT NULL
);


ALTER TABLE public.django_celery_beat_intervalschedule OWNER TO DB_USER;


ALTER TABLE public.django_celery_beat_intervalschedule ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_celery_beat_intervalschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.django_celery_beat_periodictask (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    task character varying(200) NOT NULL,
    args text NOT NULL,
    kwargs text NOT NULL,
    queue character varying(200),
    exchange character varying(200),
    routing_key character varying(200),
    expires timestamp with time zone,
    enabled boolean NOT NULL,
    last_run_at timestamp with time zone,
    total_run_count integer NOT NULL,
    date_changed timestamp with time zone NOT NULL,
    description text NOT NULL,
    crontab_id integer,
    interval_id integer,
    solar_id integer,
    one_off boolean NOT NULL,
    start_time timestamp with time zone,
    priority integer,
    headers text NOT NULL,
    clocked_id integer,
    expire_seconds integer,
    CONSTRAINT django_celery_beat_periodictask_expire_seconds_check CHECK ((expire_seconds >= 0)),
    CONSTRAINT django_celery_beat_periodictask_priority_check CHECK ((priority >= 0)),
    CONSTRAINT django_celery_beat_periodictask_total_run_count_check CHECK ((total_run_count >= 0))
);


ALTER TABLE public.django_celery_beat_periodictask OWNER TO DB_USER;


ALTER TABLE public.django_celery_beat_periodictask ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_celery_beat_periodictask_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.django_celery_beat_periodictasks (
    ident smallint NOT NULL,
    last_update timestamp with time zone NOT NULL
);


ALTER TABLE public.django_celery_beat_periodictasks OWNER TO DB_USER;


CREATE TABLE public.django_celery_beat_solarschedule (
    id integer NOT NULL,
    event character varying(24) NOT NULL,
    latitude numeric(9,6) NOT NULL,
    longitude numeric(9,6) NOT NULL
);


ALTER TABLE public.django_celery_beat_solarschedule OWNER TO DB_USER;


ALTER TABLE public.django_celery_beat_solarschedule ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_celery_beat_solarschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO DB_USER;


ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO DB_USER;


ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);



CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO DB_USER;




INSERT INTO public.core_kind (id, kind_class, priority, value, kind_group_id, tag_id) VALUES
(65, 'related', 2, 'bus_station', 19, 137),
(104, 'main', 0, 'camp_site', 29, 9);

INSERT INTO public.core_kindgroup (id, name, descriptive_name, icon, color) VALUES
(19, 'transportation', 'Transportation', 'fa-bus', 'blue'),
(29, 'camp_site', 'Camping sites', 'fa-tree', 'green');

INSERT INTO public.core_marker (id, name, location, osm_id, add_date, author_id) VALUES
(1, 'Test Marker Iceland', '0101000020E6100000005246B0526732C0375F5BEBB2355040', NULL, '2024-10-11 11:49:06.750537+00', 2),
(2, 'Test Marker Hiking Lake', '0101000020E610000080C368AFC7105BC07D51B7203AFE4A40', NULL, '2024-10-11 11:50:24.175892+00', 1);

INSERT INTO public.core_tag (id, created, name, display_name) VALUES
(9, '2023-12-22 10:07:13.275+00', 'tourism', 'Tourism'),
(137, '2023-12-22 10:07:13.275+00', 'amenity', 'Amenity');

INSERT INTO public.core_user (id, password, last_login, is_superuser, last_name, is_staff, is_active, date_joined, email, username, first_name, bio, instagram, telegram, facebook) VALUES
(1, 'pbkdf2_sha256$600000$KGkfKj4V1fuDCxP6tI79hq$KIxdlEQSmzsLcYRbjLAqNr7T8Nik3+VquMO1chFTOmU=', '2024-10-11 11:45:11.813748+00', TRUE, '', TRUE, TRUE, '2024-10-11 11:38:53.149469+00', 'super@test.py', 'hunter1231', '', NULL, NULL, NULL, NULL),
(2, 'pbkdf2_sha256$600000$UtW5FNbL5ggC2FhfthGAbA$uCkyp3G5G4Im2GJ2YR64mBzOSbxAWsFQBJcmzemksk8=', NULL, FALSE, '', FALSE, TRUE, '2024-10-11 11:46:06.33756+00', 'user@test.py', 'hunter1232', 'User', NULL, NULL, NULL, NULL),
(3, 'pbkdf2_sha256$600000$5cjP54QuTe76FyL0IQcxE2$oFlS1zig2V8sId6KKFocVqBy32f28qUOIuFDnqI7kSQ=', NULL, FALSE, '', FALSE, FALSE, '2024-10-11 11:46:53.36226+00', 'inactive@test.py', 'hunter1233', 'Inactive', NULL, NULL, NULL, NULL);


ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);



ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);



ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);



ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);



ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);



ALTER TABLE ONLY public.core_kind
    ADD CONSTRAINT core_kind_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.core_kindgroup
    ADD CONSTRAINT core_kindgroup_name_key UNIQUE (name);



ALTER TABLE ONLY public.core_kindgroup
    ADD CONSTRAINT core_kindgroup_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.core_marker
    ADD CONSTRAINT core_marker_location_key UNIQUE (location);



ALTER TABLE ONLY public.core_marker
    ADD CONSTRAINT core_marker_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.core_markercluster
    ADD CONSTRAINT core_markercluster_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.core_markerkind
    ADD CONSTRAINT core_markerkind_marker_id_key UNIQUE (marker_id);



ALTER TABLE ONLY public.core_markerkind
    ADD CONSTRAINT core_markerkind_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.core_relatedmarkerscrap
    ADD CONSTRAINT core_relatedmarkerscrap_marker_id_id_key UNIQUE (marker_id);



ALTER TABLE ONLY public.core_relatedmarkerscrap
    ADD CONSTRAINT core_relatedmarkerscrap_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.core_story
    ADD CONSTRAINT core_story_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.core_tag
    ADD CONSTRAINT core_tag_name_key UNIQUE (name);



ALTER TABLE ONLY public.core_tag
    ADD CONSTRAINT core_tag_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.core_tagvalue
    ADD CONSTRAINT core_tagvalue_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.core_updatedmarkercluster
    ADD CONSTRAINT core_updatedmarkercluster_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.core_user
    ADD CONSTRAINT core_user_email_key UNIQUE (email);



ALTER TABLE ONLY public.core_user_groups
    ADD CONSTRAINT core_user_groups_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.core_user_groups
    ADD CONSTRAINT core_user_groups_user_id_group_id_c82fcad1_uniq UNIQUE (user_id, group_id);



ALTER TABLE ONLY public.core_user
    ADD CONSTRAINT core_user_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.core_user_user_permissions
    ADD CONSTRAINT core_user_user_permissions_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.core_user_user_permissions
    ADD CONSTRAINT core_user_user_permissions_user_id_permission_id_73ea0daa_uniq UNIQUE (user_id, permission_id);



ALTER TABLE ONLY public.core_user
    ADD CONSTRAINT core_user_username_key UNIQUE (username);



ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.django_celery_beat_clockedschedule
    ADD CONSTRAINT django_celery_beat_clockedschedule_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.django_celery_beat_crontabschedule
    ADD CONSTRAINT django_celery_beat_crontabschedule_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.django_celery_beat_intervalschedule
    ADD CONSTRAINT django_celery_beat_intervalschedule_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_celery_beat_periodictask_name_key UNIQUE (name);



ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_celery_beat_periodictask_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.django_celery_beat_periodictasks
    ADD CONSTRAINT django_celery_beat_periodictasks_pkey PRIMARY KEY (ident);



ALTER TABLE ONLY public.django_celery_beat_solarschedule
    ADD CONSTRAINT django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq UNIQUE (event, latitude, longitude);



ALTER TABLE ONLY public.django_celery_beat_solarschedule
    ADD CONSTRAINT django_celery_beat_solarschedule_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);



ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);



ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);



ALTER TABLE ONLY public.core_kind
    ADD CONSTRAINT unique_kind_tag UNIQUE (tag_id, value);



ALTER TABLE ONLY public.core_tagvalue
    ADD CONSTRAINT unique_marker_tag UNIQUE (tag_id, marker_id);



CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);



CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);



CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);



CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);



CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);



CREATE INDEX core_kind_kind_group_id_ec9e3ea0 ON public.core_kind USING btree (kind_group_id);



CREATE INDEX core_kind_tag_id_85e8fb40 ON public.core_kind USING btree (tag_id);



CREATE INDEX core_kindgroup_name_2602cacf_like ON public.core_kindgroup USING btree (name varchar_pattern_ops);



CREATE INDEX core_marker_author_id_8e76ec4b ON public.core_marker USING btree (author_id);



CREATE INDEX core_marker_location_b7673d15_id ON public.core_marker USING gist (location);



CREATE INDEX core_markercluster_location_bdc058cc_id ON public.core_markercluster USING gist (location);



CREATE INDEX core_markerkind_kind_id_012b0d83 ON public.core_markerkind USING btree (kind_id);



CREATE INDEX core_story_author_id_1254658c ON public.core_story USING btree (author_id);



CREATE INDEX core_story_created_95090c50 ON public.core_story USING btree (created);



CREATE INDEX core_story_marker_id_6b2e7c08 ON public.core_story USING btree (marker_id);



CREATE INDEX core_tag_created_7fde7c4c ON public.core_tag USING btree (created);



CREATE INDEX core_tag_name_5f34f44c_like ON public.core_tag USING btree (name varchar_pattern_ops);



CREATE INDEX core_tagvalue_created_53e8629b ON public.core_tagvalue USING btree (created);



CREATE INDEX core_tagvalue_marker_id_d26e4730 ON public.core_tagvalue USING btree (marker_id);



CREATE INDEX core_tagvalue_tag_id_4a322e69 ON public.core_tagvalue USING btree (tag_id);



CREATE INDEX core_updatedmarkercluster_location_e7d76560_id ON public.core_updatedmarkercluster USING gist (location);



CREATE INDEX core_user_email_92a71487_like ON public.core_user USING btree (email varchar_pattern_ops);



CREATE INDEX core_user_groups_group_id_fe8c697f ON public.core_user_groups USING btree (group_id);



CREATE INDEX core_user_groups_user_id_70b4d9b8 ON public.core_user_groups USING btree (user_id);



CREATE INDEX core_user_user_permissions_permission_id_35ccf601 ON public.core_user_user_permissions USING btree (permission_id);



CREATE INDEX core_user_user_permissions_user_id_085123d3 ON public.core_user_user_permissions USING btree (user_id);



CREATE INDEX core_user_username_36e4f7f7_like ON public.core_user USING btree (username varchar_pattern_ops);



CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);



CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);



CREATE INDEX django_celery_beat_periodictask_clocked_id_47a69f82 ON public.django_celery_beat_periodictask USING btree (clocked_id);



CREATE INDEX django_celery_beat_periodictask_crontab_id_d3cba168 ON public.django_celery_beat_periodictask USING btree (crontab_id);



CREATE INDEX django_celery_beat_periodictask_interval_id_a8ca27da ON public.django_celery_beat_periodictask USING btree (interval_id);



CREATE INDEX django_celery_beat_periodictask_name_265a36b7_like ON public.django_celery_beat_periodictask USING btree (name varchar_pattern_ops);



CREATE INDEX django_celery_beat_periodictask_solar_id_a87ce72c ON public.django_celery_beat_periodictask USING btree (solar_id);



CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);



CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);



ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_core_user_id FOREIGN KEY (user_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.core_kind
    ADD CONSTRAINT core_kind_kind_group_id_ec9e3ea0_fk_core_kindgroup_id FOREIGN KEY (kind_group_id) REFERENCES public.core_kindgroup(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.core_kind
    ADD CONSTRAINT core_kind_tag_id_85e8fb40_fk_core_tag_id FOREIGN KEY (tag_id) REFERENCES public.core_tag(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.core_marker
    ADD CONSTRAINT core_marker_author_id_8e76ec4b_fk_core_user_id FOREIGN KEY (author_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.core_markerkind
    ADD CONSTRAINT core_markerkind_kind_id_012b0d83_fk_core_kind_id FOREIGN KEY (kind_id) REFERENCES public.core_kind(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.core_markerkind
    ADD CONSTRAINT core_markerkind_marker_id_b1d2f0dc_fk_core_marker_id FOREIGN KEY (marker_id) REFERENCES public.core_marker(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.core_relatedmarkerscrap
    ADD CONSTRAINT core_relatedmarkerscrap_marker_id_2e7024a5_fk_core_marker_id FOREIGN KEY (marker_id) REFERENCES public.core_marker(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.core_story
    ADD CONSTRAINT core_story_author_id_1254658c_fk_core_user_id FOREIGN KEY (author_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.core_story
    ADD CONSTRAINT core_story_marker_id_6b2e7c08_fk_core_marker_id FOREIGN KEY (marker_id) REFERENCES public.core_marker(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.core_tagvalue
    ADD CONSTRAINT core_tagvalue_marker_id_d26e4730_fk_core_marker_id FOREIGN KEY (marker_id) REFERENCES public.core_marker(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.core_tagvalue
    ADD CONSTRAINT core_tagvalue_tag_id_4a322e69_fk_core_tag_id FOREIGN KEY (tag_id) REFERENCES public.core_tag(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.core_user_groups
    ADD CONSTRAINT core_user_groups_group_id_fe8c697f_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.core_user_groups
    ADD CONSTRAINT core_user_groups_user_id_70b4d9b8_fk_core_user_id FOREIGN KEY (user_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.core_user_user_permissions
    ADD CONSTRAINT core_user_user_permi_permission_id_35ccf601_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.core_user_user_permissions
    ADD CONSTRAINT core_user_user_permissions_user_id_085123d3_fk_core_user_id FOREIGN KEY (user_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_core_user_id FOREIGN KEY (user_id) REFERENCES public.core_user(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_celery_beat_p_clocked_id_47a69f82_fk_django_ce FOREIGN KEY (clocked_id) REFERENCES public.django_celery_beat_clockedschedule(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_celery_beat_p_crontab_id_d3cba168_fk_django_ce FOREIGN KEY (crontab_id) REFERENCES public.django_celery_beat_crontabschedule(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_celery_beat_p_interval_id_a8ca27da_fk_django_ce FOREIGN KEY (interval_id) REFERENCES public.django_celery_beat_intervalschedule(id) DEFERRABLE INITIALLY DEFERRED;



ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_celery_beat_p_solar_id_a87ce72c_fk_django_ce FOREIGN KEY (solar_id) REFERENCES public.django_celery_beat_solarschedule(id) DEFERRABLE INITIALLY DEFERRED;



