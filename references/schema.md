# Architecture SVG Source Schema

The renderer accepts JSON or YAML. Use explicit coordinates when visual fidelity matters.

## Minimal Shape

```yaml
canvas:
  width: 760
  height: 260
  title: System architecture
  description: Compute blocks connect through cache to external memory.

groups:
  - id: die
    x: 20
    y: 16
    w: 520
    h: 220
    label: single die
    kind: die

nodes:
  - id: compute
    x: 44
    y: 58
    w: 180
    h: 52
    label: SIMT vector path
    sub: N x 32 lanes
    kind: vec
    rx: 8

  - id: cache
    x: 44
    y: 160
    w: 460
    h: 42
    label: L2 cache
    kind: mem

edges:
  - from: compute
    to: cache
    path: M134 110 V160
    kind: edge
    arrow: true

legend:
  - label: vector
    kind: vec
```

## Canvas

- `width`, `height`: positive numbers. Defaults are 760 and 300.
- `title`: concise accessible name. Required for useful output.
- `description`: one or two sentences describing the relationship. Required for useful output.
- `background`: optional SVG background color. Prefer transparent output when embedding in a themed HTML page.

## Groups

Groups are visual boundaries, not graph nodes. Fields:

- `id`: optional unique identifier.
- `x`, `y`, `w`, `h`: rectangle geometry.
- `label`: optional small group label.
- `kind`: `die`, `reserved`, or `group`. `die` uses the dashed boundary style.
- `rx`: optional corner radius.

## Nodes

Required fields are `id`, `x`, `y`, `w`, `h`, and `label`. Optional fields:

- `sub`: one secondary line.
- `tiny`: one small annotation line.
- `lines`: an array of additional lines. Use it instead of overlong labels.
- `kind`: `base`, `vec`, `uni`, `ten`, `mem`, or `ctl`.
- `rx`: corner radius, default 7.
- `emphasis`: set to `true` for a slightly stronger border.
- `anchor`: `middle`, `start`, or `end`. Default is centered text.

The renderer escapes labels and splits `\n` into separate SVG text lines. Keep each line short enough for the node width.

## Edges

Required fields are `from` and `to`. Use an explicit SVG `path` whenever the route matters. If `path` is omitted, the renderer creates a center-to-center line. Optional fields:

- `kind`: `edge`, `edge-g`, `edge-c`, `edge-l`, or `edge-p`.
- `path`: sanitized SVG path data such as `M120 80 H220 V160`.
- `arrow`: boolean; defaults to `true`.
- `dashed`: boolean; uses a short dash pattern.
- `label`: optional text at the midpoint for straight inferred edges.

Do not use raw HTML in edge labels or node labels.

## Legend

Each item uses `label` and `kind`. Keep legends compact and place them outside the SVG when the host document already has a legend component. Use a legend only when the color mapping is important to reading the figure.

## Layout Guidance

- Keep the main diagram inside the canvas with at least 16px of padding.
- Leave room for the longest label and for arrowheads at the canvas edge.
- Use repeated coordinate increments for grids, for example 56px cell pitch.
- Use explicit paths for branches, buses, and shared resources.
- Prefer a few larger figures over one overloaded diagram. Split ISA, memory, and control views when the labels become unreadable.
