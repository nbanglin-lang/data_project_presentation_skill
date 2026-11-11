"""Slide-ready matplotlib helpers for the data-project-deck skill.

Every helper follows the same rules (see references/visualization.md):
grey for context, one accent for the point of the slide, direct labels,
no gridlines or box, bars start at zero, a source line, 12pt+ text.

Each function saves a PNG (200 dpi, white background) and returns its path.
`title` is an optional on-chart headline: pass None when the slide title
already states the takeaway (usually the better choice).

Usage:
    import sys; sys.path.insert(0, "<skill dir>/scripts")
    from chart_helpers import bar_highlight, line_end_labels, waterfall, ci_dots, pipeline_diagram
"""
from __future__ import annotations

import textwrap
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Palette: blue accent + orange contrast + neutrals. Distinguishable under common
# color-vision deficiencies and in grayscale (blue is dark, orange is mid, grey is light).
ACCENT = "#0072B2"
ACCENT_LIGHT = "#56B4E9"
ACCENT_DARK = "#004C75"
CONTRAST = "#D55E00"
GREY = "#BDBDBD"       # context marks
GREY_DARK = "#757575"  # context lines / muted text
INK = "#111111"
INK_2 = "#4D4D4D"
SURFACE = "#ffffff"

BASE_FONT = 13
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": BASE_FONT,
    "axes.edgecolor": GREY,
    "axes.labelcolor": INK_2,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "text.color": INK,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
})


def _new(figsize: Tuple[float, float]):
    fig, ax = plt.subplots(figsize=figsize)
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)
    return fig, ax


def _left_for(labels: Iterable[str], fig_width: float = 11.0) -> float:
    """Left margin (fraction of figure width) wide enough for the longest y label."""
    longest = max((len(str(l)) for l in labels), default=0)
    # ~0.095 inch per character at 13pt, plus a little padding
    return min(0.45, (longest * 0.095 + 0.15) / fig_width)


def _finish(fig, ax, path: str, title: Optional[str], source: Optional[str],
            left: float = 0.0, bottom: Optional[float] = None):
    """Add optional headline and source line, then save.

    left: extra left margin as a fraction of the figure width (room for y labels).
    bottom: override the bottom margin (room for wrapped x labels).
    """
    top_pad = 0.86 if title else 0.96
    bottom_pad = bottom if bottom is not None else (0.12 if source else 0.06)
    fig.subplots_adjust(top=top_pad, bottom=bottom_pad, left=0.02 + left, right=0.97)
    if title:
        fig.text(0.02, 0.95, title, ha="left", va="top", fontsize=BASE_FONT + 4,
                 fontweight="bold", color=INK, wrap=True)
    if source:
        fig.text(0.02, 0.02, source, ha="left", va="bottom", fontsize=BASE_FONT - 1,
                 color=GREY_DARK)
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return path


def bar_highlight(labels: Sequence[str], values: Sequence[float],
                  highlight: Optional[Iterable[str]] = None,
                  path: str = "bar.png", title: Optional[str] = None,
                  source: Optional[str] = None, fmt: str = "{:.1f}",
                  horizontal: bool = True, sort: bool = True,
                  reference: Optional[float] = None, reference_label: Optional[str] = None,
                  figsize: Tuple[float, float] = (11, 5.6)) -> str:
    """Sorted bars, grey except the highlighted ones, value labels at bar ends.

    highlight: labels to color with the accent (default: the largest bar).
    reference: optional vertical/horizontal reference line (e.g. the average).
    Bars always start at zero.
    """
    pairs = list(zip(labels, values))
    if horizontal:
        # barh draws the first item at the bottom: ascending puts the largest on top;
        # unsorted keeps the caller's order top-to-bottom by reversing.
        pairs = sorted(pairs, key=lambda p: p[1]) if sort else pairs[::-1]
    elif sort:
        pairs = sorted(pairs, key=lambda p: p[1], reverse=True)
    labs = [p[0] for p in pairs]
    vals = [p[1] for p in pairs]
    if highlight is None:
        highlight = [max(pairs, key=lambda p: p[1])[0]]
    hl = set(highlight)
    colors = [ACCENT if l in hl else GREY for l in labs]

    fig, ax = _new(figsize)
    left = 0.0
    if horizontal:
        left = _left_for(labs, figsize[0])
        bars = ax.barh(labs, vals, color=colors, height=0.62)
        vmax = max(max(vals), reference or 0)
        ax.set_xlim(0, vmax * 1.15)
        ax.set_xticks([])
        for b, v, l in zip(bars, vals, labs):
            ax.text(b.get_width() + vmax * 0.012, b.get_y() + b.get_height() / 2,
                    fmt.format(v), va="center", ha="left", fontsize=BASE_FONT,
                    fontweight="bold" if l in hl else "normal",
                    color=INK if l in hl else INK_2,
                    bbox=dict(fc=SURFACE, ec="none", pad=1.5), zorder=5)
        if reference is not None:
            ax.axvline(reference, color=GREY_DARK, lw=1.2, ls="--", zorder=1)
            if reference_label:
                ax.set_ylim(-0.6, len(labs) + 0.1)
                ax.text(reference, len(labs) - 0.45, reference_label, ha="center", va="bottom",
                        fontsize=BASE_FONT - 1, color=GREY_DARK)
        ax.tick_params(axis="y", labelsize=BASE_FONT)
        ax.axvline(0, color=GREY, lw=1)
    else:
        bars = ax.bar(labs, vals, color=colors, width=0.62)
        vmax = max(max(vals), reference or 0)
        ax.set_ylim(0, vmax * 1.15)
        ax.set_yticks([])
        for b, v, l in zip(bars, vals, labs):
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + vmax * 0.015,
                    fmt.format(v), ha="center", va="bottom", fontsize=BASE_FONT,
                    fontweight="bold" if l in hl else "normal",
                    color=INK if l in hl else INK_2)
        if reference is not None:
            ax.axhline(reference, color=GREY_DARK, lw=1.2, ls="--")
            if reference_label:
                ax.text(len(labs) - 0.5, reference, " " + reference_label, ha="right", va="bottom",
                        fontsize=BASE_FONT - 1, color=GREY_DARK)
        ax.axhline(0, color=GREY, lw=1)
        ax.tick_params(axis="x", labelsize=BASE_FONT)
    return _finish(fig, ax, path, title, source, left=left)


def line_end_labels(x: Sequence, series: Dict[str, Sequence[float]],
                    highlight: Optional[Iterable[str]] = None,
                    path: str = "line.png", title: Optional[str] = None,
                    source: Optional[str] = None, fmt: str = "{:.1f}",
                    ylabel: Optional[str] = None, zero_baseline: bool = False,
                    event: Optional[Tuple[object, str]] = None,
                    figsize: Tuple[float, float] = (11, 5.6)) -> str:
    """Lines with direct labels at the right end; no legend box.

    highlight: series names drawn in the accent color, thick; the rest are grey.
    event: optional (x_value, text) vertical marker, e.g. a policy change.
    zero_baseline: force y to start at 0 (set True when the claim is about size).
    """
    if highlight is None:
        highlight = [list(series)[0]]
    hl = set(highlight)
    fig, ax = _new(figsize)
    xs = list(x)
    pos = list(range(len(xs)))
    # draw context first so highlighted lines sit on top
    order = [n for n in series if n not in hl] + [n for n in series if n in hl]
    ymax = max(max(v) for v in series.values())
    ymin = min(min(v) for v in series.values())
    for name in order:
        vals = list(series[name])
        is_hl = name in hl
        ax.plot(pos, vals, color=ACCENT if is_hl else GREY_DARK, lw=3.2 if is_hl else 1.8,
                alpha=1.0 if is_hl else 0.7, solid_capstyle="round", zorder=3 if is_hl else 2)
        ax.scatter([pos[-1]], [vals[-1]], s=46, color=ACCENT if is_hl else GREY_DARK, zorder=4)
        ax.text(pos[-1] + 0.15, vals[-1], f"{name}  {fmt.format(vals[-1])}", va="center", ha="left",
                fontsize=BASE_FONT, fontweight="bold" if is_hl else "normal",
                color=INK if is_hl else INK_2)
    ax.set_xticks(pos)
    ax.set_xticklabels([str(v) for v in xs], fontsize=BASE_FONT - 1)
    span = ymax - ymin if ymax > ymin else 1
    ax.set_ylim(0 if zero_baseline else ymin - span * 0.1, ymax + span * 0.12)
    ax.set_xlim(-0.3, pos[-1] + max(2.6, 0.32 * len(xs)))
    ax.yaxis.set_visible(bool(ylabel))
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=BASE_FONT - 1)
        ax.tick_params(axis="y", labelsize=BASE_FONT - 1)
        ax.grid(axis="y", color="#E0E0E0", lw=0.8)
        ax.set_axisbelow(True)
    ax.axhline(ax.get_ylim()[0], color=GREY, lw=1)
    if event is not None:
        ev_x, ev_text = event
        if ev_x in xs:
            ex = xs.index(ev_x)
            ax.axvline(ex, color=CONTRAST, lw=1.5, ls="--", zorder=1)
            ax.text(ex, ax.get_ylim()[1], ev_text + " ", ha="right", va="top",
                    fontsize=BASE_FONT - 1, color=CONTRAST)
    return _finish(fig, ax, path, title, source, left=0.03 if ylabel else 0.0)


def waterfall(labels: Sequence[str], values: Sequence[float],
              path: str = "waterfall.png", title: Optional[str] = None,
              source: Optional[str] = None, fmt: str = "{:,.0f}",
              end_label: str = "Result", figsize: Tuple[float, float] = (11, 5.6)) -> str:
    """Bridge from a starting total through increases/decreases to an end total.

    values[0] is the starting total; the rest are signed changes. The end total is
    computed and appended. Totals use the dark accent, increases the light accent,
    decreases the orange contrast (not red/green, so it survives color-blind viewing).
    """
    if len(labels) != len(values):
        raise ValueError("labels and values must have the same length")
    start, deltas = values[0], list(values[1:])
    end = start + sum(deltas)
    names = list(labels) + [end_label]
    fig, ax = _new(figsize)
    ax.bar(0, start, color=ACCENT_DARK, width=0.62)
    ax.text(0, start, fmt.format(start), ha="center", va="bottom", fontweight="bold", fontsize=BASE_FONT)
    running = start
    top = max(start, end)
    for i, d in enumerate(deltas, start=1):
        bottom = running if d >= 0 else running + d
        ax.bar(i, abs(d), bottom=bottom, color=ACCENT_LIGHT if d >= 0 else CONTRAST, width=0.62)
        ax.plot([i - 1 + 0.31, i - 0.31], [running, running], color=GREY_DARK, lw=1)
        ax.text(i, max(running, running + d), ("+" if d >= 0 else "-") + fmt.format(abs(d)),
                ha="center", va="bottom", fontsize=BASE_FONT, color=INK_2)
        running += d
        top = max(top, running)
    n = len(deltas) + 1
    ax.plot([n - 1 + 0.31, n - 0.31], [running, running], color=GREY_DARK, lw=1)
    ax.bar(n, end, color=ACCENT_DARK, width=0.62)
    ax.text(n, end, fmt.format(end), ha="center", va="bottom", fontweight="bold", fontsize=BASE_FONT)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels([textwrap.fill(s, 14) for s in names], fontsize=BASE_FONT - 1)
    ax.set_yticks([])
    ax.set_ylim(0, top * 1.15)
    ax.axhline(0, color=GREY, lw=1)
    wrapped = any(len(textwrap.wrap(s, 14)) > 1 for s in names)
    bottom = (0.22 if wrapped else 0.13) if source else (0.14 if wrapped else 0.06)
    return _finish(fig, ax, path, title, source, bottom=bottom)


def ci_dots(labels: Sequence[str], estimates: Sequence[float],
            lows: Sequence[float], highs: Sequence[float],
            highlight: Optional[Iterable[str]] = None, reference: Optional[float] = None,
            reference_label: Optional[str] = None, path: str = "ci.png",
            title: Optional[str] = None, source: Optional[str] = None,
            fmt: str = "{:.2f}", figsize: Tuple[float, float] = (11, 5.0)) -> str:
    """Estimate with interval per row (e.g. model scores with confidence intervals).

    Use when the claim depends on a difference being real. Overlapping intervals
    mean the title should not claim a clear winner. Rows are shown best-first
    (highest estimate on top). Dot plots may use a non-zero axis.
    """
    rows = sorted(zip(labels, estimates, lows, highs), key=lambda r: r[1])
    hl = set(highlight) if highlight is not None else {rows[-1][0]}
    fig, ax = _new(figsize)
    lo_all = min(r[2] for r in rows)
    hi_all = max(r[3] for r in rows)
    if reference is not None:
        lo_all, hi_all = min(lo_all, reference), max(hi_all, reference)
    pad = (hi_all - lo_all) * 0.18 or 0.1
    ax.set_xlim(lo_all - pad, hi_all + pad * 2.2)
    for i, (lab, est, lo, hi) in enumerate(rows):
        c = ACCENT if lab in hl else GREY_DARK
        ax.plot([lo, hi], [i, i], color=c, lw=3, solid_capstyle="round", alpha=1 if lab in hl else 0.75)
        ax.scatter([est], [i], s=110, color=c, zorder=3)
        ax.text(hi + pad * 0.25, i, f"{fmt.format(est)}  [{fmt.format(lo)}, {fmt.format(hi)}]",
                va="center", ha="left", fontsize=BASE_FONT - 1,
                fontweight="bold" if lab in hl else "normal", color=INK if lab in hl else INK_2)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=BASE_FONT)
    ax.set_ylim(-0.6, len(rows) + (0.2 if reference_label else -0.4))
    ax.tick_params(axis="x", labelsize=BASE_FONT - 1)
    ax.grid(axis="x", color="#E0E0E0", lw=0.8)
    ax.set_axisbelow(True)
    if reference is not None:
        ax.axvline(reference, color=CONTRAST, lw=1.5, ls="--")
        if reference_label:
            ax.text(reference, len(rows) - 0.45, reference_label, ha="center", va="bottom",
                    fontsize=BASE_FONT - 1, color=CONTRAST)
    return _finish(fig, ax, path, title, source, left=_left_for([r[0] for r in rows], figsize[0]))


def pipeline_diagram(stages: Sequence[Tuple[str, str]], path: str = "pipeline.png",
                     title: Optional[str] = None, source: Optional[str] = None,
                     emphasize: Optional[Iterable[int]] = None,
                     figsize: Optional[Tuple[float, float]] = None) -> str:
    """Left-to-right pipeline of (stage name, one-line detail) pairs.

    emphasize: 0-based indexes of stages to fill with the accent color (for
    example, the stage where the key decision or quality check happens).
    Keep to 4-6 stages and short text; detail wraps automatically.
    """
    n = len(stages)
    if n < 2 or n > 7:
        raise ValueError("pipeline_diagram expects between 2 and 7 stages")
    emph = set(emphasize or [])
    width = 12.5
    figsize = figsize or (width, 3.0 if title is None else 3.7)
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, width)
    ax.set_ylim(0.75, 3.0)
    ax.axis("off")
    gap = 0.45
    box_w = (width - 0.3 - gap * (n - 1)) / n
    wrap_name = max(8, int(box_w * 6.2))
    wrap_det = max(10, int(box_w * 8.2))
    for i, (name, detail) in enumerate(stages):
        x0 = 0.15 + i * (box_w + gap)
        filled = i in emph
        box = FancyBboxPatch((x0, 1.55), box_w, 1.3, boxstyle="round,pad=0.02,rounding_size=0.12",
                             linewidth=1.6, edgecolor=ACCENT if filled else GREY_DARK,
                             facecolor=ACCENT if filled else "#F2F2F2")
        ax.add_patch(box)
        ax.text(x0 + box_w / 2, 2.2, textwrap.fill(name, wrap_name), ha="center", va="center",
                fontsize=BASE_FONT + 1, fontweight="bold", color="#ffffff" if filled else INK)
        ax.text(x0 + box_w / 2, 1.35, textwrap.fill(detail, wrap_det), ha="center", va="top",
                fontsize=BASE_FONT - 1, color=INK_2)
        if i < n - 1:
            arrow = FancyArrowPatch((x0 + box_w + 0.04, 2.2), (x0 + box_w + gap - 0.04, 2.2),
                                    arrowstyle="-|>", mutation_scale=18, color=GREY_DARK, lw=2)
            ax.add_patch(arrow)
    top_pad = 0.84 if title else 0.98
    fig.subplots_adjust(top=top_pad, bottom=0.1 if source else 0.02, left=0.0, right=1.0)
    if title:
        fig.text(0.012, 0.97, title, ha="left", va="top", fontsize=BASE_FONT + 4, fontweight="bold")
    if source:
        fig.text(0.012, 0.015, source, ha="left", va="bottom", fontsize=BASE_FONT - 1, color=GREY_DARK)
    fig.savefig(path, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return path
