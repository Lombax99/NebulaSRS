
### DB da utilizzare?
Avevamo tre possibilità: postgres, azure sql e mongodb. abbiamo scelto postgres, poiché è SEMPRE conforme  alle proprietà ACID, a differenza di Mongo che non lo è e azure sql, che lo è solo con determinati motori di archiviazione

### Libreria python da usare?
Le possibilità erano due:
- psycop2 --> libreria python SOLO per il collegamento a postgres. 
- SQLAlchemy --> ORM che permette il collegamento a diversi tipi di db. Abbiamo scelto questa, perché, a differenza di psycopg, ci permette di gestire i dati immagazzinati nel db, come oggetti, riducendo il numero di query da progettare per ottenere le info. Inoltre, opera a stretto contatto con Flask, il framework che abbiamo scelto di utilizzare per la nostra webapp

>[!check]- GESTIONE CREDENZIALI
>
> Viene fatto uso della sottolibreria flask_bcrypt per salvare le password nel db in maniera sicura: la funzione generate_password_hash permette di generare un dato di tipo byte, che sarebbe l'hash della password, così da non salvarla in chiaro. Un'altra funzione è check_password_hash, che permette di verificare l'uguaglianza tra l'hash della password di un utente e la password candidata, inserita al momento del login.
> 
> Inoltre, si verifica che l'utente stia effettuando il primo accesso, in modo tale da chiedergli di cambiare la password: dato che è l'admin a creare dei nuovi profili per gli utenti, esso creerà anche una password temporanea. Nel db gestiremo due password: quella effettiva e quella assegnata dall'admin. La password effettiva è uguale a quella assegnata dall'admin, allora si chiederà di cambiare la password, controllando che non sia pari a quella vecchia.

>[!check] GENERAZIONE E DOWNLOAD CERTIFICATI TEMPORANEI
>
>L'idea sarebbe quella di utilizzare Tkinter per far scegliere all'utente dove salvare i cert tramite UI. Tuttavia, Azure presenta problemi nella import di tale libreria, sebbene il download viene eseguito con successo. 
>
>Bisognerebbe trovare un modo per far salvare direttamente tutto nella cartella di download, rendendo il suo percorso system independent...
>
>**SOLUZIONE**: non appena genera cert e key, li pone in un file zip e li fa scaricare direttamente nella cartella dei Download, attraverso l'utilizzo del metodo *send_file* di Flask.






