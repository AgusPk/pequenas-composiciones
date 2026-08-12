# -*- coding: utf-8 -*-
"""Genera la landing: papel de acuarela, una margarita que se abre, y el piano."""
import io, os

CX, CY = 300, 288          # centro de la flor, en unidades del viewBox

# Un petalo apuntando hacia arriba; despues cada uno se rota a su lugar.
PETALO_FRENTE = ('M 300 240 C 278 211, 272 168, 286 130 '
                 'C 292 113, 308 113, 314 130 C 328 168, 322 211, 300 240 Z')
PETALO_FONDO  = ('M 300 243 C 275 214, 266 174, 283 142 '
                 'C 291 124, 309 124, 317 142 C 334 174, 325 214, 300 243 Z')

def anillo(n, path, clase, paso_grados, giro_inicial, retardo_base, salto, base_idx):
    """Un anillo de petalos. Cada uno va dentro de su caja: la caja lleva el
    giro que lo ubica en la corona y, cuando suena la musica, el vuelo; el
    path de adentro solo se ocupa de abrirse al cargar. Separarlos evita que
    las dos animaciones se peleen por el mismo transform."""
    out = []
    for i in range(n):
        ang = giro_inicial + i * paso_grados
        orden = (i * 5) % n                      # abre salteado, no en fila
        retardo = retardo_base + orden * salto
        out.append(
            f'<g class="petalo-caja" data-idx="{base_idx + i}" '
            f'style="--ang:{ang:.1f}deg">'
            f'<path class="petalo {clase}" d="{path}" '
            f'style="animation-delay:{retardo:.2f}s"/></g>')
    return '\n        '.join(out)

N = 13
petalos_fondo  = anillo(N, PETALO_FONDO,  'atras',  360/N, 360/(2*N), 1.30, 0.045, 0)
petalos_frente = anillo(N, PETALO_FRENTE, 'adelante', 360/N, 0,        1.60, 0.045, N)

# granulado del boton: el pigmento de acuarela se junta en grumos
import math
granos = []
for k in range(26):
    a = k * 2.399963           # angulo aureo, reparte parejo sin verse en filas
    r = 6 + 32 * math.sqrt(k / 26)
    gx = CX + r * math.cos(a)
    gy = CY + r * math.sin(a)
    rr = 1.6 + (k % 4) * 0.7
    granos.append(f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="{rr:.1f}" fill="#9a6b1f" opacity=".30"/>')
granos = '\n        '.join(granos)


# Ciclo de la flor: se deshoja, queda desnuda un momento, se rearma y vuelve a
# empezar. Una sola animacion infinita por petalo, con su propio calendario
# metido en los fotogramas; asi pausar la musica la congela y no hay que
# coordinar nada desde JavaScript.
#
#   0 s ..... 5 s   entera
#   5 .. 120 s      se sueltan de a uno (uno cada 4.6 s, en orden salteado)
# 123 .. 128 s      desnuda
# 128 .. 139 s      vuelven de a uno, brotando desde el centro
# 139 .. 150 s      entera otra vez, y arranca de nuevo
CICLO = 150.0
TOTAL_PETALOS = N * 2
CAIDA_INI, CAIDA_FIN, VUELO = 5.0, 120.0, 3.4
REARMADO_INI, REARMADO_FIN, BROTE = 128.0, 139.0, 1.3

import random
az = random.Random(4)
pct = lambda t: round(t / CICLO * 100, 3)

bloques, asignaciones = [], []
for k in range(TOTAL_PETALOS):
    idx = (k * 7) % TOTAL_PETALOS          # 7 y 26 son coprimos: recorre todos
    j = [(m * 11) % TOTAL_PETALOS for m in range(TOTAL_PETALOS)].index(idx)
    cae = CAIDA_INI + k * (CAIDA_FIN - CAIDA_INI) / (TOTAL_PETALOS - 1)
    vuelve = REARMADO_INI + j * (REARMADO_FIN - REARMADO_INI) / (TOTAL_PETALOS - 1)
    dx, dy = az.uniform(-90, 90), az.uniform(-260, -430)
    giro = az.uniform(-160, 160)
    bloques.append(
        f'@keyframes ciclo-{idx}{{'
        f'0%,{pct(cae)}%{{transform:none;opacity:1;'
        f'animation-timing-function:cubic-bezier(.3,.05,.5,1)}}'
        f'{pct(cae + VUELO)}%{{transform:translate({dx:.0f}px,{dy:.0f}px) '
        f'rotate({giro:.0f}deg);opacity:0;animation-timing-function:linear}}'
        f'{pct(vuelve)}%{{transform:scale(.14);opacity:0;'
        f'animation-timing-function:cubic-bezier(.22,.61,.36,1)}}'
        f'{pct(vuelve + BROTE)}%,100%{{transform:none;opacity:1}}}}')
    asignaciones.append(
        f'.suena .petalo-caja[data-idx="{idx}"]'
        f'{{animation:ciclo-{idx} {CICLO:.0f}s linear infinite}}')

vuelo_css = '\n'.join(bloques + asignaciones)

CSS = """
:root{
  --tinta:#2a2620; --suave:#524b3c; --linea:#d5cab2; --acento:#745529;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
  --papel:#f4efe2; --tarjeta:rgba(255,253,247,.62); --vidrio:rgba(255,255,255,.5);
}
@media (prefers-color-scheme:dark){
  :root{--tinta:#ece7db; --suave:#bdb6a6; --linea:#403e35; --acento:#d9b478;
        /* la tarjeta tiene que oscurecerse con el papel: un panel claro con
           texto claro encima dejaba el titulo en contraste 1.98 */
        --tarjeta:rgba(42,45,38,.72); --vidrio:rgba(255,255,255,.06);}
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--papel);color:var(--tinta);
  font-family:var(--serif);font-size:19px;line-height:1.65}

/* ------------------------------------------------------- la hoja de papel */
/* Cuatro capas fijas detras de todo: aguadas de color muy diluidas, la fibra
   gruesa del papel prensado en frio, el grano fino, y un velado en los bordes.
   Es lo que hace que el fondo no se lea como un color plano. */
.papel{position:fixed;inset:0;z-index:0;pointer-events:none;
  background-color:var(--papel);
  background-image:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='4'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23g)' opacity='.042'/%3E%3C/svg%3E"),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='620' height='620'%3E%3Cfilter id='f'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.014' numOctaves='5'/%3E%3CfeColorMatrix type='saturate' values='.15'/%3E%3C/filter%3E%3Crect width='620' height='620' filter='url(%23f)' opacity='.07'/%3E%3C/svg%3E"),
    radial-gradient(58% 44% at 18% 12%, rgba(150,168,122,.13), transparent 70%),
    radial-gradient(52% 40% at 86% 26%, rgba(196,158,96,.13), transparent 72%),
    radial-gradient(60% 46% at 72% 88%, rgba(126,152,164,.11), transparent 72%),
    radial-gradient(46% 38% at 8% 76%, rgba(178,140,104,.10), transparent 74%),
    radial-gradient(120% 100% at 50% 45%, transparent 52%, rgba(120,100,64,.10));
  background-size:160px 160px, 620px 620px, auto, auto, auto, auto, auto;
}
@media (prefers-color-scheme:dark){
  /* Solo cambia el color de base. Antes habia aca un filter:invert(1) que daba
     vuelta toda la capa: el papel salia gris claro y el texto, que en oscuro es
     crema, quedaba claro sobre claro. Las texturas y las aguadas de arriba
     funcionan igual sobre fondo oscuro, no hay que invertir nada. */
  .papel{background-color:#141511}
}
.hoja{position:relative;z-index:1}

/* ------------------------------------------------------------------ cuadro */
.portada{min-height:86svh;display:grid;grid-template-columns:1fr;
  align-content:center;gap:1rem;max-width:70rem;margin:0 auto;padding:2.5rem 1.5rem 2rem}
@media (min-width:58rem){
  .portada{grid-template-columns:1fr 1fr;align-items:center;gap:3rem;padding-block:3rem}
}
.presentacion{order:2}
.flor-caja{order:1;display:flex;justify-content:center}
@media (min-width:58rem){.presentacion{order:1}.flor-caja{order:2}}
.flor{width:min(100%,31rem);height:auto;overflow:visible}

.nombre{font-size:clamp(2.1rem,6.6vw,3.4rem);line-height:1.08;margin:0 0 .7rem;
  font-weight:600;letter-spacing:-.015em}
.filete{width:4.5rem;height:1px;background:var(--linea);margin:0 0 1.5rem}
.lema{margin:0 0 2rem;color:var(--suave);font-size:1.16rem;font-style:italic;max-width:26rem}

/* ------------------------------------------------------------------ piano */
.ir-al-libro{display:inline-flex;align-items:baseline;gap:.45rem;margin:0 0 1.6rem;
  font-size:1.05rem;color:var(--tinta);text-decoration:none;
  border-bottom:1px solid var(--acento);padding-bottom:.15rem;
  transition:color .2s ease, border-color .2s ease}
.ir-al-libro em{font-style:italic}
.ir-al-libro:hover{color:var(--acento)}
.ir-al-libro:hover .flecha{transform:translateX(3px)}

.piano{max-width:24rem;padding:1rem 1.15rem;border:1px solid var(--linea);
  border-radius:12px;background:var(--tarjeta);
  -webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px)}
.rotulo-piano{font-family:var(--sans);font-size:.86rem;letter-spacing:.13em;
  text-transform:uppercase;color:var(--suave);margin:0 0 .55rem}
.mando{display:flex;align-items:center;gap:.8rem}
.tocar{flex:none;width:2.9rem;height:2.9rem;border-radius:50%;
  border:1px solid var(--linea);background:var(--vidrio);color:var(--acento);
  display:grid;place-items:center;cursor:pointer;
  transition:border-color .2s ease, color .2s ease, background-color .2s ease}
.tocar:hover{border-color:var(--acento);background:var(--vidrio);filter:brightness(1.12)}
.tocar svg{width:1.05rem;height:1.05rem}
.tocar .pausa{display:none}
.tocar[aria-pressed="true"] .play{display:none}
.tocar[aria-pressed="true"] .pausa{display:block}
.pista{flex:1;min-width:0}
.pista .titulo{font-size:1rem;margin:0 0 .35rem;line-height:1.3}
.cinta{font-family:var(--sans);font-size:.86rem;line-height:1.45;color:var(--suave);
  margin:0 0 .5rem}
.barra{display:flex;align-items:center;gap:.55rem}
.barra input[type=range]{flex:1;min-width:0;height:1.05rem;-webkit-appearance:none;
  appearance:none;background:transparent;cursor:pointer;margin:0}
.barra input[type=range]::-webkit-slider-runnable-track{height:3px;border-radius:3px;
  background:var(--linea)}
.barra input[type=range]::-moz-range-track{height:3px;border-radius:3px;background:var(--linea)}
.barra input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;
  width:11px;height:11px;border-radius:50%;background:var(--acento);margin-top:-4px}
.barra input[type=range]::-moz-range-thumb{width:11px;height:11px;border:0;border-radius:50%;
  background:var(--acento)}
.barra input[type=range]:focus-visible{outline:2px solid var(--acento);outline-offset:3px}
.reloj{font-family:var(--sans);font-size:.82rem;color:var(--suave);
  font-variant-numeric:tabular-nums;flex:none}

/* ------------------------------------------------------------------ obras */
.obras{max-width:70rem;margin:0 auto;padding:0 1.5rem 5rem;scroll-margin-top:1.5rem}
.rotulo{font-family:var(--sans);font-size:.82rem;letter-spacing:.14em;
  text-transform:uppercase;color:var(--suave);margin:0 0 1.1rem}
.obra{display:grid;gap:1.5rem;align-items:center;padding:1.5rem;
  border:1px solid var(--linea);border-radius:14px;background:var(--tarjeta);
  -webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px);
  text-decoration:none;color:inherit;
  transition:border-color .25s ease, transform .25s ease, box-shadow .25s ease}
@media (min-width:40rem){.obra{grid-template-columns:13rem 1fr;padding:1.75rem}}
.obra:hover{border-color:var(--acento);transform:translateY(-2px);
  box-shadow:0 6px 26px rgba(70,52,22,.12)}
.obra img{width:100%;height:auto;border-radius:6px;display:block;
  box-shadow:0 1px 3px rgba(0,0,0,.16),0 8px 22px rgba(0,0,0,.08)}
.obra h2{margin:0 0 .3rem;font-size:1.5rem;line-height:1.2;font-weight:600}
.obra .bajada{margin:0 0 .9rem;color:var(--suave);font-size:1rem}
.entrar{font-family:var(--sans);font-size:.85rem;color:var(--acento);
  display:inline-flex;align-items:center;gap:.4rem}
.obra:hover .flecha{transform:translateX(3px)}
.flecha{transition:transform .25s ease}

footer{max-width:70rem;margin:0 auto;padding:0 1.5rem 4rem;
  font-family:var(--sans);font-size:.86rem;color:var(--suave)}
footer p{margin:0;padding-top:1.4rem;border-top:1px solid var(--linea)}
.credito{opacity:.75}


/* --------------------------------------------------- viento, con la musica */
/* Todo esto solo existe cuando suena: .suena prende las animaciones y .quieto
   las congela donde estan, asi pausar la musica frena la planta en seco y
   retomarla sigue desde ahi. Al terminar se saca .suena y la flor vuelve
   entera, lista para la proxima escucha. */
.petalo-caja{transform-box:view-box;transform-origin:300px 288px;rotate:var(--ang)}

@media (prefers-reduced-motion: no-preference){
  .planta{transform-box:view-box;transform-origin:300px 776px}
  .cabeza{transform-box:view-box;transform-origin:300px 340px}

  .suena .planta{animation:mecer 7.5s ease-in-out infinite}
  .suena .cabeza{animation:cabecear 4.3s ease-in-out infinite}
  @keyframes mecer{
    0%{rotate:-1.6deg}  18%{rotate:1.1deg}  34%{rotate:-.5deg}
    52%{rotate:2.4deg}  68%{rotate:.2deg}   84%{rotate:-2deg}  100%{rotate:-1.6deg}
  }
  @keyframes cabecear{
    0%{rotate:1.1deg} 30%{rotate:-1.5deg} 55%{rotate:.9deg} 78%{rotate:-.7deg} 100%{rotate:1.1deg}
  }

  /* el vuelo y el rearmado de cada petalo van en su propio @keyframes,
     generados mas abajo: cada uno lleva su horario dentro del ciclo */

  /* pausar la musica congela la planta y los petalos en el aire */
  .quieto .planta,.quieto .cabeza,.quieto .petalo-caja{animation-play-state:paused}
}

/* ------------------------------------------- la margarita, pintandose sola */
/* El tallo se dibuja (pathLength=1 + stroke-dashoffset). Los petalos crecen
   desde el centro de la flor, uno por uno, en un orden salteado para que
   parezca que se abre y no que se arma en fila. Sin movimiento, la flor ya
   esta pintada al cargar. */
.tallo{stroke-dasharray:1;stroke-dashoffset:0}
.petalo{fill:url(#petalo-lavado);stroke:#c9c6b2;stroke-width:.9;
  transform-box:view-box;transform-origin:300px 288px}
.petalo.atras{fill:url(#petalo-sombra);opacity:.92}

@media (prefers-reduced-motion: no-preference){
  .tallo{stroke-dashoffset:1;animation:trazar 1.15s ease-out .15s forwards}
  @keyframes trazar{to{stroke-dashoffset:0}}

  /* 'backwards' hace que durante la espera valga el fotograma inicial, y al
     terminar cada forma vuelve a su opacidad propia: asi el anillo de atras
     (que es mas tenue) no aparece de golpe antes de que le toque su turno. */
  .hoja-verde{transform-box:view-box;
    animation:brotar 1.1s cubic-bezier(.22,.61,.36,1) backwards}
  @keyframes brotar{from{opacity:0;scale:.3}}

  .petalo{animation:abrir 1.05s cubic-bezier(.22,.7,.3,1) backwards}
  @keyframes abrir{from{opacity:0;scale:.12;filter:blur(2px)}}

  .boton-flor{transform-box:view-box;transform-origin:300px 288px;
    animation:brotar 1s cubic-bezier(.22,.61,.36,1) 2.55s backwards}
  .lavado{animation:aguada 2s ease-out .1s backwards}
  @keyframes aguada{from{opacity:0;scale:.55}}
  .salpicon{animation:aguada 1.4s ease-out backwards}

  .presentacion>*{opacity:0;animation:subir .9s ease-out forwards}
  @keyframes subir{from{opacity:0;translate:0 .7rem}to{opacity:1;translate:0 0}}
  .presentacion>*:nth-child(1){animation-delay:2.75s}
  .presentacion>*:nth-child(2){animation-delay:2.88s}
  .presentacion>*:nth-child(3){animation-delay:3.0s}
  .presentacion>*:nth-child(4){animation-delay:3.12s}
  .presentacion>*:nth-child(5){animation-delay:3.24s}

  @supports ((animation-timeline: view()) and (animation-range: entry)){
    .obras .obra{animation:asomar auto linear backwards;
      animation-timeline:view();animation-range:entry 8% entry 55%}
    @keyframes asomar{from{opacity:0;translate:0 1.4rem}}
  }
}
"""

JS = """
(function(){
  var au = document.getElementById('piano');
  var btn = document.querySelector('.tocar');
  var rango = document.querySelector('.barra input');
  var transcurrido = document.querySelector('.transcurrido');
  var total = document.querySelector('.total');
  if(!au || !btn) return;

  function reloj(s){
    if(!isFinite(s)) return '--:--';
    var m = Math.floor(s/60), r = Math.floor(s%60);
    return m + ':' + (r<10?'0':'') + r;
  }
  btn.addEventListener('click', function(){
    if(au.paused){ au.play(); } else { au.pause(); }
  });
  var flor = document.querySelector('.flor');
  function rearmar(){
    flor.classList.remove('suena','quieto');
    flor.getBoundingClientRect();
  }
  au.addEventListener('play',  function(){ btn.setAttribute('aria-pressed','true');
    btn.setAttribute('aria-label','Pausar');
    if(au.currentTime < 0.3) rearmar();   // arranca de cero: flor entera de nuevo
    flor.classList.add('suena'); flor.classList.remove('quieto'); });
  au.addEventListener('pause', function(){ btn.setAttribute('aria-pressed','false');
    btn.setAttribute('aria-label','Escuchar');
    flor.classList.add('quieto'); });
  au.addEventListener('ended', rearmar);
  au.addEventListener('loadedmetadata', function(){
    rango.max = au.duration; total.textContent = reloj(au.duration);
  });
  au.addEventListener('timeupdate', function(){
    if(!rango.matches(':active')) rango.value = au.currentTime;
    transcurrido.textContent = reloj(au.currentTime);
    rango.setAttribute('aria-valuetext', reloj(au.currentTime));
  });
  rango.addEventListener('input', function(){ au.currentTime = +rango.value; });
  au.addEventListener('ended', function(){ rango.value = 0; });
})();
"""

HTML = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Margarita Sastre Inchauspe</title>
<meta name="description" content="Los escritos y el piano de Margarita Sastre Inchauspe. Pequenas composiciones de una nina: una vida contada en veintitres movimientos.">
<meta name="author" content="Margarita Sastre Inchauspe">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="__SITIO__">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_AR">
<meta property="og:title" content="Margarita Sastre Inchauspe">
<meta property="og:description" content="Los escritos y el piano de Margarita Sastre Inchauspe.">
<meta property="og:url" content="__SITIO__">
<meta property="og:image" content="__SITIO__pequenas-composiciones/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%8C%BC%3C/text%3E%3C/svg%3E">
<style>__CSS____VUELOS_CSS__</style>
</head>
<body>
<div class="papel" aria-hidden="true"></div>

<div class="hoja">
<section class="portada">
  <div class="presentacion">
    <h1 class="nombre">Margarita Sastre<br>Inchauspe</h1>
    <div class="filete"></div>
    <p class="lema">Una vida entre pianos, campos y amigas.</p>

    <a class="ir-al-libro" href="pequenas-composiciones/">
      Leer <em>Pequenas composiciones de una nina</em> <span class="flecha">&rarr;</span></a>

    <div class="piano">
      <p class="rotulo-piano">Margarita al piano</p>
      <div class="mando">
        <button class="tocar" type="button" aria-pressed="false" aria-label="Escuchar"
                aria-controls="piano">
          <svg class="play" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M8 5.2v13.6c0 .8.9 1.3 1.6.9l10.2-6.8a1 1 0 0 0 0-1.8L9.6 4.3A1 1 0 0 0 8 5.2z"/></svg>
          <svg class="pausa" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <rect x="7" y="5" width="3.6" height="14" rx="1"/>
            <rect x="13.4" y="5" width="3.6" height="14" rx="1"/></svg>
        </button>
        <div class="pista">
          <p class="titulo">Beethoven &middot; Sonata n.&ordm;&nbsp;7, primer movimiento</p>
          <p class="cinta">Grabacion casera en cassette, en Ombu. Se escucha lo que
            guardo la cinta.</p>
          <div class="barra">
            <input type="range" min="0" max="100" value="0" step="0.5"
                   aria-label="Posicion de la grabacion">
            <span class="reloj"><span class="transcurrido">0:00</span> / <span class="total">5:06</span></span>
          </div>
        </div>
      </div>
      <audio id="piano" preload="metadata">
        <source src="audio/beethoven-sonata7-margarita.m4a" type="audio/mp4">
        <source src="audio/beethoven-sonata7-margarita.mp3" type="audio/mpeg">
      </audio>
    </div>
  </div>

  <div class="flor-caja">
    <svg class="flor" viewBox="0 0 600 800" role="img"
         aria-label="Acuarela de una margarita abriendose sobre papel">
      <defs>
        <filter id="acuarela" x="-30%" y="-30%" width="160%" height="160%">
          <feTurbulence type="fractalNoise" baseFrequency="0.024" numOctaves="4" seed="11" result="r"/>
          <feDisplacementMap in="SourceGraphic" in2="r" scale="14"
                             xChannelSelector="R" yChannelSelector="G"/>
        </filter>
        <filter id="acuarela-fina" x="-30%" y="-30%" width="160%" height="160%">
          <feTurbulence type="fractalNoise" baseFrequency="0.055" numOctaves="3" seed="5" result="r"/>
          <feDisplacementMap in="SourceGraphic" in2="r" scale="4.5"
                             xChannelSelector="R" yChannelSelector="G"/>
        </filter>
        <filter id="difuso" x="-40%" y="-40%" width="180%" height="180%">
          <feGaussianBlur stdDeviation="26"/>
        </filter>
        <linearGradient id="petalo-lavado" x1="0.5" y1="1" x2="0.5" y2="0">
          <stop offset="0%" stop-color="#e6e2cd"/>
          <stop offset="45%" stop-color="#faf7ec"/>
          <stop offset="100%" stop-color="#fffdf7"/>
        </linearGradient>
        <linearGradient id="petalo-sombra" x1="0.5" y1="1" x2="0.5" y2="0">
          <stop offset="0%" stop-color="#cfcdb8"/>
          <stop offset="60%" stop-color="#e8e4d2"/>
          <stop offset="100%" stop-color="#f2eee0"/>
        </linearGradient>
        <radialGradient id="boton" cx="40%" cy="35%" r="70%">
          <stop offset="0%" stop-color="#f0c35c"/>
          <stop offset="60%" stop-color="#d79f31"/>
          <stop offset="100%" stop-color="#a97117"/>
        </radialGradient>
        <linearGradient id="tallo-verde" x1="0" y1="1" x2="0.2" y2="0">
          <stop offset="0%" stop-color="#5f7038"/><stop offset="100%" stop-color="#87994f"/>
        </linearGradient>
        <radialGradient id="hoja-verde" cx="30%" cy="40%" r="75%">
          <stop offset="0%" stop-color="#9db063"/><stop offset="100%" stop-color="#5e7038"/>
        </radialGradient>
      </defs>

      <!-- la aguada de fondo: la mancha diluida sobre la que se pinta la flor -->
      <g class="lavado" filter="url(#difuso)" style="mix-blend-mode:multiply">
        <ellipse cx="302" cy="292" rx="215" ry="200" fill="#cfd6b4" opacity=".34"/>
        <ellipse cx="356" cy="236" rx="130" ry="110" fill="#d8c79a" opacity=".26"/>
        <ellipse cx="250" cy="352" rx="120" ry="100" fill="#b9c6cc" opacity=".22"/>
      </g>

      <g class="planta">
      <!-- tallo y hojas -->
      <g fill="none" stroke-linecap="round" filter="url(#acuarela-fina)">
        <path class="tallo" pathLength="1" stroke="url(#tallo-verde)" stroke-width="11"
              d="M 300 338 C 295 440, 303 548, 296 646 C 291 706, 297 744, 301 776"/>
      </g>
      <g filter="url(#acuarela)" style="mix-blend-mode:multiply">
        <path class="hoja-verde" fill="url(#hoja-verde)" opacity=".85"
              style="animation-delay:.95s;transform-origin:300px 566px"
              d="M 298 566 C 256 544, 210 552, 180 590 C 216 614, 268 608, 298 566 Z"/>
        <path class="hoja-verde" fill="url(#hoja-verde)" opacity=".8"
              style="animation-delay:1.1s;transform-origin:300px 476px"
              d="M 301 476 C 343 456, 389 464, 416 500 C 380 522, 330 516, 301 476 Z"/>
      </g>

      <!-- los petalos: primero el anillo de atras, despues el de adelante -->
      <g class="cabeza">
      <g filter="url(#acuarela-fina)">
        __PETALOS_FONDO__
      </g>
      <g filter="url(#acuarela-fina)">
        __PETALOS_FRENTE__
      </g>

      <!-- el boton, con el granulado del pigmento -->
      <g class="boton-flor" filter="url(#acuarela-fina)">
        <circle cx="300" cy="288" r="52" fill="url(#boton)"/>
        __GRANOS__
      </g>
      </g><!-- /cabeza -->
      </g><!-- /planta -->

      <!-- salpicaduras sueltas, como en el papel de verdad -->
      <g filter="url(#acuarela)" style="mix-blend-mode:multiply">
        <circle class="salpicon" cx="126" cy="196" r="7" fill="#9aa864" opacity=".38"
                style="animation-delay:3.2s"/>
        <circle class="salpicon" cx="486" cy="150" r="5" fill="#c39a4e" opacity=".34"
                style="animation-delay:3.35s"/>
        <circle class="salpicon" cx="470" cy="618" r="9" fill="#93a6ab" opacity=".30"
                style="animation-delay:3.5s"/>
        <circle class="salpicon" cx="150" cy="700" r="6" fill="#a58a5c" opacity=".32"
                style="animation-delay:3.6s"/>
      </g>
    </svg>
  </div>
</section>

<section class="obras">
  <p class="rotulo">Lo publicado</p>
  <a class="obra" href="pequenas-composiciones/">
    <img src="pequenas-composiciones/img/image102.jpg" width="655" height="673" alt="" loading="lazy">
    <div>
      <h2>Pequenas composiciones de una nina</h2>
      <p class="bajada">Sus memorias, en veintitres movimientos: la infancia entre pianos,
        El Correntino, la familia, los amigos y una vida entera. Con 121 fotos.</p>
      <span class="entrar">Leer el libro <span class="flecha">&rarr;</span></span>
    </div>
  </a>
</section>

<footer><p>Buenos Aires &middot; 2026 <span class="credito">&middot; Diseno y desarrollo:
  Agustin Perkins</span></p></footer>
</div>

<script>__JS__</script>
</body>
</html>
"""

SITIO = os.environ.get('SITE_URL', 'https://aguspk.github.io/pequenas-composiciones/')
salida = (HTML
          .replace('__CSS__', CSS)
          .replace('__JS__', JS)
          .replace('__PETALOS_FONDO__', petalos_fondo)
          .replace('__PETALOS_FRENTE__', petalos_frente)
          .replace('__GRANOS__', granos)
          .replace('__SITIO__', SITIO)
          .replace('__VUELOS_CSS__', vuelo_css))

# el archivo se escribe en utf-8 con los acentos correctos
salida = (salida
  .replace('Pequenas composiciones de una nina', 'Pequeñas composiciones de una niña')
  .replace('veintitres', 'veintitrés')
  .replace('hacian las manos', 'hacían las manos')
  .replace('Posicion de la grabacion', 'Posición de la grabación')
  .replace('abriendose', 'abriéndose')
  .replace('Grabacion casera en cassette, en Ombu. Se escucha lo que\n            guardo la cinta.', 'Grabación casera en cassette, en Ombú. Se escucha lo que guardó la cinta.')
  .replace('Diseno y desarrollo:', 'Diseño y desarrollo:')
  .replace('Agustin Perkins</span>', 'Agustín Perkins</span>')
  .replace('Leer <em>Pequenas composiciones de una nina</em>', 'Leer <em>Pequeñas composiciones de una niña</em>')
  .replace('escritos y el piano', 'escritos y el piano'))

destino = '/Users/agustin/Personal/pequenas-composiciones/index.html'
with io.open(destino, 'w', encoding='utf-8') as f:
    f.write(salida)
print('landing escrita:', destino, len(salida), 'bytes')
print('petalos:', N*2, ' granos:', 26)
