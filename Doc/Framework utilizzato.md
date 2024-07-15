### Quali opzioni esistono per fare web development in python?
**Bottle** : smallest framework around (just one file). Best to use it for disposable tests, very small sites, etc. Fanstastique to teach and learn web programming.

**django** : most famous python framework. You can do pretty much everything with it, the ecosystem is fantastic (there is a3rd party django app for every thing, it's crazy) , how ever there is much to be learn before you can be productive with it. Use it if you have a complexe web site to code, with a lot custom logic. You will have to learn it in the end if you want to be serious about web programming in python.

**flask** : size is between django and bottle. Good for small to medium sites. Is now pretty well equiped with a lot of 3rd party plugins. Use it when you want to build a site with custom features but don't want to load the whole django thing.

**wep2py** : try to compete with django AND flask, but provide a different philosophy and includes a lot of graphical tools. Honestly, I'm not a fan of it's style, but some collegues like it, and it's perfectly capable.

**cherrypy** : a pure Python WSGI framework with very decent perfs without adding anything. But now that its server is available to be used separatly, I would recommand to just use bottle/flask/django with the server and forget about its framework part cause it's very verbose.

**pyramid** : strongest competitor to django in terme of features, it is much less monolithic and much more flexible. You got control. However, django components intégration make things easier, doc is better and it has a way bigger ecosystem. So I prefer django. But you can do everything django does with pyramid, it's a matter of taste.

**twisted** : asyncronous internet framework. You read it well : INTERNET framework, not WEB framework. You can do HTTP, of course, but also SSH, IMAP, FTP and so much more with it. Most powerful framwork of all, incredible performance, and the shittiest API ever. Learning/using twisted is like trying to fap with boxing gloves while saying the alphabet backward.

**tornado** : asynchronous web framework. Basically the current only nodejs competitor in pure Python (so no gevent, no extension, etc). The API is not fantastic, but not too hard and perfs are good. Websocket works out of the box.

**cyclone** : technically tornado running on the twisted event loop. Meaning you can use the easy tornado syntaxe for the web on a twisted setup, and still leverage tornado crazy tool box for other things. This is so advanced you should not even think about it.

**webpy** : very old. Use it only if you like it's syntaxe that feels like you are talking HTTP directly, but with a nice Python wrapper.

### I 3 big: Flask vs Django vs Web2py
- **Django** nasce con l’obiettivo di semplificare lo sviluppo web, permettendo agli sviluppatori di creare applicazioni web in modo rapido senza compromettere la qualità. La sua filosofia si basa su due principi fondamentali: la “riusabilità” del codice e la connessione “batterie incluse”, che significa che Django include tutto ciò di cui uno sviluppatore potrebbe aver bisogno per iniziare.
- Nato dalla visione di offrire uno strumento che potesse semplificare lo sviluppo web senza sacrificare la potenza, **Web2Py** si è rapidamente affermato come uno dei framework Python di riferimento. La sua filosofia centrale è quella di rendere lo sviluppo web accessibile a tutti, indipendentemente dal livello di esperienza, garantendo al contempo la sicurezza e la robustezza delle applicazioni create.
- **Flask** nasce come un progetto “aprile fool’s” (pesce d’aprile) ma si è rapidamente evoluto in uno dei framework web più popolari per Python. La sua filosofia principale è offrire una base solida per lo sviluppo web, ma al contempo rimanere estremamente leggero e modulare. Questo approccio “micro” permette agli sviluppatori di utilizzare solo ciò di cui hanno bisogno, senza l’ingombro di funzionalità non necessarie.

Maggiori informazioni al seguente [link](https://www.codemotion.com/magazine/it/backend-it/i-tre-giganti-dei-framework-python-django-web2py-e-flask/).

### Perchè scegliamo Flask
Usare Flask per creare l'interfaccia web potrebbe essere una scelta ragionevole per diverse ragioni:

1. **Semplicità e leggerezza**: Flask è un microframework web leggero per Python. È progettato per essere semplice da usare e facile da imparare.
2. **Flessibilità**: Flask è altamente flessibile e modulare. Puoi aggiungere le estensioni necessarie per gestire l'autenticazione, la gestione delle sessioni e altre funzionalità senza dover adottare un intero framework con funzionalità preconfezionate che potrebbero non essere necessarie.
3. **Azure e Flask**: Azure offre supporto per applicazioni Flask tramite Azure App Service, che semplifica il deployment e la gestione dell'applicazione web Flask su Azure.

Altri punti a nostro favore:
- Django ha una curva di apprendimento più ripida rispetto a Flask
- Il microframework di Flask potrebbe adattarsi bene al concetto di microservizi che si cerca di ottenere in cloud. Questo punto verrà confermato solo dopo aver accumulato abbastanza esperienza e aver lavorato un minimo al progetto.