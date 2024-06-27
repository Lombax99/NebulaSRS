![[SchemaDB.png]]

CREATE TABLE UTENTE (
		  id SERIAL PRIMARY KEY,
		  nome VARCHAR(255) NOT NULL,
		  cognome VARCHAR(255) NOT NULL,
		  username VARCHAR(255) UNIQUE NOT NULL
		 );

CREATE TABLE MACCHINA(
			id SERIAL PRIMARY KEY,
			descrizione VARCHAR(255),
			cert  INTEGER NOT NULL REFERENCES CERT(id), 
			conf INTEGER NOT NULL REFERENCES CONF(id)
		  );

  CREATE TABLE USA (
            id SERIAL PRIMARY KEY,
            utente_id INTEGER NOT NULL REFERENCES UTENTE(id),
            macchina_id INTEGER NOT NULL REFERENCES MACCHINA(id),
            UNIQUE (utente_id, macchina_id)
            );

CREATE TABLE CERT(
			id SERIAL PRIMARY KEY,
			cifrato VARCHAR(512) NOT NULL
);

CREATE TABLE  CONF(
			id SERIAL PRIMARY KEY,
			ip_addr VARCHAR(20) UNIQUE NOT NULL,
			tcp_timeout VARCHAR(255),
			udp_timeout VARCHAR(255),
			def_timeout VARCHAR(255)
);

CREATE TABLE REGOLA(
			id UNIQUE NOT NULL,
			inout varchar(10) NOT NULL,
			conf_id INTEGER NOT NULL REFERENCES CONF(id),
			port VARCHAR(10),
			proto VARCHAR(10),
			host VARCHAR(255),
			ca_name VARCHAR(255),
			group VARCHAR(500),
			cidr VARCHAR(20),
);