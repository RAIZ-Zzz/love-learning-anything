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
  9. page coverage: every page in the frontmatter `pages` range is cited somewhere as (p.N) or
     listed in `pages_skipped` (title, agenda, Q&A pages), so no slide is skipped silently.
     Multi-PDF notes (`pages: "W02 44-69; W04 1-79"`) also need `page_scope: "1-2=W02; 3-6=W04"`
     (which `##` parts cite which PDF; the opening section counts as the first part; a prefix
     like "W04 p.5" always wins; other decks such as "CS224N p.19" are ignored).
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


PCITE = re.compile(r"(?:([A-Za-z][A-Za-z0-9]*)\s+)?p\.\s?(\d+(?:\s*[–-]\s*\d+)?(?:\s*[,，、]\s*\d+(?:\s*[–-]\s*\d+)?)*)")
PART = re.compile(r"^## (?:第([一二三四五六七八九十]{1,2})部分|Part (\d+)) · ")
CN = {c: i for i, c in enumerate("零一二三四五六七八九")}


def nums(s):
    out = set()
    for a, b in re.findall(r"(\d+)(?:\s*[–-]\s*(\d+))?", s):
        out.update(range(int(a), int(b or a) + 1))
    return out


def labelled(s):
    """'W02 44-69; W04 1-79' -> {'W02': {...}, 'W04': {...}};  '1-75' -> {'': {...}}"""
    out = {}
    for seg in filter(None, (x.strip() for x in s.split(";"))):
        m = re.match(r"([A-Za-z]\w*)\s+(.*)", seg)
        key, rest = (m.group(1), m.group(2)) if m else ("", seg)
        out.setdefault(key, set()).update(nums(re.sub(r"\([^)]*\)", "", rest)))
    return out


def part_no(raw):
    m = PART.match(raw)
    if not m:
        return None
    if m.group(2):
        return int(m.group(2))
    s = m.group(1)  # 三 / 十 / 十二 / 二十
    if s == "十":
        return 10
    if s[0] == "十":
        return 10 + CN[s[1]]
    if s[-1] == "十":
        return CN[s[0]] * 10
    return CN[s]


def coverage(lines):
    fm = {}
    if lines and lines[0] == "---":
        for l in lines[1:lines.index("---", 1)]:
            m = re.match(r"^(\w+):\s*\"?([^\"]*)\"?\s*$", l)
            if m:
                fm[m.group(1)] = m.group(2)
    if "pages" not in fm:
        return []
    want, skip = labelled(fm["pages"]), labelled(fm.get("pages_skipped", ""))
    multi = len(want) > 1
    scope = {}
    if multi:
        if "page_scope" not in fm:
            return ["multi-PDF note: add page_scope, e.g. 'page_scope: \"1-2=W02; 3-6=W04\"'"]
        for seg in fm["page_scope"].split(";"):
            rng, _, lab = seg.partition("=")
            for p in nums(rng):
                scope[p] = lab.strip()
    first = scope[min(scope)] if scope else ""
    got, part, in_scope_box = {k: set() for k in want}, 0, False
    for raw in lines[lines.index("---", 1) + 1 if lines and lines[0] == "---" else 0:]:
        if REF_HEAD.match(raw):
            break
        p = part_no(raw)
        if p is not None:
            part = p
        if re.match(r"^> \[!info\][-+]? (课程与范围|Course & scope)", raw):
            in_scope_box = True
        if in_scope_box and not raw.startswith(">"):
            in_scope_box = False
        if in_scope_box or raw.startswith("| [[#"):
            continue  # scope box and reading-route table give whole ranges: a table of contents, not coverage
        default = (scope.get(part) or (first if part == 0 else None)) if multi else ""
        for pre, body in PCITE.findall(strip_code_math(raw)):
            key = pre if pre in want else (None if pre else default)
            if key is not None:
                got[key].update(nums(body))
    issues = []
    for key, pages in want.items():
        miss = sorted(pages - got[key] - skip.get(key, set()))
        if miss:
            where = f"{key} " if key else ""
            issues.append(f"{where}pages never cited and not in pages_skipped: {', '.join(map(str, miss))}")
    return issues


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
    issues.extend(coverage(lines))
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
