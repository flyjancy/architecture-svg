# Architecture SVG Theme

This theme follows the supplied engineering-diagram references: a medium-gray canvas, light diagram panels, pale blue/green/peach modules, black outlines and connectors, and Calibri typography. Keep the semantic mapping stable across figures.

## Tokens

```css
--bg: #858585;
--bg-2: #f1f1f1;
--bg-3: #e7edf3;
--bg-4: #dfe5eb;
--line: #171717;
--line-2: #2e2e2e;
--ink: #111111;
--ink-dim: #383838;
--ink-faint: #686868;
--fill-peach: #f7e5d7;
--fill-peach-2: #f1d8c5;
--fill-blue: #e4ebf3;
--fill-green: #b8d18a;
--fill-green-2: #d6e4b6;
```

Use `--fill-peach`, `--fill-blue`, and `--fill-green` for semantic module fills. Keep outlines and data paths black or near-black, with thin strokes around 1.3-1.6px. The gray `--bg` is the outer canvas and `--bg-2` is the light figure surface.

## Typography

- Display headings: `Calibri`, with Arial and a CJK-capable system fallback.
- Diagram labels and technical values: `Calibri`, with Arial and a CJK-capable system fallback.
- Body copy: `Calibri`, with Arial and a CJK-capable system fallback.
- Diagram label: about 13px, weight 600.
- Diagram sublabel: about 10.5px, weight 400.
- Diagram tiny annotation: about 9.5px, weight 400.

Keep label hierarchy visible through size and color. Do not use many font weights or large text inside compact blocks.

## Collision And Spacing Pass

- Treat any text touching or crossing a connector, arrowhead, node border, group boundary, legend, caption, or another label as a visual defect.
- Keep labels in clear lanes above or below paths. Use explicit offsets and short second lines instead of placing long text on top of a line.
- Inspect the final `viewBox` at normal rendered size. If a label collides, move the path or label and enlarge the block before reducing font size.
- Check narrow-width rendering as well as desktop rendering; responsive scaling must not turn a small gap into an overlap.

## SVG Classes

The shared SVG classes are:

```text
.dgm .box       neutral module fill and border
.dgm .die       dashed conceptual or die boundary
.dgm .lbl       primary label
.dgm .sub       secondary label
.dgm .tiny      annotation or bit width
.dgm .vec       pale peach semantic fill and black stroke
.dgm .uni       pale blue semantic fill and black stroke
.dgm .ten       pale green semantic fill and black stroke
.dgm .mem       soft green semantic fill and black stroke
.dgm .ctl       pale peach semantic fill and black stroke
.dgm .t-vec     black label text
.dgm .t-uni     black label text
.dgm .t-ten     black label text
.dgm .t-mem     black label text
.dgm .t-ctl     black label text
.dgm .edge     neutral connector
.dgm .edge-g   black emphasized connector
.dgm .edge-c   black emphasized connector
.dgm .edge-l   black emphasized connector
.dgm .edge-p   black emphasized connector
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

Use explicit orthogonal paths and a single reading direction. Place annotations above or below the path, never on top of edges. Leave enough vertical clearance for arrowheads and labels.

### Bitfield

Use proportional rectangles in one row, then a second row expanding the field under discussion. Mark reserved or guard fields with a neutral or control color.

### Array

Use a regular grid with one semantic color. Put input arrows on the top and left, output or accumulation arrows on the right or bottom, and place a compact precision or metadata panel beside the grid.
