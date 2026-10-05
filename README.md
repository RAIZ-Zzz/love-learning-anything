# LLA · Love Learning Anything

**Turn lecture slides into notes that *teach*, not notes you memorise.**

[![Claude Code skill](https://img.shields.io/badge/Claude%20Code-skill-8A2BE2)](https://claude.com/claude-code)
[![Obsidian](https://img.shields.io/badge/output-Obsidian%20vault-7C3AED)](https://obsidian.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Slides are a list of answers. You read *"BatchNorm: normalise each channel with the mini-batch mean
and variance"*, nod, and forget it by Friday, because you never had the problem it solves.

`lla` (Love Learning Anything, formerly `lecture-note`) is a [Claude Code](https://claude.com/claude-code) skill that reads a lecture PDF and
writes a step-by-step **teaching note** into your Obsidian vault. Every idea arrives the way a
good tutor would bring it in: first the problem, then you try what you already know, you watch it
break, and only then the slides give the fix a name. It can also **tutor you live** on any
section, one question at a time.

> [!WARNING]
> **Please read before you rely on a note.**
>
> 1. **The model can still be wrong.** At the time of release (September 2026), OpenAI's flagship
>    model is GPT-6 Astra, and this skill was built and used with Claude Code running Claude Opus
>    5.5. Today's LLMs are very capable, and they still make mistakes. In the very study sessions
>    that shaped this skill, the model miscounted the examples on a slide, reused the same numbers
>    with a new meaning without saying so, and repeated a tutorial answer that computed cosine
>    similarity on vectors that were not normalised. `verify.py` and online grounding catch many
>    errors, but not all. Therefore, **please use your own critical thinking!**
>
> 2. **The skill has a validation option.** It is an independent evaluator agent that checks every
>    claim against the slides and primary sources (`references/evaluator.md`; just ask for a
>    "strict review"). You can also simply ask your AI assistant to fact-check a note on its own,
>    without the skill. In practice validation does find many problems, but it **costs a lot of
>    tokens**, and even after it the note is still **not guaranteed to be 100% correct**. Check the
>    note against your slides and question anything that looks off.
>
> 3. **The skill is still improving.** Its teaching rules change as we learn from real study
>    sessions (see the dated notes in [`references/learning-design.md`](references/learning-design.md)).
>    Notes generated with an earlier version may not follow the latest rules. Issues and pull
>    requests are welcome.
>
> 4. **Better learning, not guaranteed grades.** The notes aim to make studying more efficient
>    and more interesting, to improve the whole learning process, and to build the habit of solving
>    engineering problems by reasoning from the problem. They do **not** guarantee a high score.
>    Whether you do well depends on you, not on how good the notes are.

---

## What it feels like

The slide says:

> **Batch Normalization.** Use mini-batch statistics; at inference use running mean and variance.

The note tells one story instead, and keeps it from the first BatchNorm lesson to the last:

> Our cat classifier's layer 1 outputs **2, 4, 6, 8** for four training images, and layer 2 has
> learned *"above 5 means cat"*. After one training step layer 1 outputs **6, 10, 14, 18**, and
> suddenly every image is "a cat". **What went wrong, and how would you fix it?**
> → you invent "subtract the mean, divide by the std" yourself → *that's BatchNorm*.
>
> Later the GPU fits only **2** of those 4 images: how far off is the mean now?
> Later still the model is deployed and a user uploads **one** photo (layer-1 output 7), and
> "subtract this batch's mean" gives 0 for *every* photo. What should inference use instead?
> → running statistics, and the story ends where it began: with stale statistics, the drift from
> lesson 1 comes back.

Every number in that story is checked by a script before the note is published.

## Example: Einstein 1905

[`examples/special-relativity-1905`](examples/special-relativity-1905) is a full note generated from
the 24-page English translation of *On the Electrodynamics of Moving Bodies*, written for a student
in 1905 and told through one story: an imagined Bern express at 0.6c. Three of its six animations:

| | | |
| --- | --- | --- |
| <img src="examples/special-relativity-1905/attachments/specrel-1905-anim-simul.svg" width="280"><br>Simultaneity is relative | <img src="examples/special-relativity-1905/attachments/specrel-1905-anim-passing.svg" width="280"><br>Contraction and dilation | <img src="examples/special-relativity-1905/attachments/specrel-1905-anim-veladd.svg" width="280"><br>Adding velocities |

**This example has not been validated**: the optional strict review was not run on it (it passed
`verify.py`, online grounding, the lint and the student test). See the example's README.

## How every lesson is built

```mermaid
flowchart LR
    A["1 · The problem<br/>(what breaks, in plain words)"] --> B["2 · Work it out yourself<br/>(apply what you know → it fails → 3–5 guided questions)"]
    B --> C["3 · The slides' concept<br/>(name, definition, formula mapped onto your answers)"]
    C --> D["4 · What it solves<br/>(connections, real uses)"]
    D --> E["5 · Pros and cons"]
    E -- "remaining weakness = next lesson's problem" --> A
```

A topic that spans several lessons runs on **one scenario from start to end**, so ideas chain
together instead of piling up.

## Why it's built this way

The design isn't taste. Each rule follows a research result:

| Rule | Grounded in |
|---|---|
| One running story per topic | **Anchored instruction**: CTGV / Bransford's *Jasper* series, which targets "inert knowledge" |
| Try with old knowledge, fail, then learn the concept | **Productive failure**: Kapur; meta-analysis of 166 comparisons, better conceptual understanding and transfer (Sinha & Kapur, 2021) |
| New ideas hang on what you already know | **Meaningful learning**: Ausubel; **cognitive conflict**: Piaget |
| Guided questions, never "go figure it out" | Minimal guidance fails novices (Kirschner, Sweller & Clark, 2006) |
| The tutor never hands over the answer first | Unrestricted GPT-4 help lowered unassisted exam scores by 17%; hint-only tutors removed the harm (Bastani et al., *PNAS* 2025). A research-designed AI tutor doubled learning gains (Kestin et al., *Sci. Rep.* 2025) |
| Struggle is kept, not smoothed away | Active learners learn more but *feel* they learn less (Deslauriers et al., *PNAS* 2019) |
| Every question must catch a real misconception | **Hinge questions**: a question is worth asking only if someone who has not understood would get it wrong (Wiliam, 2011; Barton, 2018) |
| Explanation depth follows *your* level | **Subgoal labels** (Catrambone, 1998), **faded worked examples** (Renkl & Atkinson, 2003); detail that helps a novice hinders an expert (**expertise reversal**, Kalyuga et al., 2003) |
| New ideas are taught as one causal chain in sentences, not as tables of terms; you check by restating it | AI text is rated as clear as human text but understood worse (Guo et al., 2025). Low-knowledge readers need every link spelled out (McNamara et al., 1996). Jargon makes explanations feel satisfying while lowering understanding, and explaining first breaks the illusion (Cruz & Lombrozo, *Nat. Hum. Behav.* 2025) |

Full reasoning, the session notes that shaped each rule, and 31 references are in
[`references/learning-design.md`](references/learning-design.md).

## Features

**Learning first**
- **Taught at your level.** On first use, `/lla` asks about your background: new to the subject,
  related but rusty, solid, or your own description. The answer sets how much each step is spelled
  out.
- **Prerequisites up front.** Before writing, it tells you what the material assumes you already
  know. Something the slides use but never explain is taught properly where it is first needed,
  marked as a supplement. Background the slides never mention is only added if you say yes.
- **Easy → hard.** A learning ladder is planned before writing; no term is used before it is explained, and every term is re-explained in one line where a later lesson uses it.
- **Plain words as the bridge, professional terms as the destination.** Each lesson ends with *"In professional terms"*, so you can talk like a practitioner.
- **Simple main line, depth on demand.** Derivations, proofs and extras sit in collapsible *deep dive* callouts.
- **Check-ins after every part** and 10+ practice questions with folded answers.
- **Interactive tutor mode.** "Teach me WEEK 5 section 14.3, you ask and I answer." It asks one question per turn, and when you get one wrong it shows where your number came from instead of re-teaching the section.

**Trustworthy**
- **Every number verified** by a generated `verify.py` with exact arithmetic, including the numbers inside animations.
- **One house style: a paper's rigor, a tutorial site's look.** Every element has exactly one format, is numbered where it is referred to, and every outside claim is cited. The look follows mainstream teaching sites (format only): prev/next navigation like Runoob, `实例` example blocks with their results, bold **注意：** notes, d2l-style section-numbered figures and equations, author–year citations with a reference list, and every note ending in summary → exercises → glossary → references (`references/note-template.md`). `lint_note.py` enforces the mechanical parts.
- **Questions tested on a "student".** A fresh agent that sees only the note answers every question before opening its answer, and flags any that it misreads: a hidden setup, a letter with two meanings, two asks in one, an ambiguous count. Flagged questions are rewritten.
- **Grounded.** The slides are the ground truth; anything beyond them is checked online against papers or standard textbooks and cited, or marked *(to verify)*.
- **Optional strict review.** A fresh evaluator agent checks every claim and teaching rule over up to 3 fix-or-rebut rounds (`references/evaluator.md`).

**Made for Obsidian**
- **Animated SVGs for anything that moves**: optimizer steps, forward and backward passes, sliding kernels, tokens flowing through an LLM, agent loops. They are generated from code and play inside `![[file.svg]]` embeds.
- **Slide screenshots** where a picture says what text can't.
- **Course mind map (optional).** One markmap per course; every node explains *what / why / formula / example / pitfall* and links back into the notes.
- **Safe publishing.** It never overwrites edits you made in Obsidian, and every embed is checked.

**Your language.** Choose per note:

| Option | Result |
|---|---|
| `zh+en` (recommended) | Plain Chinese narrative; every technical point is stated in Chinese, then in English |
| `zh` | Chinese only, English term in parentheses on first use |
| `en` | English throughout |
| `en+zh` | Plain English narrative; every technical point is stated in English, then in Chinese |
| custom | Any mix you describe |

Callout labels ("Analogy", "Deep dive", "Pause", …) follow the note language (see the label table in `references/note-template.md`).

## Quick start

```bash
pip install pymupdf cli-anything-obsidian
git clone https://github.com/RAIZ-Zzz/love-learning-anything ~/.claude/skills/lla
```

Set `OBSIDIAN_VAULT` and `OBSIDIAN_API_KEY` (details below), open your vault in Obsidian, then in
Claude Code:

```text
/lla AI6103 5 "slides/Lecture 4.pdf" --lang zh+en
```

or *"teach me WEEK 5 section 14.3, you ask and I answer"*.

## Installation on a new machine

The skill holds nothing machine-specific, so nothing in this repo needs editing.

### Required

1. [Claude Code](https://claude.com/claude-code).
2. Python 3 and the two packages the scripts use (both on PyPI):
   ```bash
   pip install pymupdf cli-anything-obsidian
   ```
   On macOS / Linux the command may be `python3` / `pip3`.
3. [Obsidian](https://obsidian.md), with your vault open whenever the skill runs:
   - install and enable the community plugin **Local REST API**;
   - copy its API key into the environment variable `OBSIDIAN_API_KEY`.

   Check: `cli-anything-obsidian --json vault list` prints your vault's top-level folders.
4. The environment variable `OBSIDIAN_VAULT` = absolute path of that same vault folder
   (attachments are copied there on disk; the publish script refuses to run if it is not the
   vault Obsidian has open).
5. The skill itself:
   ```bash
   git clone https://github.com/RAIZ-Zzz/love-learning-anything ~/.claude/skills/lla
   ```
   Update later with `git pull`. Without git, download the zip and unpack it to the same folder.

Notes go to `Lecture Notes/<course>/` inside the vault; create one folder per course there.

### Optional

- Google Chrome or Microsoft Edge, only for previewing animation frames. Set `$CHROME` if it is
  not in a standard location.
- `local.md`: a two-column table (`| Vault folder | Slides |`) listing where each course's slides
  live on this machine. It is git-ignored. Without it, the skill asks for the PDF path and offers
  to create the file.
- The Obsidian plugin **Mindmap NextGen**, only for the optional course mind map.
- `pip install youtube-transcript-api` (no API key), so the skill can read explainer videos'
  captions and borrow their teaching path. Without it, that step is skipped.

### Use

`/lla <subject> <note name | vault path> [file to learn] [pages A-B] [--lang zh|en|zh+en|en+zh]`, or ask it to
teach a section of an existing note.

## Under the hood

| Path | Purpose |
|---|---|
| `SKILL.md` | The workflow and writing rules Claude follows |
| `references/learning-design.md` | Why the notes teach this way: principles, session notes, references |
| `references/note-template.md` | Frontmatter and section skeleton of a note |
| `references/evaluator.md` | Prompt for the optional strict-review loop |
| `scripts/prep_slides.py` | PDF → text with page markers, overview contact sheets and slide screenshots (PyMuPDF) |
| `scripts/svg_anim.py` | `Scene` helper that builds animated SVGs from computed data; `lint` checks Obsidian compatibility; `frames` renders chosen moments with headless Chrome/Edge for visual review |
| `scripts/mindmap.py` | Optional course mind map: an outline with `@week\|heading@` link tokens becomes an inline `markmap` note; every heading link is checked |
| `scripts/video_transcript.py` | YouTube captions → plain text with [m:ss] stamps, for distilling how explainer videos teach a topic |
| `scripts/lint_note.py` | House-style check: slide pages as (p. N), every supplement cited author–year, citations match the reference list, every figure captioned, every example block has a result line |
| `scripts/publish_note.py` | Writes the note and attachments into the vault through `cli-anything-obsidian`, refuses to overwrite edits made in Obsidian, and checks that every embed resolves |

### How animations stay accurate

1. Positions are computed by a generator script from the same numbers used in the note, never typed by hand.
2. `svg_anim.py lint` enforces SMIL-only animation on one shared looping timeline (no scripts, click triggers or CSS keyframes, which do not run when Obsidian embeds an SVG as an image), an opaque background for dark themes, and a CJK font stack.
3. `svg_anim.py frames` pauses the timeline at chosen times and screenshots each frame, so every key moment is checked against the text before publishing.
4. Every animation is followed by a static table of the same numbers, so the note still works if the animation does not play.

## License

MIT, see [LICENSE](LICENSE).
