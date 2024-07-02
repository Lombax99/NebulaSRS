Lasciare che gli utenti si autentichino ad un’applicazione solo con username e password, risulta essere molto rischioso, perché quando la password viene compromessa, l’aggressore ottiene l’accesso completo. Per ridurre questo rischio, le applicazioni attente alla sicurezza, possono implementare l’autenticazione a più fattori, che richiede all'utente di fornire oltre all’username e alla password, anche un ulteriore informazione, che può essere per esempio una password monouso (token).

L’idea delle password monouso è che esse siano valide solo per una singola sessione di accesso. Queste password vengono generate algoritmicamente da un dispositivo hardware o da un'app per smartphone. Per convalidare una password monouso, il server esegue lo stesso algoritmo e confronta il risultato con la password fornita dall'utente. Esistono diversi algoritmi per password monouso, alcuni proprietari, altri standard aperti come HOTP e TOTP.

- HOTP: genera token basati su un segreto e un contatore, entrambi noti al dispositivo di generazione token e al server di autenticazione. Ogni volta che viene utilizzato un token, il contatore viene incrementato su entrambi i lati e ciò fa sì che l'algoritmo generi un token diverso per il successivo tentativo di accesso.

- TOTP: anche questo standard utilizza un segreto condiviso, ma elimina il contatore, che viene sostituito dall'ora corrente. Con questo algoritmo il token cambia a intervalli di tempo predefiniti, solitamente ogni 30 secondi.

Il vantaggio di TOTP rispetto a HOTP è che i token sono una funzione del tempo e quindi cambiano costantemente. Ciò significa che anche se un aggressore può dare un'occhiata al token corrente visualizzato sulla tua app per smartphone, pochi secondi dopo verrà sostituito da uno nuovo. Lo svantaggio di TOTP è che richiede che il generatore di token e il server di autenticazione abbiano i loro orologi impostati approssimativamente sulla stessa ora. Questo non è un problema per lo smartphone, ma sul server è consigliabile eseguire un client NTP per evitare che l'orologio si sposti.

### Esempio di seguito, usa TOTP:
Per questa applicazione, ho utilizzato Flask-SQLAlchemy, Flask-Login, Flask-WTF e Flask-Bootstrap. Per quanto riguarda, l’implementazione dell’algoritmo TOTP, andiamo ad usare il pacchetto **onetimepass** (piccola libreria che supporta HOTP e TOTP, ed è compatibile con **Python 2** e **3.**
Ora vediamo le modifiche apportate nel modello Utente:
```
import os 
import base64 
import onetimepass

class User(UserMixin, db.Model): 
# ... 
otp_secret = db.Column(db.String(16))

	def __init__(self, **kwargs): 
		super(User, self).__init__(**kwargs) 
		if self.otp_secret is None: 
		# generate a random secret 
		self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8') 
		
		# ...
		
def get_totp_uri(self): 
	return 'otpauth://totp/2FA-Demo:{0}?secret={1}&issuer=2FA-Demo' \
	.format(self.username, self.otp_secret)

def verify_totp(self, token): 
	return onetimepass.valid_totp(token, self.otp_secret)
		
```

Viene aggiunto:

- ***otp_secret:*** memorizza il token condiviso che l’algoritmo TOTP usa come imput. Questa dovrebbe essere una stringa binaria di lunghezza 10, codificata come stringa _base32,_ il che la rende una stringa stampabile con 16 caratteri.
- Costruttore *_init__:* Il costruttore della classe User chiama il costruttore della classe base con super (User, self).init(kwargs). Poi fa un controllo, che se otp_secret è none viene generato un segreto casuale. 
- La _funzione **get_totp_uri()**_ restituisce un URI di autenticazione. Questa viene usato per trasferire il segreto condiviso e le informazioni aggiuntive dell’account allo smartphone. L’URI verrà reso come un codice QR, che bisogna scansionare col telefono. Di seguito mostriamo la struttura dell’URI:
```
otpauth://<protocol>/<service-name>:<user-account>?secret=<shared-secret>&issuer=<service-name>

```
- Struttura:
	- Protocol: TOTP o HOTP
	- Service Name: nome dell’applicazione a cui l’utente si sta autenticando
	- User_account: nome utente, email o qualsiasi cosa identifichi l’account utente
	- Shared_secret: codice usato per inizializzare l’algoritmo del generatore di token
	- issuer: impostato di solito sul nome del servizio
	- period: facoltativo, può essere usato per modificare l’intervallo per le modifiche del token (default 30 secondi).

- Funzione **verify_totp()**: funzione accetta un token come input e lo convalida utilizzando il supporto fornito dal pacchetto onetimepass. 

### Registrazione
Ci sono due possibilità:

- Lasciare all’utente la cosa che una volta che si è registrato decide lui se abilitare autenticazione a due fattori
- Rendere l’autenticazione a due fattori obbligatoria e quindi incorporarla nel processo di registrazione

Nell'esempio che vedremo, si opta per la seconda cosa, ovvero una volta registrato, all’utente viene mostrata una pagina di configurazione dell’autenticazione a due fattori, che si presenta così:
![[Pasted image 20240702172108.png]]

Qui l'utente deve avviare l'app del generatore di token sullo smartphone e usarla per scansionare il codice QR. Questo è tutto ciò che serve per registrare il segreto condiviso e le informazioni dell'account sul telefono. Dopo aver completato questo passaggio, l'utente può andare alla pagina di accesso e accedere utilizzando password e token per la prima volta.

Quello che si deve fare innanzitutto è modificare il **percorso di registrazione originale,** in modo tale da reindirizzare ad un nuovo percorso chiamato per esempio: _two_factor_setup._ Prima del reindirizzamento, aggiunge _username_ alla sessione utente, in modo che la pagina del codice QR sappia quale utente si sta registrando:

```
@app.route('/register', methods=['GET', 'POST'])
def register():
	#...
	form = RegisterForm() 
	if form.validate_on_submit(): 
	# ...

	# redirect to the two-factor auth page, passing username in session 
	session['username'] = user.username 
	return redirect(url_for('two_factor_setup')) 
return render_template('register.html', form=form)	
```

Implementazione del **two_factor_setup()**:
```
@app.route('/twofactor') 
def two_factor_setup(): 
	if 'username' not in session: 
	return redirect(url_for('index')) 
user = User.query.filter_by(username=session['username']).first() 
if user is None: 
	return redirect(url_for('index')) 
	# since this page contains the sensitive qrcode, make sure the browser 
	# does not cache it 
	return render_template('two-factor-setup.html'), 200, { 'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0'}
```

Dopo aver verificato che c’è un utente memorizzato nella sessione, questo assicura che l’utente esiste e se esiste esegue semplicemente il reindirizzamento di un nuovo modello denominato two_factor-setup.html. Questa pagina viene servita con intestazioni extra che indicano al browser di non effettuare alcuna memorizzazione nella cache. Il motivo è che questa pagina includerà un codice QR che può dare a un aggressore l'accesso ai token basati sul tempo, quindi è meglio prendere precauzioni e assicurarsi che non ci siano copie del codice QR perse in una cache.

**Two_factor-setup.html**
```
{% extends "base.html" %} 
{% import "bootstrap/wtf.html" as wtf %} 

{% block page_content %} 
	<h1>Two Factor Authentication Setup</h1> 
	<p>You are almost done! Please start FreeOTP on your smartphone and scan the following QR Code with it:</p> 
	<p><img id="qrcode" src="{{ url_for('qrcode') }}"></p> 
	<p>I'm done, take me to the <a href="{{ url_for('login') }}">Login</a> page!</p> 
	{% endblock %}
```
La pagina include un riferimento all'immagine del codice QR, ma l'URL per questa immagine non è un normale collegamento all'immagine, è un URL dinamico generato con la funzione di Flask _**url_for()**_. Questo perché l'immagine del codice QR deve essere generata specificamente per ogni utente, quindi viene invocata una route Flask per svolgere questo lavoro.

La route _qrcod_ è diverasa dalle altre, perché invece di restituire html, restituisce dati immagine (SVG). Per generare il codice QR sto usando il pacchetto pyqrcode, ecco il codice:

```
@app.route('/qrcode') 
def qrcode(): 
	if 'username' not in session: 
		abort(404) 
	user = User.query.filter_by(username=session['username']).first() 
	if user is None: 
		abort(404) 
	# for added security, remove username from session 
	del session['username'] 
	
	# render qrcode for FreeTOTP 
	url = pyqrcode.create(user.get_totp_uri()) 
	stream = BytesIO() 
	url.svg(stream, scale=5) 
	return stream.getvalue(), 200, { 
	'Content-Type': 'image/svg+xml', 
	'Cache-Control': 'no-cache, no-store, must-revalidate', 
	'Pragma': 'no-cache', 
	'Expires': '0'}
```
Qui controllo ancora una volta che il nome utente sia nella sessione e che sia un utente noto. Se uno di questi controlli fallisce, restituisco un codice di errore 404, che al browser sembrerà che abbia richiesto un file immagine che non esiste. Se l'utente è valido, lo rimuovo rapidamente dalla sessione, perché una volta che l'utente richiede il codice QR voglio assicurarmi che questa immagine non possa essere richiesta di nuovo. Ciò significa che se l'utente non esegue la scansione del codice QR in questa unica occasione in cui viene presentato, l'account non sarà accessibile.

### Login
L'unica parte che resta da fare è estendere il modulo di login per accettare un token e anche per convalidarlo. Ho detto sopra che le applicazioni possono scegliere di rendere l'autenticazione a due fattori facoltativa o obbligatoria. Se questa è resa facoltativa, il modulo di login non cambia, gli utenti inseriscono il loro nome utente e password e, dopo la verifica, l'applicazione può scoprire se l'autenticazione a due fattori è abilitata e presentare un modulo aggiuntivo in cui l'utente inserisce il token. Nel caso di questa applicazione, tuttavia, è richiesta la configurazione a due fattori per tutti gli account, quindi ho deciso di creare una singola finestra di dialogo di login che accetta nome utente, password e token insieme.

Aggiungo quindi il campo token nel modulo di login:
```
class LoginForm(FlaskForm): 
	username = StringField('Username', validators=[Required(), Length(1, 64)]) 
	password = PasswordField('Password', validators=[Required()]) 
	token = StringField('Token', validators=[Required(), Length(6, 6)]) 
	submit = SubmitField('Login')
```
E poi il percorso di accesso viene semplicemente migliorato con un ulteriore controllo di convalida
```
@app.route('/login', methods=['GET', 'POST']) 
def login(): 
	# ... 
	form = LoginForm() 
	if form.validate_on_submit(): 
		user = User.query.filter_by(username=form.username.data).first() 
		if user is None or not user.verify_password(form.password.data) or \ 
				not user.verify_totp(form.token.data):
			flash('Invalid username, password or token.') 
			return redirect(url_for('login')) 
			
		# log user in 
		# ... 
	return render_template('login.html', form=form)
```

