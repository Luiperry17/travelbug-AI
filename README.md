# TravelBug AI — starter gratuito

## Funzionalità già pronte
- Web app responsive/PWA installabile; ricerche Google Flights, Skyscanner e Booking con link esterni.
- Monitor Python su feed JSON pubblici **autorizzati**; confronto con mediana di almeno 3 osservazioni precedenti per la stessa offerta.
- Notifiche Telegram per possibili anomalie (calo >=35%) e aggiornamento di `data/deals.json`.
- GitHub Actions ogni 6 ore (orario indicativo, le esecuzioni programmate possono ritardare).

**Importante:** non esiste ancora alcun feed prezzi configurato: `sources.json` è vuoto. Fino a quando non aggiungi una fonte gratuita che consenta accesso automatizzato e fornisca prezzi e URL, il monitor non troverà offerte. Nessun accesso automatizzato a Google Flights, Skyscanner, Booking o Airbnb è incluso. Il rilevatore confronta prezzi storici per la stessa chiave, non la media di mercato; segnala anomalie, non conferma error fares. Per tariffe con date o condizioni diverse servono ID distinti. La ricerca manuale apre pagine esterne e non garantisce precompilazione perfetta delle date.

## Pubblicazione (senza carta di credito)
1. Crea account GitHub gratuito, se necessario.
2. Crea repository **pubblico** chiamato `travelbug-ai`.
3. Carica tutti i file e cartelle di questo ZIP nella radice del repository (non la cartella esterna). GitHub web può non caricare direttamente cartelle vuote: qui tutte le cartelle contengono file.
4. Vai in **Settings → Pages → Build and deployment → Deploy from a branch**, scegli `main` e `/(root)`, poi Save.
5. Attendi la pubblicazione e visita `https://TUO_USERNAME.github.io/travelbug-ai/`.
6. In **Actions**, apri `TravelBug monitor`, abilita i workflow se richiesto e usa **Run workflow** per testarlo.

## Telegram (facoltativo)
1. Su Telegram apri **@BotFather**, crea un bot con `/newbot`, conserva il token **privatamente**.
2. Invia `/start` al tuo nuovo bot. Recupera il tuo chat ID tramite API `getUpdates` del tuo bot (non condividere token o chat ID in chat pubbliche).
3. In GitHub → **Settings → Secrets and variables → Actions**, crea due repository secrets: `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID`.
4. Esegui manualmente il workflow. Nessun messaggio verrà inviato finché non saranno presenti anomalie su dati reali.

## Configurare fonti
In `sources.json` inserisci ad esempio:
```json
[
  {"name":"Fonte autorizzata", "url":"https://esempio.org/feed-offerte.json"}
]
```
**L'URL qui sopra è illustrativo e non è una fonte funzionante.** La fonte deve consentire il download automatizzato. Il JSON remoto deve essere una lista di record con campi `id`, `title`, `kind` (`flight`/`hotel`), `price` (numero in EUR), `currency` (`EUR`), `date`, `url` (HTTPS). Non usare feed senza licenza o permesso. Non aggiungere token o API key ai file pubblici.

## Costi e limiti
Il prototipo usa solo software e servizi con opzioni gratuite, soggetti a quote e policy che possono cambiare. GitHub Actions sui repository pubblici standard ha condizioni d'uso proprie; GitHub Pages è pubblico. Nessuna promessa di copertura mondiale automatica finché non saranno collegate fonti autorizzate. Le notifiche Telegram richiedono un bot personale. GitHub Pages è hosting statico: il Python gira solo nelle Actions.

## Privacy e sicurezza
Non pubblicare token, chat ID, dati personali o credenziali nel repository. Le offerte pubblicate in `data/deals.json` sono visibili a chiunque visiti il sito. Usa soltanto fonti fidate; il motore accetta solo URL HTTPS, ma il gestore del repository deve verificare personalmente le fonti configurate.
