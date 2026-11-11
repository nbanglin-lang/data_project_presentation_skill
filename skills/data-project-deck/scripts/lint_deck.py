#!/usr/bin/env python3
"""Lint a .pptx data-project deck against the data-project-deck skill's rules.

Checks (per slide): topic-label titles, crowded text, tiny fonts, missing source
line on data slides, missing alt text, missing speaker notes, duplicate titles.
Deck-level: slide count vs time slot. Prints the title sequence so you can run the
"titles test" on the real file. Optionally lists numbers on slides that are not in
a ledger CSV.

Usage:
    python lint_deck.py deck.pptx [--minutes 10] [--ledger ledger.csv] [--json]

Exit code: 1 if any ERROR, else 0. WARN and INFO never fail the run.
The linter reads text and shape properties only; it cannot see layout, so still
render the slides and look at them.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from typing import Dict, List, Optional

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE, PP_PLACEHOLDER
from pptx.util import Pt

# Titles that name a topic instead of stating a takeaway.
TOPIC_LABELS = {
    "overview", "introduction", "background", "summary", "results", "findings", "analysis",
    "methodology", "methods", "approach", "data", "data overview", "model", "model results",
    "conclusion", "conclusions", "recommendations", "next steps", "discussion", "key findings",
    "problem statement", "objectives", "eda", "exploratory data analysis", "results and discussion",
}
# Slides exempt from the action-title and source rules.
EXEMPT = re.compile(
    r"^(agenda|contents|appendix|q\s*&\s*a|questions|thank you|thanks|references|"
    r"appendix\b.*divider|table of contents)$", re.I)
VERB_HINT = re.compile(
    r"\b(is|are|was|were|has|have|had|will|can|could|would|should|does|do|did|drives?|drove|"
    r"cuts?|raises?|lifts?|rises?|rose|fell|falls?|drops?|dropped|grows?|grew|shows?|showed|"
    r"explains?|explained|beats?|outperforms?|flags?|catches|reduces?|reduced|increases?|"
    r"increased|saves?|costs?|puts?|concentrates?|account(s|ed)?|cover(s|ed)?|means?|needs?|"
    r"leads?|led|predicts?|identif(y|ies|ied)|recommend(s|ed)?|pilot(s|ing)?|lack(s|ed)?|"
    r"improves?|improved|misses|missed|arrive(s|d)?|hold(s)?)\b", re.I)
NUM_RE = re.compile(r"(?<![\w.])[$]?\d[\d,]*\.?\d*%?(?![\w])")

MAX_BODY_WORDS_WARN = 80
MAX_BODY_WORDS_ERROR = 130
MAX_BULLETS_WARN = 7
MIN_FONT_WARN = 12
MIN_FONT_ERROR = 10


def title_of(slide) -> Optional[str]:
    """Title placeholder text, else the topmost sizeable text box."""
    try:
        t = slide.shapes.title
        if t is not None and t.has_text_frame and t.text_frame.text.strip():
            return " ".join(t.text_frame.text.split())
    except Exception:
        pass
    best, best_top = None, None
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            top = sh.top if sh.top is not None else 10**12
            if best_top is None or top < best_top:
                best, best_top = sh, top
    return " ".join(best.text_frame.text.split()) if best is not None else None


def is_title_shape(slide, sh) -> bool:
    try:
        return slide.shapes.title is not None and sh.shape_id == slide.shapes.title.shape_id
    except Exception:
        return False


def iter_shapes(shapes):
    for sh in shapes:
        yield sh
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from iter_shapes(sh.shapes)


AUTO_ALT = re.compile(r"^(picture|image|chart|graphic|figure)\s*\d*$|^[\w\-. ()]+\.(png|jpe?g|gif|svg|emf|bmp|tiff?)$", re.I)


def alt_text(sh) -> str:
    """Real alt text only: tool-generated defaults (file names, 'Picture 3') count as missing."""
    try:
        cnv = sh._element.xpath(".//p:cNvPr")
        text = (cnv[0].get("descr") or "").strip() if cnv else ""
    except Exception:
        return ""
    return "" if AUTO_ALT.match(text) else text


def slide_report(idx: int, slide, title_text: Optional[str], is_first: bool) -> List[Dict]:
    out: List[Dict] = []

    def add(level, rule, msg):
        out.append({"slide": idx, "level": level, "rule": rule, "message": msg})

    exempt = bool(title_text and EXEMPT.match(title_text.strip())) or is_first
    body_words, bullets, has_visual, has_source = 0, 0, False, False
    min_font = None
    picture_without_alt = 0

    for sh in iter_shapes(slide.shapes):
        is_pic = sh.shape_type == MSO_SHAPE_TYPE.PICTURE
        is_chart = getattr(sh, "has_chart", False) and sh.has_chart
        is_table = getattr(sh, "has_table", False) and sh.has_table
        if is_pic or is_chart:
            has_visual = True
            if not alt_text(sh):
                picture_without_alt += 1
        if is_table:
            has_visual = True
        if sh.has_text_frame:
            txt = sh.text_frame.text.strip()
            if re.match(r"^(source|sources|data|note)s?\s*[:\-]", txt, re.I) or re.search(r"\bsource:", txt, re.I):
                has_source = True
            for para in sh.text_frame.paragraphs:
                ptxt = "".join(r.text for r in para.runs).strip()
                if not ptxt:
                    continue
                for r in para.runs:
                    if r.font.size is not None and r.text.strip():
                        pts = r.font.size.pt
                        min_font = pts if min_font is None else min(min_font, pts)
            if not is_title_shape(slide, sh) and not re.match(r"^(source|sources)\s*[:\-]", txt, re.I):
                body_words += len(txt.split())
                bullets += sum(1 for p in sh.text_frame.paragraphs if "".join(r.text for r in p.runs).strip())

    # Title checks
    if not title_text:
        if has_visual or body_words:
            add("ERROR", "title-missing", "Slide has content but no title text.")
    elif not exempt:
        words = title_text.split()
        low = title_text.lower().strip(" .:")
        if low in TOPIC_LABELS or len(words) <= 3:
            add("ERROR", "topic-title", f'Title "{title_text}" is a topic label. State the takeaway as a sentence.')
        elif len(words) < 6 and not re.search(r"\d", title_text):
            add("WARN", "short-title", f'Title "{title_text}" is very short; is it a full takeaway sentence?')
        elif len(words) < 8 and not VERB_HINT.search(title_text) and not re.search(r"\d", title_text):
            add("WARN", "no-verb", f'Title "{title_text}" may be a label (no verb or number found).')
        if len(words) > 22:
            add("WARN", "long-title", f"Title is {len(words)} words; aim for two lines at most (~20 words).")
        if re.search(r"\band\b", title_text, re.I) and len(words) > 14:
            add("INFO", "two-messages", "Long title with 'and': check the slide carries one message.")

    # Density
    if not exempt:
        if body_words > MAX_BODY_WORDS_ERROR:
            add("ERROR", "crowded", f"{body_words} words of body text; split the slide or move detail to the appendix.")
        elif body_words > MAX_BODY_WORDS_WARN:
            add("WARN", "dense", f"{body_words} words of body text; aim for about 60 or fewer.")
        if bullets > MAX_BULLETS_WARN:
            add("WARN", "many-bullets", f"{bullets} text lines/bullets; trim to the few that prove the title.")

    # Fonts
    if min_font is not None:
        if min_font < MIN_FONT_ERROR:
            add("ERROR", "tiny-font", f"Smallest explicit font is {min_font:g}pt; nothing under {MIN_FONT_WARN}pt.")
        elif min_font < MIN_FONT_WARN:
            add("WARN", "small-font", f"Smallest explicit font is {min_font:g}pt; use {MIN_FONT_WARN}pt or larger.")

    # Data slides
    if has_visual and not exempt:
        if not has_source:
            add("WARN", "no-source", "Slide shows a chart/table/picture but no 'Source:' line.")
    if picture_without_alt:
        add("WARN", "no-alt-text", f"{picture_without_alt} picture/chart without alt text.")

    # Notes
    if not exempt:
        notes = ""
        try:
            if slide.has_notes_slide:
                notes = slide.notes_slide.notes_text_frame.text.strip()
        except Exception:
            notes = ""
        if not notes:
            add("INFO", "no-notes", "No speaker notes (add a short talk track and a likely question).")
    return out


def ledger_numbers(path: str) -> set:
    nums = set()
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            for cell in row:
                for m in NUM_RE.findall(cell):
                    nums.add(normalize(m))
    return nums


def normalize(tok: str) -> str:
    t = tok.replace("$", "").replace(",", "").replace("%", "").strip().rstrip(".")
    try:
        v = float(t)
        return f"{v:g}"
    except ValueError:
        return t


def numbers_not_in_ledger(prs, ledger: set) -> List[Dict]:
    out = []
    for i, slide in enumerate(prs.slides, start=1):
        seen = set()
        for sh in iter_shapes(slide.shapes):
            if not sh.has_text_frame:
                continue
            for m in NUM_RE.findall(sh.text_frame.text):
                n = normalize(m)
                try:
                    v = float(n)
                except ValueError:
                    continue
                if 1900 <= v <= 2100 and "." not in n and "%" not in m:
                    continue  # years
                if v <= 10 and "%" not in m and "$" not in m and "." not in n:
                    continue  # small counts and list numbers
                if n not in ledger and n not in seen:
                    seen.add(n)
                    out.append({"slide": i, "level": "WARN", "rule": "number-not-in-ledger",
                                "message": f"'{m}' appears on the slide but not in the numbers ledger."})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pptx")
    ap.add_argument("--minutes", type=float, help="talk length; flags decks with too many main slides")
    ap.add_argument("--ledger", help="CSV of verified numbers; lists slide numbers not found in it")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    try:
        prs = Presentation(args.pptx)
    except Exception as exc:  # missing file, not a .pptx, corrupt package
        print(f"Could not open {args.pptx}: {exc}", file=sys.stderr)
        return 2
    findings: List[Dict] = []
    titles: List[Optional[str]] = []
    appendix_start = None

    for i, slide in enumerate(prs.slides, start=1):
        t = title_of(slide)
        titles.append(t)
        if appendix_start is None and t and re.match(r"^\s*appendix\b", t, re.I):
            appendix_start = i
        findings += slide_report(i, slide, t, is_first=(i == 1))

    # Duplicate titles
    seen: Dict[str, int] = {}
    for i, t in enumerate(titles, start=1):
        if not t:
            continue
        key = t.lower()
        if key in seen:
            findings.append({"slide": i, "level": "WARN", "rule": "duplicate-title",
                             "message": f'Same title as slide {seen[key]}: "{t}"'})
        else:
            seen[key] = i

    # Deck length
    total = len(titles)
    main_count = (appendix_start - 1) if appendix_start else total
    if args.minutes:
        if main_count > args.minutes * 1.5:
            findings.append({"slide": 0, "level": "WARN", "rule": "too-many-slides",
                             "message": f"{main_count} main slides for {args.minutes:g} minutes (over 1.5 per minute)."})
        elif main_count > args.minutes * 1.2:
            findings.append({"slide": 0, "level": "INFO", "rule": "slide-pace",
                             "message": f"{main_count} main slides for {args.minutes:g} minutes; a brisk pace."})

    if args.ledger:
        findings += numbers_not_in_ledger(prs, ledger_numbers(args.ledger))

    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    findings.sort(key=lambda f: (f["slide"], order[f["level"]]))
    counts = {k: sum(1 for f in findings if f["level"] == k) for k in order}

    if args.json:
        print(json.dumps({"slides": total, "main_slides": main_count, "titles": titles,
                          "counts": counts, "findings": findings}, indent=2))
    else:
        print(f"{args.pptx}: {total} slides ({main_count} before appendix)")
        print("\nTitle sequence (read it as a story):")
        for i, t in enumerate(titles, start=1):
            print(f"  {i:>2}. {t if t else '(no title)'}")
        print("\nFindings:")
        if not findings:
            print("  none")
        for f in findings:
            where = f"slide {f['slide']}" if f["slide"] else "deck"
            print(f"  [{f['level']}] {where}: {f['message']}  ({f['rule']})")
        print(f"\n{counts['ERROR']} error(s), {counts['WARN']} warning(s), {counts['INFO']} info")
    return 1 if counts["ERROR"] else 0


if __name__ == "__main__":
    sys.exit(main())
