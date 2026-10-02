// Transitions thématiques entre la carte et les régions
// frost = Mes projets (Froid), shadow = Veille (Ombre), sun = Mon parcours (Soleil), arcane = Compétences (Force)
(function () {
    const THEMES = {
        frost: {
            bg: 'radial-gradient(circle at 50% 40%, rgba(220,245,255,0.95), rgba(120,190,230,0.97) 45%, rgba(20,50,90,1))',
            colors: ['#ffffff', '#dff6ff', '#a8e4ff'],
            count: 220,
            spawn: (w, h) => ({ x: Math.random() * w, y: -Math.random() * h, vx: -1 + Math.random() * 3, vy: 2 + Math.random() * 5, r: 1 + Math.random() * 3.5 }),
            draw: (c, p) => { c.beginPath(); c.arc(p.x, p.y, p.r, 0, Math.PI * 2); c.fill(); }
        },
        shadow: {
            bg: 'radial-gradient(circle at 50% 50%, rgba(20,60,50,0.95), rgba(5,15,15,0.99) 60%, #000)',
            colors: ['rgba(80,255,190,0.35)', 'rgba(40,180,140,0.3)', 'rgba(150,255,220,0.25)'],
            count: 70,
            spawn: (w, h) => ({ x: Math.random() * w, y: h + Math.random() * h * 0.5, vx: -0.6 + Math.random() * 1.2, vy: -(0.8 + Math.random() * 2), r: 20 + Math.random() * 60 }),
            draw: (c, p) => {
                const g = c.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r);
                g.addColorStop(0, c.fillStyle); g.addColorStop(1, 'rgba(0,0,0,0)');
                c.save(); c.fillStyle = g; c.beginPath(); c.arc(p.x, p.y, p.r, 0, Math.PI * 2); c.fill(); c.restore();
            }
        },
        sun: {
            bg: 'radial-gradient(circle at 50% 50%, rgba(255,250,210,1), rgba(255,200,60,0.97) 35%, rgba(170,90,10,1) 75%, #3a1d02)',
            colors: ['#fff3b0', '#ffd700', '#ffae34'],
            count: 160,
            spawn: (w, h) => {
                const a = Math.random() * Math.PI * 2, s = 2 + Math.random() * 6;
                return { x: w / 2, y: h / 2, vx: Math.cos(a) * s, vy: Math.sin(a) * s, r: 1 + Math.random() * 3 };
            },
            draw: (c, p) => { c.beginPath(); c.arc(p.x, p.y, p.r, 0, Math.PI * 2); c.fill(); }
        },
        arcane: {
            bg: 'radial-gradient(circle at 50% 50%, rgba(60,40,10,0.95), rgba(20,12,2,0.99) 60%, #000)',
            colors: ['#ffd700', '#2ecc71', '#e6c27a'],
            count: 90,
            spawn: (w, h) => {
                const a = Math.random() * Math.PI * 2, d = Math.max(w, h) * (0.4 + Math.random() * 0.4);
                return { x: w / 2 + Math.cos(a) * d, y: h / 2 + Math.sin(a) * d, cx: w / 2, cy: h / 2, r: 6 + Math.random() * 10, rot: Math.random() * 6 };
            },
            move: p => { p.x += (p.cx - p.x) * 0.03; p.y += (p.cy - p.y) * 0.03; p.rot += 0.05; },
            draw: (c, p) => {
                c.save(); c.translate(p.x, p.y); c.rotate(p.rot); c.strokeStyle = c.fillStyle; c.lineWidth = 1.5;
                c.shadowColor = c.fillStyle; c.shadowBlur = 10;
                c.beginPath(); c.moveTo(0, -p.r); c.lineTo(p.r * 0.7, 0); c.lineTo(0, p.r); c.lineTo(-p.r * 0.7, 0); c.closePath(); c.stroke();
                c.restore();
            }
        }
    };

    function createOverlay(themeName, startVisible) {
        const t = THEMES[themeName];
        const overlay = document.createElement('div');
        overlay.className = 'theme-transition theme-' + themeName + (startVisible ? ' active' : '');
        overlay.style.background = t.bg;
        const canvas = document.createElement('canvas');
        overlay.appendChild(canvas);
        document.body.appendChild(overlay);

        const ctx = canvas.getContext('2d');
        const w = canvas.width = window.innerWidth;
        const h = canvas.height = window.innerHeight;
        const parts = Array.from({ length: t.count }, (_, i) => Object.assign(t.spawn(w, h), { color: t.colors[i % t.colors.length] }));
        let running = true;
        (function frame() {
            if (!running) return;
            ctx.clearRect(0, 0, w, h);
            parts.forEach(p => {
                if (t.move) t.move(p); else { p.x += p.vx; p.y += p.vy; }
                ctx.fillStyle = p.color;
                t.draw(ctx, p);
            });
            requestAnimationFrame(frame);
        })();
        overlay.stop = () => { running = false; overlay.remove(); };
        return overlay;
    }

    // Sortie : recouvre l'écran avec l'environnement puis navigue
    window.playThemeTransition = function (themeName, url) {
        if (!THEMES[themeName]) { window.location.href = url; return; }
        try { sessionStorage.setItem('arriveTheme', themeName); } catch (e) { }
        const overlay = createOverlay(themeName, false);
        void overlay.offsetWidth;
        overlay.classList.add('active');
        setTimeout(() => { window.location.href = url; }, 1000);
    };

    // Arrivée : l'environnement se dissipe pour révéler la page
    document.addEventListener('DOMContentLoaded', () => {
        let theme = null;
        try { theme = sessionStorage.getItem('arriveTheme'); sessionStorage.removeItem('arriveTheme'); } catch (e) { }
        if (theme && THEMES[theme]) {
            const overlay = createOverlay(theme, true);
            setTimeout(() => overlay.classList.remove('active'), 150);
            setTimeout(() => overlay.stop(), 1300);
        }

        // Bouton retour des pages régions : transition dans le thème de la page
        const pageTheme = document.body.dataset.theme;
        document.querySelectorAll('.back-btn').forEach(btn => {
            btn.addEventListener('click', e => {
                if (!pageTheme) return;
                e.preventDefault();
                playThemeTransition(pageTheme, btn.href);
            });
        });
    });

    // Retour arrière du navigateur (cache bfcache) : nettoie un éventuel voile resté affiché
    window.addEventListener('pageshow', e => {
        if (e.persisted) document.querySelectorAll('.theme-transition').forEach(o => o.stop());
    });
})();
