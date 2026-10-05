# Review mode: from a finished practice quiz to an error report

Read this when the learner has finished a practice quiz ("做完了", "I'm done", "check my answers")
or asks for a review / weak-spot report. It covers how to grade, how to analyse the errors, and
how to write a report the learner can study from without going back to the notes.

## Why the report looks like this (the evidence)

- **Sort errors by type, not only by chapter.** After an exam, students who reflect on how they
  studied and sort their mistakes by type (an *exam wrapper*) improved their grades and their
  metacognition across ten disciplines, and changed how they planned to study
  (Sethares & Asselin, 2022). The point of sorting is to choose the fix. Two failure modes are
  common. One is calling every error a knowledge gap, which sends the learner back to rereading
  when the real problem is something else. The other is using categories too broad to act on
  ("Lecture 4").
- **Teach confusable items side by side.** Learners mix up similar concepts. Practice that makes
  them tell the concepts apart works much better than practice that covers one concept at a time.
  In a randomized trial with 787 students, the mixed-practice group scored 61% on a delayed test
  and the blocked-practice group 38% (Rohrer et al., 2020). The proposed mechanism is
  discrimination: mixing forces the learner to notice what separates one category from another
  (Rohrer, 2012).
- **Write it to be recalled, not reread.** Building a summary sheet did not by itself improve
  learning (Dickson & Bauer, 2008). So the report ends in questions with folded answers, and the
  learner answers before opening each fold.

## Workflow

1. **Grade.**
   ```bash
   python <skill>/scripts/grade_quiz.py "<quiz note>" --json "<work>/grade.json"
   ```
   The script reads the quiz format described at its top. It reports questions left
   unanswered or ticked more than once **first**. Ask whether to grade now or let the learner
   fill those in first, and never silently count them as wrong. If the quiz uses a different
   format, adapt the parsing instead of guessing.
2. **Find the error types.** Sort every wrong answer into one of these, most specific first:
   - **Default guess:** the same wrong option text chosen two or more times. The script lists
     these as `default guess`. This is the most valuable finding, because one rule fixes several
     questions.
   - **Swapped pair:** two facts each attached to the other's question (e.g. "POS tags is the
     feature for subjectivity detection" vs "lemmatization is the feature for POS tagging").
   - **Name lure:** a definition question answered with the option that shares a word with the
     term ("panalogy" → "parallel corpora").
   - **Test-taking rule:** a question type with a fixed answer pattern, e.g. "why is X important"
     → "improves downstream tasks".
   - **Content gap:** the learner did not know the idea at all. Use this only when none of the
     above fits.
3. **Build the answer table from the answer key, not from memory.** List every question's stem
   and keyed answer (the script's JSON and the quiz file have both). Fill the master table only
   from those, and mark each cell the learner got wrong.
4. **Write the report** (skeleton below), lint and publish it like a note
   (`Lecture Notes/<course>/<COURSE> 错题报告.md`, or the English label).
5. **Reply:** the score, a sentence on the main error type, and the order to use the report in.
   Record the score and the wrong question numbers in the progress memory, so the next attempt
   can be compared.

## Report skeleton

Every part obeys the gist-first and causal-chain rules of the note itself: plain words first, one
idea per sentence, tables only for parallel items.

1. **At a glance** (`> [!abstract]`): the score, how many errors share one type, the learner's
   default guesses by name, and the one or two things to do, in ≤ 3 sentences. Then a small
   per-section score table.
2. **First, what each tool is for.** Before any habit or table, explain every option family the
   errors involve (datasets, algorithms, resources) in plain words: what it *is* and what it
   *contains or does*. Then the pairing follows by reasoning instead of memory. Give the one or
   two principles that generate all the pairings ("a dataset goes with the task whose labels it
   contains"; "an algorithm goes with the task of the same shape: tag each word → HMM/CRF,
   classify a whole text → SVM, no labels → K-means/LDA"). End with one Pause question that
   needs the reasoning.
3. **Error habits, one per default guess or swapped pair.** One sentence naming the habit and
   the questions it cost, then the correction phrased as the question to ask yourself ("does
   this task have labelled data? then not K-means"), built on part 2. State when the guessed
   option *is* right ("K-means is right only for unsupervised WSD").
4. **One master contrast table** for the confusable family: one row per item (task, model,
   concept), columns for what the questions ask about (dataset, model, related task, metric…),
   cells from the answer key, ★ on cells the learner missed. This is the side-by-side contrast
   the discrimination evidence points to.
5. **Test-taking rules** that work without the content: answer patterns per question type,
   distractor families to rule out, aliases.
6. **Name-lure table** for definition errors: term · correct definition (keyword in bold) · the
   lure the learner chose and the word that lured them.
7. **Self-test:** every wrong question, in original (mixed) order, as
   `> [!question]- Qn · <short stem>` with the answer and a one-line reason inside that goes
   back to what the tool is for (part 2), not to a mnemonic. Mixed order
   on purpose: it makes the learner discriminate.
8. **Check standard** (`> [!tip]`): cover the table's answer columns and recite them, then redo
   the self-test, aiming for 100%.

Keep it to what the errors need. A report that repeats the whole course is just another note to
reread.

## References

- Dickson, K. L., & Bauer, J. J. (2008). Do students learn course material during crib sheet
  construction? *Teaching of Psychology*, 35(2), 117–120. https://doi.org/10.1080/00986280801978343
- Rohrer, D. (2012). Interleaving helps students distinguish among similar concepts. *Educational
  Psychology Review*, 24(3), 355–367. https://files.eric.ed.gov/fulltext/ED536926.pdf
- Rohrer, D., Dedrick, R. F., Hartwig, M. K., & Cheung, C.-N. (2020). A randomized controlled
  trial of interleaved mathematics practice. *Journal of Educational Psychology*, 112(1), 40–52.
- Sethares, K. A., & Asselin, M. E. (2022). Use of exam wrapper metacognitive strategy to promote
  student self-assessment of learning: An integrative review. *Nurse Educator*, 47(1), 37–41.
  https://doi.org/10.1097/NNE.0000000000001026

## Session note (2026-10-05)

First real use: AI6127 mock quiz, 100 MCQs, score 74/100. 18 of the 26 errors were "which
dataset / model / related task goes with this task", and three wrong options had each been chosen
4 times: OntoNotes, K-means, POS tagging. An earlier per-chapter list of errors had hidden that
pattern. Grouping by default guess turned 12 errors into three one-line rules. The report built
this way (`AI6127 错题报告.md`) is the model for the skeleton above.

Later the same day the learner read the report and said: memorising these pairings does not stick,
"I should know what these datasets and algorithms are for". The report's mnemonic boxes ("OntoNotes only
for anaphora and metaphor") were rote rules with no reason attached. The report was rewritten to
open with what each dataset contains and what shape of task each algorithm fits, from which every
pairing can be derived. That is now part 2 of the skeleton.
