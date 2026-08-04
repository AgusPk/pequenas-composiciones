# Pequeñas composiciones de una niña
### Margarita Sastre Inchauspe — Buenos Aires, febrero 2026

**Publicado en → https://aguspk.github.io/pequenas-composiciones/**

Versión ordenada del original `2 PEQUEÑAS COMPOSICIONES (1).docx`.

## Qué hay acá

| Archivo | Para qué |
|---|---|
| `index.html` | El libro como página web. Un solo archivo + la carpeta `img/`. Se abre en cualquier navegador y se puede subir tal cual a un blog. |
| `img/` | Las 118 fotos, optimizadas para web (24 MB → 7,7 MB, ninguna pierde nitidez). |
| `Pequenas-composiciones-de-una-nina.docx` | El mismo contenido en Word, para copiar y pegar en WordPress, Medium, Substack, etc. Se descarga también desde el pie de la página. |
| `og.jpg` | La imagen de vista previa que aparece al compartir el link por WhatsApp o redes. |

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
