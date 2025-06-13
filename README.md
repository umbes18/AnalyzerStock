# AnalyzerStock

Semplice applicazione web per analizzare una stock e stimarne il fair value.
L'app usa [Flask](https://flask.palletsprojects.com/) e recupera i dati da
[Yahoo Finance](https://finance.yahoo.com/) tramite la libreria `yfinance`.
Inoltre legge alcuni post da Reddit per calcolare un punteggio di sentiment.

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

## Avvio dell'app
```bash
python app.py
```
L'app sarà disponibile su `http://localhost:5000`.

## Funzionalità
- Inserimento ticker e analisi dei dati storici degli ultimi 5 anni.
- Calcolo di un valore equo semplificato basato su media storica e multipli.
- Analisi del sentiment Reddit (numero di post e media del punteggio VADER).
- Interfaccia minimale con animazione di fade‑in.

Questa è una base di partenza per creare uno strumento più avanzato.

## Test
Per eseguire i test automatizzati:
```bash
pytest
```
