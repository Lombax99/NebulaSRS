# Prima versione

La versione embrionale del DB prevedeva solo tre tabelle, per effettuare dei test su assegnazione/revoca dei permessi di accesso a determinate macchine:
- MACCHINA, che includeva solamente un ID e il nome simbolico della macchina;
- UTENTE, che conteneva tutte le info necessarie per gestire gli utenti nel nostro sistema (nome, cognome, username, password);
- USA, una tabella associativa che è stata utile a risolvere la relazione N a N che legava le due tabelle di cui sopra. Essa contiene, oltre all'ID che identifica le entry, anche i riferimenti agli identificativi di utenti e macchine, con la peculiarità che la coppia (ID_UTENTE, ID_MACCHINA) sia unica all'interno della tabella. Ciò è stato ottenuto tramite l'utilizzo della clausola UNIQUE (utente_id, macchina_id).

![[ER_MODEL.png]]

### VANTAGGI:
- ##### Scalabilità:
	  Posso avere più macchine e più utenti, ma alla fine l'associazione è una sola, e giocando su di essa posso realizzare cose più complesse, senza stravolgere l'architettura.
- ##### Semplicità:
	  Posso gestire il database in maniera semplice ed efficiente, perché la struttura viene semplificata dall'utilizzo di un'entità centrale (es. USA).
- ##### Eliminazione della ridondanza
	  tramite l'utilizzo di UNIQUE

### SVANTAGGI:
- ##### Maggiore complessità delle query più articolate
	  Tuttavia, una volta trovata la query adatta alle nostre esigenze, potremmo inserirla in uno script e lanciarla in automatico quando l'admin ne fa richiesta.
- ##### Problemi nella cancellazione di entry nelle tabelle MACCHINA e UTENTE:
	  Provando a cancellare una entry in tali tabelle, se l'ID di tale entry è presente in una o più righe di USA, avremo dei problemi della cancellazione delle chiavi esterne in tale tabella. Tuttavia, questo problema è facilmente risolvibile tramite l'impiego della clausola **ON DELETE CASCADE**, in seguito alla definizione di ogni chiave esterna in USA.


# Seconda versione

![[SchemaDB.png]]

Man mano che si studiavano meglio i requisito del progetto, la struttura del database ha subito graduali modifiche, fino ad arrivare alla forma in foto. In questa seconda versione del DB sono stati aggiunte le tabelle **CERT** e **CONF**. Inizialmente avrebbero dovuto contenere i file di configurazione e i certificati veri e propri, sottoforma di BYTEA; tuttavia, data l'impossibilità di ottenere i permessi di superadmin, necessari al caricamento dei file su DB hostato in remoto, si è deciso di inserire:
- nella tabella CONF, alcune regole di configurazione, come quelle in foto, e l'ip address, unico all'interno della tabella. Questo, perché le regole TCP/UDP/DEFAULT TIMEOUT sono regole generali al di fuori delle regole di inbound ed outbound. 
- nella tabella CERT, il cifrato del certificato, cioè il contenuto del file .crt generato da Nebula. Si noti bene che tale tabella contiene solo i certificati PERMANENTI delle macchine, perché a seguito di analisi e chiarimenti con i tutor, abbiamo deciso che non sarebbe stato opportuno memorizzare gli short-lived certificates, essendo temporanei. Ciò, oltre a semplificare di molto la realizzazione del progetto, lo rende più leggero, evitando controlli regolari sui timestamp, che a questo punto sarebbero stati FONDAMENTALI per la gestione di tali cert, e chiamate continue al DB per gestire tali entry "volanti".

Inoltre, si può notare la presenza della tabella **REGOLA**, che contiene le regole di inbound e outbound relative alle macchine. Il collegamento tra macchine e regole è stato effettuato sfuttando la tabella **CONF** come **tabella associativa**, realizzando di fatto una relazione 1 a N, in cui:
- una macchina può avere una o più regole;
- una o più regole possono riferirsi ad una e una sola macchina.
Ovviamente, tramite l'utilizzo della clausola **ON DELETE CASCADE** si è evitato il problema descritto in precedenza per quanto riguarda la cancellazione di entry presenti anche nella tabella associativa.

## Versione finale

Durante lo sviluppo della Web App, ci siamo accorti che regole come  TCP/UDP/DEF TIMEOUT non erano necessarie al nostro goal; quindi, abbiamo deciso di rimuoverle. Tale rimozione ci ha portato a ragionare sull'effettiva utilità della tabella CONF che, a questo punto, avrebbe contenuto solamente l'indirizzo IP della macchina. Pertanto, abbiamo deciso di **eliminare questa tabella**, spostando l'informazione sull'IP nella tabella MACCHINA. Conseguentemente, si è cambiato il riferimento nella tabella REGOLA, facendolo puntare alla entry nella tabella MACCHINA, piuttosto che alla tabella CONF. In questo modo, non solo abbiamo tenuto salda la relazione 1 a N tra macchine e regole, ma abbiamo anche snellito il DB, semplificando sia la sua gestione che la progettazione e la stesura di alcune query, come quella relativa alle regole di firewall di ogni macchina.

![[DB_FINAL.png]]

Inoltre, sono stati aggiunti i campi AUTH ed ADMIN nella tabella UTENTE, per gestire l'attivazione della 2FA e l'assegnazione di privilegi di superadmin per gli user.