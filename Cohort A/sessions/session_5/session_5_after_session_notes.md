# Session 5 After-Session Notes: Add Mock Answer Evaluator

## What We Built Today

Today we added the Mock Answer Evaluator feature to the AI Interview Prep Copilot.

The feature allows a student to:

- select an interview question from the Session 4 generated list via a dropdown
- type a custom question manually if needed
- type their answer in a text area
- submit the answer for AI evaluation
- receive a structured feedback card

The feedback card includes:

- Score out of 10
- Strengths in the answer
- Missing Key Points
- Improved Answer version
- One Follow-Up Question

The key AI concept introduced today was rubric-based prompting: designing a prompt that gives AI specific evaluation criteria and forces structured output rather than a vague opinion.

---

# Why This Feature Matters

Before this feature, a student using the app could see the job description analysis, understand the skill gap, and review a list of likely questions. But they had no way to practice and get feedback.

The Mock Answer Evaluator closes that loop.

It gives students a structured mirror. They can type an answer they would give in a real interview, see how it is scored against specific criteria, understand exactly what they are missing, read a better version, and prepare for the follow-up question.

This is a meaningful product decision. Every feature in this app was added because it solves a specific problem in the interview preparation journey. The evaluator solves the feedback gap.

It also demonstrates one of the most important AI design patterns — rubric-based evaluation — which appears in hiring tools, EdTech platforms, compliance systems, and customer support quality scoring tools across the industry.

---

# App Flow

The complete app flow through Session 5 is:

User enters full profile (name, target role, skills, projects, weak areas, job description)  
↓  
App saves profile to localStorage  
↓  
JD Analyzer reads the job description and extracts required skills, responsibilities, role type, and interview topics  
↓  
Profile vs JD Match compares the student profile with the JD analysis and generates a gap report with match score  
↓  
Interview Question Generator uses the profile and JD context to generate categorized questions and stores them in app state  
↓  
Student opens Mock Answer Evaluator and selects a question from the dropdown (or types a custom question)  
↓  
Student types their answer in the text area  
↓  
Student clicks Submit for Evaluation  
↓  
App validates that both question and answer are present  
↓  
App constructs a rubric-based evaluation prompt combining the question, the answer, and specific scoring criteria  
↓  
Prompt is sent to the AI API  
↓  
App shows loading state while waiting  
↓  
AI evaluates against the rubric and returns structured feedback  
↓  
App parses the response into five components  
↓  
Feedback card is displayed with score, strengths, missing points, improved answer, and follow-up question  
↓  
Student reads feedback, decides what to improve, and can try again

---

# What is Rubric-Based AI Evaluation?

Rubric-based evaluation is a way of instructing AI to judge something against a specific set of criteria, rather than asking for a general impression.

When you ask AI a vague question like "Was this answer good?", AI will give you a general response. It might say "Your answer was decent but could be more detailed." That is not very useful because it does not tell you what specifically was missing or how to fix it.

A rubric changes this entirely. A rubric defines what to evaluate and how much weight each criterion carries. For example, a rubric for interview answer evaluation might say: score on correctness out of 3 points, clarity out of 2 points, depth out of 2 points, use of examples out of 2 points, and professional terminology out of 1 point. Now AI has a clear standard to apply. The output becomes comparable across different answers, structured enough to parse, and specific enough to act on.

In the Mock Answer Evaluator, the rubric is embedded directly in the prompt. The prompt tells AI the question, the candidate's answer, the rubric criteria, and the exact output format — score, strengths, missing key points, improved answer, and follow-up question. AI follows these instructions and returns a structured evaluation. The app then parses that structured output and renders each component in its own section of the feedback card. The rubric in the prompt is the entire evaluation standard. If you change the rubric, the evaluation changes.

---

# What Students Should Understand

1. Rubric-based prompting means giving AI specific evaluation criteria rather than asking for a vague opinion
2. The five-component feedback card (score, strengths, missing points, improved answer, follow-up question) was designed to make feedback actionable, not just informational
3. The question dropdown is populated from Session 4 — Add Interview Question Generator (generated questions available in app state) — this is how sessions in the same app share data
4. The evaluation prompt must include both the question and the answer — without the question, AI has no context to evaluate against
5. Structured output from AI (JSON or labeled sections) is more reliable than raw text when the app needs to display different parts separately
6. AI scoring is guidance, not ground truth — AI can be too generous, miss domain nuances, or reward fluency over accuracy
7. The loading state is not cosmetic — it prevents users from clicking Submit again and making duplicate API calls
8. Empty state handling matters: if no questions exist from Session 4, the app should guide the user rather than showing a broken or empty dropdown
9. The rubric can be improved: adding the student's target role or the question difficulty level makes the evaluation more context-aware
10. This pattern — rubric prompt, structured output, parsed feedback card — is used in real-world products including hiring tools, EdTech platforms, and compliance evaluation systems

---

# Interview-Ready Explanation

```text
In Session 5, I added the Mock Answer Evaluator to the AI Interview Prep Copilot. A student selects an interview question from the generated list or types a custom question, types their answer, and submits it for evaluation. The app sends a rubric-based prompt to AI that defines specific scoring criteria and forces a structured response. The feedback card displays a score out of 10, strengths, missing key points, an improved answer version, and one follow-up question — turning AI evaluation from a vague impression into actionable, structured feedback.
```

---

# What Happens When Submit for Evaluation is Clicked?

```text
When the student clicks Submit for Evaluation, the app first validates that both a question and an answer are present. If either is missing, it shows a validation error message and does not make the API call. If both are present, the app constructs a rubric-based evaluation prompt that includes the question, the student's answer, and specific scoring criteria with their weights. This prompt is sent to the AI API. While waiting for the response, the app shows a loading state and disables the Submit button. When the AI response arrives, the app parses it into five components — score, strengths, missing key points, improved answer, and follow-up question — and renders each in its own labeled section inside the feedback card.
```

---

# What AI Was Used For

AI was used to help:

- construct the rubric-based evaluation prompt
- evaluate the student's answer against the rubric criteria
- generate the strengths analysis
- identify missing key points
- write an improved version of the student's answer
- generate a contextually relevant follow-up question
- generate the overall app code structure for the evaluator feature

But students still need to:

- design the rubric criteria in the prompt (what to score and how much weight each criterion gets)
- test whether the feedback card is displaying all five components correctly
- verify that the dropdown is correctly connected to Session 4's question state
- check that validation and error states work as expected
- understand the generated code well enough to explain it in an interview
- decide whether the AI feedback is valid or if the rubric needs improvement
- explain the difference between rubric-based evaluation and general AI feedback in plain language

---

# Common Issues and Fixes

## Issue 1: Feedback card shows raw text instead of five separate sections

Possible reason:

- the AI response is being displayed as-is without parsing
- the parsing logic is looking for the wrong labels or format
- the prompt did not clearly specify the output format

What to ask AI:

```text
The Mock Answer Evaluator is displaying the AI response as raw text instead of five separate sections. Please update the parsing logic to split the response into: Score, Strengths, Missing Key Points, Improved Answer, and Follow-Up Question. Also update the evaluation prompt to make the output format more explicit so it is easier to parse. Optionally, switch to JSON output format for more reliable parsing.
```

## Issue 2: Question dropdown is empty even though Session 4 generated questions

Possible reason:

- the questions array from Session 4 state is not being passed to the evaluator component
- the evaluator component is reading from a different state variable name
- the Session 4 questions were stored in local component state and are not accessible at the app level

What to ask AI:

```text
The question dropdown in the Mock Answer Evaluator is empty. Session 4 generated interview questions are stored in app state. Please check how the questions are stored in Session 4 and update the evaluator component to read from the same state. If the questions are only in local component state, lift the state to the app level so both the Question Generator and the Answer Evaluator can access it.
```

## Issue 3: AI returns a score outside the 0–10 range or returns no score at all

Possible reason:

- the prompt did not clearly specify the scoring scale
- AI interpreted the rubric differently and returned a percentage or letter grade instead
- the score is present in the response but the parsing logic is not extracting it correctly

What to ask AI:

```text
The evaluation is returning a score that is not in the expected 0 to 10 format, or the score is not being displayed in the feedback card. Please update the rubric prompt to explicitly state: "Return a single integer score between 0 and 10." Also update the parsing logic to extract the score correctly from the response and display it in the score section of the feedback card.
```

---

# Key Takeaways

1. Rubric-based prompting is more powerful than general feedback prompting. When you tell AI exactly what to score, how to score it, and what format to return, the output becomes structured, consistent, and parseable. The quality of your evaluation is determined entirely by the quality of your rubric prompt.

2. AI scoring is guidance, not truth. AI can score too generously, miss domain-specific nuances, and reward fluency over accuracy. Students should use the score as a starting point and always read the improved answer section to understand what a genuinely strong answer looks like.

3. Structured output design matters. The five-component feedback card was not an arbitrary choice. Each section was included because it serves a specific purpose: the score gives a quick judgment, strengths tell the student what to keep, missing points tell them what to add, the improved answer shows them a better version, and the follow-up question prepares them for deeper probing. When you design an AI-powered feature, the output structure is as important as the input prompt.

4. App state continuity across sessions is a real engineering decision. The fact that Session 5 reads questions generated in Session 4 means we had to think about where that data lives and how components share it. This is a practical lesson in state management that applies directly to real-world applications.

---

# Session 6 Preview

In Session 6 — Add RAG-Lite Doubt Solver — we will add:

Instead of generating fixed content, the app will let the student type a specific doubt or question, and the AI will retrieve relevant information and answer it.

This is a simplified version of Retrieval-Augmented Generation (RAG) — a technique where AI answers are grounded in specific source material rather than general knowledge.

Main AI concept for Session 6:

Retrieval-Augmented Generation (simplified) — how to use stored context (the student's profile, JD analysis, and session notes) as source material for AI to answer specific doubts more accurately than general knowledge alone.

Session 6 will build on top of the same running app. Make sure your Session 5 evaluator is working before the next session.
