#!/usr/bin/env python3
"""Render a small explicit-layout architecture description as themed SVG."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


SKILL_ROOT = Path(__file__).resolve().parents[1]
THEME_PATH = SKILL_ROOT / "assets" / "architecture-theme.css"
PATH_RE = re.compile(r"^[0-9A-Za-z\s.,+\-()MmLlHhVvCcSsQqTtAaZz]+$")
NODE_KINDS = {"base", "vec", "uni", "ten", "mem", "ctl"}
EDGE_KINDS = {"edge", "edge-g", "edge-c", "edge-l", "edge-p"}
GROUP_KINDS = {"die", "reserved", "group"}


class SourceError(ValueError):
    """Raised when the source description cannot be rendered safely."""


def number(value: Any, name: str, default: float | None = None) -> float:
    if value is None and default is not None:
        return default
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise SourceError(f"{name} must be a number") from exc
    if result != result or result in (float("inf"), float("-inf")):
        raise SourceError(f"{name} must be finite")
    return result


def text_lines(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        values: list[str] = []
        for item in value:
            values.extend(str(item).splitlines())
        return values
    return str(value).splitlines()


def xml_text(value: Any) -> str:
    return escape(str(value), quote=False)


def load_source(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SourceError(f"cannot read {path}: {exc}") from exc

    try:
        if path.suffix.lower() == ".json":
            data = json.loads(raw)
        else:
            if yaml is None:
                raise SourceError(
                    "YAML input requires PyYAML; use JSON or install the yaml package"
                )
            data = yaml.safe_load(raw)
    except SourceError:
        raise
    except Exception as exc:
        raise SourceError(f"cannot parse {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise SourceError("top-level source must be an object")
    return data


def source_parts(data: dict[str, Any]) -> tuple[dict[str, Any], list[Any], list[Any], list[Any], Any]:
    graph = data.get("graph") if isinstance(data.get("graph"), dict) else {}
    canvas = data.get("canvas") if isinstance(data.get("canvas"), dict) else {}
    nodes = data.get("nodes", graph.get("nodes", []))
    groups = data.get("groups", graph.get("groups", []))
    edges = data.get("edges", graph.get("edges", []))
    legend = data.get("legend", graph.get("legend", []))
    for name, value in (("nodes", nodes), ("groups", groups), ("edges", edges)):
        if not isinstance(value, list):
            raise SourceError(f"{name} must be a list")
    return canvas, nodes, groups, edges, legend


def validate_and_index(data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], Any]:
    canvas, raw_nodes, raw_groups, raw_edges, legend = source_parts(data)
    width = number(canvas.get("width"), "canvas.width", 760)
    height = number(canvas.get("height"), "canvas.height", 300)
    if width <= 0 or height <= 0:
        raise SourceError("canvas width and height must be positive")

    nodes: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(raw_nodes):
        if not isinstance(raw, dict):
            raise SourceError(f"nodes[{index}] must be an object")
        node_id = str(raw.get("id", "")).strip()
        if not node_id:
            raise SourceError(f"nodes[{index}] is missing id")
        if node_id in nodes:
            raise SourceError(f"duplicate node id: {node_id}")
        for field in ("x", "y", "w", "h"):
            value = number(raw.get(field), f"nodes[{index}].{field}")
            if field in ("w", "h") and value <= 0:
                raise SourceError(f"nodes[{index}].{field} must be positive")
        kind = str(raw.get("kind", "base"))
        if kind not in NODE_KINDS:
            raise SourceError(f"nodes[{index}].kind must be one of {sorted(NODE_KINDS)}")
        if not text_lines(raw.get("label")):
            raise SourceError(f"nodes[{index}] is missing label")
        nodes[node_id] = raw

    groups: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_groups):
        if not isinstance(raw, dict):
            raise SourceError(f"groups[{index}] must be an object")
        for field in ("x", "y", "w", "h"):
            value = number(raw.get(field), f"groups[{index}].{field}")
            if field in ("w", "h") and value <= 0:
                raise SourceError(f"groups[{index}].{field} must be positive")
        kind = str(raw.get("kind", "group"))
        if kind not in GROUP_KINDS:
            raise SourceError(f"groups[{index}].kind must be one of {sorted(GROUP_KINDS)}")
        groups.append(raw)

    edges: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_edges):
        if not isinstance(raw, dict):
            raise SourceError(f"edges[{index}] must be an object")
        for field in ("from", "to"):
            endpoint = str(raw.get(field, "")).strip()
            if endpoint not in nodes:
                raise SourceError(f"edges[{index}].{field} references unknown node {endpoint!r}")
        kind = str(raw.get("kind", "edge"))
        if kind not in EDGE_KINDS:
            raise SourceError(f"edges[{index}].kind must be one of {sorted(EDGE_KINDS)}")
        if raw.get("path") is not None:
            path = str(raw["path"]).strip()
            if not path or not PATH_RE.fullmatch(path):
                raise SourceError(f"edges[{index}].path contains unsupported SVG path characters")
        edges.append(raw)

    normalized_canvas = dict(canvas)
    normalized_canvas["width"] = width
    normalized_canvas["height"] = height
    return normalized_canvas, nodes, groups, edges, legend


def fmt(value: float) -> str:
    value = float(value)
    if value.is_integer():
        return str(int(value))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def center(node: dict[str, Any]) -> tuple[float, float]:
    return (
        number(node["x"], "node.x") + number(node["w"], "node.w") / 2,
        number(node["y"], "node.y") + number(node["h"], "node.h") / 2,
    )


def boundary_point(node: dict[str, Any], target: tuple[float, float]) -> tuple[float, float]:
    x = number(node["x"], "node.x")
    y = number(node["y"], "node.y")
    w = number(node["w"], "node.w")
    h = number(node["h"], "node.h")
    cx, cy = x + w / 2, y + h / 2
    dx, dy = target[0] - cx, target[1] - cy
    if abs(dx) * h >= abs(dy) * w:
        return (x + w if dx >= 0 else x, cy)
    return (cx, y + h if dy >= 0 else y)


def inferred_path(source: dict[str, Any], target: dict[str, Any]) -> str:
    source_center = center(source)
    target_center = center(target)
    start = boundary_point(source, target_center)
    end = boundary_point(target, source_center)
    return f"M {fmt(start[0])} {fmt(start[1])} L {fmt(end[0])} {fmt(end[1])}"


def marker_for(kind: str) -> str:
    suffix = {
        "edge": "",
        "edge-g": "-g",
        "edge-c": "-c",
        "edge-l": "-l",
        "edge-p": "-p",
    }[kind]
    return f"arch-arrow{suffix}"


def draw_lines(
    out: list[str],
    lines: list[str],
    x: float,
    center_y: float,
    class_name: str,
    anchor: str = "middle",
    line_height: float = 15,
) -> None:
    if not lines:
        return
    start_y = center_y - (len(lines) - 1) * line_height / 2
    for index, line in enumerate(lines):
        out.append(
            f'    <text class="{class_name}" x="{fmt(x)}" y="{fmt(start_y + index * line_height)}" '
            f'text-anchor="{anchor}">{xml_text(line)}</text>'
        )


def draw_node(out: list[str], node: dict[str, Any]) -> None:
    x = number(node["x"], "node.x")
    y = number(node["y"], "node.y")
    w = number(node["w"], "node.w")
    h = number(node["h"], "node.h")
    kind = str(node.get("kind", "base"))
    rx = number(node.get("rx"), "node.rx", 7)
    classes = f"box {kind}" + (" emphasis" if node.get("emphasis") else "")
    out.append(
        f'    <rect class="{classes}" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" '
        f'height="{fmt(h)}" rx="{fmt(rx)}" />'
    )

    anchor = str(node.get("anchor", "middle"))
    if anchor not in {"start", "middle", "end"}:
        raise SourceError(f"node {node.get('id')} has invalid anchor")
    text_x = x + w / 2 if anchor == "middle" else (x + 10 if anchor == "start" else x + w - 10)
    lines: list[tuple[str, str, float]] = []
    lines.extend(("lbl" if index == 0 else "sub", line, 15 if index == 0 else 13) for index, line in enumerate(text_lines(node.get("label"))))
    lines.extend(("sub", line, 13) for line in text_lines(node.get("sub")))
    lines.extend(("tiny", line, 12) for line in text_lines(node.get("tiny")))
    lines.extend(("tiny", line, 12) for line in text_lines(node.get("lines")))
    if not lines:
        return
    total = sum(spacing for _, _, spacing in lines)
    baseline = y + h / 2 - total / 2 + 10
    for class_name, line, spacing in lines:
        out.append(
            f'    <text class="{class_name} t-{kind}" x="{fmt(text_x)}" y="{fmt(baseline)}" '
            f'text-anchor="{anchor}">{xml_text(line)}</text>'
        )
        baseline += spacing


def draw_group(out: list[str], group: dict[str, Any]) -> None:
    x = number(group["x"], "group.x")
    y = number(group["y"], "group.y")
    w = number(group["w"], "group.w")
    h = number(group["h"], "group.h")
    kind = str(group.get("kind", "group"))
    class_name = "die" if kind == "die" else "reserved" if kind == "reserved" else "box"
    rx = number(group.get("rx"), "group.rx", 14)
    if class_name == "box":
        out.append(
            f'    <rect class="box" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" '
            f'height="{fmt(h)}" rx="{fmt(rx)}" fill="none" />'
        )
    else:
        out.append(
            f'    <rect class="{class_name}" x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" '
            f'height="{fmt(h)}" rx="{fmt(rx)}" />'
        )
    label = text_lines(group.get("label"))
    if label:
        out.append(
            f'    <text class="tiny" x="{fmt(x + 14)}" y="{fmt(y + 20)}">{xml_text(label[0])}</text>'
        )


def draw_edge(out: list[str], edge: dict[str, Any], nodes: dict[str, dict[str, Any]]) -> None:
    kind = str(edge.get("kind", "edge"))
    path = str(edge.get("path")).strip() if edge.get("path") is not None else inferred_path(nodes[str(edge["from"])], nodes[str(edge["to"])])
    attrs = [f'class="{kind}"', f'd="{path}"']
    if edge.get("dashed"):
        attrs.append('stroke-dasharray="3 3"')
    if edge.get("arrow", True):
        attrs.append(f'marker-end="url(#{marker_for(kind)})"')
    out.append(f"    <path {' '.join(attrs)} />")

    if edge.get("label") and edge.get("path") is None:
        x1, y1 = center(nodes[str(edge["from"])])
        x2, y2 = center(nodes[str(edge["to"])])
        out.append(
            f'    <text class="tiny" x="{fmt((x1 + x2) / 2)}" y="{fmt((y1 + y2) / 2 - 5)}" '
            f'text-anchor="middle">{xml_text(edge["label"])}</text>'
        )


def normalize_legend(legend: Any, height: float) -> tuple[list[dict[str, Any]], float, float]:
    if isinstance(legend, dict):
        items = legend.get("items", [])
        x = number(legend.get("x"), "legend.x", 20)
        y = number(legend.get("y"), "legend.y", height - 12)
    else:
        items = legend
        x, y = 20, height - 12
    if not isinstance(items, list):
        raise SourceError("legend or legend.items must be a list")
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise SourceError(f"legend[{index}] must be an object")
        kind = str(item.get("kind", "base"))
        if kind not in NODE_KINDS:
            raise SourceError(f"legend[{index}].kind must be one of {sorted(NODE_KINDS)}")
        normalized.append(item)
    return normalized, x, y


def draw_legend(out: list[str], legend: Any, height: float) -> None:
    items, x, y = normalize_legend(legend, height)
    cursor = x
    for item in items:
        label = str(item.get("label", ""))
        kind = str(item.get("kind", "base"))
        out.append(
            f'    <rect class="{kind}" x="{fmt(cursor)}" y="{fmt(y - 9)}" width="11" height="11" rx="3" />'
        )
        out.append(
            f'    <text class="tiny" x="{fmt(cursor + 18)}" y="{fmt(y)}">{xml_text(label)}</text>'
        )
        cursor += max(74, 22 + len(label) * 7)


def render(data: dict[str, Any]) -> str:
    canvas, nodes, groups, edges, legend = validate_and_index(data)
    width = canvas["width"]
    height = canvas["height"]
    title = str(canvas.get("title", "Architecture diagram"))
    description = str(canvas.get("description", "Technical architecture diagram"))
    background = canvas.get("background")

    try:
        theme = THEME_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        raise SourceError(f"cannot read bundled theme: {exc}") from exc

    labelled = "arch-svg-title"
    described = "arch-svg-desc"
    out = [
        f'<svg class="dgm" viewBox="0 0 {fmt(width)} {fmt(height)}" width="100%" height="auto" '
        f'role="img" aria-labelledby="{labelled} {described}" preserveAspectRatio="xMidYMid meet">',
        "  <style><![CDATA[",
        theme.rstrip(),
        "  ]]></style>",
        f'  <title id="{labelled}">{xml_text(title)}</title>',
        f'  <desc id="{described}">{xml_text(description)}</desc>',
        "  <defs>",
        '    <marker id="arch-arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6 z" fill="var(--ink-faint)" /></marker>',
        '    <marker id="arch-arrow-g" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6 z" fill="var(--gold)" /></marker>',
        '    <marker id="arch-arrow-c" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6 z" fill="var(--cyan)" /></marker>',
        '    <marker id="arch-arrow-l" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6 z" fill="var(--lime)" /></marker>',
        '    <marker id="arch-arrow-p" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6 z" fill="var(--pink)" /></marker>',
        "  </defs>",
    ]
    if background:
        out.append(f'  <rect width="100%" height="100%" fill="{escape(str(background), quote=True)}" />')
    for group in groups:
        draw_group(out, group)
    for edge in edges:
        draw_edge(out, edge, nodes)
    for node in nodes.values():
        draw_node(out, node)
    if legend:
        draw_legend(out, legend, height)
    out.append("</svg>")
    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="JSON or YAML architecture description")
    parser.add_argument("-o", "--output", type=Path, help="output SVG path")
    args = parser.parse_args()

    output = args.output or args.source.with_suffix(".svg")
    try:
        svg = render(load_source(args.source))
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(svg.encode("utf-8"))
    except SourceError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"error: cannot write {output}: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
