- Test di distribuzione (azure load tester)
### Get started
[Quickstart: Run a load test on a website](https://go.microsoft.com/fwlink/?linkid=2225968)
[Identify performance bottlenecks](https://go.microsoft.com/fwlink/?linkid=2226130)
[Create a load test with a JMeter script](https://go.microsoft.com/fwlink/?linkid=2226327)
[Test applications with authentication](https://go.microsoft.com/fwlink/?linkid=2226328)
### Automate load testing
[Continuous load testing with GitHub Actions](https://go.microsoft.com/fwlink/?linkid=2226033)
[Continuous load testing with Azure Pipelines](https://go.microsoft.com/fwlink/?linkid=2226033)

- Test di sicurezza (owasp zap, snyk)
[Owasp Zap](https://www.zaproxy.org/)
[snyk](https://app.snyk.io/org/lombax99/)
[git guardian](https://dashboard.gitguardian.com/workspace/553882/get-started)


# Vulnerabilità trovate con Synk

Dopo aver effettuato l'accesso su Snyk tramite GitHub, e dopo aver importato la repo sul tool, sono state riscontrate le seguenti vulnerabilità:
- **Versioni non aggiornate di librerie**, le quali possono avere degli exploit. Fra i tanti, il più "importante" è quello dovuto alla versione della libreria werkzeug, usata nel nostro progetto: infatti, in questa versione è presente una vulnerabilità, dovuta all'uso di funzioni come *eval()*, che potrebbe rendere possibili attacchi di tipo **Code Injection**.
- L'esecuzione del comando *db.session.execute* di SQLAlchemy porta a **SQL Injection**. Ciò è dovuto ad input non "sanificati" dati in pasto a tale funzione. Pertanto, questa vulnerabilità è stata risolta utilizzando il parametro '%s' nella query, passando l'username prelevato dalla sessione come valore da sostituire nella query