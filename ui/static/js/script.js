/**
 * Script for the Floor Plan Display - UNIFIED TIME FINAL VERSION
 */
document.addEventListener('DOMContentLoaded', function() {
    // --- Riferimenti al DOM ---
    var dom = {
        clock: document.getElementById('clock'),
        date: document.getElementById('current-date'),
        label: document.getElementById('floor-label'),
        body: document.body
    };

    // --- Stato e Configurazione ---
    var state = {
        currentLanguage: 'it',
        timeDifference: 0 // Differenza tra ora del server e ora locale
    };

    var config = {
        // URL del nostro time service.
        timeServiceUrl: 'http://172.16.32.13/api/time/', 
        languageToggleInterval: 15, // in secondi
        dataRefreshInterval: 5 * 60 // Intervallo per risincronizzare l'ora
    };

    var translations = {
        it: {
            // Questi non sono più necessari per la data, ma li teniamo per l'etichetta del piano
            floor: "Piano",
            building: { "A": "Edificio A", "B": "Edificio B", "SBA": "Edificio SBA" }
        },
        en: {
            floor: "Floor",
            building: { "A": "Building A", "B": "Building B", "SBA": "Building SBA" }
        }
    };

    // NUOVA FUNZIONE per sincronizzare con il server
    function syncTimeWithServer() {
        fetch(config.timeServiceUrl)
            .then(function(response) {
                if (!response.ok) throw new Error('Time API not responding');
                return response.json();
            })
            .then(function(data) {
                var serverNow = new Date(data.time);
                var clientNow = new Date();
                state.timeDifference = serverNow - clientNow;
                dom.clock.style.color = ''; // Rimuove il colore rosso in caso di successo
                console.log('Time synchronized. Server/client difference:', state.timeDifference, 'ms');
            })
            .catch(function(error) {
                console.error('Could not sync time with server:', error);
                state.timeDifference = 0; // Fallback: usa l'ora locale in caso di errore
                dom.clock.style.color = 'red'; // Indica visivamente un problema
            });
    }

    /** MODIFICATO: Aggiorna l'orologio e la data usando l'ora locale di Roma */
    function updateSyncedElements() {
        var serverTime = new Date(new Date().getTime() + state.timeDifference);
        
        // --- Orologio (ora locale di Roma) ---
        var clockOptions = {
            timeZone: 'Europe/Rome',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        };
        dom.clock.textContent = serverTime.toLocaleTimeString('it-IT', clockOptions);

        // --- Data (data locale di Roma) ---
        var dateOptions = {
            timeZone: 'Europe/Rome', // Assicura che il giorno sia corretto
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        };
        // Usa la lingua corretta per formattare la data
        var locale = (state.currentLanguage === 'it') ? 'it-IT' : 'en-GB';
        var formattedDate = serverTime.toLocaleDateString(locale, dateOptions);

        // Mette in maiuscolo la prima lettera del giorno
        dom.date.textContent = formattedDate.charAt(0).toUpperCase() + formattedDate.slice(1);
    }

    /** Aggiorna gli elementi statici dell'UI (solo etichetta piano) */
    function updateStaticUI() {
        var lang = translations[state.currentLanguage];
        var buildingKey = dom.body.dataset.building;
        var floorNumber = dom.body.dataset.floor;
        var buildingName = lang.building[buildingKey] || buildingKey;
        dom.label.innerHTML = buildingName + ' - ' + lang.floor + ' ' + floorNumber;
    }

    /** Cambia la lingua e aggiorna l'UI */
    function toggleLanguage() {
        state.currentLanguage = (state.currentLanguage === 'en') ? 'it' : 'en';
        dom.body.className = 'lang-' + state.currentLanguage;
        updateStaticUI();
    }

    window.onload = function() {
        var loader = document.getElementById('loader');
        if (loader) {
            loader.classList.add('hidden');
        }
    };
    
    /** Funzione di avvio */
    function init() {
        dom.body.className = 'lang-' + state.currentLanguage;
        updateStaticUI();
        syncTimeWithServer(); // Sincronizza l'orologio all'avvio

        var secondsCounter = 0;

        setInterval(function() {
            try {
                secondsCounter++;
                updateSyncedElements(); // Ora aggiorna sia orologio che data

                if (secondsCounter % config.languageToggleInterval === 0) {
                    toggleLanguage();
                }
                
                // Risincronizza l'orario periodicamente per evitare disallineamenti
                if (secondsCounter % config.dataRefreshInterval === 0) {
                    syncTimeWithServer();
                }
            } catch (e) {
                console.error("Errore nell'intervallo principale:", e);
            }
        }, 1000);

        setTimeout(function() { 
            window.location.reload(true); 
        }, 4 * 60 * 60 * 1000);
    }

    init();
});