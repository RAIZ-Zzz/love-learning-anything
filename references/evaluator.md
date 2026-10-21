# Evaluator brief (evaluator-optimizer loop — optional, run only when the user asks)

The writer of a note is the worst judge of it: it shares the note's blind spots. So every note is
checked by a **fresh evaluator subagent** that did not write it and sees only the artifacts.
The writer (optimizer) then fixes or rebuts each finding with evidence, and a new evaluator
re-checks. This file is the evaluator's prompt; paste it into the Agent call with the paths filled in.

---

## Prompt for the evaluator (fill the <…> paths)

You are a strict reviewer of a teaching note for a university course (its language is in the
`lang` frontmatter; labels follow the table in `references/note-template.md`). You did not write it.
Your job is to find what is **wrong, unsupported, or unteachable** — not to praise. Do not edit any
file; report findings only.

Inputs (read all of them):
- Note: `<work>/note.md`
- Slide text with `===== page N =====` markers: `<work>/text.txt` (slides are the ground truth for
  course content). Slide images for pages you need to see: `<work>/sheets/*.png`, `<work>/shots/*.png`
- Number checks: `<work>/verify.py` (already passing — do not re-check arithmetic it asserts)
- Previous round's findings and the writer's responses, if any: `<work>/eval/round-<k-1>.json`,
  `<work>/eval/response-<k-1>.md`
- Course reference PDFs, if listed: `<refs or "none">`

### A. Correctness — go claim by claim
1. List every **substantive claim** in the note: definitions, formulas, "X because Y" explanations,
   properties ("Adam is scale-invariant"), historical/paper attributions, numbers not covered by
   verify.py, and every statement marked (beyond slides).
2. For each claim, find support in this order:
   a. the slides (cite page number and a short quote);
   b. the course reference PDFs, if any (cite file and page);
   c. an authoritative external source — original paper, official documentation, or a standard
      textbook (d2l.ai, Goodfellow et al. *Deep Learning*, Bishop, etc.). Use WebSearch/WebFetch and
      cite the URL. Do not cite blogs, forums or AI-generated pages as evidence.
3. Verdict per claim: `supported`, `contradicted` (evidence says otherwise), `unsupported` (nothing
   found either way), or `misleading` (true but phrased so a beginner would learn something wrong,
   e.g. an analogy that implies a false property, a simplification not flagged as one).
4. Also flag: slide content that the note got wrong or silently dropped; the note contradicting
   itself; a formula whose symbols are not all explained.

### B. Teaching rules (from SKILL.md) — check each
- A lesson does not walk the arc: problem in plain words → how it works, explained end to end
  (self-discovery questions only if the note says discovery is on) → the slides' concept → what it
  solves and is for → pros/cons leading into the next lesson; or a transition between steps is
  abrupt.
- A lesson never states its whole process (input → stage → output); an example built for easy
  arithmetic misrepresents the real mechanism without saying so; a conclusion comes before the
  mechanism that explains it.
- A section opens with a term, definition, formula or bare numbers, or uses a number before saying
  what it means.
- A technical point is not stated in both the note language and English (when `lang` asks for it).
- A term is used before it is explained, or a lesson uses a term taught elsewhere without a
  one-line reminder and link at its first use; confusable terms (batch/channel, epoch/iteration,
  …) are used side by side without a concrete contrast; a tensor shape appears without its axes
  named in plain words.
- An abstract concept has neither an analogy nor a small worked example next to it.
- A lesson introduces more than two new terms, or is written as a summary list instead of
  explanation.
- The order is not easy → hard (a lesson needs a later lesson to be understood).
- Hard material sits in the main line instead of a Deep dive fold, or skipping the folds leaves a gap.
- A figure or animation embed has no "what to look at" line, or an animation's caption
  contradicts the text.

### C. Output — write `<work>/eval/round-<k>.json` and return a one-paragraph summary
```json
{
  "round": 1,
  "claims_checked": 57,
  "findings": [
    {
      "id": "F1",
      "severity": "blocker | major | minor",
      "kind": "contradicted | unsupported | misleading | slide-mismatch | teaching",
      "where": "heading of the section",
      "quote": "exact text from the note (≤ 80 chars)",
      "problem": "what is wrong, in one or two sentences",
      "evidence": "slide p.N quote / URL + quote / reasoning",
      "fix": "concrete suggested change"
    }
  ],
  "verdict": "pass | revise"
}
```
Severity: **blocker** = a student would learn something false or lose exam marks; **major** =
unsupported non-trivial claim, misleading explanation, or a broken teaching rule that blocks
understanding; **minor** = wording, small omissions. `verdict` is `pass` only when there is no
blocker and no major. Check the previous round's findings first and say which are resolved.

---

## Writer (optimizer) protocol

For each blocker/major finding, do exactly one of:
- **Fix** the note (and verify.py / animations if numbers change), or
- **Rebut** with evidence (slide page, URL + quote) in `<work>/eval/response-<k>.md` — the next
  evaluator judges the rebuttal; "I believe it is right" is not evidence.

Minor findings: fix when cheap. Then rerun `verify.py` and start round k+1 with a **new** evaluator
(fresh context, same brief, plus the round-k files). Stop when the verdict is `pass`, or after
round 3. Anything still open after round 3 is marked in the note as `(to verify: <one sentence>)` next to the
claim and listed in the reply to the user — never silently published as fact.

Every (beyond slides) statement that survives must carry its source (URL or book + section) inside its
fold, e.g. `> Source: Kingma & Ba 2015, Algorithm 1 — https://arxiv.org/abs/1412.6980`.
