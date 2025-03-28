CREATE SEQUENCE user_id_seq;
CREATE SEQUENCE locality_id_seq;
CREATE SEQUENCE locality_type_id_seq;
CREATE SEQUENCE region_id_seq;
CREATE SEQUENCE district_id_seq;
CREATE SEQUENCE educational_institution_id_seq;
CREATE SEQUENCE education_level_id_seq;
CREATE SEQUENCE education_direction_id_seq;
CREATE SEQUENCE habitation_id_seq;
CREATE SEQUENCE user_photo_id_seq;
CREATE SEQUENCE habitation_photo_id_seq;
CREATE SEQUENCE match_id_seq;
CREATE SEQUENCE message_id_seq;
CREATE SEQUENCE chat_id_seq;

CREATE TABLE IF NOT EXISTS district (
	id bigint NOT NULL UNIQUE DEFAULT nextval('district_id_seq'),
	name varchar(255) NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS region (
	id bigint NOT NULL UNIQUE DEFAULT nextval('region_id_seq'),
	name varchar(255) NOT NULL,
	district_id bigint NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (district_id) REFERENCES district(id)
);

CREATE TABLE IF NOT EXISTS locality_type (
	id bigint NOT NULL UNIQUE DEFAULT nextval('locality_type_id_seq'),
	name varchar(255) NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS education_level (
	id bigint NOT NULL UNIQUE DEFAULT nextval('education_level_id_seq'),
	title varchar(255) NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS locality (
	id bigint NOT NULL UNIQUE DEFAULT nextval('locality_id_seq'),
	type_id bigint NOT NULL,
	region_id bigint NOT NULL,
	name varchar(255) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (type_id) REFERENCES locality_type(id),
	FOREIGN KEY (region_id) REFERENCES region(id)
);

CREATE TABLE IF NOT EXISTS educational_institution (
	id bigint NOT NULL UNIQUE DEFAULT nextval('educational_institution_id_seq'),
	full_name varchar(255) NOT NULL,
	short_name varchar(255) NOT NULL,
	type bigint NOT NULL,
	region_id bigint NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (region_id) REFERENCES region(id)
);

CREATE TABLE IF NOT EXISTS education_direction (
	id bigint NOT NULL UNIQUE DEFAULT nextval('education_direction_id_seq'),
	code varchar (10) NOT NULL CHECK (code ~ '^\d\.\d\d\.\d\d\.\d\d$'),
	title varchar(255) NOT NULL,
	education_level_id bigint NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (education_level_id) REFERENCES education_level(id)
);

CREATE TABLE IF NOT EXISTS users (
	id bigint NOT NULL UNIQUE DEFAULT nextval('user_id_seq'),
	ei_id bigint,
	deleted boolean NOT NULL DEFAULT true,
	name varchar(255) NOT NULL,
	age bigint NOT NULL CHECK (age >= 18),
	email varchar(255) NOT NULL UNIQUE CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
	phone varchar(20) NOT NULL UNIQUE CHECK (phone ~ '^\+7\d{10}$'),
	vk_id varchar(100) NOT NULL UNIQUE,
	about varchar(255),
	locality_id bigint NOT NULL,
	password_hash varchar(255) NOT NULL,
	education_direction bigint,
	is_search boolean NOT NULL DEFAULT true,
	created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
	last_log_moment timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
	rating double precision,
	PRIMARY KEY (id),
	FOREIGN KEY (ei_id) REFERENCES educational_institution(id),
	FOREIGN KEY (locality_id) REFERENCES locality(id),
	FOREIGN KEY (education_direction) REFERENCES education_direction(id)
);

CREATE TABLE IF NOT EXISTS habitation (
	id bigint NOT NULL UNIQUE DEFAULT nextval('habitation_id_seq'),
	user_id bigint NOT NULL,
	address varchar(255) NOT NULL,
	geo_coords jsonb NOT NULL,
	link varchar(255) CHECK (link ~ '^(https?:\/\/)?(([a-zA-Z0-9-]+\.)?(avito\.ru|domclick\.ru|cian\.ru)|arenda\.yandex\.ru)(\/.*)?$'),
	created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS user_photo (
	id bigint NOT NULL UNIQUE DEFAULT nextval('user_photo_id_seq'),
	user_id bigint NOT NULL,
	file_name varchar(255) NOT NULL UNIQUE,
	created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS habitation_photo (
	id bigint NOT NULL UNIQUE DEFAULT nextval('habitation_photo_id_seq'),
	habitation_id bigint NOT NULL,
	file_name varchar(255) NOT NULL UNIQUE,
	created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	FOREIGN KEY (habitation_id) REFERENCES habitation(id)
);

CREATE TABLE IF NOT EXISTS match (
	id bigint NOT NULL UNIQUE DEFAULT nextval('match_id_seq'),
	user_id1 bigint NOT NULL,
	user_id2 bigint NOT NULL,
	habitation_id bigint,
	created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	FOREIGN KEY (user_id1) REFERENCES users(id),
	FOREIGN KEY (user_id2) REFERENCES users(id),
	FOREIGN KEY (habitation_id) REFERENCES habitation(id)
);

CREATE TABLE IF NOT EXISTS chat (
	id bigint NOT NULL UNIQUE DEFAULT nextval('chat_id_seq'),
	match_id bigint NOT NULL,
	created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	FOREIGN KEY (match_id) REFERENCES match(id)
);

CREATE TABLE IF NOT EXISTS message (
	id bigint NOT NULL UNIQUE DEFAULT nextval('message_id_seq'),
	message varchar(255) NOT NULL,
	user_id bigint NOT NULL,
	chat_id bigint NOT NULL,
	created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (id),
	FOREIGN KEY (user_id) REFERENCES users(id),
	FOREIGN KEY (chat_id) REFERENCES chat(id)
);

CREATE TABLE IF NOT EXISTS user_score (
	user_from_id bigint NOT NULL,
	user_to_id bigint NOT NULL,
	created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
	score bigint NOT NULL,
	PRIMARY KEY (user_from_id, user_to_id),
	FOREIGN KEY (user_from_id) REFERENCES users(id),
	FOREIGN KEY (user_to_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS habitation_response (
	created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
	habitation_id bigint NOT NULL,
	request_user_id bigint NOT NULL,
	PRIMARY KEY (habitation_id, request_user_id),
	FOREIGN KEY (habitation_id) REFERENCES habitation(id),
	FOREIGN KEY (request_user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS user_response (
	created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
	response_user_id bigint NOT NULL,
	request_user_id bigint NOT NULL,
	PRIMARY KEY (response_user_id, request_user_id),
	FOREIGN KEY (response_user_id) REFERENCES users(id),
	FOREIGN KEY (request_user_id) REFERENCES users(id)
);

CREATE UNIQUE INDEX user_id_idx ON users(id);
CREATE UNIQUE INDEX user_email_idx ON users(email);
CREATE UNIQUE INDEX user_phone_idx ON users(phone);
CREATE UNIQUE INDEX user_vk_id_idx ON users(vk_id);

CREATE UNIQUE INDEX locality_id_idx ON locality(id);

CREATE UNIQUE INDEX locality_type_id_idx ON locality_type(id);

CREATE UNIQUE INDEX region_id_idx ON region(id);

CREATE UNIQUE INDEX district_id_idx ON district(id);

CREATE UNIQUE INDEX educational_institution_id_idx ON educational_institution(id);

CREATE UNIQUE INDEX habitation_id_idx ON habitation(id);

CREATE UNIQUE INDEX user_photo_id_idx ON user_photo(id);

CREATE UNIQUE INDEX habitation_photo_id_idx ON habitation_photo(id);

CREATE UNIQUE INDEX match_id_idx ON match(id);

CREATE UNIQUE INDEX chat_id_idx ON chat(id);

CREATE UNIQUE INDEX message_id_idx ON message(id);

CREATE UNIQUE INDEX user_score_idx ON user_score(user_from_id, user_to_id);

CREATE UNIQUE INDEX habitation_response_idx ON habitation_response(habitation_id, request_user_id);

CREATE UNIQUE INDEX user_reponse_idx ON user_response(response_user_id, request_user_id);
