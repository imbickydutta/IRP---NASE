# Session 5 Instructor File: Add Mock Answer Evaluator

## Session Title

Add Mock Answer Evaluator

## Duration

2 hours

## Project

AI Interview Prep Copilot

## Session 5 Objective

By the end of Session 5, students should have a working mock answer evaluator feature inside the AI Interview Prep Copilot.

The evaluator allows a student to:

- select a question from the list generated in Session 4, or type a custom question
- type their answer in a text area
- submit the answer for AI evaluation
- receive a structured feedback card with score, strengths, missing points, improved answer, and a follow-up question

Students should also understand how AI evaluation using rubric-based prompting works, why it is useful, and how to explain it in an interview.

## Session 5 Deliverable

Students will add a Mock Answer Evaluator feature to their existing app. The feature includes:

1. Question input — dropdown populated from Session 4 generated questions, plus a manual entry option
2. Answer text area — for student to type their response
3. Submit for Evaluation button
4. Feedback card displaying:
   - Score out of 10
   - Strengths in the answer
   - Missing key points
   - Improved answer version
   - One follow-up question

The feature must be integrated into the same app built across Sessions 1 through 4.

## Strict Scope Control

### Include

- Question selection via dropdown from Session 4 generated questions
- Manual/custom question entry option
- Answer text area
- Submit for Evaluation button
- Feedback card with score / strengths / missing points / improved answer / follow-up question
- Rubric-based prompt design sent to AI
- Loading state during evaluation
- Empty state when no evaluation has been submitted
- Basic error handling

### Do Not Include

- Voice input or voice output
- Timed interview mode
- Multi-question sequential interview room
- AI voice feedback
- Speech-to-text
- Full video interview simulation
- Saving all answers to a database
- Answer history tracking across sessions
- Leaderboard or comparative scoring
- Complex rating animations

Session 5 is only about adding structured answer evaluation using text input and text output.

---

# Instructor Framing

## Opening Message

In Session 4, we built the Interview Question Generator. The app can now take the student's profile and job description and generate targeted interview questions.

Today we go one step further. We will add the Mock Answer Evaluator. A student can now select a question, type an answer, and receive a detailed structured evaluation from AI.

This is not just a useful feature. It is a demonstration of one of the most important AI design patterns: rubric-based evaluation. Instead of asking AI to give vague feedback, we will ask it to evaluate against specific criteria and return a structured score card.

## Key Philosophy

Students are not expected to code everything from scratch.

They are expected to:

- guide AI with a well-structured rubric prompt
- understand what AI returned in the evaluation
- test the evaluator feature end to end
- debug issues using AI
- explain the rubric-based approach in interview language
- understand the limitations of AI scoring

## Repeated Instructor Line

AI can evaluate, but the rubric you give it determines the quality of the feedback. Your prompt is the evaluation standard.

---

# Session Flow

## 0–10 min: Opening and Recap of Session 4 — Add Interview Question Generator (generated questions available in app state)

### Instructor Goal

Re-anchor the class to what was built in Session 4 and make clear what problem today's feature solves.

### Recap Session 4

Ask students:

- What feature did we add in Session 4?
- How did the app generate questions?
- Where are the generated questions stored in the app?
- What is missing from the experience so far?

Expected answers:

- Session 4 added the Interview Question Generator
- It sent the student profile and job description to AI with a structured prompt
- Questions are stored in app state and displayed in a list
- The student cannot yet practice answering or get feedback

### Introduce Today

Tell students:

In Session 4, the app helped students prepare by showing them what questions to expect. In Session 5, the app will help them practice answering and understand where they are strong and where they need improvement.

This is called mock evaluation. And the key to good mock evaluation is giving AI a clear rubric.

### Set the Frame

Ask students what they want the evaluation to include.

Accept answers. Then reveal the structured feedback card:

- Score out of 10
- Strengths
- Missing key points
- Improved answer
- Follow-up question

Tell students: This structure is not accidental. We will design the AI prompt to force exactly this output.

---

## 10–20 min: Product Breakdown Before Prompting

### Instructor Goal

Before generating any code, build a shared mental model of the feature layout and the data flow.

### Ask Students

What does this feature need as input?

Expected answers:

- a question (either from Session 4 list or custom typed)
- the student's answer

What should the feature return?

Expected answers:

- score
- strengths
- what is missing
- better answer
- follow-up question

### Draw the Feature Map on Screen

Write this visible to the class:

Input:
- Question (dropdown or manual entry)
- Answer (text area)
- Submit for Evaluation button

Processing:
- Build a rubric prompt using the question and answer
- Send to AI
- Parse structured output

Output — Feedback Card:
- Score out of 10
- Strengths
- Missing Key Points
- Improved Answer
- Follow-Up Question

### Instructor Explanation

Before writing a single prompt, we know exactly what the app needs to collect and what the AI needs to return. This is product thinking. This is what interviewers want to see from you.

### The Most Important Question to Ask Now

Ask students: If you had to write a rubric for a technical interview answer, what would you score on?

Expected answers: correctness, clarity, depth, use of examples, terminology

Tell students: We will include exactly these criteria in the evaluation prompt.

---

## 20–35 min: Generate Add Mock Answer Evaluator Feature in AI Tool

### Instructor Goal

Use the main build prompt to generate the complete Mock Answer Evaluator feature.

### Run Prompt 1

The main prompt should clearly specify:

- full app context (Sessions 1 through 4 already built)
- the new feature components (question input, answer area, submit button, feedback card)
- the rubric-based prompt the app should send to AI
- the exact feedback card structure
- what NOT to add (voice, timed mode, history)
- comments requirement

### What to Watch For in the Generated Code

- Is the question dropdown populated from Session 4 state?
- Is the manual entry option present?
- Is the answer text area present?
- Is the Submit for Evaluation button present?
- Is the rubric prompt clearly constructed before sending to AI? (Gemini 1.5 Flash via @google/generative-ai — free tier)
- Does the AI call use `genAI.getGenerativeModel({ model: "gemini-1.5-flash" })` and `model.generateContent(prompt)`?
- Does the feedback card display all five components?
- Is there a loading state while AI processes the evaluation?

### Instructor Control Rule

Do not let students modify the rubric prompt during generation. First confirm the feature works as specified, then discuss the rubric in the concept pause segment.

---

## 35–50 min: Instructor Walkthrough of Generated Feature

### Instructor Goal

Help students understand what AI generated — both the UI structure and the critical rubric prompt.

### Walkthrough Areas

1. Where is the question dropdown built and how is it populated from Session 4 state
2. How the manual entry option works alongside the dropdown
3. Where the answer text area is defined
4. How the Submit for Evaluation button triggers the evaluation function
5. The rubric prompt — show students the full prompt being sent to AI
6. How the AI response is parsed into the five feedback components
7. How the feedback card is rendered in the UI
8. What happens when the answer text area is empty (empty state)

### Ask During Walkthrough

- Where does the list of questions come from?
- What exactly is sent to AI when Submit is clicked?
- What does the rubric prompt say?
- How does the app know to put the score in one place and strengths in another?
- What does the loading state look like?

### Simple Explanation

The AI does not magically know how to evaluate. We told it exactly what to score, what structure to return, and what tone to use. That instruction is the rubric prompt. We will read it out loud together.

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students run the main prompt in their AI tool and add the Mock Answer Evaluator feature to their own running app.

### Instructor Support Areas

Help students with:

- questions not loading in the dropdown (Session 4 state integration)
- feedback card not appearing after submission
- AI returning unstructured text instead of the five components
- score not displaying correctly
- loading state stuck or missing
- Submit button not triggering the evaluation function

### If Student Setup Fails

Do not block the class.

The student should:

- follow the instructor screen
- note which parts of the feature they did not complete
- use the shared completed code after class
- never skip the concept and interview sections even if the build is incomplete

---

## 65–80 min: Improve and Refine

### Instructor Goal

Improve the visual presentation of the feedback card and the quality of the rubric prompt.

### Expected Improvements

- color coding the score (green for 7-10, yellow for 4-6, red for 1-3)
- clear section headers in the feedback card for each of the five components
- a "Try Again" button that clears the feedback and resets the form
- showing a placeholder message before any evaluation is submitted
- displaying the question that was evaluated at the top of the feedback card

### Rubric Prompt Improvement

Ask students: What would make this evaluation more useful?

Guide discussion toward:

- adding the target role from the profile as context for the rubric
- telling AI the difficulty level of the question (basic, intermediate, advanced)
- asking AI to keep feedback constructive and not discouraging

Run Prompt 2 (UI and rubric improvement prompt) during this segment.

### Instructor Explanation

Refinement is part of the build process. The first output from AI is rarely the best version. We improve both the UI and the prompt until the feature feels genuinely useful.

---

## 80–95 min: Edge Cases and Error States

### Instructor Goal

Build error-handling awareness and test the feature against bad inputs.

### Must Add and Test

1. Empty answer submission — what happens if student clicks Submit without typing an answer
2. Very short answer (one word) — does the evaluator still return useful feedback
3. Off-topic answer — student types something completely unrelated to the question
4. Very long answer — does the feedback card still display cleanly
5. No questions from Session 4 — what happens if the dropdown is empty because no questions were generated yet
6. AI API call fails — what does the user see

### Instructor Explanation

Every feature has edge cases. Demonstrating that you thought about them is exactly what distinguishes a thoughtful developer from someone who only builds happy-path flows. Interviewers notice this.

### Ask Students

What would happen in your app if:

- The student submits a blank answer?
- The AI API is temporarily unavailable?
- No questions exist in the dropdown?

Make sure all three cases show a meaningful message to the user.

---

## 95–105 min: Concept Pause — AI Evaluation and Rubric-Based Feedback

### Instructor Goal

Convert the implementation into interview-ready conceptual understanding.

### Explain the Concept

Tell students:

Most people think AI feedback means asking: "Was this answer good?"

That is not how professional AI evaluation works.

Professional AI evaluation works by giving AI a rubric: a set of specific criteria to score against.

In our app, we do not ask: "Was this answer good?"

We ask: "Score this answer on correctness (1-3 points), clarity (1-2 points), use of examples (1-2 points), technical terminology (1-2 points), and completeness (1 point). Return the total score, list the strengths, list what is missing, provide an improved version, and ask one follow-up question."

This is rubric-based prompting. You are not asking for a vague opinion. You are asking for a structured judgment.

### Explain the Flow

Student selects question and types answer  
↓  
App builds a rubric prompt combining the question, the answer, and the evaluation criteria  
↓  
Prompt is sent to AI  
↓  
AI evaluates against the rubric and returns structured output  
↓  
App parses the output and renders the five-component feedback card  
↓  
Student reads feedback and decides what to improve

### Explain the Limitation

Tell students:

AI evaluation is not perfect. AI can:

- score too generously
- miss domain-specific nuances
- reward fluency over correctness
- misunderstand niche technical terms

Students should use this feedback as guidance, not as truth. If AI gives you an 8 out of 10 but you know your answer was weak, investigate. If AI gives you a 5 and you believe your answer was strong, check against the improved version and decide if the criticism is valid.

### Student Writing Task

Ask every student to write a 2–3 line answer:

What is the difference between asking AI "Was this answer good?" and using a rubric-based evaluation prompt?

Expected answer:

Asking AI if an answer was good gives a vague impression with no structure. A rubric-based prompt gives AI specific criteria to score against and forces a structured output — score, strengths, missing points, improved version, and follow-up — which is far more useful for preparation.

---

## 105–115 min: Interview Discussion and Viva Practice

### Instructor Goal

Prepare students to speak about this feature in interview settings.

Use the interview questions section below.

Run at least five questions from the list. Prioritize the AI Topic questions (Q11–Q15) in this segment.

Ask students to answer verbally, not by reading notes.

Correct and guide. If a student gives a weak answer, ask the class to improve it together.

---

## 115–120 min: Wrap-Up and Session 6 Preview

### Instructor Closing

Today we built the Mock Answer Evaluator. This feature introduced one of the most important AI concepts in the entire course: rubric-based evaluation. Instead of asking AI for a vague opinion, we gave it a precise rubric and got structured, actionable feedback.

Next session, we will add the RAG-Lite Doubt Solver — Session 6 — Add RAG-Lite Doubt Solver. Instead of pre-generating all answers, the app will retrieve relevant information and answer specific doubts the student types in. This introduces a different kind of AI pattern: retrieval-augmented generation, simplified for a frontend app.

Make sure your Session 5 evaluator is working before next session. Session 6 will build on the same running app.

---

# Instructor Notes

## What to Emphasize

Session 5 introduces two layered skills:

1. Building a structured evaluation UI that integrates with existing app state from Session 4
2. Designing a rubric-based AI prompt that forces structured output

Students must understand both the product thinking (what does useful feedback look like?) and the prompt thinking (how do I instruct AI to produce it?).

Emphasize throughout:

- The rubric in the prompt is the core of this feature
- Structured output requires a structured prompt — you must tell AI exactly what sections to return
- AI scoring is guidance, not ground truth
- The feedback card design reflects the rubric structure — they must match

## Common Student Mistakes

1. Sending only the answer to AI without including the question in the evaluation prompt — this makes the evaluation context-free and useless
2. Not including the rubric criteria in the prompt and instead asking AI to "evaluate the answer and give feedback" — produces vague text, not a structured card
3. Not connecting the question dropdown to the actual Session 4 generated questions — building a separate static dropdown instead
4. Not handling the case when no questions exist from Session 4 (empty dropdown)
5. Displaying the full AI response text in one block instead of parsing it into five separate sections of the feedback card
6. Not adding a loading state and confusing students when Submit is clicked and nothing appears to happen for a few seconds
7. Adding voice input or timed mode because it "sounds cool" — this breaks scope and introduces complexity that cannot be completed in session
8. Not testing the empty answer submission case and assuming users will always type something
9. Treating the AI score as the only metric and not pairing it with the improved answer section — students need to see both the score and the better version
10. Not asking AI to be constructive in tone — AI can produce harsh feedback that discourages students if the tone is not specified in the prompt

## How to Control the Session

Use this rule:

If a feature requires voice, timing, or storing full answer history to a database, it is out of scope for Session 5. Redirect immediately.

The single focus of Session 5 is: question in, answer in, structured feedback card out.

## Setup Rule

Do not spend more than 5 minutes troubleshooting the Session 4 state integration during live class. If the questions dropdown is not loading from Session 4, use a manually typed test question to keep the class moving. Fix the integration after the main feature is working.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### Q1. What feature did you add in Session 5?

Expected answer:

In Session 5, I added the Mock Answer Evaluator feature to the AI Interview Prep Copilot. A student can select an interview question from the list generated in Session 4 or type a custom question, type their answer in a text area, and submit it for AI evaluation. The app returns a structured feedback card with a score out of 10, strengths in the answer, missing key points, an improved version of the answer, and one follow-up question.

### Q2. Who is the user of this feature?

Expected answer:

The user is a student or fresher who is actively preparing for interviews. They have already generated a list of likely questions in Session 4 and now want to practice answering those questions and understand where their answers are weak before the actual interview.

### Q3. What problem does the Mock Answer Evaluator solve?

Expected answer:

Most students practice answering interview questions but have no way to know if their answers are good or what is missing. The Mock Answer Evaluator gives them structured, specific feedback — not just a vague judgment. It tells them their score, what they did well, what they missed, how a better answer would look, and what the interviewer might ask next.

### Q4. Why does the feedback card have five sections?

Expected answer:

Each section of the feedback card serves a different purpose. The score gives a quick overall judgment. The strengths tell the student what to keep in future answers. The missing key points tell them what to add. The improved answer shows them a better version to learn from. The follow-up question prepares them for the next level of probing. Together, these five sections make the feedback actionable rather than just informational.

### Q5. What is the difference between this feature and just asking AI to tell you if your answer was good?

Expected answer:

Asking AI to tell you if an answer is good produces a vague response with no structure. The Mock Answer Evaluator uses a rubric-based prompt that gives AI specific evaluation criteria and forces it to return a structured five-component feedback card. This makes the output consistent, parseable, and far more useful for improvement.

---

## App Flow Questions

### Q6. How does the question dropdown get populated?

Expected answer:

The question dropdown is populated from the app state that was set in Session 4 when the Interview Question Generator ran. The generated questions are already stored in the app's state. Session 5 reads that state and maps each question into the dropdown options. There is also a manual entry option for custom questions not in the generated list.

### Q7. What exactly happens when the student clicks Submit for Evaluation?

Expected answer:

When the student clicks Submit for Evaluation, the app first checks that both a question and an answer are present. If valid, it constructs a rubric-based prompt that combines the question, the student's answer, and specific scoring criteria. This prompt is sent to the AI API. While waiting, the app shows a loading state. When the response arrives, it is parsed into five components and displayed as the feedback card.

### Q8. How does the app parse the AI response into five sections?

Expected answer:

The rubric prompt instructs AI to return the response in a specific structure — for example, with clear labeled sections for Score, Strengths, Missing Key Points, Improved Answer, and Follow-Up Question. The app then parses the returned text by looking for these labels or by requesting JSON format output. Each labeled section is mapped to the corresponding part of the feedback card UI.

### Q9. What happens if the student submits an empty answer?

Expected answer:

The app validates the input before sending it to AI. If the answer text area is empty, the app shows a validation error message telling the student to type an answer before submitting. The API call is not made. This prevents unnecessary API usage and gives the user clear guidance.

### Q10. What happens if no questions were generated in Session 4?

Expected answer:

If the Session 4 question generator was not run or no questions are in app state, the dropdown will be empty. The app should detect this and display a message telling the student to go to the Question Generator section first. The student can still use the manual entry option to type a custom question and proceed with evaluation.

---

## AI Topic Questions

### Q11. What is rubric-based evaluation in the context of AI prompting?

Expected answer:

Rubric-based evaluation means giving AI a specific set of criteria to score against, rather than asking for a general opinion. In the Mock Answer Evaluator, instead of asking AI "Was this answer good?", the prompt says: evaluate this answer on correctness, clarity, depth, use of examples, and completeness. Return a score for each, a total score out of 10, what was done well, what was missing, a better version, and a follow-up question. This forces the AI to produce structured, comparable, and actionable feedback.

### Q12. Why does the prompt structure matter so much for evaluation features?

Expected answer:

The quality of AI evaluation is entirely determined by the quality of the prompt. If the prompt is vague, the feedback is vague. If the prompt specifies what to score, how to score it, what format to return, and what tone to use, the output is structured and consistent. In the Mock Answer Evaluator, the prompt is the rubric. Without it, AI has no standard to evaluate against, and students get impressions rather than feedback.

### Q13. What are the limitations of AI scoring for interview answers?

Expected answer:

AI scoring has several important limitations. AI can be overly generous with scores, especially for fluent but shallow answers. It may not recognize domain-specific nuances or recent industry changes. It can reward confident language over technical accuracy. It may penalize unconventional but valid approaches. For these reasons, students should treat AI scores as guidance and always read the improved answer section rather than relying on the number alone.

### Q14. How would you explain the design of the rubric prompt in a technical interview?

Expected answer:

I would explain that the rubric prompt is a structured instruction sent to the AI that defines the evaluation standard. It includes the question being evaluated, the student's answer, and a list of scoring criteria with their weights. The prompt also specifies the output format — typically JSON or labeled sections — so the app can parse and display each component separately. This design separates the rubric logic from the rendering logic, making both easier to update independently.

### Q15. How is rubric-based AI evaluation used in real-world applications?

Expected answer:

Rubric-based AI evaluation is used in many real-world products. Hiring platforms use it to screen candidate responses at scale. EdTech companies use it to give feedback on student writing and coding answers. Customer support tools use it to score agent responses against quality standards. Legal and compliance tools use it to evaluate whether documents meet specific criteria. In all these cases, the AI is not making an intuitive judgment — it is following a structured rubric provided in the prompt, which makes the evaluation consistent, auditable, and improvable.

---

# Session 5 Completion Checklist

Students should complete the following by the end of the session:

- [ ] Question dropdown is present and populated from Session 4 generated questions
- [ ] Manual/custom question entry option works alongside the dropdown
- [ ] Answer text area is present and accepts student input
- [ ] Submit for Evaluation button is connected to the evaluation function
- [ ] Loading state appears while AI processes the evaluation
- [ ] Feedback card displays score out of 10
- [ ] Feedback card displays strengths section
- [ ] Feedback card displays missing key points section
- [ ] Feedback card displays improved answer version
- [ ] Feedback card displays one follow-up question
- [ ] Empty answer submission is handled with a validation message
- [ ] Student can explain what a rubric-based prompt is in plain language

---

# Instructor Backup Plan

If the AI tool generation fails or integration with Session 4 state is taking too long:

1. Instructor continues live build on screen.
2. For the dropdown, use a hardcoded array of sample questions as a temporary replacement for Session 4 state — this unblocks the class immediately.
3. Students follow conceptually and note which parts they need to complete after class.
4. Share the final Session 5 code after the session.
5. Students use the prompts to regenerate or fix their own app after class.
6. Do not sacrifice the concept pause and interview explanation section. Even if the build is incomplete, every student must be able to explain rubric-based evaluation.
7. If the AI response is not parsing into five sections cleanly, switch to Prompt 6 (structured JSON output prompt) which forces a JSON schema return — this is easier to parse reliably.

## Gemini API Troubleshooting

If AI calls fail during the session:

- Check that the student's `.env` file is in the project root (same folder as `package.json`) and contains `VITE_GEMINI_API_KEY=...` with a valid key
- The dev server must be restarted after adding or changing the `.env` file — `npm run dev` again
- Confirm the import is correct: `import { GoogleGenerativeAI } from "@google/generative-ai"`
- Confirm the key is read as: `import.meta.env.VITE_GEMINI_API_KEY` (VITE_ prefix required for Vite to expose it to the browser)
- Free tier rate limit is 15 RPM — if a student hits the rate limit, wait 1 minute and try again; this is sufficient for classroom use
- Get a free key at: aistudio.google.com (no credit card required)
