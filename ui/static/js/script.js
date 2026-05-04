/**
 * EN: Script for the Floor Plan Display. Handles the live clock, date,
 * and dynamic labels, all synchronized with a central time server.
 * IT: Script per il Display delle Planimetrie. Gestisce l'orologio, la data
 * e le etichette dinamiche, tutto sincronizzato con un time server centrale.
 */
document.addEventListener('DOMContentLoaded', function() {
    // EN: Centralized object for DOM element references.
    // IT: Oggetto centralizzato per i riferimenti agli elementi del DOM.
    var dom = {
        clock: document.getElementById('clock'),
        date: document.getElementById('current-date'),
        label: document.getElementById('floor-label'),
        body: document.body,
        loader: document.getElementById('loader')
    };

    // EN: Centralized state management object.
    // IT: Oggetto centralizzato per la gestione dello stato.
    var state = {
        currentLanguage: 'it',
        timeDifference: 0 // EN: Difference in ms between server and client time. / IT: Differenza in ms tra ora del server e del client.
    };

    // EN: Static configuration values.
    // IT: Valori di configurazione statici.
    var config = {
        // EN: Use a relative path for the time service, as it's behind the same proxy.
        // IT: Usa un percorso relativo per il time service, dato che è dietro lo stesso proxy.
        timeServiceUrl: '/api/time/',
        languageToggleInterval: 15, // seconds
        dataRefreshInterval: 5 * 60 // seconds
    };

    // EN: Object containing all translation strings.
    // IT: Oggetto contenente tutte le stringhe di traduzione.
    var translations = {
        it: {
            floor: "Piano",
            building: { "A": "Edificio A", "B": "Edificio B", "SBA": "Edificio SBA" }
        },
        en: {
            floor: "Floor",
            building: { "A": "Building A", "B": "Building B", "SBA": "Building SBA" }
        }
    };

    /**
     * EN: Syncs the local time with the server's time to correct for clock drift.
     * IT: Sincronizza l'ora locale con quella del server per correggere imprecisioni.
     */
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
                dom.clock.style.color = '';
                console.log('Time synchronized. Difference:', state.timeDifference, 'ms');
            })
            .catch(function(error) {
                console.error('Could not sync time with server:', error);
                state.timeDifference = 0;
                dom.clock.style.color = 'red';
            });
    }

    /**
     * EN: Updates the clock and date using the server-synced time.
     * IT: Aggiorna l'orologio e la data usando l'ora sincronizzata con il server.
     */
    function updateSyncedElements() {
        var serverTime = new Date(new Date().getTime() + state.timeDifference);
        
        var clockOptions = { timeZone: 'Europe/Rome', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
        dom.clock.textContent = serverTime.toLocaleTimeString('it-IT', clockOptions);

        var dateOptions = { timeZone: 'Europe/Rome', weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
        var locale = (state.currentLanguage === 'it') ? 'it-IT' : 'en-GB';
        var formattedDate = serverTime.toLocaleDateString(locale, dateOptions);
        dom.date.textContent = formattedDate.charAt(0).toUpperCase() + formattedDate.slice(1);
    }

    /**
     * EN: Updates the static UI labels based on the current language.
     * IT: Aggiorna le etichette statiche della UI in base alla lingua corrente.
     */
    function updateStaticUI() {
        var lang = translations[state.currentLanguage];
        var buildingKey = dom.body.dataset.building;
        var floorNumber = dom.body.dataset.floor;
        var buildingName = lang.building[buildingKey] || buildingKey;
        dom.label.innerHTML = buildingName + ' - ' + lang.floor + ' ' + floorNumber;
    }

    /**
     * EN: Toggles the display language and updates the UI.
     * IT: Alterna la lingua di visualizzazione e aggiorna la UI.
     */
    function toggleLanguage() {
        state.currentLanguage = (state.currentLanguage === 'en') ? 'it' : 'en';
        dom.body.className = 'lang-' + state.currentLanguage;
        updateStaticUI();
    }

    /**
     * EN: Hides the loader when the window is fully loaded.
     * IT: Nasconde il loader quando la finestra è completamente caricata.
     */
    var hideLoader = function() {
        if (dom.loader) {
            dom.loader.classList.add('hidden');
        }
    };
    window.onload = hideLoader;
    
    /**
     * EN: Helper to get URL parameters without URLSearchParams (for broad compatibility).
     */
    function getUrlParameter(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(window.location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    /**
     * EN: Main initialization function.
     * IT: Funzione di inizializzazione principale.
     */
    function init() {
        dom.body.className = 'lang-' + state.currentLanguage;
        updateStaticUI();
        syncTimeWithServer();

        var secondsCounter = 0;

        setInterval(function() {
            try {
                secondsCounter++;
                updateSyncedElements();

                if (secondsCounter % config.languageToggleInterval === 0) {
                    toggleLanguage();
                }
                
                if (secondsCounter % config.dataRefreshInterval === 0) {
                    syncTimeWithServer();
                }
            } catch (e) {
                console.error("Error in main interval:", e);
            }
        }, 1000);

        // EN: Fallback to ensure loader is hidden even if onload already fired.
        // IT: Fallback per garantire che il loader venga nascosto anche se onload è già avvenuto.
        setTimeout(hideLoader, 500);

        setTimeout(function() { window.location.reload(true); }, 4 * 60 * 60 * 1000);
    }

    init();
});