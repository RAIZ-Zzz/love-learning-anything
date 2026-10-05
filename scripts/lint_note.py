"""Check a note against the house style in references/note-template.md.

    python lint_note.py NOTE.md

Checks the mechanical parts only:
  1. slide pages are cited as (p.N) / (p. N), not "第 N 页" / "pp."
  2. beyond-slides content carries an author-year citation: "(补充 [Author, Year])", or a
     "> [!info]- 补充：…" / "Supplement: …" fold whose last line is "来源：[Author, Year]";
     no bare "（补充）", "(beyond slides)", "补充推理"
  3. every [Author, Year] cited in the text has a References entry "- [Author, Year] …",
     and every entry is cited
  4. every image / SVG embed is followed by a caption "*图 14.3 · …*" / "*Figure 14.3 · …*"
  5. every "> [!example]" block is titled "实例 14.3：…" / "Example 14.3: …" and has a
     result line (计算结果：/ 运行结果：/ Result: / Output:)
  6. a link to a section targets the heading: [[WEEK 5#14. …|WEEK 5 §14]], not "[[WEEK 5]] §14"
  7. a slide picture the text points at ("p.8 的图", "p.64 是一张…照片") is embedded in the note
  8. no display math in a callout title, and no math shorthand (diag(...), sqrt(...), [[1,2],...])
Exits 1 and lists line numbers if anything fails.
"""
import re
import sys
from pathlib import Path

REF_HEAD = re.compile(r"^##\s+(参考文献|References)\s*$")
REF_ENTRY = re.compile(r"^-\s+\[([^\[\]]+,\s*\d{4}[a-z]?)\]\s+\S")
CITE = re.compile(r"\[([A-Z][^\[\]]*?,\s*\d{4}[a-z]?)\]")
EMBED = re.compile(r"!\[\[[^\]]+\.(png|jpe?g|svg|gif)(\|[^\]]*)?\]\]", re.I)
CAPTION = re.compile(r"^\*(图|Figure) \d+(\.\d+)* · ")
OLD_PAGE = re.compile(r"第\s*\d+(\s*[–-]\s*\d+)?\s*页|\bpp\.\s*\d")
BARE_SUPP = re.compile(r"（补充）|（补充[，,]|\(beyond slides\)|补充推理|（补充(?! \[[A-Z][^\]]*\d{4}[a-z]?\]）)")
SUPP_FOLD = re.compile(r"^>\s*\[!\w+\]-?\s*(补充：|Supplement: )")
SOURCE_LINE = re.compile(r"^>\s*(来源：|Sources?: )(.*)$")
EXAMPLE_HEAD = re.compile(r"^>\s*\[!example\]-?\s*(.*)$")
EXAMPLE_TITLE = re.compile(r"^(实例 \d+(\.\d+)*：|Example \d+(\.\d+)*: )")
NOTE_LINK_SECTION = re.compile(r"\[\[[^\]#|]+(\|[^\]]*)?\]\]\s*(§\s*\d|第\s*\d+(\.\d+)*\s*[节部])")
FIG_REF = re.compile(r"p\.\s?(\d+)[^。；\n]{0,15}?(的图|错觉图|示意图|照片|插图|figure|picture|photo)", re.I)
CALLOUT_TITLE = re.compile(r"^(>\s*)+\[!\w+\]")
MATH_SHORTHAND = re.compile(r"\\mathrm\{diag\}|\bdiag\s*\(|\bsqrt\s*\(|\[\[\s*-?\d")
RESULT = re.compile(r"\*\*(计算结果：|运行结果：|Result:|Output:)\*\*")


def strip_code_math(line):
    line = re.sub(r"`[^`]*`", "", line)
    line = re.sub(r"\[\[[^\]|]*#[^\]|]*\\?\|", "[[", line)   # heading text inside a link target
    return re.sub(r"\$[^$]*\$", "", line)


def main():
    path = Path(sys.argv[1])
    lines = path.read_text(encoding="utf-8").splitlines()
    issues, cited, entries, fig_refs = [], set(), set(), set()
    in_refs = in_fence = False
    open_supp = open_example = None  # (line number, found?) of the callout being scanned

    def close_callouts():
        nonlocal open_supp, open_example
        if open_supp:
            issues.append(f"{open_supp}: supplement fold must end with '来源：[Author, Year]'")
        if open_example:
            issues.append(f"{open_example}: 实例 block needs a '**计算结果：**' / '**运行结果：**' line")
        open_supp = open_example = None

    for i, raw in enumerate(lines, 1):
        if raw.lstrip("> ").startswith("```"):  # also fences inside callouts
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if REF_HEAD.match(raw):
            close_callouts()
            in_refs = True
            continue
        if in_refs:
            m = REF_ENTRY.match(raw)
            if m:
                entries.add(re.sub(r"\s+", " ", m.group(1)))
            elif raw.startswith("## "):
                in_refs = False
            if in_refs:
                continue
        if not raw.startswith(">"):
            close_callouts()
        line = strip_code_math(raw)

        if SUPP_FOLD.match(raw):
            open_supp = i
        m = SOURCE_LINE.match(raw)
        if m:
            if not CITE.search(m.group(2)):
                issues.append(f"{i}: source line must cite author-year, e.g. '来源：[Wu & He, 2018]'")
            open_supp = None
        m = EXAMPLE_HEAD.match(raw)
        if m:
            if not EXAMPLE_TITLE.match(m.group(1)):
                issues.append(f"{i}: example block must be titled '实例 14.3：…' / 'Example 14.3: …'")
            open_example = i
        if open_example and RESULT.search(raw):
            open_example = None

        if CALLOUT_TITLE.match(raw) and ("$$" in raw or "\\begin{" in raw):
            issues.append(f"{i}: display math in a callout title; move it into the fold body")
        if MATH_SHORTHAND.search(re.sub(r"`[^`]*`", "", raw)):
            issues.append(f"{i}: write the formula out (bmatrix / \\frac / \\sqrt), not diag(...) / sqrt(...) shorthand")
        if OLD_PAGE.search(line):
            issues.append(f"{i}: cite slide pages as （p.N） / (p. N)")
        fig_refs.update((int(n), i) for n, _ in FIG_REF.findall(line) if not raw.startswith(("*图", "*Figure")))
        if NOTE_LINK_SECTION.search(line):
            issues.append(f"{i}: link the section's heading, e.g. [[WEEK 5#14. …|WEEK 5 §14]], not [[WEEK 5]] §14")
        if BARE_SUPP.search(line):
            issues.append(f"{i}: beyond-slides content needs '（补充 [Author, Year]）' or a '补充：' fold")
        cited.update(re.sub(r"\s+", " ", c) for c in CITE.findall(line))

        if EMBED.search(raw):
            nxt = next((l for l in lines[i:] if l.strip()), "")
            if not CAPTION.match(nxt):
                issues.append(f"{i}: embed needs a caption '*图 14.3 · p.N · …*' / '*Figure 14.3 · …*'")
    close_callouts()

    for c in sorted(cited - entries):
        issues.append(f"[{c}] is cited but has no References entry")
    for c in sorted(entries - cited):
        issues.append(f"References entry [{c}] is never cited")
    text = "\n".join(lines)
    for n, i in sorted(fig_refs):
        if not re.search(rf"-s{n:02d}\.(png|jpe?g)", text):
            issues.append(f"{i}: the text points at the picture on p.{n}; embed its screenshot (…-s{n:02d}.png)")
    if cited and not entries:
        issues.append("citations used but no '## 参考文献' / '## References' section")
    if not re.search(r"^> \[!abstract\][-+]? (一眼看懂|At a glance)", text, re.M):
        issues.append("no '> [!abstract] 一眼看懂' / 'At a glance' gist block before the first part")

    sys.stdout.reconfigure(encoding="utf-8")
    if issues:
        print(f"{path.name}: {len(issues)} house-style issue(s)")
        print("\n".join(issues))
        sys.exit(1)
    print(f"{path.name}: house style ok")


if __name__ == "__main__":
    main()
