# Floor Plan Service (Servizio Planimetrie)

[![Stato del Servizio](https://img.shields.io/badge/status-stabile-green.svg)](https://shields.io/)
[![Linguaggio](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Flask-2.3-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Licenza](https://img.shields.io/badge/licenza-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Un microservizio visuale che mostra planimetrie di edifici e piani specifici, progettato per essere visualizzato su display dedicati.

![Showcase del Servizio FloorPlan](https://github.com/Mantineo-Massimo/DigitalSignageSuite/blob/master/docs/floorplan-showcase.png?raw=true)

---

## Indice

- [Panoramica del Progetto](#panoramica-del-progetto)
- [Caratteristiche Principali](#caratteristiche-principali)
- [Tecnologie Utilizzate](#tecnologie-utilizzate)
- [Struttura della Directory](#struttura-della-directory)
- [Struttura delle Immagini](#struttura-delle-immagini-importante)
- [Prerequisiti](#prerequisiti)
- [Guida all'Installazione](#guida-allinstallazione)
- [Accesso e Link Utili](#accesso-e-link-utili)
- [Variabili d'Ambiente](#variabili-dambiente)
- [Esecuzione dei Test](#esecuzione-dei-test)
- [Come Contribuire](#come-contribuire)
- [Licenza](#licenza)

---

## Panoramica del Progetto

Il `floorplan-service` fornisce un contesto visuale all'interno della Digital Signage Suite. Il suo scopo è mostrare una specifica immagine (planimetria, mappa, indicazione) a schermo intero, determinata dinamicamente dai parametri passati nell'URL. Questo permette di avere display dedicati a mostrare mappe di piani o percorsi specifici.

---

## Caratteristiche Principali

- ✅ **Visualizzazione Dinamica**: Mostra un'immagine diversa in base ai parametri `edificio`, `piano` e `nome_immagine` nell'URL.
- ⚙️ **Configurazione Flessibile**: La mappatura tra sigle degli edifici e nomi delle cartelle è gestita da variabili d'ambiente, senza hardcoding.
- 🛡️ **Sicurezza**: Include estensioni come `Talisman` e `CORS` e una Content Security Policy configurata per prevenire attacchi comuni.
- ❤️ **Health Check**: Endpoint `/health` per un facile monitoraggio dello stato del servizio.
- 📄 **Pagina di Errore Personalizzata**: Mostra una pagina 404 coerente con la grafica del sistema.
- 🐳 **Containerizzato**: Completamente gestito tramite Docker e Docker Compose per un deploy semplice e ripetibile.

---

## Tecnologie Utilizzate

- **Backend**: Python 3.11, Flask, Gunicorn
- **Containerizzazione**: Docker, Docker Compose
- **Sicurezza**: Flask-Talisman, Flask-Cors
- **Configurazione**: Python-dotenv

---

## Struttura della Directory

```
floorplan-service/
├── app/                  # Codice sorgente dell'applicazione Flask
│   ├── __init__.py       # Application factory (crea l'app Flask)
│   ├── config.py         # Carica e processa la configurazione da .env
│   └── routes.py         # Definisce tutte le rotte e la logica di ricerca immagini
│
├── tests/                # (da implementare) Test automatici
│
├── ui/                   # Tutti i file del front-end
│   ├── assets/           # Immagini delle planimetrie e assets comuni
│   ├── static/           # File CSS e JavaScript
│   ├── 404.html          # Template per la pagina di errore
│   └── index.html        # Template principale per la visualizzazione
│
├── .env.example          # File di esempio per le variabili d'ambiente
├── Dockerfile            # Istruzioni per costruire l'immagine Docker
├── requirements.txt      # Dipendenze Python
└── run.py                # Punto di ingresso per avviare il server Gunicorn
```

---

## Struttura delle Immagini (Importante!)

Perché il servizio funzioni, le immagini delle planimetrie devono essere organizzate in una struttura di cartelle specifica all'interno di `ui/assets/`. Il nome della cartella dell'edificio deve corrispondere a quanto configurato nel file `.env`.

```
ui/
└── assets/
    ├── building_A/
    │   ├── floor0/
    │   │   ├── A-S-1.png
    │   │   └── A-S-6.png
    │   ├── floor1/
    │   │   └── A-1-1.png
    │   └── floor_1/  <-- Nota: il nome della cartella deve corrispondere al parametro nell'URL
    │       └── A-1-6.jpg
    │
    ├── building_B/
    │   └── ...
    │
    └── building_SBA/
        └── ...
```

---

## Prerequisiti

- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose V2](https://docs.docker.com/compose/install/)

---

## Guida all'Installazione

1.  **Clona il Repository** e naviga nella cartella principale `DigitalSignageSuite`.

2.  **Configura le Variabili d'Ambiente**:
    - Naviga in `floorplan-service` e copia `.env.example` in `.env`.
    - Modifica `.env` se necessario per riflettere la tua configurazione di edifici e piani.

3.  **Prepara la Struttura delle Immagini**:
    - Assicurati di aver creato la struttura di cartelle e inserito le immagini come descritto nella sezione [Struttura delle Immagini](#struttura-delle-immagini-importante).

4.  **Avvia lo Stack Docker**:
    Dalla cartella principale `DigitalSignageSuite`, esegui:
    ```bash
    docker compose up --build -d
    ```

---

## Accesso e Link Utili 

- **Formato del Link per Planimetrie**:
  `http://<IP_SERVER>/floorplan/{EDIFICIO}/{PIANO}/{IMMAGINE}`
  - **Esempio:** `http://localhost/floorplan/A/floor_1/A-1-6`

- **Health Check**:
  `http://localhost/floorplan/health`

---

## Variabili d'Ambiente

- `BUILDINGS`: Lista di sigle di edifici e nomi di cartelle, separati da virgola (es. `A:building_A,B:building_B`).
- `ALLOWED_FLOORS`: Lista di tutti i numeri di piano permessi, separati da virgola (es. `-1,0,1,2,3`).

---

## Esecuzione dei Test

La suite di test per questo servizio non è ancora stata implementata.

---

## Come Contribuire

I contributi sono sempre i benvenuti! Segui la procedura standard di Fork & Pull Request.

---

## Licenza

Questo progetto è rilasciato sotto la Licenza MIT.