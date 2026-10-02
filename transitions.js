// Transitions 8-bit entre la carte et les régions
// frost = Mes projets (cheval dans les montagnes enneigées)
// arcane = Mes compétences (cheval dans le désert)
// shadow = Veille technologique (sous-marin)
// sun = Mon parcours (bateau vers l'île)
(function () {
    const DURATION = 2400; // durée de la barre de chargement (ms)

    // --- Sprites (chaque caractère = 1 pixel, '.' = transparent) ---
    const HORSE = [
        [
            "...........dd....",
            "..........dbbb...",
            ".........ddbkbbb.",
            ".........dbbb.bbb",
            "........dbbb.....",
            ".dd....dbbb......",
            "d..bbbbbbbb......",
            "..bbbbbbbbb......",
            "..bbbbbbbbb......",
            "..b.b....b.b.....",
            ".b...b..b...b....",
            ".k...k.k.....k..."
        ],
        [
            "...........dd....",
            "..........dbbb...",
            ".........ddbkbbb.",
            ".........dbbb.bbb",
            "........dbbb.....",
            "dd.....dbbb......",
            "..dbbbbbbbb......",
            "..bbbbbbbbb......",
            "..bbbbbbbbb......",
            "...bb...bb.......",
            "...bb...bb.......",
            "...kk...kk......."
        ]
    ];
    const HORSE_PAL = { b: '#8b5a2b', d: '#3b2410', k: '#111111' };

    const SUB = [
        [
            "..........yy..........",
            "..........yy..........",
            ".........yyyy.........",
            "....yyyyyyyyyyyyyy....",
            "p.yyyyyyyyyyyyyyyyyy..",
            "pyyyyycyyyycyyyycyyyy.",
            "p.yyyyyyyyyyyyyyyyyy..",
            "....yyyyyyyyyyyyyy...."
        ],
        [
            "..........yy..........",
            "..........yy..........",
            ".........yyyy.........",
            "....yyyyyyyyyyyyyy....",
            "..yyyyyyyyyyyyyyyyyy..",
            "pyyyyycyyyycyyyycyyyy.",
            "..yyyyyyyyyyyyyyyyyy..",
            "....yyyyyyyyyyyyyy...."
        ]
    ];
    const SUB_PAL = { y: '#f2c230', c: '#7fdcff', p: '#9a9a9a' };

    const BOAT = [
        ".......m........",
        ".......ws.......",
        ".......wws......",
        ".......wwws.....",
        ".......wwwws....",
        ".......wwwwws...",
        ".......wwwwwws..",
        ".......m........",
        "hhhhhhhhhhhhhhhh",
        ".hhhhhhhhhhhhhh.",
        "..hhhhhhhhhhhh.."
    ];
    const BOAT_PAL = { m: '#4a2a12', w: '#fdf6e3', s: '#d9cfb8', h: '#7a4520' };

    // --- Petits utilitaires de dessin ---
    function rect(c, x, y, w, h, col) { c.fillStyle = col; c.fillRect(Math.round(x), Math.round(y), w, h); }
    function sprite(c, rows, pal, x, y) {
        rows.forEach((row, j) => {
            for (let i = 0; i < row.length; i++) {
                const col = pal[row[i]];
                if (col) rect(c, x + i, y + j, 1, 1, col);
            }
        });
    }
    function bands(c, W, y0, y1, cols) {
        const h = (y1 - y0) / cols.length;
        cols.forEach((col, i) => rect(c, 0, y0 + i * h, W, Math.ceil(h) + 1, col));
    }
    const tri = (x, period, amp) => amp * (1 - Math.abs((((x / period) % 1) + 1) % 1 * 2 - 1));
    const mod = (a, n) => ((a % n) + n) % n;

    // --- Scènes ---
    const SCENES = {
        frost: {
            label: 'En route vers mes projets',
            draw(c, W, H, t) {
                bands(c, W, 0, H, ['#1b2a4a', '#24365e', '#2c4372', '#3a5a8c', '#4a6fa5']);
                const ground = H - 22;
                // montagnes lointaines
                for (let x = 0; x < W; x++) {
                    const hgt = 18 + tri(x + t * 6, 70, 34) + tri(x + t * 6 + 17, 23, 8);
                    rect(c, x, ground - hgt, 1, hgt, '#6b85b5');
                    rect(c, x, ground - hgt, 1, Math.max(0, hgt - 30), '#eef6ff');
                }
                // montagnes proches
                for (let x = 0; x < W; x++) {
                    const hgt = 6 + tri(x + t * 16, 50, 22);
                    rect(c, x, ground - hgt, 1, hgt, '#3d5580');
                    if (hgt > 20) rect(c, x, ground - hgt, 1, hgt - 20, '#dbe9f7');
                }
                // sol enneigé + traces
                rect(c, 0, ground, W, 22, '#e8f4ff');
                for (let x = -20; x < W + 20; x += 14) rect(c, x - mod(t * 40, 14), ground + 8, 5, 1, '#b8d4ee');
                for (let x = -20; x < W + 20; x += 22) rect(c, x - mod(t * 40, 22), ground + 15, 7, 1, '#b8d4ee');
                // cheval qui galope sur place
                const f = Math.floor(t * 8) % 2;
                sprite(c, HORSE[f], HORSE_PAL, Math.floor(W / 2 - 8), ground - 12 - f);
                // neige qui tombe
                for (let i = 0; i < 70; i++) {
                    const x = mod(i * 37 - t * (20 + (i % 4) * 8), W);
                    const y = mod(i * 53 + t * (18 + (i % 3) * 10), H);
                    rect(c, x, y, 1, 1, '#ffffff');
                }
            }
        },
        arcane: {
            label: 'En route vers mes compétences',
            draw(c, W, H, t) {
                bands(c, W, 0, H, ['#f9d98a', '#f7c873', '#f4b766', '#f4a65a']);
                // soleil
                const sx = W * 0.75, sy = 22;
                for (let y = -10; y <= 10; y++) for (let x = -10; x <= 10; x++)
                    if (x * x + y * y <= 100) rect(c, sx + x, sy + y, 1, 1, '#fff3b0');
                const ground = H - 22;
                // dunes lointaines
                for (let x = 0; x < W; x++) {
                    const hgt = 10 + Math.sin((x + t * 6) / 22) * 6 + Math.sin((x + t * 6) / 9) * 2;
                    rect(c, x, ground - hgt, 1, hgt, '#d9a35b');
                }
                // dunes proches
                for (let x = 0; x < W; x++) {
                    const hgt = 4 + Math.sin((x + t * 18) / 14) * 3;
                    rect(c, x, ground - hgt, 1, hgt, '#c48a45');
                }
                // pyramide au loin
                const px = mod(W * 0.3 - t * 6, W + 60) - 30;
                for (let j = 0; j < 18; j++) rect(c, px - j, ground - 28 + j, j * 2 + 1, 1, j % 3 ? '#b77b3a' : '#a06a30');
                // sol
                rect(c, 0, ground, W, 22, '#e8c07a');
                for (let x = -20; x < W + 20; x += 16) rect(c, x - mod(t * 40, 16), ground + 9, 4, 1, '#c99d55');
                // cactus
                for (let k = 0; k < 3; k++) {
                    const cx = mod(k * 90 - t * 40, W + 90) - 20;
                    rect(c, cx, ground - 14, 3, 14, '#3c8a3c');
                    rect(c, cx - 3, ground - 10, 3, 2, '#3c8a3c'); rect(c, cx - 3, ground - 13, 2, 3, '#3c8a3c');
                    rect(c, cx + 3, ground - 8, 3, 2, '#3c8a3c'); rect(c, cx + 4, ground - 11, 2, 3, '#3c8a3c');
                }
                const f = Math.floor(t * 8) % 2;
                sprite(c, HORSE[f], HORSE_PAL, Math.floor(W / 2 - 8), ground - 12 - f);
                // poussière derrière le cheval
                for (let i = 0; i < 6; i++) {
                    const dx = mod(t * 30 + i * 5, 30);
                    rect(c, W / 2 - 10 - dx, ground - 1 - (i % 3), 2, 1, '#d8b06a');
                }
            }
        },
        shadow: {
            label: 'Plongée vers la veille technologique',
            draw(c, W, H, t) {
                bands(c, W, 0, H, ['#13567c', '#0f4a6d', '#0b3d5c', '#0a2e47', '#071f33']);
                // rayons de lumière
                for (let i = 0; i < 4; i++) {
                    const x0 = mod(i * 50 + t * 4, W + 40) - 20;
                    for (let y = 0; y < H * 0.6; y += 2) rect(c, x0 + y * 0.3, y, 3, 1, 'rgba(160,220,255,0.12)');
                }
                // fond marin
                const floor = H - 12;
                rect(c, 0, floor, W, 12, '#c2a46b');
                for (let x = 0; x < W; x += 6) rect(c, x - mod(t * 20, 6), floor + 4, 2, 1, '#a68a55');
                // algues
                for (let k = 0; k < 8; k++) {
                    const ax = mod(k * 31 - t * 20, W + 20) - 10;
                    const h = 10 + (k % 3) * 6;
                    for (let j = 0; j < h; j++) rect(c, ax + Math.round(Math.sin(t * 3 + j / 3 + k)), floor - j, 1, 1, '#2f8f4e');
                }
                // poissons
                for (let k = 0; k < 4; k++) {
                    const fx = mod(-k * 60 - t * (25 + k * 6), W + 20) - 10;
                    const fy = 20 + k * 14;
                    rect(c, fx, fy, 4, 2, '#ff8c42'); rect(c, fx + 4, fy - 1, 1, 4, '#ff8c42');
                }
                // sous-marin
                const f = Math.floor(t * 10) % 2;
                const sx = Math.floor(W / 2 - 11), sy = Math.floor(H / 2 - 6 + Math.sin(t * 2) * 2);
                sprite(c, SUB[f], SUB_PAL, sx, sy);
                // bulles
                for (let i = 0; i < 18; i++) {
                    const age = mod(t * 1.2 + i * 0.37, 2.5);
                    const bx = sx - 2 - age * 12 + Math.sin(age * 6 + i) * 2;
                    const by = sy + 5 - age * 18;
                    rect(c, bx, by, 1 + (i % 2), 1 + (i % 2), '#bfefff');
                }
            }
        },
        sun: {
            label: 'Cap sur mon parcours',
            draw(c, W, H, t, p) {
                bands(c, W, 0, H * 0.6, ['#ffe08a', '#ffcf6b', '#ffb85e', '#ff9f5a', '#e9705a']);
                const sea = Math.floor(H * 0.6);
                // soleil couchant
                for (let y = -12; y <= 0; y++) for (let x = -12; x <= 12; x++)
                    if (x * x + y * y <= 144) rect(c, W * 0.3 + x, sea + y, 1, 1, '#fff1b8');
                // mer + vagues
                bands(c, W, sea, H, ['#2a73a6', '#1e5f8c', '#174c72', '#103a59']);
                for (let row = 0; row < 6; row++) {
                    const y = sea + 3 + row * 6;
                    const off = mod(t * (8 + row * 4) * (row % 2 ? 1 : -1), 12);
                    for (let x = -12; x < W + 12; x += 12) rect(c, x + off, y, 4, 1, '#4f9fd1');
                }
                // île au-dessus de l'eau avec palmier
                const ix = W - 42;
                for (let j = 0; j < 8; j++) rect(c, ix - 16 + j * 2, sea - 8 + j, 32 - j * 4 + 16, 1, '#e8c07a');
                rect(c, ix - 18, sea - 1, 52, 2, '#d9a35b');
                rect(c, ix + 6, sea - 26, 2, 18, '#7a4a20');
                rect(c, ix - 2, sea - 28, 18, 2, '#2f9a4a'); rect(c, ix, sea - 30, 14, 2, '#2f9a4a');
                rect(c, ix - 4, sea - 26, 4, 2, '#2f9a4a'); rect(c, ix + 14, sea - 26, 4, 2, '#2f9a4a');
                rect(c, ix + 5, sea - 25, 2, 2, '#5a3418'); rect(c, ix + 8, sea - 24, 2, 2, '#5a3418');
                // bateau qui avance vers l'île selon le chargement
                const bx = 6 + (ix - 46 - 6) * p;
                const by = sea - 9 + Math.round(Math.sin(t * 4));
                sprite(c, BOAT, BOAT_PAL, Math.floor(bx), by);
                // sillage
                for (let i = 1; i < 5; i++) rect(c, bx - i * 4 - mod(t * 10, 4), sea + 2 + (i % 2), 3, 1, '#cfe9ff');
            }
        }
    };

    // --- Police pixel ---
    if (!document.getElementById('pixel-font')) {
        const l = document.createElement('link');
        l.id = 'pixel-font'; l.rel = 'stylesheet';
        l.href = 'https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap';
        document.head.appendChild(l);
    }

    function createOverlay(theme, startVisible) {
        const scene = SCENES[theme];
        const overlay = document.createElement('div');
        overlay.className = 'pixel-transition' + (startVisible ? ' active' : '');
        overlay.innerHTML =
            '<canvas></canvas>' +
            '<div class="pixel-loading"><div class="pixel-label"></div>' +
            '<div class="pixel-bar"><div class="pixel-fill"></div></div></div>';
        overlay.querySelector('.pixel-label').textContent = scene.label;
        document.body.appendChild(overlay);

        const canvas = overlay.querySelector('canvas');
        const fill = overlay.querySelector('.pixel-fill');
        const H = 108;
        const W = Math.round(H * window.innerWidth / window.innerHeight);
        canvas.width = W; canvas.height = H;
        const ctx = canvas.getContext('2d');
        ctx.imageSmoothingEnabled = false;

        overlay.progress = startVisible ? 1 : 0;
        const t0 = performance.now();
        let running = true;
        (function frame(now) {
            if (!running) return;
            const t = (now - t0) / 1000;
            ctx.clearRect(0, 0, W, H);
            scene.draw(ctx, W, H, t, overlay.progress);
            // barre en paliers pour l'effet rétro
            fill.style.width = (Math.floor(overlay.progress * 20) * 5) + '%';
            requestAnimationFrame(frame);
        })(t0);
        overlay.stop = () => { running = false; overlay.remove(); };
        return overlay;
    }

    // Sortie : la scène apparaît, la barre se remplit, puis on change de page
    window.playThemeTransition = function (theme, url) {
        if (!SCENES[theme]) { window.location.href = url; return; }
        try { sessionStorage.setItem('arriveTheme', theme); } catch (e) { }
        const overlay = createOverlay(theme, false);
        void overlay.offsetWidth;
        overlay.classList.add('active');
        const start = performance.now();
        (function tick(now) {
            overlay.progress = Math.min(1, (now - start) / DURATION);
            if (overlay.progress < 1) requestAnimationFrame(tick);
            else setTimeout(() => { window.location.href = url; }, 150);
        })(start);
    };

    // Arrivée : la scène terminée s'efface pour révéler la page
    document.addEventListener('DOMContentLoaded', () => {
        let theme = null;
        try { theme = sessionStorage.getItem('arriveTheme'); sessionStorage.removeItem('arriveTheme'); } catch (e) { }
        if (theme && SCENES[theme]) {
            const overlay = createOverlay(theme, true);
            setTimeout(() => overlay.classList.remove('active'), 300);
            setTimeout(() => overlay.stop(), 1000);
        }

        // Bouton retour des pages régions : même scène, puis retour à la carte
        const pageTheme = document.body.dataset.theme;
        document.querySelectorAll('.back-btn').forEach(btn => {
            btn.addEventListener('click', e => {
                if (!pageTheme) return;
                e.preventDefault();
                playThemeTransition(pageTheme, btn.href);
            });
        });
    });

    // Retour arrière du navigateur (bfcache) : retire un éventuel écran resté affiché
    window.addEventListener('pageshow', e => {
        if (e.persisted) document.querySelectorAll('.pixel-transition').forEach(o => o.stop());
    });
})();
