/**
 * Noutrora v2.1.0 — Lóxica Interactiva da Web Oficial
 * Motor: Vanilla JavaScript · Cero dependencias invasivas · Calma Atlántica
 */

// 1. Selector de Pestanas do Instalador (macOS, Windows, Linux)
function showInstallTab(k) {
    document.querySelectorAll('.install-panel').forEach(e => e.classList.add('hidden'));
    const panel = document.getElementById('install-' + k);
    if (panel) panel.classList.remove('hidden');
    document.querySelectorAll('.install-tab').forEach(b => b.classList.toggle('bg-sand', b.dataset.tab === k));
}

function copyMacInstallCmd(btn) {
    const cmd = document.getElementById('mac-install-cmd')?.textContent || 'curl -fsSL https://noutrora.es/downloads/Noutrora-Mac.command | bash';
    navigator.clipboard.writeText(cmd).then(() => {
        const orig = btn.textContent;
        btn.textContent = '✓ Copiado!';
        setTimeout(() => { btn.textContent = orig; }, 2200);
    });
}

// 2. Detección do Sistema Operativo
(function detectOS() {
    const ua = navigator.userAgent || '';
    const btnText = document.getElementById('os-download-text');
    const modalLink = document.getElementById('primary-download-link');
    const modalLabel = document.getElementById('modal-os-download-label');

    if (btnText) {
        if (ua.indexOf('Mac') !== -1) {
            btnText.textContent = 'Instalar Noutrora en macOS (En Galego)';
            if (modalLink) {
                modalLink.removeAttribute('download');
                modalLink.href = '#instalar';
                modalLink.onclick = function() { closeDownloadModal(); showInstallTab('mac'); };
            }
            if (modalLabel) modalLabel.textContent = 'Ver comando de 1 clic para macOS →';
            showInstallTab('mac');
        } else if (ua.indexOf('Win') !== -1) {
            btnText.textContent = 'Descargar Noutrora para Windows (En Galego)';
            if (modalLink) modalLink.href = 'downloads/Noutrora-Setup-Windows.cmd';
            if (modalLabel) modalLabel.textContent = 'Descargar Instalador para Windows (En Galego)';
            showInstallTab('win');
        } else if (ua.indexOf('Linux') !== -1) {
            btnText.textContent = 'Descargar Noutrora para Linux (.deb) — En Galego';
            if (modalLink) modalLink.href = 'downloads/noutrora_2.0_all.deb';
            if (modalLabel) modalLabel.textContent = 'Descargar Instalador Completo para Linux (.deb) — En Galego';
            showInstallTab('linux');
        } else {
            btnText.textContent = 'Descargar Noutrora de Balde (En Galego)';
            showInstallTab('linux');
        }
    }
})();

// 3. Cambio de pestanas interactivas no Mockup do Navegador
const tabOrder = ['travesia', 'pdf', 'lectura', 'camarotes'];
let currentTabIndex = 0;

const urlMap = {
    travesia: 'about:ocean — Rumbo despexado · Protección Quilla Estrita activa',
    pdf: 'file:///caderno-bitacora/Carta_Nautica_Fisterra.pdf — Editor PDF Nativo',
    lectura: 'reader://atlantic-chronicle.org/quiet-web — Tradución Local Privada',
    camarotes: 'about:containers — Camarotes Multi-Conta illados (Traballo · Persoal · Banca)'
};

function switchBrowserTab(tabId) {
    currentTabIndex = tabOrder.indexOf(tabId);
    document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.add('hidden'));
    const activePane = document.getElementById('tab-content-' + tabId);
    if (activePane) activePane.classList.remove('hidden');

    tabOrder.forEach(id => {
        const btn = document.getElementById('tab-btn-' + id);
        if (!btn) return;
        if (id === tabId) {
            btn.className = 'browser-tab group flex items-center gap-2 px-3.5 py-1.5 rounded-t-xl rounded-b-md text-xs font-medium bg-foam dark:bg-deepAtlantic text-atlantic dark:text-foam shadow-sm transition';
        } else {
            btn.className = 'browser-tab group flex items-center gap-2 px-3.5 py-1.5 rounded-t-xl rounded-b-md text-xs font-medium text-slateText dark:text-foam/70 hover:bg-foam/60 dark:hover:bg-deepAtlantic/50 transition';
        }
    });

    const urlBar = document.getElementById('browser-url-bar');
    if (urlBar && urlMap[tabId]) {
        urlBar.textContent = urlMap[tabId];
    }
}

function cycleTabs(direction) {
    currentTabIndex = (currentTabIndex + direction + tabOrder.length) % tabOrder.length;
    switchBrowserTab(tabOrder[currentTabIndex]);
}

// 4. Animación da icona Marea (Recargar)
function animateReloadMarea() {
    const btn = document.getElementById('reload-marea-btn');
    if (!btn) return;
    btn.classList.remove('animate-marea');
    void btn.offsetWidth;
    btn.classList.add('animate-marea');
}

// 5. Popup do Escudo Quilla
function toggleShieldPopup() {
    const popup = document.getElementById('shield-popup');
    if (popup) popup.classList.toggle('hidden');
}

// 6. Marcar favorito con Estrela Polar
let isBookmarked = false;
function toggleStarBookmark() {
    isBookmarked = !isBookmarked;
    const btn = document.getElementById('bookmark-star-btn');
    if (btn) {
        btn.classList.toggle('text-tide', isBookmarked);
        btn.classList.toggle('scale-110', isBookmarked);
    }
}

// 7. Busca tranquila no Mockup
function handleCalmSearch(e) {
    e.preventDefault();
    const input = document.getElementById('calm-search-input');
    const resultBox = document.getElementById('calm-search-result');
    if (!input || !resultBox) return;
    const query = input.value.trim() || 'Faros do Atlántico Norte';
    resultBox.classList.remove('hidden');
    resultBox.textContent = '';
    const prefix = document.createTextNode('🧭 Rumbo fixado cara a «');
    const strong = document.createElement('strong');
    strong.textContent = query;
    const suffix = document.createTextNode('» — Busca privada sen anuncios patrocinados nin rastrexadores de perfilado.');
    resultBox.appendChild(prefix);
    resultBox.appendChild(strong);
    resultBox.appendChild(suffix);
}

// 8. Editor de PDF integrado (demo interactiva)
function highlightPdfSample() {
    const target = document.getElementById('pdf-highlight-target');
    if (target) {
        target.classList.toggle('bg-mist/40');
        target.classList.toggle('font-medium');
    }
}

function signPdfSample() {
    const box = document.getElementById('pdf-signature-box');
    if (box) {
        box.innerHTML = `<span class="text-atlantic dark:text-foam font-semibold not-italic">✓ Asinado: Cap. Breogán (43°21'N)</span>`;
        box.classList.add('bg-mist/15', 'border-solid');
    }
}

// 9. Tradución privada local (Firefox Translations)
const translations = {
    en: {
        badge: 'Inglés (EN)',
        title: 'The Quiet Architecture of the North Atlantic Web',
        body: '"True calm on the internet requires a browser that respects human attention. By translating articles directly inside your device\'s processor—just like Firefox Translations—not a single word you read is ever sent to third-party cloud servers."'
    },
    es: {
        badge: 'Castelán (Traducido localmente)',
        title: 'La arquitectura silenciosa de la web del Atlántico Norte',
        body: '«La verdadera calma en internet exige un navegador que respete la atención humana. Al traducir los artículos directamente en el procesador de tu dispositivo —igual que Firefox Translations—, ni una sola palabra de lo que lees se envía jamás a servidores en la nube.»'
    },
    gl: {
        badge: 'Galego (Traducido localmente)',
        title: 'A arquitectura silenciosa da web do Atlántico Norte',
        body: '«A verdadeira calma na rede esixe un navegador que respecte a atención humana. Ao traducir os artigos directamente no procesador do teu dispositivo —igual ca Firefox Translations—, nin unha soa palabra do que les se envía xamais a servidores externos.»'
    }
};

function translateLocalArticle(lang) {
    const data = translations[lang];
    if (!data) return;
    document.getElementById('lang-badge').textContent = data.badge;
    document.getElementById('article-title').textContent = data.title;
    document.getElementById('article-body').textContent = data.body;
}

// 10. Ventá Picture-in-Picture (PiP)
function togglePipPlayer() {
    const pip = document.getElementById('pip-floating-window');
    if (pip) pip.classList.toggle('hidden');
}

// 11. Simulador de Privacidade Quilla
function setPrivacySimulation(mode) {
    const btnCalm = document.getElementById('btn-sim-calm');
    const btnNoisy = document.getElementById('btn-sim-noisy');
    const badge = document.getElementById('sim-status-badge');
    const title = document.getElementById('sim-title');
    const speed = document.getElementById('sim-speed');
    const trackers = document.getElementById('sim-trackers');
    const ram = document.getElementById('sim-ram');
    const fingerprint = document.getElementById('sim-fingerprint');
    const desc = document.getElementById('sim-description');

    if (mode === 'calm') {
        btnCalm.className = 'px-4 py-2.5 rounded-xl text-xs font-semibold bg-atlantic dark:bg-mist text-foam dark:text-nightSky transition';
        btnNoisy.className = 'px-4 py-2.5 rounded-xl text-xs font-semibold bg-sand dark:bg-deepAtlantic text-slateText dark:text-foam/80 hover:text-atlantic transition';
        badge.textContent = 'Escudo Quilla: ACTIVO';
        badge.className = 'inline-block px-3 py-1 rounded-full text-xs font-mono bg-mist/20 text-tide dark:text-mist mb-1';
        title.textContent = 'Augas tranquilas e lectura despexada';
        speed.textContent = '0.8 s';
        trackers.textContent = '0 permitidos';
        ram.textContent = '-38 % RAM';
        fingerprint.textContent = 'Camuflada';
        desc.textContent = 'Os scripts de vixilancia de terceiros fican bloqueados antes de descargarse. A batería do teu portátil dura máis e as páxinas móstranse limpas coma as follas dun libro.';
    } else {
        btnNoisy.className = 'px-4 py-2.5 rounded-xl text-xs font-semibold bg-coralAlert text-foam transition';
        btnCalm.className = 'px-4 py-2.5 rounded-xl text-xs font-semibold bg-sand dark:bg-deepAtlantic text-slateText dark:text-foam/80 hover:text-atlantic transition';
        badge.textContent = 'Sen Protección Quilla';
        badge.className = 'inline-block px-3 py-1 rounded-full text-xs font-mono bg-coralAlert/20 text-coralAlert mb-1';
        title.textContent = 'Navegación saturada de rastrexadores comerciais';
        speed.textContent = '3.4 s';
        trackers.textContent = '27 activos';
        ram.textContent = '1.9 GB RAM';
        fingerprint.textContent = 'Exposta';
        desc.textContent = 'Sen o bloqueo por defecto de Firefox/Noutrora, ducias de redes publicitarias crean un perfil oculto co teu historial de lectura e fan lenta a carga de cada páxina.';
    }
}

// 12. Conmutador de Tema: Calma Diurna vs Noite Cometa '94
function toggleTheme() {
    const html = document.documentElement;
    const isDark = html.classList.toggle('dark');
    document.body.classList.toggle('constellation-bg', isDark);
    const label = document.getElementById('theme-label');
    if (label) {
        label.textContent = isDark ? 'Calma Diurna' : 'Modo Cometa ’94';
    }
}

// 13. Easter Egg Cometa '94 (Netscape Navigator)
function triggerCometEasterEgg() {
    const comet = document.getElementById('comet-effect');
    if (!comet) return;
    comet.classList.remove('hidden', 'comet-trail');
    void comet.offsetWidth;
    comet.classList.add('comet-trail');
    setTimeout(() => {
        comet.classList.add('hidden');
    }, 2500);
}

// 14. Simulación de envío de pestana (Mozilla Sync)
function sendTabSimulation() {
    const toast = document.getElementById('sync-toast');
    if (toast) toast.classList.remove('hidden');
}

// 15. Modal de descarga
function openDownloadModal() {
    const modal = document.getElementById('download-modal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function closeDownloadModal() {
    const modal = document.getElementById('download-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

document.getElementById('download-modal')?.addEventListener('click', (e) => {
    if (e.target.id === 'download-modal') closeDownloadModal();
});

document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeDownloadModal();
        closePrivacyModal();
    }
});

// 15b. Modal de Privacidade e Aviso Legal (RGPD / LSSI-CE)
function openPrivacyModal() {
    const modal = document.getElementById('privacy-modal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

function closePrivacyModal() {
    const modal = document.getElementById('privacy-modal');
    if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

document.getElementById('privacy-modal')?.addEventListener('click', (e) => {
    if (e.target.id === 'privacy-modal') closePrivacyModal();
});

// 16. Selector de Lingua de Instalación e Tradución TWP + Contador de Travesías (descargas.json)
let currentInstallLang = 'gl';
let descargasData = null;

const langMeta = {
    gl: { name: 'Galego', flagId: 'flag-estreleira', note: 'Galego por defecto · Menús nativos e tradución TWP en galego.' },
    eu: { name: 'Euskera', flagId: 'flag-ikurrina', note: 'Euskera seleccionado · Menús nativos e tradución TWP en euskera.' },
    ca: { name: 'Català', flagId: 'flag-estelada', note: 'Català seleccionado · Menús nativos e tradución TWP en català.' },
    es: { name: 'Castelán', flagId: 'flag-castelan', note: 'Castelán seleccionado · Menús nativos e tradución TWP en castelán.' }
};

function selectInstallLanguage(lang) {
    if (!langMeta[lang]) return;
    currentInstallLang = lang;

    // Actualizar estilo de botóns na sección principal
    document.querySelectorAll('.lang-sel-btn').forEach(btn => {
        const isSelected = btn.id === 'lang-btn-' + lang;
        if (isSelected) {
            btn.className = 'lang-sel-btn px-3 py-2 rounded-xl text-xs font-semibold bg-atlantic text-foam dark:bg-mist dark:text-nightSky border border-atlantic transition flex items-center justify-center gap-2 shadow-sm';
        } else {
            btn.className = 'lang-sel-btn px-3 py-2 rounded-xl text-xs font-medium bg-foam dark:bg-nightSky text-atlantic dark:text-foam border border-warmSand/70 dark:border-mist/30 hover:border-mist transition flex items-center justify-center gap-2';
        }
    });

    // Actualizar estilo de botóns no modal
    document.querySelectorAll('.modal-lang-btn').forEach(btn => {
        const isSelected = btn.dataset.lang === lang;
        if (isSelected) {
            btn.className = 'modal-lang-btn px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-atlantic text-foam dark:bg-mist dark:text-nightSky transition flex items-center gap-1.5';
        } else {
            btn.className = 'modal-lang-btn px-2.5 py-1 rounded-lg text-[11px] font-medium bg-sand dark:bg-nightSky text-atlantic dark:text-foam transition flex items-center gap-1.5';
        }
    });

    const note = document.getElementById('lang-active-note');
    if (note) note.textContent = '✓ ' + langMeta[lang].note;

    const modalLabel = document.getElementById('modal-os-download-label');
    if (modalLabel) {
        const baseText = modalLabel.textContent.split(' — ')[0];
        modalLabel.textContent = baseText + ' — En ' + langMeta[lang].name;
    }

    // Actualizar comando macOS
    const macCmd = document.getElementById('mac-install-cmd');
    if (macCmd) {
        macCmd.textContent = 'curl -fsSL https://noutrora.es/downloads/Noutrora-Mac.command | bash -s -- --lang=' + lang;
    }

    updateDownloadCountersDisplay();
}

function updateDownloadCountersDisplay() {
    if (!descargasData || !descargasData.descargas) return;
    const d = descargasData.descargas;
    const plats = d.plataformas;

    const totalBadge = document.getElementById('tracker-total-count');
    if (totalBadge) {
        const ver = (descargasData.version || 'v2.1.0').replace(/^v+/, 'v');
        totalBadge.textContent = d.total.toLocaleString('gl-ES') + ' travesías iniciadas no Atlántico (' + ver + ')';
    }

    const lCount = document.getElementById('tracker-linux-count');
    const wCount = document.getElementById('tracker-win-count');
    const mCount = document.getElementById('tracker-mac-count');

    if (lCount && plats.linux) {
        const langCount = plats.linux.idiomas[currentInstallLang] || 0;
        lCount.textContent = plats.linux.total + ' (' + langCount + ' en ' + langMeta[currentInstallLang].name + ')';
    }
    if (wCount && plats.windows) {
        const langCount = plats.windows.idiomas[currentInstallLang] || 0;
        wCount.textContent = plats.windows.total + ' (' + langCount + ' en ' + langMeta[currentInstallLang].name + ')';
    }
    if (mCount && plats.mac) {
        const langCount = plats.mac.idiomas[currentInstallLang] || 0;
        mCount.textContent = plats.mac.total + ' (' + langCount + ' en ' + langMeta[currentInstallLang].name + ')';
    }
}

// Carga anónima e lixeira de descargas.json
fetch('descargas.json')
    .then(res => res.json())
    .then(data => {
        descargasData = data;
        updateDownloadCountersDisplay();
    })
    .catch(() => {
        descargasData = {
            version: 'v2.1.0',
            descargas: {
                total: 0,
                plataformas: {
                    linux: { total: 0, idiomas: { gl: 0, es: 0, eu: 0, ca: 0 } },
                    windows: { total: 0, idiomas: { gl: 0, es: 0, eu: 0, ca: 0 } },
                    mac: { total: 0, idiomas: { gl: 0, es: 0, eu: 0, ca: 0 } }
                }
            }
        };
        updateDownloadCountersDisplay();
    });

