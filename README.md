# Floor Plan Service

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3-black?logo=flask)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)
![Status](https://img.shields.io/badge/Status-Production-brightgreen)

Un microservizio semplice e robusto progettato per visualizzare immagini di planimetrie a schermo intero, con selezione dinamica tramite URL.

![Showcase del Servizio](./docs/floorplan-showcase.png)

---

## Descrizione

Lo **Floor Plan Service** ha un unico scopo: mostrare un'immagine specifica di una planimetria. Il servizio è controllato interamente dall'URL, che specifica l'edificio, il piano e il nome dell'immagine da caricare.

Il backend Flask valida i parametri, controlla che il file esista e lo imposta come sfondo di una pagina HTML. La pagina include anche degli overlay informativi (orologio, data, nome del piano) con supporto bilingue.

---

## Funzionalità

* **Visualizzazione Dinamica**: Seleziona quale planimetria mostrare direttamente dall'URL.
* **Basato su File System**: L'aggiunta di nuove mappe è semplice: basta inserire i file immagine nelle cartelle corrette.
* **Overlay Bilingue**: L'orologio, la data e l'etichetta del piano cambiano lingua automaticamente (Italiano/Inglese).
* **Leggero e Veloce**: Nessun database o dipendenza complessa. Estremamente efficiente nel servire immagini statiche.
* **Servizio Dockerizzato**: Pronto per il deployment come container indipendente e gestito tramite Docker Compose.

---

## Setup & Struttura File

Questo servizio **non richiede un file `.env`**. La sua configurazione dipende interamente dalla struttura delle cartelle in cui vengono inserite le immagini.

Per aggiungere una planimetria, posiziona il file immagine nel seguente percorso:
`floorplan-service/ui/assets/<nome_cartella_edificio>/<nome_cartella_piano>/<file_immagine>`

* **Esempio di Struttura:**
    ```
    ui/assets/
    ├── 📂 building_a/
    │   ├── 📂 floor-1/
    │   │   └── 📄 blockA.jpg
    │   ├── 📂 floor0/
    │   └── 📂 floor1/
    │       └── 📄 3_docenti.jpg
    ├── 📂 building_b/
    └── 📂 building_sba/
    ```

I nomi delle immagini e degli edifici devono essere registrati nel file `run.py` per essere validati.

---

## Avvio

Questo servizio è parte della `DigitalSignageSuite` e viene avviato tramite il file `docker-compose.yml` nella directory principale.

1.  Assicurati di essere nella cartella `DigitalSignageSuite`.
2.  Esegui il comando:
    ```bash
    docker compose up --build -d
    ```
3.  Il servizio sarà accessibile sulla porta **8082**.

---

## Utilizzo e URL di Esempio

L'URL segue lo schema: `/<edificio>/floor<piano>/<nome_immagine>`

* **URL di Esempio:**
    ```
    http://localhost:8082/A/floor1/blockA
    ```

* **Parametri Disponibili:**

| Parametro      | Descrizione                                                              | Esempio Valido |
| :------------- | :----------------------------------------------------------------------- | :------------- |
| `building`     | La chiave breve dell'edificio (`A`, `B`, `SBA`).                         | `A`            |
| `floor`        | Il numero del piano (es. `-1`, `0`, `1`).                                | `1`            |
| `image_name`   | Il nome base del file immagine (senza estensione).                       | `blockA`       |

---

## Tecnologie Utilizzate

* **Backend**: Python, Flask, Gunicorn
* **Frontend**: HTML5, CSS3, JavaScript
* **Deployment**: Docker