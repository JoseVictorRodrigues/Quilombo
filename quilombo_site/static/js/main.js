/* ============================================================
   QUILOMBO ARAUCÁRIA - JavaScript Principal
   Animações, mapa, calendário, acessibilidade e interações
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
    // Inicializar ícones Lucide
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    initAccessibility();
    initNavbar();
    initScrollAnimations();
    initMessages();
    initCalendar('calendar');
    initFallingLeaves();
});


/* ---- Acessibilidade: Tema, Contraste, Fonte ---- */
function initAccessibility() {
    var STORAGE_KEY_THEME = 'qa-theme';
    var STORAGE_KEY_CONTRAST = 'qa-contrast';
    var STORAGE_KEY_FONT = 'qa-font-scale';

    // Restaurar preferências salvas
    var savedTheme = localStorage.getItem(STORAGE_KEY_THEME);
    var savedContrast = localStorage.getItem(STORAGE_KEY_CONTRAST);
    var savedFont = localStorage.getItem(STORAGE_KEY_FONT);

    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    }
    if (savedContrast === 'high') {
        document.documentElement.setAttribute('data-contrast', 'high');
    }
    if (savedFont) {
        document.documentElement.style.setProperty('--font-scale', savedFont);
    }

    // Atualizar ícone do botão de tema (sol/lua)
    function updateThemeIcon() {
        var icon = document.getElementById('theme-icon');
        if (!icon) return;
        var current = document.documentElement.getAttribute('data-theme') || 'light';
        icon.classList.remove('fa-moon', 'fa-sun');
        icon.classList.add(current === 'dark' ? 'fa-sun' : 'fa-moon');
    }

    // Sincronizar aria-pressed no botão de contraste
    function updateContrastBtn() {
        var btn = document.getElementById('btn-toggle-contrast');
        if (!btn) return;
        var active = document.documentElement.getAttribute('data-contrast') === 'high';
        btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    }

    updateThemeIcon();
    updateContrastBtn();

    // Tema: botão único que alterna claro/escuro
    var btnToggleTheme = document.getElementById('btn-toggle-theme');
    if (btnToggleTheme) {
        btnToggleTheme.addEventListener('click', function () {
            var current = document.documentElement.getAttribute('data-theme') || 'light';
            var next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem(STORAGE_KEY_THEME, next);
            updateThemeIcon();
        });
    }

    // Alto contraste
    var btnContrast = document.getElementById('btn-toggle-contrast');
    if (btnContrast) {
        btnContrast.addEventListener('click', function () {
            var current = document.documentElement.getAttribute('data-contrast');
            if (current === 'high') {
                document.documentElement.removeAttribute('data-contrast');
                localStorage.removeItem(STORAGE_KEY_CONTRAST);
            } else {
                document.documentElement.setAttribute('data-contrast', 'high');
                localStorage.setItem(STORAGE_KEY_CONTRAST, 'high');
            }
            updateContrastBtn();
        });
    }

    // Tamanho da fonte
    var fontScale = parseFloat(savedFont || '1');
    var MIN_SCALE = 0.8;
    var MAX_SCALE = 1.5;
    var STEP = 0.1;

    function setFontScale(scale) {
        fontScale = Math.max(MIN_SCALE, Math.min(MAX_SCALE, scale));
        document.documentElement.style.setProperty('--font-scale', fontScale);
        localStorage.setItem(STORAGE_KEY_FONT, fontScale.toString());
    }

    var btnDecrease = document.getElementById('btn-decrease-font');
    var btnIncrease = document.getElementById('btn-increase-font');

    if (btnDecrease) {
        btnDecrease.addEventListener('click', function () { setFontScale(fontScale - STEP); });
    }
    if (btnIncrease) {
        btnIncrease.addEventListener('click', function () { setFontScale(fontScale + STEP); });
    }
}


/* ---- Navbar ---- */
function initNavbar() {
    const header = document.querySelector('.main-header');
    const toggle = document.getElementById('nav-toggle');
    const menus = document.querySelectorAll('.nav-menu');

    // Scroll - adicionar sombra no header
    if (header) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 10) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }, { passive: true });
    }

    // Menu mobile toggle
    if (toggle && menus.length) {
        toggle.addEventListener('click', function () {
            const isOpen = !menus[0].classList.contains('active');
            menus.forEach(function (menu) { menu.classList.toggle('active', isOpen); });
            toggle.setAttribute('aria-expanded', isOpen);

            // Trocar ícone
            const icon = toggle.querySelector('[data-lucide]');
            if (icon) {
                icon.setAttribute('data-lucide', isOpen ? 'x' : 'menu');
                if (typeof lucide !== 'undefined') lucide.createIcons();
            }
        });

        // Fechar menu ao clicar em link
        menus.forEach(function (menu) {
            menu.querySelectorAll('.nav-link').forEach(function (link) {
                link.addEventListener('click', function () {
                    menus.forEach(function (m) { m.classList.remove('active'); });
                    toggle.setAttribute('aria-expanded', 'false');
                    var icon = toggle.querySelector('[data-lucide]');
                    if (icon) {
                        icon.setAttribute('data-lucide', 'menu');
                        if (typeof lucide !== 'undefined') lucide.createIcons();
                    }
                });
            });
        });
    }
}


/* ---- Scroll Animations (Intersection Observer) ---- */
function initScrollAnimations() {
    var elements = document.querySelectorAll('.animate-on-scroll');
    if (!elements.length) return;

    if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -40px 0px'
        });

        elements.forEach(function (el) {
            observer.observe(el);
        });
    } else {
        // Fallback: mostrar tudo
        elements.forEach(function (el) {
            el.classList.add('visible');
        });
    }
}


/* ---- Mensagens auto-dismiss ---- */
function initMessages() {
    document.querySelectorAll('.message-close').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var msg = btn.closest('.message');
            if (msg) {
                msg.style.opacity = '0';
                msg.style.transform = 'translateX(100%)';
                setTimeout(function () { msg.remove(); }, 300);
            }
        });
    });

    // Auto-dismiss após 6 segundos
    document.querySelectorAll('.message').forEach(function (msg) {
        setTimeout(function () {
            if (msg.parentNode) {
                msg.style.opacity = '0';
                msg.style.transform = 'translateX(100%)';
                setTimeout(function () { msg.remove(); }, 300);
            }
        }, 6000);
    });
}


/* ---- Calendário Mensal ---- */
function initCalendar(containerId) {
    var container = document.getElementById(containerId);
    if (!container) return;

    var currentDate = new Date();
    var currentMonth = currentDate.getMonth();
    var currentYear = currentDate.getFullYear();
    var events = [];

    // Buscar eventos da API
    fetch('/api/eventos/')
        .then(function (response) { return response.json(); })
        .then(function (data) {
            events = data;
            renderCalendar();
        })
        .catch(function () {
            renderCalendar();
        });

    var meses = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ];
    var diasSemana = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];

    function renderCalendar() {
        var firstDay = new Date(currentYear, currentMonth, 1).getDay();
        var daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
        var daysInPrevMonth = new Date(currentYear, currentMonth, 0).getDate();
        var today = new Date();

        var html = '<div class="cal-header">';
        html += '<button type="button" class="cal-nav-btn" data-dir="-1" aria-label="Mês anterior">&lsaquo;</button>';
        html += '<h3>' + meses[currentMonth] + ' ' + currentYear + '</h3>';
        html += '<button type="button" class="cal-nav-btn" data-dir="1" aria-label="Próximo mês">&rsaquo;</button>';
        html += '</div>';

        html += '<div class="cal-grid">';

        // Nomes dos dias
        diasSemana.forEach(function (dia) {
            html += '<div class="cal-day-name">' + dia + '</div>';
        });

        // Dias do mês anterior
        for (var i = firstDay - 1; i >= 0; i--) {
            html += '<div class="cal-day other-month">' + (daysInPrevMonth - i) + '</div>';
        }

        // Dias do mês atual
        for (var d = 1; d <= daysInMonth; d++) {
            var dateStr = currentYear + '-' + String(currentMonth + 1).padStart(2, '0') + '-' + String(d).padStart(2, '0');
            var isToday = today.getDate() === d && today.getMonth() === currentMonth && today.getFullYear() === currentYear;
            var hasEvent = events.some(function (e) { return e.date === dateStr; });

            var classes = 'cal-day';
            if (isToday) classes += ' today';
            if (hasEvent) classes += ' has-event';

            var title = '';
            if (hasEvent) {
                var dayEvents = events.filter(function (e) { return e.date === dateStr; });
                title = dayEvents.map(function (e) { return e.title + ' - ' + e.time; }).join(', ');
            }

            html += '<div class="' + classes + '"' + (title ? ' title="' + title.replace(/"/g, '&quot;') + '"' : '') + '>' + d + '</div>';
        }

        // Dias do próximo mês
        var totalCells = firstDay + daysInMonth;
        var remaining = totalCells % 7 === 0 ? 0 : 7 - (totalCells % 7);
        for (var r = 1; r <= remaining; r++) {
            html += '<div class="cal-day other-month">' + r + '</div>';
        }

        html += '</div>';

        container.innerHTML = html;

        // Event listeners para navegação
        container.querySelectorAll('.cal-nav-btn').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var dir = parseInt(btn.getAttribute('data-dir'));
                currentMonth += dir;
                if (currentMonth > 11) { currentMonth = 0; currentYear++; }
                if (currentMonth < 0) { currentMonth = 11; currentYear--; }
                renderCalendar();
            });
        });
    }
}


/* ---- Mapa Leaflet ---- */
function initMap(containerId, defaultLat, defaultLng, points) {
    var mapContainer = document.getElementById(containerId);
    if (!mapContainer) return;

    var map = L.map(containerId).setView([defaultLat, defaultLng], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);

    // Marcador principal fixo
    var mainIcon = L.divIcon({
        html: '<div style="background:linear-gradient(135deg,#2d6a4f,#40916c);width:32px;height:32px;border-radius:50%;border:3px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,0.3);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:bold;font-size:14px;">QA</div>',
        className: '',
        iconSize: [32, 32],
        iconAnchor: [16, 16]
    });

    var googleMapsUrl = 'https://www.google.com/maps/search/?api=1&query=' + defaultLat + ',' + defaultLng;
    var popupContent = '<strong>Quilombo Araucária</strong><br>' +
        'Rua Ecaúna, 137, Umarizal<br>' +
        'São Paulo - SP, 05754-040<br>' +
        '<a href="' + googleMapsUrl + '" target="_blank" rel="noopener noreferrer">Abrir no Google Maps</a>';

    L.marker([defaultLat, defaultLng], { icon: mainIcon })
        .addTo(map)
        .bindPopup(popupContent);

    // Pontos adicionais do banco de dados
    if (points && points.length > 0) {
        points.forEach(function (point) {
            var pointIcon = L.divIcon({
                html: '<div style="background:linear-gradient(135deg,#8b6914,#d4a244);width:28px;height:28px;border-radius:50%;border:2px solid #fff;box-shadow:0 2px 6px rgba(0,0,0,0.25);display:flex;align-items:center;justify-content:center;color:#fff;font-size:12px;">&#9679;</div>',
                className: '',
                iconSize: [28, 28],
                iconAnchor: [14, 14]
            });

            L.marker([point.lat, point.lng], { icon: pointIcon })
                .addTo(map)
                .bindPopup('<strong>' + point.nome + '</strong>' + (point.descricao ? '<br>' + point.descricao : ''));
        });

        // Ajustar vista para incluir todos os pontos
        var allCoords = [[defaultLat, defaultLng]];
        points.forEach(function (p) { allCoords.push([p.lat, p.lng]); });
        if (allCoords.length > 1) {
            map.fitBounds(allCoords, { padding: [40, 40] });
        }
    }

    // Forçar resize para corrigir tiles não carregados
    setTimeout(function () { map.invalidateSize(); }, 200);
}


/* ---- Folhas Caindo (Falling Leaves) ---- */
function initFallingLeaves() {
    var container = document.querySelector('.falling-leaves');
    if (!container) return;

    var leafSymbols = ['\u{1F342}', '\u{1F343}', '\u{1F341}'];
    var MAX_LEAVES = 12;

    function createLeaf() {
        if (container.childElementCount >= MAX_LEAVES) return;

        var leaf = document.createElement('span');
        leaf.className = 'leaf';
        leaf.textContent = leafSymbols[Math.floor(Math.random() * leafSymbols.length)];
        leaf.style.left = Math.random() * 100 + 'vw';
        leaf.style.fontSize = (14 + Math.random() * 18) + 'px';

        var duration = 8 + Math.random() * 10;
        var drift = (Math.random() - 0.5) * 200;
        var rotation = (Math.random() - 0.5) * 720;

        leaf.style.setProperty('--leaf-drift', drift + 'px');
        leaf.style.setProperty('--leaf-rotation', rotation + 'deg');
        leaf.style.animationDuration = duration + 's';
        leaf.style.animationDelay = Math.random() * 2 + 's';

        container.appendChild(leaf);

        leaf.addEventListener('animationend', function () {
            leaf.remove();
        });
    }

    // Criar folhas periodicamente
    setInterval(createLeaf, 2500);
    // Criar algumas folhas iniciais com delay
    for (var i = 0; i < 4; i++) {
        setTimeout(createLeaf, i * 800);
    }
}
