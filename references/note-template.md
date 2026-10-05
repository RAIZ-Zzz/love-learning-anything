# Note template

Copy this skeleton. Replace `<…>`; drop optional lines marked `(optional)` when not applicable.
The skeleton uses the **English labels**; for `zh` / `zh+en` notes, swap in the Chinese label for
each one from the [label table](#labels-per-note-language) below. SKILL.md refers to the labels by
their English names (e.g. "the Deep dive fold").

````markdown
---
course: <vault folder name, e.g. AI6103-DeepLearning>
week: <n>
part: <p>                      # (optional) only for WEEK n.p notes
topic: <topic in the note language, with English keywords>
lang: <zh | en | zh+en | en+zh | custom>
lecturer: <name>               # (optional) if on the title slide
source_pdf: "<absolute path with forward slashes>"
pages: "<A-B>"
pdf_page_count: <total pages of the PDF>
created: <YYYY-MM-DD>          # keep the original date when rewriting
updated: <YYYY-MM-DD>
tags:
  - <COURSE CODE, e.g. AI6103>
  - <kebab-case-topic>
  - <kebab-case-topic>
---

# WEEK <n>[ · Part <p>] · <title>

> [!info] Course & scope
> « Previous: [[WEEK <n-1>]] · Next: [[WEEK <n+1>]] »   ← only link notes that exist
> **<course>** · `<pdf file name>` · **PDF p. A–B**
> A step-by-step teaching note: easy → hard, one new idea at a time. Every lesson follows
> **the problem → work it out yourself → the concept from the slides → what it solves and is for → pros and cons → next**.
> The folded Deep dive blocks can be skipped; the main line still makes sense without them.

| Reading route (easy → hard) | Slides | After it you can answer |
| --- | --- | --- |
| [[#Part 1 · <…>]] | p.A–p.X | <one real question> |
| … | … | … |

> [!abstract] At a glance
> <The gist in ≤ 3 plain sentences, ≤ 1 term: what this lecture's main thing does, shown as one
> familiar example going in and coming out, and why anyone wants that. E.g. "MetaPro reads
> *She devoured his novel*, spots that 'devoured' is not literal, rewrites it as *She enjoyed his
> novel*, and names the pattern PLEASURE IS BODILY_PROCESS. Collect many such patterns from someone's
> writing and you can see how they think.">

## Before we start: what problem this lecture solves

<One running scenario with 2–3 numbers: where we are stuck and what this lecture gives us.
Tell it as a story, not a list.>

## Part 1 · <topic>

### 1.1 <concept> (<English term>) (p. A–B)

**Why we need it**
<Plain words: what goes wrong without this idea, as a concrete failure. Say where every number
comes from and what it means. No term, definition or formula yet.>

<No label here. The last sentence of "Why we need it" moves the topic's running scenario into this
lesson's new situation and hands the reader the first question in plain words, e.g. "Now the GPU
only fits 2 of the 4 images. What mean does BN compute? Try it before opening the fold." Then the
reader applies what they already learned, watches it fail inside the story, and is guided to the fix:>

> [!question]- Question 1: <count / observe something on a tiny case>
> <answer> — <one-line takeaway>

<one or two sentences carrying the reader to the next question>

> [!question]- Question 2: <change one thing>
> <answer> — <one-line takeaway>

**The concept from the slides**
<The slides' name for what the reader just built, in the note language and in English; the slides'
definition and every point they make.>
$$<formula>\tag{1.1}$$
<which number from the questions each symbol stands for.>

> [!example] Example 1.1: <title>
> <a worked calculation or code run the reader should follow>
>
> **Result:** <the numbers; for code, **Output:** and a block with the real output>

**Note:** <a short caution inside prose, Runoob style>.

**In professional terms:** <one or two sentences the way a practitioner would say it, with the proper
terms (e.g. "use ReLU as the activation"), in the note language and in English.>

**What it solves and what it is for**
<Connect to earlier knowledge points / weeks; what exactly it fixes; where it is used in practice.>

> [!quote] Analogy
> <optional everyday picture if the idea is still abstract.> Where the analogy breaks: <one sentence>.

**Table 1.1 · <title>**
| Step | … | … |
| --- | --- | --- |

![[Lecture Notes/<course>/attachments/week<n>[.<p>]-<topic>-s<NN>.png]]
*Figure 1.1 · p. N · <short title>: <what to look at in this picture and what it shows>*

![[Lecture Notes/<course>/attachments/week<n>[.<p>]-<topic>-anim-<slug>.svg]]
*Figure 1.2 · own diagram · <short title>: <which element to follow and what its change means>* (If the animation does not play, Table 1.1 has the same numbers.)

> [!note]- Deep dive: <full derivation / proof / edge cases of slide content> (optional)
> <material the main line does not need. Anything from outside the slides goes in a Supplement fold instead.>

> [!info]- Supplement: <topic>
> <content beyond the slides, checked online (step 6b)>
> Sources: [Author, Year]

> [!warning] Common pitfall
> <only real, common misunderstandings + the correct view>

**Pros and cons**
<What it buys vs what it costs. End with the weakness that the next lesson fixes, phrased as the
next lesson's problem.>

### 1.2 <next concept> … (same arc; its "Why we need it" grows out of 1.1's pros and cons)

> [!question]- Pause: <one question checking this part's core idea>
> <answer + one or two sentences of explanation>

… (continue part by part in slide order) …

## Part N · Review and practice

### Summary
| Concept | In one sentence | Key formula |
| --- | --- | --- |

### Exercises

#### Exercise 1 · <title>
<question>

> [!success]- Show answer
> <answer + reasoning>

… (≥ 10 questions) …

### Glossary
| Term | English | Meaning in one sentence |
| --- | --- | --- |

> [!tip] Self-check after studying
> **Can compute:** …
> **Can explain:** …
> **Can connect:** …

## References
- [Author & Author, Year] Author, A., & Author, B. (Year). Title. *Venue*, vol(issue), pages. https://doi.org/…

« Previous: [[WEEK <n-1>]] · Next: [[WEEK <n+1>]] »
````

## Labels per note language

`en` and `en+zh` use the English column; `zh` and `zh+en` use the Chinese column. A `custom`
language follows whichever column is closer, or asks the user.

| Label (English) | Chinese |
| --- | --- |
| Course & scope | 课程与范围 |
| Reading route (easy → hard) · Slides · After it you can answer | 阅读路线（从易到难） · 课件页 · 学完能回答 |
| At a glance | 一眼看懂 |
| Before we start: what problem this lecture solves | 开始之前：这一讲要解决什么问题 |
| Part 1 · … / Part N · Review and practice | 第一部分 · … / 第 N 部分 · 复习与练习 |
| Why we need it | 为什么需要它 |
| Question k: … | 第 k 题：… |
| The concept from the slides | 课件里的概念 |
| In professional terms | 专业说法 |
| What it solves and what it is for | 它解决了什么、能用来干嘛 |
| Analogy | 打个比方 |
| Pros and cons | 优点与代价 |
| What to watch | 看动画时注意 |
| Deep dive: … (optional) | 深入：…（可跳过） |
| Supplement: … | 补充：… |
| (supplement [Author, Year]) | （补充 [Author, Year]） |
| (derived here) | （本笔记推导） |
| (to verify: …) | （待核对：…） |
| Sources: | 来源： |
| References | 参考文献 |
| Example 14.3: … · Result: · Output: | 实例 14.3：… · 计算结果： · 运行结果： |
| Note: | 注意： |
| Previous · Next | 上一讲 · 下一讲 |
| Figure 14.3 | 图 14.3 |
| own diagram | 自绘 |
| Table 14.3 | 表 14.3 |
| Eq. (14.3) | 式 (14.3) |
| Cause and effect | 前因后果 |
| Common pitfall | 易错点 |
| Pause: … | 停一下：… |
| Summary | 本讲小结 |
| Exercises · Exercise k · Show answer | 练习 · 练习 k · 展开答案 |
| Glossary | 术语中英对照 |
| Self-check after studying · Can compute / explain / connect | 学完后的检查标准 · 会算 / 会解释 / 会串联 |
| Original note | 原笔记 |
| Mind map note `<COURSE> Mind Map` · frontmatter key `mindmap` | `<COURSE> 知识导图` · frontmatter key `知识导图` |
| Mind map items: What · Why needed · Example · Pitfall | 是什么 · 为什么需要 · 例 · 注意 |

Glossary columns: in `zh` / `zh+en` it is *Chinese · English · one-line meaning*; in `en` it is
*Term · one-line meaning* (drop the English column); in `en+zh` it is *English · Chinese · meaning*.


## House style (one format per element, modelled on mainstream teaching sites)

The *rigor* is a paper's: every element has exactly one format, is numbered where it is referred
to, and every outside claim is cited. The *look* follows mainstream teaching sites (format only,
not content):
- **Runoob 菜鸟教程**: prev/next navigation, a labelled 实例 block with its result right after it,
  bold **注意：** notes, tables that always have a header row.
- **MDN**: a fixed section order, and a closing "See also" list.
- **d2l.ai 动手学深度学习**: decimal section numbers, figures and equations numbered by section,
  author–year citations with a reference list, and every section ending in 小结 → 练习.

Nothing is improvised: if an element is not listed here, add it here first. `scripts/lint_note.py`
checks the mechanical parts before publishing (step 7). Examples are in Chinese; `en` notes use the
English labels from the table above.

### Page frame
- **Top:** the `> [!info] 课程与范围` box, whose first line is the navigation
  `« 上一讲：[[WEEK n-1]] · 下一讲：[[WEEK n+1]] »` (only notes that exist), then the reading-route
  table as the page contents (本讲目录).
- **Sections:** decimal numbers throughout (`## 第四部分 · …`, `### 14. …`, `#### 14.3 …`).
  A lesson heading carries its slide pages: `#### 14.3 为什么 batch 不能太小（Batch Size）（p.53）`.
- **End of the note, in this order:** `本讲小结` (one-page summary) → `练习` → `术语中英对照` →
  `参考文献` → the same navigation line as the top.

### Worked examples (the 实例 block)
Every hand-worked calculation or code run that the reader should follow is one block:
```markdown
> [!example] 实例 14.3：batch = 2 时均值有多晃
> 4 张图的值 2、4、6、8，每次只抽 2 张……
>
> **计算结果：** 6 种 batch 的均值是 3、4、5、5、6、7，最多偏离 5 两个单位。
```
The label `实例 <section>.<k>` is numbered by section. The result line always starts with
**计算结果：** (for code: **运行结果：** followed by a code block of the real output).
Analogies are **not** 实例 blocks; they use `> [!quote] 打个比方`.

### Where content comes from: three kinds, three looks
| Kind | Format | Example |
| --- | --- | --- |
| **On the slides** | Plain text; cite the page as `（p.N）`, ranges `p.51–52` | 用当前 batch 的统计量代替整个数据集的统计量（p.51）。 |
| **Beyond the slides, one sentence** | Sentence + `（补充 [Author, Year]）` | batch = 2 时 GroupNorm 的错误率比 BN 低约 10 个百分点（补充 [Wu & He, 2018]）。 |
| **Beyond the slides, a paragraph or more** | A fold titled `补充：<topic>`, whose last line is `来源：[Author, Year]` | see below |
| **Derived here from slide content** (algebra, a worked example, no outside claim) | `（本笔记推导）`, or inside a `深入：` fold; covered by `verify.py` | 两式相减即得 ρ = 2/‖w‖（本笔记推导）。 |
| **Could not be confirmed** | `（待核对：<what is unsure>）` | |

```markdown
> [!info]- 补充：为什么小 batch 下 GroupNorm 更稳
> <explanation>
> 来源：[Wu & He, 2018]
```

A `> [!note]- 深入：…（可跳过）` fold holds **deeper treatment of slide content** (a full
derivation, edge cases). Anything from outside the slides goes in a `补充：` fold instead. Never mix
the two, and never write a bare `（补充）` without a citation.

### Citations and the reference list (d2l style)
- In text: author–year in square brackets: `[Ioffe & Szegedy, 2015]`, `[Wu & He, 2018]`,
  `[Freeman et al., 2014]` (three or more authors → `et al.`).
- `## 参考文献` near the end, one entry per source, sorted by first author:
  `- [Ioffe & Szegedy, 2015] Ioffe, S., & Szegedy, C. (2015). Batch normalization: … *ICML*. https://arxiv.org/abs/1502.03167`
  Prefer a DOI, otherwise a stable URL (arXiv, official docs, a textbook page).
- The course slides are not listed; they are cited by page `（p.N）`.
- Every citation in the text has an entry, and every entry is cited at least once.

### Figures, tables, equations (numbered by section, like d2l)
- **Figure:** every embed is followed on the next line by an italic caption
  `*图 14.3 · p.58 · <short title>：<what to look at>*`, or `*图 14.3 · 自绘 · …*` for our own
  diagrams. Refer to it in text as 「见图 14.3」.
- **Table:** a table that carries data or a comparison has a bold caption on the line above,
  `**表 14.3 · <title>**`, and always a header row. Layout tables (reading route, glossary) have no
  caption.
- **Set comparison table:** closes every set of parallel items, captioned
  `**表 14.3 · <set name> 对比**`, columns `名称（English） | 是什么 | 解决什么 / 何时用 | 例子`.
- **Equation:** a display equation that is referred to later ends with `\tag{14.3}` and is cited
  as 式 (14.3). Other equations have no number.

### Text conventions
- **Short notes** inside prose, Runoob style: a paragraph starting with **注意：** in bold.
  A real, common misconception gets a `> [!warning] 易错点` box instead.
- **New term, first definition:** **中文（English）** in bold, then the one-line `*EN: …*` statement.
- **Bilingual statements:** the Chinese sentence, then `*EN: …*` on the next line (`zh+en`).
- **Symbols:** one letter, one meaning for the whole note (symbol table in `plan.md`), and the
  slide's own notation when it has one.
- **Numbers:** `×` for multiplication and `−` for minus in prose, an en dash for ranges (`3–7`),
  math in `$…$`.

### Callouts (fixed titles)
| Use | Callout |
| --- | --- |
| Scope box and top navigation | `> [!info] 课程与范围` |
| Worked example | `> [!example] 实例 14.3：…` (result line **计算结果：** / **运行结果：**) |
| Question chain | `> [!question]- 第 k 题：…` |
| Question needing a matrix / display formula | `> [!question]- 第 k 题：<short ask>`; setup + `$$…$$` in the body; answer nested as `> > [!success]- 展开答案` |
| End-of-part check | `> [!question]- 停一下：…` |
| Practice answer | `> [!success]- 展开答案` under `#### 练习 k · <title>` |
| Analogy | `> [!quote] 打个比方` |
| Common pitfall | `> [!warning] 易错点` |
| Exam-critical | `> [!important] <title>` |
| Chain recap | `> [!tip] 前因后果` |
| Deeper slide content | `> [!note]- 深入：…（可跳过）` |
| Beyond the slides | `> [!info]- 补充：…` (last line `来源：[Author, Year]`) |
| Closing checklist | `> [!tip] 学完后的检查标准` |
| Kept user text | `> [!quote] 原笔记` |
