"""Grade a checkbox practice quiz note and find the learner's default guesses.

Quiz format (one block per question):
    #### Q12 · <stem>
    - [x] **A.** <option>          <- the learner ticks one box in Obsidian
    - [ ] **B.** <option>
    > [!success]- 展开答案
    > **B. <option>**                <- answer key

Usage: python grade_quiz.py <quiz.md> [--json out.json]
Prints unanswered / multi-ticked questions first, then the score, the wrong answers, and
"default guesses": wrong option texts the learner picked two or more times.
"""
import argparse
import json
import re
import sys
from collections import Counter

Q = re.compile(r"^#### Q(\d+) · (.*)$", re.M)
OPT = re.compile(r"^- \[([ xX])\] \*\*([A-D])\.\*\* (.*)$", re.M)
KEY = re.compile(r"^> \*\*([A-D])\.", re.M)


def grade(text):
    parts = Q.split(text)
    out = {"none": [], "multi": [], "wrong": [], "right": 0}
    for i in range(1, len(parts), 3):
        q, stem, body = int(parts[i]), parts[i + 1].strip(), parts[i + 2]
        opts = {k: v.strip() for _, k, v in OPT.findall(body)}
        ticked = [k for t, k, _ in OPT.findall(body) if t in "xX"]
        key = KEY.search(body)
        if not key:
            continue
        key = key.group(1)
        if not ticked:
            out["none"].append(q)
        elif len(ticked) > 1:
            out["multi"].append(q)
        elif ticked[0] == key:
            out["right"] += 1
        else:
            out["wrong"].append({"q": q, "stem": stem, "chose": ticked[0], "chose_text": opts[ticked[0]],
                                 "key": key, "key_text": opts.get(key, "")})
    out["total"] = (len(parts) - 1) // 3
    norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
    c = Counter(norm(w["chose_text"]) for w in out["wrong"])
    out["default_guesses"] = {t: [w["q"] for w in out["wrong"] if norm(w["chose_text"]) == t]
                              for t, n in c.most_common() if n >= 2}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("quiz")
    ap.add_argument("--json")
    a = ap.parse_args()
    r = grade(open(a.quiz, encoding="utf-8").read())
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"questions {r['total']} · unanswered {r['none']} · multi-ticked {r['multi']}")
    answered = r["total"] - len(r["none"]) - len(r["multi"])
    print(f"score {r['right']}/{answered} answered ({r['right']}/{r['total']} overall)")
    for t, qs in r["default_guesses"].items():
        print(f"default guess '{t}': wrong {len(qs)}x in Q{', Q'.join(map(str, qs))}")
    for w in r["wrong"]:
        print(f"Q{w['q']} {w['stem'][:70]}\n   chose {w['chose']}: {w['chose_text'][:60]}\n   key   {w['key']}: {w['key_text'][:60]}")
    if a.json:
        json.dump(r, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


SAMPLE = """#### Q1 · Dataset for SBD?
- [x] **A.** OntoNote
- [ ] **B.** Penn Treebank
> [!success]- 展开答案
> **B. Penn Treebank**
#### Q2 · Dataset for NER?
- [x] **A.** OntoNote
- [ ] **B.** CoNLL-2003
> [!success]- 展开答案
> **B. CoNLL-2003**
#### Q3 · Model for NER?
- [ ] **A.** K-means
- [x] **B.** CRF
> [!success]- 展开答案
> **B. CRF**
#### Q4 · Skipped?
- [ ] **A.** x
- [ ] **B.** y
> [!success]- 展开答案
> **A. x**
"""

if __name__ == "__main__":
    s = grade(SAMPLE)
    assert (s["total"], s["right"], s["none"], len(s["wrong"])) == (4, 1, [4], 2), s
    assert s["default_guesses"] == {"ontonote": [1, 2]}, s
    main()
