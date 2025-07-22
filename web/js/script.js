;(function() {
  const clockElem     = document.getElementById('clock');
  const dateElem      = document.getElementById('current-date');
  const labelElem     = document.getElementById('floor-label');
  const buildingCode  = document.body.dataset.building;
  const floorNumber   = document.body.dataset.floor;

  // Lingue
  const LANGS       = ['it','en'];
  let   langIndex   = 0;
  let   currentLang = LANGS[0];

  // Giorni e mesi IT
  const dayNamesIt   = ['domenica','lunedì','martedì','mercoledì','giovedì','venerdì','sabato'];
  const monthNamesIt = ['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre'];

  // Nomi edifici e nomi "Piano"/"Floor"
  const BUILDING_NAMES = {
    it: { 'SBA': 'Edificio SBA', 'B': 'Edificio B', 'A': 'Edificio A' },
    en: { 'SBA': 'Building SBA', 'B': 'Building B', 'A': 'Building A' }
  };
  const FLOOR_LABEL = { it: 'Piano', en: 'Floor' };

  function pad2(n){ return (n<10?'0':'')+n; }

  function updateClock(){
    const now = new Date();
    clockElem.textContent = `${pad2(now.getHours())}:${pad2(now.getMinutes())}:${pad2(now.getSeconds())}`;
  }

  function formatDate(){
    const now = new Date();
    let day   = currentLang === 'it'
              ? dayNamesIt[now.getDay()]
              : now.toLocaleDateString('en-GB',{weekday:'long'}).toLowerCase();
    let month = currentLang === 'it'
              ? monthNamesIt[now.getMonth()]
              : now.toLocaleDateString('en-GB',{month:'long'});
    day   = day.charAt(0).toUpperCase() + day.slice(1);
    month = month.charAt(0).toUpperCase() + month.slice(1);
    return `${day} ${now.getDate()} ${month} ${now.getFullYear()}`;
  }

  function updateDate(){
    dateElem.textContent = formatDate();
  }

  function updateLabel(){
    const buildingText = BUILDING_NAMES[currentLang][buildingCode];
    const floorText    = FLOOR_LABEL[currentLang];
    labelElem.textContent = `${buildingText} – ${floorText} ${floorNumber}`;
  }

  function toggleLang(){
    langIndex = 1 - langIndex;
    currentLang = LANGS[langIndex];
    document.body.classList.toggle('lang-it');
    document.body.classList.toggle('lang-en');
    updateClock();
    updateDate();
    updateLabel();
  }

  // Init
  updateClock();
  updateDate();
  updateLabel();
  setInterval(updateClock, 1000);
  setInterval(toggleLang, 15000);
})();
