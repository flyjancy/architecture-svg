# Architecture SVG Theme

This theme is a restrained dark technical style inspired by Jerry's design language. Keep the semantic mapping stable across figures.

## Tokens

```css
--bg: #0b0f14;
--bg-2: #0e141b;
--bg-3: #141c26;
--bg-4: #1a2430;
--line: #23303f;
--line-2: #2e3e50;
--ink: #e7eef5;
--ink-dim: #9fb0c0;
--ink-faint: #62748a;
--gold: #f4b740;
--gold-2: #ffd27a;
--cyan: #48cbe0;
--lime: #9bd84e;
--blue: #5e9be6;
--pink: #ec6fa6;
--red: #ef6f6f;
```

Use `--gold` for the primary emphasis and navigation state. Use the other semantic colors only for persistent categories. Use low-opacity fills around 0.10-0.15 and thin strokes around 1.3-1.6px.

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
.dgm .vec       gold semantic fill and stroke
.dgm .uni       cyan semantic fill and stroke
.dgm .ten       lime semantic fill and stroke
.dgm .mem       blue semantic fill and stroke
.dgm .ctl       pink semantic fill and stroke
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

The wrapper uses `background: var(--bg-2)`, `border: 1px solid var(--line)`, a modest radius, and padding. The SVG itself should remain transparent unless a filled region is part of the diagram.

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
