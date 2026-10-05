# Learning design: why the notes teach the way they do

This file explains the teaching approach behind the lesson arc in `SKILL.md` and the research each
rule rests on. `SKILL.md` says *what* to do; this file says *why*, so the rules are not changed by
accident. It grew out of live study sessions with the skill's user. The dated notes below record
what went wrong and what fixed it.

## The approach in one paragraph

A topic is taught through **one running scenario** that stays the same from the first lesson to the
last. An example is a cat classifier whose layer 1 outputs 2, 4, 6, 8 on four training images and
whose layer 2 has learned "above 5 means cat". Each new lesson moves that scenario into a new
situation: layer 1 is updated, the GPU fits only 2 images, the model is deployed and receives one
photo. The reader first **applies what they already learned**, watches it **fail inside the
story**, and is then **guided, one small question at a time**, to the fix. Only after that does the
slides' name and formula appear, mapped onto the reader's own answers. The chain ends with
result → consequence → conclusion, and the topic's last lesson calls back to its first.

## Principles and the evidence behind them

### 1. One running scenario per topic (anchored instruction)
- **Rule:** reuse one story across all lessons of a topic. Never bring in free-floating toy data,
  and never give an existing number a new role without saying so.
- **Why:** the Cognition and Technology Group at Vanderbilt (CTGV, led by John Bransford) built
  whole curricula around one "anchor" story, the *Jasper Woodbury* series. All later sub-problems
  live inside that story. Their target was **inert knowledge**, knowledge that can be recited but is
  not used when a real situation calls for it.
- **Session note (2026-09-30):** the same numbers {2, 4, 6, 8} meant "one batch" in one lesson and
  "the whole dataset" in the next, and the switch was never stated. The learner was lost. A
  separate "purpose / mapping" box bolted onto each example was then judged too rigid. What worked
  was letting the story carry the purpose.
- **Session note (2026-10-05):** for the same reason, the learner asked to drop the bold
  "自己动手推一推 / Work it out yourself" label between the problem and the question chain. It
  reads as stiff. A bridging sentence inside the story now hands over the first question instead.

### 2. Apply old knowledge → see it fail → introduce the new idea (productive failure)
- **Rule:** in step 2 of the arc, the reader tries what they already know on the new situation
  before the new concept is named.
- **Why:** Kapur's *Productive Failure* has two phases. In the first, students attempt problems with
  their prior knowledge and usually fail. In the second, the teacher consolidates the canonical
  concept on top of those attempts. A meta-analysis of 166 comparisons found better conceptual
  understanding and transfer than instruction-first, with no loss in procedural skill (Sinha &
  Kapur, 2021; Hedges' g = 0.36). The effect was larger when the productive-failure principles were
  followed closely, and it reversed for young children (grades 2–5). Adult university learners, the
  audience of this skill, are in the favourable range. This fits Piaget's account of learning through **cognitive conflict**: an existing
  scheme fails, and the learner restructures it. It also fits Bjork's **desirable difficulties**.

### 3. Build on what the learner already knows; chain lessons (meaningful learning)
- **Rule:** every lesson's problem grows out of the previous lesson's weakness (step 5 → step 1).
  Link back to earlier weeks, and remind the reader of every term where it is used.
- **Why:** Ausubel held that the most important single factor in learning is what the learner
  already knows. New ideas stick when they are anchored to existing ones rather than memorised in
  isolation, which is the "banking" (rote-filling) model that Freire criticised.

### 4. Guided, not minimal-guidance discovery
- **Rule:** discovery is always scaffolded. Use a 3–5 question chain, Q1 is pure observation, each
  question changes one thing, and small integers keep the arithmetic easy. The slides' concept is
  always stated explicitly at the end.
- **Why:** Kirschner, Sweller & Clark (2006) showed that minimally guided discovery overloads
  novices' working memory and underperforms. Productive failure itself depends on a designed
  problem and a teacher-led consolidation phase.

### 5. In live tutoring, never hand over the answer first
- **Rule (Mode B):** ask one question per turn and wait. On a wrong answer, diagnose where the
  learner's number came from rather than re-teaching. The learner does the conceptual step and the
  tutor does the tedious arithmetic.
- **Why:** in a randomised trial with about 1,000 high-school students, unrestricted GPT-4 help
  raised practice scores but lowered unassisted exam scores by 17%. A tutor limited to hints removed
  the harm (Bastani et al., 2025). An AI tutor built on active-learning principles more than doubled
  learning gains, in less time than an active-learning class (Kestin et al., 2025). One-to-one
  tutoring has long been known to beat class teaching (Bloom, 1984, "2 sigma"; see VanLehn, 2011,
  for more modest effect sizes). An AI tutor makes one-to-one cheap, but only if it tutors.

### 6. Expect discomfort; don't mistake fluency for learning
- **Rule:** keep the struggle, and don't collapse a question chain into a finished explanation just
  because the learner hesitates. Do stop adding new content when the learner is lost on basic terms,
  and ground those terms first.
- **Why:** students in active-learning classes learned more but *felt* they learned less than
  students in polished lectures (Deslauriers et al., 2019). Across 225 STEM studies, lecturing had
  1.5× the failure rate of active learning (Freeman et al., 2014).

### 7. Every number checked, every beyond-slides claim sourced
- **Rule:** use `verify.py` for all numbers (step 6), online grounding for anything beyond the
  slides (step 6b), and report errors honestly.
- **Why:** AI tutors make mistakes. In these sessions a count was wrong (12 vs 9 surface forms), and
  a tutorial's cosine answer silently used unnormalised vectors. A learner who trusts wrong numbers
  learns the wrong thing.

### 8. Questions that can be understood, not just answered
- **Rule:** every question is self-contained, asks one thing, uses each symbol with a single
  meaning across the whole note, states exactly what is counted and how, and has a stepwise answer
  (question-writing rules in `SKILL.md` step 5). A fresh "student" subagent then answers every
  question from the note alone, and whatever it misreads is rewritten (step 6d).
- **Why:** unclear wording adds extraneous cognitive load. The learner spends working memory on
  decoding the question instead of on the idea (Sweller, 1988; Kirschner et al., 2006). Checking
  that the answers are correct (`verify.py`) cannot catch this. Only a reader without the author's
  context can.
- **Session note (2026-09-30):** a question on normalisation groups used N for "number of images",
  while an earlier lesson used N for "number of values averaged". It also packed two scenarios into
  one question and said "split channels into groups" without saying how. The learner read it as a
  C(4,2) combination count and could not see why "all 4 channels" gave 2 groups instead of 1.

### 9. The learner chooses the story
- **Rule:** before a multi-lesson topic, offer 2–3 candidate running stories (one recommended,
  "Other" for the learner's own) and keep the chosen one for the whole topic.
- **Why:** personalising the context of a lesson to the learner's own interests improved
  engagement and learning (Cordova & Lepper, 1996). Choice also supports autonomy, one of the
  basic needs behind intrinsic motivation in self-determination theory (Deci & Ryan, 2000). A
  story the learner picked is one they can picture, and that is what anchored instruction relies
  on.
- **Session note (2026-09-30):** the learner designed the story-driven approach and asked that
  the story itself be theirs to choose, not imposed.

### 10. A telling slide figure beats a page of prose
- **Rule:** when a slide figure *is* the concept (the normalization cube, an architecture diagram),
  bring it in early, read it for the learner (axes, what the highlight means, the slide's own
  symbols), and ask questions on it. Text and tables fill in only what the figure cannot show.
- **Why:** people learn better from words and pictures together than from words alone (the
  multimedia principle), and cues that point attention at the key part of a graphic help further
  (the signalling principle; Mayer, 2009). A figure shows at once what prose has to build up in
  sequence, and it spares working memory.
- **Session note (2026-09-30):** several text tables about "which numbers form one group" did not
  land. The slide's cube with a blue block along N, C and H,W made it clear at once, and the
  learner pointed out that the slide's picture was more effective than the long explanation.

### 11. Plain words as a bridge, professional terms as the destination
- **Rule:** tell the story in plain language and land every point on the professional term, stated
  in the note language and in English ("In professional terms").
- **Why:** this is the learner's stated preference. They find the English wording clearer and need
  to talk to practitioners. It is a user requirement, not a research claim.

### 12. Questions worth asking, inside the story (hinge questions)
- **Rule:** every question has a card in `plan.md` naming the misconception or insight it targets,
  the story object it uses, and its number of inference steps. Cut questions whose answer can be
  read off the prompt, and give every problem lesson one consequence question that shows the
  damage in the story. Choose the story at plan time so it can show every failure (step 3.3).
- **Why:** a hinge question is diagnostic: learners who hold the target misconception answer it
  wrongly, so answering it right is evidence of understanding (Wiliam, 2011; Barton, 2018). A
  question that everyone gets right teaches nothing and costs attention. Anchored instruction
  (principle 1) only works if the anchor can show the phenomenon.
- **Session note (2026-10-02):** in WEEK 6 the learner found some questions trivial (§1 Q1 asks
  whether 0.2377 < 0.25). Others left the story: §8 changed the bias to 0 and let "each layer's
  bias adjust itself". The running story had a single cat image, so it could not show what
  vanishing gradients *do*. The learner asked "can't we still tune ω?" and only got it once a dog
  was added: the 10-layer net output 0.500 for both images and the loss stuck at 0.5. Misconceptions
  seen that session, which make good hinge targets: "backprop only gives the sign", "vanishing is
  backprop's fault", "the last layers can make up for frozen front layers", "a better loss
  function fixes vanishing", "clipping caps each component at ±c".

### 13. Answer depth follows inference steps (subgoals, faded examples)
- **Rule:** a one-step answer is one line. A multi-step answer gives one labelled sub-step per
  inference. An operation the reader meets for the first time is worked in full once, and later
  uses fade to the result.
- **Why:** labelling the subgoals of a worked solution helps learners rebuild and transfer it
  (Catrambone, 1998; Margulieux, Guzdial & Catrambone, 2012). Fading worked steps as competence
  grows smooths the move from studying examples to solving problems (Renkl & Atkinson, 2003).
  Detail that helps a novice is redundant for someone who already knows it (the expertise reversal
  effect; Kalyuga, Ayres, Chandler & Sweller, 2003). So depth must follow what *this* reader
  can already do, not how important the topic is.
- **Session note (2026-10-02):** §4 Q3 answered "(1×10)(10×10) = 1×10" with no product shown, and
  the learner did not know how to multiply a row by a matrix. §5 Q3 gave scientific notation
  without steps, and §7 Q3 wrote `diag(0.25, 0.25)`. Meanwhile trivial questions got full
  paragraphs.

### 14. Fluent is not understood: causal chains, plain words before terms, restate to check
- **Rule:** teach a new idea as one scenario plus one connected chain of sentences ("because… so…
  which means…") ending in the outcome. Tables and bullets hold only numbers and parallel
  comparisons. Describe the thing in plain words before naming it, with at most one new term per
  sentence. In live chat give one idea per turn, and check understanding by asking the learner to
  restate the chain, not by asking "got it?".
- **Why:** AI-written explanations can look excellent and still confuse. In a 150-reader study,
  LLM-written summaries were rated as clear and coherent as human-written ones, yet readers
  understood the human versions significantly better. Surface readability metrics did not predict
  comprehension (Guo et al., 2025). Three mechanisms explain the gap:
  - **Coherence.** Readers with little background knowledge learn more from high-coherence text,
    where the links between statements are explicit; only knowledgeable readers can fill the gaps
    themselves (McNamara, Kintsch, Songer & Kintsch, 1996). Understanding a text means finding
    the causal chain from its opening to its outcome (Fletcher & Bloom, 1988).
  - **Lists.** Bullet outlines leave the causal relations between items unstated (Tufte, 2003).
    This is an argument from case analysis, not a controlled experiment, and it fits the
    causal-chain account above.
  - **Jargon.** Across nine experiments, jargon lowered understanding while making short
    explanations more satisfying, because readers assumed the terms filled the gaps. Asking
    people to explain first made them judge such explanations, and their own understanding, more
    accurately (Cruz & Lombrozo, 2025).
- **Session note (2026-10-02):** the learner read WEEK 6 Part 3 (PyTorch autograd) and said they
  were lost. My first reply was a 4-row table: dynamic graph, memory cost, freezing, no_grad and
  inference_mode, one term-heavy cell each, with nothing linking the rows. The learner called it
  "鬼话" ("gibberish"). What had worked earlier the same day was the opposite. The cat–dog run
  showed one scenario, real numbers and a single chain: gradient ≈ 10⁻⁷ → w₁ cannot learn → the
  cat–dog gap is squashed → both images output 0.5 → the loss sticks at 0.5.

### 15. Gist first: cut it down before building it up
- **Rule:** before any problem, question chain, table or term, give the gist: what the thing does,
  as one familiar example going in and coming out, plus why anyone wants that. Use at most three
  plain sentences and one term. Put it at the top of the note, of each part and of each lesson.
  Hand calculations come afterwards, to deepen and check the idea. Borrow the opening example and
  the order of ideas from good explainer videos where they exist.
- **Why:** a short, general introduction given *before* new material helps people learn and
  remember it, because it gives the details something to attach to. Ausubel (1960) called this an
  advance organizer. Without it, every detail has to be held in working memory unconnected, and
  working memory is small. Problem solving before the learner has a frame uses the capacity that
  should go to building one (Sweller, 1988). That is why a question chain fails when the reader
  does not yet know what the numbers are for: they guess.
- **Session note (2026-10-05):** the learner read the guest-lecture note on Metaphorical Cognition
  (6 lessons, 2 questions each, tables of study numbers) and could not say what MetaPro does. Then
  one paragraph that started from L4's *She devoured his novel* and gave the in → out of MetaPro
  made it clear at once. The learner's verdict: the hand calculations are useful, but only after
  you know what the thing is about; before that you answer them blind. Two explainer videos on
  conceptual metaphor, read through their transcripts, followed the same path: one familiar line,
  the essence in one sentence, a family of examples, terms last, no calculation.
- **Session note (2026-10-05, later):** the learner then pointed at the MetaPro concept block
  itself as "乱糟糟" ("a mess"). It had a page number in nearly every sentence. It used three
  different example sentences for three stages. One bullet packed definition, example,
  granularity and variants together. The rewrite followed how widely read explainers teach a
  pipeline:
  - Alammar's *Illustrated Transformer* starts from a black box and zooms in.
  - The Hugging Face course follows one example through every step and shows each output.
  - Google's technical-writing course asks for one idea per sentence.

  So the rewrite opened with one black-box line, then a three-row table with one sentence going
  through all three stages, then one short paragraph per stage. The slide details went into a
  single fold. This became the SKILL.md rule "The concept block".

## References

- Alammar, J. (2018). The Illustrated Transformer. https://jalammar.github.io/illustrated-transformer/
- Ausubel, D. P. (1960). The use of advance organizers in the learning and retention of meaningful
  verbal material. *Journal of Educational Psychology*, 51(5), 267–272. https://doi.org/10.1037/h0046669
- Ausubel, D. P. (1968). *Educational Psychology: A Cognitive View*. Holt, Rinehart & Winston.
- Barton, C. (2018). *How I Wish I'd Taught Maths*. John Catt Educational.
- Bastani, H., Bastani, O., Sungu, A., Ge, H., Kabakcı, Ö., & Mariman, R. (2025). Generative AI
  without guardrails can harm learning: Evidence from high school mathematics. *PNAS*, 122(26),
  e2422633122. https://doi.org/10.1073/pnas.2422633122
- Bjork, R. A. (1994). Memory and metamemory considerations in the training of human beings. In J.
  Metcalfe & A. Shimamura (Eds.), *Metacognition: Knowing about knowing* (pp. 185–205). MIT Press.
- Bloom, B. S. (1984). The 2 sigma problem: The search for methods of group instruction as effective
  as one-to-one tutoring. *Educational Researcher*, 13(6), 4–16.
- Catrambone, R. (1998). The subgoal learning model: Creating better examples so that students can
  solve novel problems. *Journal of Experimental Psychology: General*, 127(4), 355–376.
- Cognition and Technology Group at Vanderbilt (1990). Anchored instruction and its relationship to
  situated cognition. *Educational Researcher*, 19(6), 2–10.
- Cognition and Technology Group at Vanderbilt (1992). The Jasper series as an example of anchored
  instruction: Theory, program description, and assessment data. *Educational Psychologist*,
  27(3), 291–315. https://doi.org/10.1207/s15326985ep2703_3
- Cordova, D. I., & Lepper, M. R. (1996). Intrinsic motivation and the process of learning:
  Beneficial effects of contextualization, personalization, and choice. *Journal of Educational
  Psychology*, 88(4), 715–730.
- Cruz, F., & Lombrozo, T. (2025). How laypeople evaluate scientific explanations containing
  jargon. *Nature Human Behaviour*, 9(10), 2038–2053. https://doi.org/10.1038/s41562-025-02227-0
- Deci, E. L., & Ryan, R. M. (2000). Self-determination theory and the facilitation of intrinsic
  motivation, social development, and well-being. *American Psychologist*, 55(1), 68–78.
- Deslauriers, L., McCarty, L. S., Miller, K., Callaghan, K., & Kestin, G. (2019). Measuring actual
  learning versus feeling of learning in response to being actively engaged in the classroom.
  *PNAS*, 116(39), 19251–19257. https://doi.org/10.1073/pnas.1821936116
- Fletcher, C. R., & Bloom, C. P. (1988). Causal reasoning in the comprehension of simple
  narrative texts. *Journal of Memory and Language*, 27(3), 235–244.
  https://doi.org/10.1016/0749-596X(88)90052-6
- Freeman, S., Eddy, S. L., McDonough, M., Smith, M. K., Okoroafor, N., Jordt, H., & Wenderoth, M. P.
  (2014). Active learning increases student performance in science, engineering, and mathematics.
  *PNAS*, 111(23), 8410–8415. https://doi.org/10.1073/pnas.1319030111
- Freire, P. (1970). *Pedagogy of the Oppressed*. Herder and Herder.
- Google for Developers (n.d.). Technical Writing One: Short sentences. https://developers.google.com/tech-writing/one/short-sentences
- Guo, Y., Sohn, J. H., Leroy, G., & Cohen, T. (2025). Are LLM-generated plain language summaries
  truly understandable? A large-scale crowdsourced evaluation. arXiv:2505.10409.
  https://arxiv.org/abs/2505.10409
- Hugging Face (n.d.). LLM Course, Chapter 2: Behind the pipeline. https://huggingface.co/learn/llm-course/chapter2/2
- Kalyuga, S., Ayres, P., Chandler, P., & Sweller, J. (2003). The expertise reversal effect.
  *Educational Psychologist*, 38(1), 23–31.
- Kapur, M. (2008). Productive failure. *Cognition and Instruction*, 26(3), 379–424.
- Kapur, M., & Bielaczyc, K. (2012). Designing for productive failure. *Journal of the Learning
  Sciences*, 21(1), 45–83.
- Kestin, G., Miller, K., Klales, A., Milbourne, T., & Ponti, G. (2025). AI tutoring outperforms
  in-class active learning: An RCT introducing a novel research-based design in an authentic
  educational setting. *Scientific Reports*, 15, 17458. https://doi.org/10.1038/s41598-025-97652-6
- Kirschner, P. A., Sweller, J., & Clark, R. E. (2006). Why minimal guidance during instruction does
  not work. *Educational Psychologist*, 41(2), 75–86.
- Margulieux, L. E., Guzdial, M., & Catrambone, R. (2012). Subgoal-labeled instructional material
  improves performance and transfer in learning to develop mobile applications. *Proceedings of
  ICER '12*, 71–78.
- Mayer, R. E. (2009). *Multimedia Learning* (2nd ed.). Cambridge University Press.
- McNamara, D. S., Kintsch, E., Songer, N. B., & Kintsch, W. (1996). Are good texts always better?
  Interactions of text coherence, background knowledge, and levels of understanding in learning
  from text. *Cognition and Instruction*, 14(1), 1–43. https://doi.org/10.1207/s1532690xci1401_1
- Piaget, J. (1985). *The Equilibration of Cognitive Structures*. University of Chicago Press.
- Renkl, A., & Atkinson, R. K. (2003). Structuring the transition from example study to problem
  solving in cognitive skill acquisition: A cognitive load perspective. *Educational
  Psychologist*, 38(1), 15–22.
- Sinha, T., & Kapur, M. (2021). When problem solving followed by instruction works: Evidence for
  productive failure. *Review of Educational Research*, 91(5), 761–798.
  https://doi.org/10.3102/00346543211019105
- Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive
  Science*, 12(2), 257–285.
- Tufte, E. R. (2003). *The Cognitive Style of PowerPoint*. Graphics Press.
- VanLehn, K. (2011). The relative effectiveness of human tutoring, intelligent tutoring systems,
  and other tutoring systems. *Educational Psychologist*, 46(4), 197–221.
- Wiliam, D. (2011). *Embedded Formative Assessment*. Solution Tree Press.
