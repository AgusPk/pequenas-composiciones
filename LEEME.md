# Pequeñas composiciones de una niña
### Margarita Sastre Inchauspe — Buenos Aires, febrero 2026

**Publicado en → https://aguspk.github.io/pequenas-composiciones/**

El sitio tiene dos piezas:

- `index.html` en la raíz: la **landing**, con la margarita en acuarela que se
  abre sola, la grabación al piano y el acceso al libro. La genera
  `hacer-landing.py` (los 26 pétalos se emiten por código, no a mano).
  Al poner play se levanta viento: la planta se mece y los pétalos se van
  soltando uno cada ~11 s, repartidos a lo largo de los 5:06. Pausar congela
  todo donde está; volver a empezar devuelve la flor entera.
- `audio/`: la grabación, en AAC (5 MB, la que suena) y el MP3 original de
  320 kbps (12 MB, respaldo para navegadores viejos).
- `pequenas-composiciones/`: el **libro** completo.

Cuando se compre `margaritasastre.com` y se apunte al repo, las direcciones
quedan `margaritasastre.com` y `margaritasastre.com/pequenas-composiciones/`.

Versión ordenada del original `2 PEQUEÑAS COMPOSICIONES (1).docx`.

## Qué hay acá

| Archivo | Para qué |
|---|---|
| `index.html` | La landing del sitio: acuarela animada y acceso al libro. |
| `pequenas-composiciones/index.html` | El libro como página web. Un solo archivo + la carpeta `img/`. |
| `pequenas-composiciones/img/` | Las 118 fotos, optimizadas para web (24 MB → 7,7 MB, ninguna pierde nitidez). |
| `pequenas-composiciones/Pequenas-composiciones-de-una-nina.docx` | El mismo contenido en Word, para copiar y pegar en WordPress, Medium, Substack, etc. Se descarga también desde el pie de la página. |
| `pequenas-composiciones/og.jpg` | La imagen de vista previa que aparece al compartir el link por WhatsApp o redes. |
| `pequenas-composiciones/img/fondo-beethoven.jpg` | Fondo opcional: boceto autógrafo de la Sonata para piano op. 101 de Beethoven (1816), Library of Congress (Digital ID molden-0508), **dominio público**. Recortado, desaturado y aclarado para que no compita con el texto. |

## Qué se ordenó

- **Las fotos ya no flotan.** En el original las 112 imágenes estaban ancladas a
  posiciones absolutas de la página: se superponían entre sí y encima del texto.
  Ahora cada una va en el flujo del documento. **Cero superposiciones.**
- **Cada foto quedó con su epígrafe**, inmediatamente debajo. Varios epígrafes
  estaban a media página de distancia de su foto, o pegados a la foto equivocada.
- **Los epígrafes que describían dos o tres fotos juntas se dividieron.**
  Ej.: «A caballo, en la manga y andando en jeep por la laguna Las Tunas» ahora
  son tres epígrafes, uno por foto.
- **Se quitaron las referencias de posición** que ya no aplican («Foto izq.»,
  «Derecha», «Arriba», «F2»), porque cada foto lleva su propio epígrafe.
- **Se unieron los párrafos que el original cortaba al medio** para esquivar una
  foto (ej.: «...papel de diario que hacía mucho ruido cuando» / «nos sentábamos»).
- **Se separaron oraciones pegadas** («...de mi boca.Olga escuchaba» → «. Olga»),
  que venían de usar saltos de línea de Word como punto final.
- **Se eliminó una foto duplicada** (aparecía dos veces, en dos tamaños).
- **Índice de los 23 movimientos** al principio, con enlaces.

## Qué NO se tocó

- **El texto.** Ni una palabra, ni la ortografía, ni la puntuación de la autora.
  Sólo espacios: los cambios de arriba son de espaciado y de orden, nunca de contenido.
- **Las fotos que no tenían epígrafe siguen sin epígrafe.** No se inventó ninguno.

## Los cuatro fondos

Abajo a la derecha el lector elige: claro, oscuro, papel de partitura o el
manuscrito de Beethoven. La elección se recuerda en el navegador. Si no elige
nada, la página sigue al tema del sistema.

Contraste del texto verificado en los cuatro (mínimo WCAG AA = 4.5):

| Fondo | Texto | Epígrafes |
|---|---|---|
| Claro | 15.38 · AAA | 6.05 · AA |
| Oscuro | 14.37 · AAA | 6.87 · AA |
| Partitura | 15.07 · AAA | 7.16 · AAA |
| Beethoven | 14.53 · AAA | 6.90 · AA |

Los pentagramas del fondo "partitura" son gradientes CSS, no una imagen. El de
Beethoven es la única imagen de fondo, y no se regenera con el build: está
versionada en `img/`.

## Actualizarlo

El sitio se sirve con GitHub Pages desde la rama `main` de
[AgusPk/pequenas-composiciones](https://github.com/AgusPk/pequenas-composiciones).
Para publicar un cambio:

```bash
git add -A && git commit -m "corrección" && git push
```

Tarda uno o dos minutos en verse online.

La página es pública y **sí** se indexa en Google. Para que el link siga
funcionando pero deje de aparecer en búsquedas, agregar en el `<head>` de
`index.html`:

```html
<meta name="robots" content="noindex, nofollow">
```

Para un blog ya existente (WordPress, Medium, Substack) conviene el `.docx`:
se pega con las fotos incluidas.
