# Architecture SVG Theme

This theme is a restrained soft light technical style inspired by Jerry's design language. Keep the semantic mapping stable across figures.

## Tokens

```css
--bg: #f4f6f3;
--bg-2: #ffffff;
--bg-3: #edf2ef;
--bg-4: #e3ebe7;
--line: #d8e1dc;
--line-2: #b8c7c0;
--ink: #25363a;
--ink-dim: #5d7072;
--ink-faint: #829294;
--gold: #b4863b;
--gold-2: #d2ad68;
--cyan: #4b9da5;
--lime: #78a35f;
--blue: #668ab2;
--pink: #b47c94;
--red: #c87368;
```

Use `--gold` for the primary emphasis and navigation state. Use the other muted semantic colors only for persistent categories. Use low-opacity fills around 0.12-0.16 and thin strokes around 1.3-1.6px so the figure stays soft without losing structure.

## Typography

- Display headings: `Chakra Petch`, with `IBM Plex Sans` fallback.
- Diagram labels and technical values: `IBM Plex Mono`, with `Cascadia Code` or a system monospace fallback.
- Body copy: `IBM Plex Sans`, with a CJK-capable system fallback.
- Diagram label: about 13px, weight 600.
- Diagram sublabel: about 10.5px, weight 400.
- Diagram tiny annotation: about 9.5px, weight 400.

Keep label hierarchy visible through size and color. Do not use many font weights or large text inside compact blocks.

## SVG Classes

The shared SVG classes are:

```text
.dgm .box       neutral module fill and border
.dgm .die       dashed conceptual or die boundary
.dgm .lbl       primary label
.dgm .sub       secondary label
.dgm .tiny      annotation or bit width
.dgm .vec       muted ochre semantic fill and stroke
.dgm .uni       muted cyan semantic fill and stroke
.dgm .ten       muted green semantic fill and stroke
.dgm .mem       muted blue semantic fill and stroke
.dgm .ctl       muted rose semantic fill and stroke
.dgm .t-vec    gold label text
.dgm .t-uni    cyan label text
.dgm .t-ten    lime label text
.dgm .t-mem    blue label text
.dgm .t-ctl    pink label text
.dgm .edge     neutral connector
.dgm .edge-g   gold connector
.dgm .edge-c   cyan connector
.dgm .edge-l   lime connector
.dgm .edge-p   pink connector
```

Draw connectors before blocks so nodes visually sit above the data path. Use `stroke-dasharray="3 3"` for zoom guides or optional paths and `stroke-dasharray="5 4"` for a group boundary.

## Figure Wrapper

Use a single wrapper around each diagram:

```html
<figure class="arch-figure">
  <svg class="dgm" viewBox="0 0 760 300" role="img"
       aria-labelledby="arch-title arch-desc">
    <title id="arch-title">System architecture</title>
    <desc id="arch-desc">A single die connects the compute blocks to cache and external memory.</desc>
    <!-- SVG primitives -->
  </svg>
  <figcaption><b>Figure 1</b> - Short explanatory caption.</figcaption>
</figure>
```

The wrapper uses a white surface with `background: var(--bg-2)`, `border: 1px solid var(--line)`, a modest radius, and padding. The SVG itself should remain transparent unless a filled region is part of the diagram.

## Layout Patterns

### System hierarchy

Use a dashed outer boundary for die or package, a grid of repeated blocks, a shared cache below, and external memory to the right. Keep the external interface outside the boundary.

### Datapath

Use a horizontal sequence of blocks. Group the new or emphasized backend in a semantic colored region and keep reused infrastructure neutral.

### Pipeline

Use explicit orthogonal paths and a single reading direction. Place annotations above or below the path, never on top of edges.

### Bitfield

Use proportional rectangles in one row, then a second row expanding the field under discussion. Mark reserved or guard fields with a neutral or control color.

### Array

Use a regular grid with one semantic color. Put input arrows on the top and left, output or accumulation arrows on the right or bottom, and place a compact precision or metadata panel beside the grid.
