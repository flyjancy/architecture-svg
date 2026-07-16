---
name: architecture-svg
description: Create polished static architecture and data-path diagrams from structured JSON or YAML using inline SVG, with a Calibri-based engineering-diagram style, medium-gray canvas, pale blue/green/peach modules, black connectors, manual layout control, legends, captions, and accessible responsive HTML embedding. Use for RTL, CPU/GPU, SoC, compiler, ISA, memory, pipeline, dependency, and other engineering architecture figures when exact visual composition matters.
---

# Architecture SVG

## Purpose

Create technical architecture figures that look like a deliberate engineering document, not a default graph-renderer output. Use structured JSON/YAML for semantic content and SVG for precise geometry.

Use the bundled renderer when the input already has coordinates or when a repeatable JSON/YAML-to-SVG path is useful:

```text
python scripts/render_architecture_svg.py input.yaml --output architecture.svg
```

Read `references/schema.md` for the input contract and `references/theme.md` for the complete visual system. Use `assets/architecture-svg-template.html` when adding a figure to a static HTML document.

## Workflow

1. Identify the diagram purpose and the main reading direction. Prefer a single dominant figure with a short caption.
2. Normalize the source into nodes, groups, edges, legends, and annotations. Validate unique node IDs and all edge references before drawing.
3. Choose a fixed `viewBox`, normally 760px wide. Use explicit `x`, `y`, `w`, and `h` for important blocks. Do not use automatic layout by default; manual geometry is what gives this style its editorial precision.
4. Draw edges before nodes. Use simple orthogonal or gently curved paths with restrained neutral strokes. Add arrow markers only where direction matters.
5. Draw group boundaries, nodes, labels, sublabels, and notes using the shared classes from `references/theme.md`.
6. Add a compact legend only when color has persistent semantic meaning. Add `<title>`, `<desc>`, `role="img"`, and `aria-labelledby` to every SVG.
7. Wrap the SVG in a `figure` with a light diagram surface and a Calibri caption. Keep the caption outside the SVG so the figure can be reused in documents.
8. Inspect the rendered result at desktop and narrow widths. Fix clipped text, crossing edges, cramped labels, and unclear arrow direction before delivering it.
9. Perform a collision pass: confirm that text never overlaps lines, arrowheads, node borders, group boundaries, legends, captions, or other labels. Adjust geometry, connector lanes, label offsets, or block sizes when it does; do not hide the collision by merely shrinking the font.
10. If the SVG will be opened directly as a file, add `xmlns="http://www.w3.org/2000/svg"` and explicit root `width`/`height` attributes. Keep the responsive `width:100%; height:auto` behavior in the HTML wrapper, but do not rely on `height="auto"` for a standalone SVG because some viewers calculate a zero-height canvas.

## Rendering Choices

- Use inline SVG for diagrams that need exact composition, semantic fills, arrows, bit fields, grids, or mixed labels.
- Use the bundled Python renderer for stable, repeatable output from JSON/YAML. It supports explicit geometry, semantic node kinds, groups, legends, multiline labels, and edge paths.
- Use Mermaid only for a quick rough sketch when exact styling is unimportant.
- Use Graphviz only when the user explicitly needs automatic graph layout or the graph is too large for manual composition. If Graphviz is used, treat its output as geometry input and restyle or redraw the final SVG to match this theme.
- Do not introduce a JavaScript graph library for a static architecture figure.

## Semantic Vocabulary

Use these node kinds consistently. Keep the fills pale and the outlines/text black, matching the reference engineering diagrams:

- `base`: neutral structure or unlabeled infrastructure; light gray or pale blue
- `vec`: vector/SIMT/compute path; pale peach
- `uni`: uniform/scalar/control-adjacent path; pale blue
- `ten`: tensor/accelerator path; pale green
- `mem`: register/cache/shared/external memory; soft green
- `ctl`: scheduler/control/synchronization; pale peach

Use the matching edge classes for important flows: `edge`, `edge-g`, `edge-c`, `edge-l`, and `edge-p`. Keep most structural edges neutral. Color the edge only when it carries the same meaning as its source or destination.

## Composition Rules

- Start with the visual relationship, not a decorative title or card grid.
- Prefer a few large, legible blocks over many tiny boxes.
- Keep labels short. Put detail in a second line, a note, or the caption.
- Reserve clear space around every label. Never route a connector or arrowhead through text, and never place text on top of a boundary unless the overlap is an intentional, documented annotation.
- Use one visual language per figure: blocks plus connectors, a bitfield, a matrix, or a pipeline.
- Use dashed boundaries for dies, clusters, reserved fields, or conceptual groupings. Use dashed connectors for zoom guides or optional paths.
- Use pale semantic fills, solid black or near-black borders, and black connectors. Do not color every border or line with a different hue.
- Use a stronger stroke only for a deliberately highlighted shared resource or critical path.
- Keep the canvas wide and shallow when the relationship is sequential. Use square geometry only for arrays and grids.
- Keep the figure surface unframed in the outer page when the host already provides a figure wrapper; do not nest decorative cards.
- Treat port and interface labels such as `Configuration Loads`, `Instruction Loads`, and `Stream Data I/O` as annotations, not functional modules: use plain text and connector lanes instead of drawing boxes around them.
- Reserve filled rectangles for actual architectural blocks and conceptual groups. Remove placeholder/invisible nodes from the final SVG when they were only needed to anchor bidirectional edges.
- Leave intentional breathing room below shared resources such as accumulators or sum engines. Extend the canvas or enclosing panel rather than pushing the resource closer to the bottom edge.

## SVG Requirements

Every generated SVG must:

- Have a stable `viewBox` and `width="100%" height="auto"` in HTML.
- Define arrow markers in `<defs>` when arrows are used.
- Escape all user-provided text. Never inject raw HTML into labels.
- Use `currentColor` only when the surrounding document intentionally supplies the color; otherwise use the theme classes.
- Scope styles under `svg.dgm` or an equivalent unique root. Never apply a broad `svg` selector to a page containing icons.
- Include `title` and `desc` text that summarize the structure without repeating the entire caption.
- Avoid external data requests and runtime fetches for static diagrams.
- Use an explicit two-tier typography system: one consistent size/weight for all lines of a module label, and a smaller consistent size for parameters and interface annotations. Do not let multiline rendering implicitly make the first line bold and later lines normal unless that hierarchy is intentional.

## Responsive and Accessibility Checks

Before delivery, verify:

- Labels fit inside their parent blocks at the final `viewBox` scale.
- Text does not overlap connectors, arrowheads, node borders, group boundaries, legends, captions, other labels, or the canvas edge.
- Lines do not pass through text or create ambiguous tangencies with text and borders; adjust paths and label offsets until the figure reads cleanly at normal viewing size.
- The SVG scales down without horizontal page overflow. Use `width:100%` and preserve aspect ratio.
- Color is paired with text, position, shape, or line style; meaning must not depend on color alone.
- The figure remains understandable in grayscale or with semantic colors muted.
- The SVG has a useful accessible name and description.

## Output Modes

- For an existing documentation site, edit the project HTML/CSS and preserve its build and deployment conventions.
- For a standalone SVG, run the bundled renderer and return the generated `.svg`.
- For a standalone HTML figure, use the template and inline the generated SVG. Load fonts only when the target environment permits it; keep system-font fallbacks.
- When the user asks for an in-conversation visual, combine this skill's SVG rules with the `visualize` skill's inline visualization contract.

## Resources

- `references/schema.md`: JSON/YAML source contract and examples.
- `references/theme.md`: Jerry-inspired palette, typography, CSS classes, and layout rules.
- `scripts/render_architecture_svg.py`: deterministic JSON/YAML-to-SVG renderer with validation.
- `assets/architecture-theme.css`: reusable SVG and figure CSS.
- `assets/architecture-svg-template.html`: minimal static HTML embedding template.
