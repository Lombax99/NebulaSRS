![[SchemaDB.png]]

CREATE TABLE UTENTE (
<<<<<<< Updated upstream
		  id SERIAL PRIMARY KEY,
		  nome VARCHAR(255) NOT NULL,
		  cognome VARCHAR(255) NOT NULL,
		  username VARCHAR(255) UNIQUE NOT ,
		  password VARCHAR(255)
		 );
=======
	id SERIAL PRIMARY KEY,
	nome VARCHAR(255) NOT NULL,
	cognome VARCHAR(255) NOT NULL,
	username VARCHAR(255) UNIQUE NOT NULL
	password VARCHAR(255)
 );
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
			id SERIAL NOT NULL,
			inout varchar(10) NOT NULL,
			conf_id INTEGER NOT NULL REFERENCES CONF(id),
			port VARCHAR(10),
			proto VARCHAR(10),
			host VARCHAR(255),
			ca_name VARCHAR(255),
			gruppi VARCHAR(500),
			cidr VARCHAR(20),
);

### Query  da fare

- mostrare le info nella tabella creata da pasquale: IP, descrizione
  
SELECT c.ip_addr, m.descrizione
FROM UTENTE u
JOIN USA as ua ON u.id = ua.macchina_id
JOIN MACCHINA as m ON ua.macchina_id = m.id
JOIN CONF as c ON m.conf = c.id
WHERE u.username = 'NOME_UTENTE';

- mostra le regole di firewall di una macchina di cui si conosce l'ip

SELECT *
FROM REGOLA AS R
JOIN CONF AS C ON C.ID = R.CONF_ID
WHERE C.IP_ADDR = 'IPADDR';
=======
	id SERIAL NOT NULL,
	inout varchar(10) NOT NULL,
	conf_id INTEGER NOT NULL REFERENCES CONF(id),
	port VARCHAR(10),
	proto VARCHAR(10),
	host VARCHAR(255),
	ca_name VARCHAR(255),
	gruppi VARCHAR(500),
	cidr VARCHAR(20),
);
>>>>>>> Stashed changes
