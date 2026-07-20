# Architecture SVG

Codex skill for creating polished static architecture and data-path diagrams with inline SVG, structured JSON/YAML input, semantic colors, manual layout control, and accessible desktop HTML embedding.

The default visual style uses a medium-gray canvas, pale blue/green/peach modules, black connectors, and Calibri typography. Composition and QA are optimized for desktop viewing; mobile-specific layout is out of scope.

## Contents

- `SKILL.md`: workflow, composition rules, SVG requirements, and accessibility checks.
- `agents/openai.yaml`: Codex agent metadata.
- `assets/`: reusable HTML and CSS templates.
- `references/`: input schema and visual theme documentation.
- `scripts/render_architecture_svg.py`: deterministic JSON/YAML-to-SVG renderer.

## Quick Start

```powershell
python scripts/render_architecture_svg.py input.yaml --output architecture.svg
```

## Installation

Copy this directory into your Codex skills directory, for example:

```text
%USERPROFILE%\\.codex\\skills\\architecture-svg
```
