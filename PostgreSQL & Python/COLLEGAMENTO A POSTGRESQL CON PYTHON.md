
#### DEPENDENCIES
- psycopg2: `pip install psycopg2`

#### STEPS

- Puoi seguire i passaggi da: https://www.postgresqltutorial.com/postgresql-python/connect/ (ovviamente evita i passaggi di creazione del DB, visto che li hai già fatti durante la [[CONFIGURAZIONE DI POSTGRESQL]])
- ##### COME HO CREATO LE TABELLE
	- **Tabella MACCHINA**
		- Specs: La MACCHINA deve avere un ID univoco, un certificato (CERT) e un file di configurazione (CONF).
		  
		  CREATE TABLE MACCHINA(
			id SERIAL PRIMARY KEY,
			descrizione VARCHAR(255),
			cert BYTEA NOT NULL, 
			conf BYTEA NOT NULL
		  );
		 - Spiegazione: 
			 - **SERIAL** = AUTO_INCREMENT di mySQL --> 0 sbatti a incrementare il contatore ogni volta che inseriamo qualcosa
			 - **PRIMARY KEY** = chiave primaria della tabella (d'ora in poi evito di rispiegarlo)
			 - **BYTEA** --> tipo per tenere i file
			 - **NOT NULL** --> NON DEVE ESSERE NULLO
	 - **Tabella UTENTE**
		 - Specs: il minimo indispensabile --> un ID e un USERNAME
		   
		 CREATE TABLE UTENTE (
		  id SERIAL PRIMARY KEY,
		  username VARCHAR(255) UNIQUE NOT NULL
		 );
		 - Spiegazione: 
			 - **UNIQUE** --> Non ci sarà alcun utente con lo stesso username
	 - **Tabella USA** --> Tabella associativa in cui salvo le coppie Utente - Macchina
		 - Specs: ID per ogni coppia + chiavi di UTENTE e MACCHINA
		   
		   CREATE TABLE USA (
            id SERIAL PRIMARY KEY,
            utente_id INTEGER NOT NULL REFERENCES UTENTE(id),
            macchina_id INTEGER NOT NULL REFERENCES MACCHINA(id),
            UNIQUE (utente_id, macchina_id)
            );
        - Spiegazione:
	        - **REFERENCES TABELLA(id)** --> Fa riferimento alla chiave primaria di un'altra tabella
	        - **UNIQUE (utente_id, macchina_id)** --> Non ci saranno mai due coppie uguali.
	    **N.B.**: Questa roba verrà automatizzata con gli script in Python

		 
