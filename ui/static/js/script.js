/**
 * Script for the Floor Plan Display.
 * Handles the live clock, bilingual date, and floor label overlays.
 * The main content (floor plan) is a server-rendered background image.
 */
document.addEventListener('DOMContentLoaded', () => {
    const dom = {
        clock: document.getElementById('clock'),
        date: document.getElementById('current-date'),
        label: document.getElementById('floor-label'),
        body: document.body
    };

    let currentLanguage = 'en';

    const translations = {
        it: {
            days: ["Domenica", "Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato"],
            months: ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"],
            floor: "Piano",
            building: { "A": "Edificio A", "B": "Edificio B", "SBA": "Edificio SBA" }
        },
        en: {
            days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            floor: "Floor",
            building: { "A": "Building A", "B": "Building B", "SBA": "Building SBA" }
        }
    };

    function padZero(n) {
        return String(n).padStart(2, '0');
    }

    function updateClockAndDate() {
        const now = new Date();
        dom.clock.textContent = `${padZero(now.getHours())}:${padZero(now.getMinutes())}:${padZero(now.getSeconds())}`;

        const lang = translations[currentLanguage];
        const dayName = lang.days[now.getDay()];
        const monthName = lang.months[now.getMonth()];
        dom.date.textContent = `${dayName} ${now.getDate()} ${monthName} ${now.getFullYear()}`;
    }

    function updateFloorLabel() {
        const buildingKey = dom.body.dataset.building;
        const floorNumber = dom.body.dataset.floor;
        const lang = translations[currentLanguage];
        
        const buildingName = lang.building[buildingKey] || buildingKey;
        dom.label.innerHTML = `${buildingName} - ${lang.floor} ${floorNumber}`;
    }

    function toggleLanguage() {
        currentLanguage = (currentLanguage === 'en') ? 'it' : 'en';
        dom.body.classList.toggle('lang-en');
        dom.body.classList.toggle('lang-it');
        updateClockAndDate();
        updateFloorLabel();
    }

    // Initial setup
    updateClockAndDate();
    updateFloorLabel();
    setInterval(updateClockAndDate, 1000);
    setInterval(toggleLanguage, 15000);
});