Lo script *download_files.py* si trova nella cartella *provasrs* nella repository principale.
### FUNZIONAMENTO
Lo script si collega al db e lancia la query `SELECT * FROM MACCHINA;`, che restituisce:
- id = row[0];
- descrizione = row[1];
- cert = row[2];
- conf = row[3].
Dopodiché, volta per volta lo script controlla che nella cartella di destinazione (*src*) i file non siano già presenti, altrimenti avvisa l'utente. Nel caso in cui non esistono, li scarica e li salva in quella cartella.

### SCELTA IMPLEMENTATIVA
Lo script controlla la presenza dei singoli file all'interno della cartella di destinazione, così che se uno c'è già e l'altro no, allora scarica quello che non c'è. Dopo di che, passa i seguenti parametri ad uno script che scarica effettivamente i file (sono 2 istruzioni in croce, ma così è più snello e più bello):
- percorso di destinazione;
- nome del file;
- dati recuperati dalla query.