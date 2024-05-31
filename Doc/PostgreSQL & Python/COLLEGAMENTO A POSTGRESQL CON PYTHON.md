
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
- ##### Come inserire una riga nella tabella "MACCHINA"
  
		 INSERT INTO MACCHINA (descrizione, cert, conf) VALUES ('Laptop_1', pg_read_file('/tmp/laptop.crt')::bytea, pg_read_file('/tmp/config.yaml')::bytea);

	E' molto importante che file di config. e certificato si trovino all'interno della cartella /tmp/, poiché dato che tutti hanno il permesso di lettura per quella cartella, non ci sono problemi relativi ai permessi (= non scoreggia psql).
- ##### Come inserire una riga nella tabella "UTENTE"
  
		 INSERT INTO UTENTE (username)
		 VALUES ('username');
		 
- ##### Come inserire una riga in "USA"
  
		INSERT INTO USA (macchina_id, utente_id)`
		VALUES (1, 1);
		
#### QUERY: CONTROLLARE A QUALI MACCHINE HA ACCESSO UN UTENTE
		SELECT M.descrizione
		FROM MACCHINA AS M
		JOIN USA AS U ON M.id= U.macchina_id
		JOIN UTENTE AS UT ON U.utente_id = UT.id
		WHERE UT.username = 'username';


**N.B.**: Questa roba verrà automatizzata con gli script in Python


QUERY: VEDERE QUALI MACCHINE A QUALI UTENTI SONO ASSOCIATI 
Una cosa che il super admin potrebbe fare è quella di vedere, a quel determinato utente quali macchine sono associate. Questo viene fatto dal super admin, perchè un utente normale non ha bisogno di conoscere quali altre macchine siano assegnate ad altri utenti, poiché questo non è rilevante per le loro operazioni quotidiane. Da un punto di vista della sicurezza, le associazioni tra utenti e macchine, potrebbero avere delle informazioni sensibili , per esempio quali utenti sono responsabili di quali macchine. Quindi limitando l’accesso solo al superadmin si permette di ridurre il rischio di divulgare delle informazioni sensibili. Inoltre consente di mantenere una migliore tracciabilità delle azioni eseguite nel database. Se solo il superadmin ha accesso a questa informazione, è più facile identificare chi ha eseguito la query e quando è stata eseguita.

La query che permette di verificare quel determinato utente a quali macchine è associato è:
`SELECT u.username AS utente, string_agg(m.descrizione, ',') AS macchine_associate`
`FROM UTENTE u`
`JOIN USA us ON u.id = us.utente_id`
`JOIN MACCHINA m ON us.macchina_id = m.id`
`WHERE u.id = 'Id_utente'`
`GROUP BY u.username;`

Con la SELECT andiamo ad indicare quali colonne vogliamo selezionare nel risultato finale, e quindi stiamo selezionando il il nome utente dalla tabella UTENTE e usiamo la funzione string_agg per aggregare le descrizioni delle macchine dalla tabella Macchina. Con il FROM andiamo a selezionare da quali tabelle vogliamo selezionare i dati, e quindi li stiamo selezionando i dati dalla tabella UTENTE, dalla tabella USA, e da MACCHINA. Con la JOIN uniamo la tabella UTENTE con la tabella USA basandoci sull'ID dell'utente e uniamo la tabella USA con la tabella MACCHINA basandoci sull'ID della macchina. Con la where filtriamo i dati, ovvero limitiamo i risultati agli utenti con ID_Utente.`