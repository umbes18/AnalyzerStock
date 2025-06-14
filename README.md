# AnalyzerStock

Semplice applicazione web per analizzare una stock e stimarne il fair value.
L'app usa [Flask](https://flask.palletsprojects.com/) e recupera i dati da
[Yahoo Finance](https://finance.yahoo.com/) tramite la libreria `yfinance`.
Inoltre legge post da più subreddit Reddit per calcolare un punteggio di sentiment
e un indicatore di engagement complessivo.

## Requisiti
- Python 3.8+
- Dipendenze elencate in `requirements.txt`

## Installazione
```bash
pip install -r requirements.txt
```

Per abilitare il sentiment da Reddit è necessario creare un'applicazione
su [Reddit](https://www.reddit.com/prefs/apps) e impostare le variabili
`REDDIT_CLIENT_ID` e `REDDIT_CLIENT_SECRET` (basta un account gratuito).

### Configurazione API di Reddit
1. Visita la pagina [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) ed effettua l'accesso.
2. Seleziona "create app" (o "create another app") per aggiungere una nuova applicazione.
3. Inserisci un nome a piacere, scegli il tipo **script** e imposta il *redirect URI* a `http://localhost`.
4. Dopo il salvataggio troverai sotto il nome dell'app il `client id` e il `client secret`.
5. Esporta questi valori come variabili d'ambiente prima di avviare l'applicazione:
   ```bash
   export REDDIT_CLIENT_ID=zr_wEJtRXyJIdXvu7gN11Q
   export REDDIT_CLIENT_SECRET=zWFiOQO2hich0nsw8a8UhFnau2J-yA
   export REDDIT_USER_AGENT="analyzerstock"
   ```

## Avvio dell'app
```bash
python app.py
```
L'app sarà disponibile su `http://localhost:5000`.

## Funzionalità
- Inserimento ticker e analisi dei dati storici degli ultimi 5 anni.
- Calcolo di un valore equo semplificato basato su media storica e multipli.
- Analisi del sentiment Reddit su più subreddit con calcolo di engagement e
  social score.
- Interfaccia minimale con animazione di fade‑in.

Questa è una base di partenza per creare uno strumento più avanzato.

## Test
Per eseguire i test automatizzati:
```bash
pytest
```
