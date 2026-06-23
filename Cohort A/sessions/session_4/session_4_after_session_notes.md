# Session 4 After-Session Notes: Add Interview Question Generator

## What We Built Today

Today we added the Interview Question Generator to the AI Interview Prep Copilot.

The feature:

- reads the student profile from Session 1 (name, role, skills, projects, weak areas)
- reads the JD analysis from Session 2 (required skills, role type, topics)
- reads the match report from Session 3 (match band, missing skills, risk areas)
- combines all three into a single chained context prompt
- generates 5 technical questions, 3 project-based questions, 2 HR questions, and 2 scenario-based questions
- displays all 12 questions in labelled collapsible sections with a copy button
- stores the questions in app state for use in Session 5

---

# Why This Feature Matters

Before this feature, the app had collected and analyzed data but had not done anything actionable with it.

The Interview Question Generator is the first feature that puts all of that context to work. It does not ask the user for anything new. It takes what was already computed and turns it into something directly useful: a personalized set of interview questions.

This is the difference between an app that stores data and an app that uses data intelligently.

For the student, the value is immediate — instead of browsing generic question lists, they receive questions that are specific to their target role, their skills, their projects, and their gaps. These are questions they actually need to prepare for.

For the interview, this feature demonstrates that the student understands how AI can be given rich context to produce targeted output — not just a single isolated call.

---

# App Flow

The complete flow across all sessions so far:

Session 1: User enters profile → App validates and saves to localStorage
↓
Session 2: User triggers JD Analyzer → App extracts skills, role type, topics → JD analysis saved to app state
↓
Session 3 — Add Profile vs JD Match: User triggers Profile vs JD Match → App compares profile and JD analysis → Match band, missing skills, risk areas saved to app state
↓
Session 4: User triggers Question Generator → App reads profile + JD analysis + match report → Builds chained context prompt → AI generates 12 targeted questions → Questions displayed in 4 collapsible sections → Questions stored in app state
↓
Session 5 — Add Mock Answer Evaluator (next): User reads a question and types an answer → App evaluates the answer using AI → Score, feedback, and improvement tips displayed

---

# What is Prompt Chaining?

Prompt chaining is a technique where the output of one AI interaction is used as the input for the next.

In most basic AI use, each prompt is independent. You ask AI something, you get an answer, and then the next question starts fresh. Prompt chaining is different. It means you deliberately carry forward the results of earlier steps so that each new AI call has more context to work with.

In this app, we applied prompt chaining across sessions. The JD analyzer in Session 2 produced structured output: required skills, role type, and interview topics. The match report in Session 3 produced more structured output: match band, missing skills, and risk areas. In Session 4, the question generator did not repeat that analysis. Instead, it read those already-processed outputs from app state and combined them with the student profile into a single context block before making the AI call.

This means by the time AI generates questions, it already knows the student's name, role, skills, projects, and weak areas; it knows what the JD requires; and it knows where the student falls short. The result is questions that are actually relevant to this specific student and this specific role — not a generic list that any random candidate might receive.

This is how professional AI products are designed. Context is not thrown away after each feature. It accumulates. Each step makes the next step smarter.

---

# What Students Should Understand

1. The question generator does not ask the user to re-enter any data — it reads everything from app state
2. Prompt chaining means using one feature's output as the next feature's input, accumulating context across the app
3. The chained context prompt is assembled from three data sources: profile, JD analysis, and match report
4. The 12 questions are split across four categories for a reason — technical, project-based, HR, and scenario-based questions test different things
5. Context-aware questions are more useful than generic questions because they target the student's actual gaps and experience
6. The loading state is important — AI calls take time and the app must not appear frozen
7. The generated questions are stored in app state so Session 5 can use them without regenerating
8. The edge case where match report is missing must be handled with a helpful message, not a crash
9. The copy button uses the browser's clipboard API — a standard web API students should be able to explain
10. The regenerate button allows a fresh call with the same context — useful when the first set of questions is not satisfactory

---

# Interview-Ready Explanation

```text
In Session 4, I added an Interview Question Generator to my AI Interview Prep Copilot. The feature reads the student profile, JD analysis, and match report that were already stored in app state from earlier sessions, and combines them into a single chained context prompt. This is called prompt chaining — using one feature's output as the next feature's input. The AI generates 12 targeted questions across four categories: 5 technical, 3 project-based, 2 HR, and 2 scenario-based. The questions are specific to this student's role, skills, and gaps — not generic. They are displayed in collapsible sections with a copy option and stored in app state for the Session 5 answer evaluator.
```

---

# What Happens When the User Clicks Generate Questions?

```text
When the user clicks Generate Questions, the app first checks whether the required data is available in app state — specifically the student profile, JD analysis, and match report. If any of these are missing, it shows a helpful message directing the user to the incomplete step. If all data is present, the app assembles a chained context prompt by combining the student's name, role, skills, projects, weak areas, the JD's required skills and role type, and the match report's band, missing skills, and risk areas into a single structured prompt. It sends this prompt to AI with instructions to return 12 questions across four labelled categories. While the AI call is running, a loading state is shown. Once the response arrives, it is parsed into four categories and displayed in collapsible sections. The questions are also saved to app state so the Session 5 evaluator can access them.
```

---

# What AI Was Used For

AI was used to help generate:

- the combined context prompt structure
- the question generation logic
- parsing the AI response into four categories
- collapsible section components
- copy button with clipboard logic
- loading and empty state handling
- storing questions in app state

But students still need to:

- verify that the generated questions actually reference the JD and profile data
- check that all four categories appear with correct counts
- test the copy button in each category
- test the edge case where match report is missing
- confirm that questions are stored in app state after generation
- test the regenerate button
- understand the assembled prompt string and be able to explain it
- explain prompt chaining in their own words without reading notes

---

# Common Issues and Fixes

## Issue 1: Questions are generic and do not mention specific skills or projects

Possible reasons:

- the context data is not being read from app state before the AI call
- the chained prompt is assembled without including the profile, JD analysis, or match report values
- the AI call is being made with a minimal prompt instead of the full context block

What to ask AI:

```text
The generated questions are generic and do not reference my specific JD or profile. Please check how the context prompt is assembled before the AI call. Show me the final prompt string that is sent to AI. Ensure it includes the student's target role, current skills, project details, required skills from JD analysis, role type, match band, missing skills, and risk areas. Fix the context assembly and explain what was missing.
```

## Issue 2: Questions are not separated into four categories

Possible reasons:

- the AI response is not being parsed by category
- the prompt does not clearly instruct AI to label questions by type
- the response format is plain text instead of structured JSON

What to ask AI:

```text
The question generator is returning all questions in one block without separating them into Technical, Project-Based, HR, and Scenario-Based categories. Please update the AI prompt to explicitly request responses in JSON format with keys: technical (5 questions), projectBased (3 questions), hr (2 questions), scenarioBased (2 questions). Update the parsing logic to read from the JSON keys and display each category in its own collapsible section.
```

## Issue 3: Generated questions are lost after page refresh

Possible reasons:

- questions are stored in local component state but not in app state or localStorage
- app state is reset on refresh because it is not backed by localStorage

What to ask AI:

```text
The generated questions disappear when I refresh the page. Please update the question generator to save the generated questions to localStorage in addition to app state. When the app loads, check localStorage for saved questions and restore them to app state if they exist. The questions should persist across page refreshes so the Session 5 evaluator can access them even after a refresh.
```

---

# Key Takeaways

1. Prompt chaining is not a theory — it is what we built today. Each feature's output becomes the next feature's input, and by Session 4 the app has enough accumulated context to generate truly personalized interview questions.

2. Context-aware AI output is always more useful than generic AI output. When you give AI specific, structured context — the student's profile, the JD analysis, the match gaps — the generated questions are meaningfully different from anything a generic question list could provide.

3. Storing outputs in app state is a design decision, not just a technical one. The reason we store questions in app state today is so Session 5 can use them tomorrow. Every feature should think about what it produces and who uses it next.

4. Interviews will test whether you understand what you built, not just whether you built it. You should be able to explain prompt chaining, describe the assembled context prompt, state the four question categories, and walk through what happens at each step — without reading notes.

---

# Session 5 Preview — Add Mock Answer Evaluator

In Session 5, we will add the Mock Answer Evaluator.

The user will select one of the generated questions from Session 4, type their answer, and the app will evaluate it using AI.

The evaluator will return:

- a score
- what was good about the answer
- what was missing or unclear
- a suggested improvement

Main AI concept:

Evaluation prompting — structuring a prompt to make AI act as an evaluator and return a scored, structured critique instead of a generative response.

Session 5 will use the questions stored in app state today.

The key shift in Session 5 is the direction of the AI interaction. In Sessions 2, 3, and 4, AI generated output for the user. In Session 5, AI evaluates output from the user. That is a different prompt design and a different kind of context — and it builds directly on everything the app has accumulated so far.

Before Session 5, make sure:

- your profile is saved (Session 1)
- your JD analysis has run (Session 2)
- your match report has run (Session 3)
- your questions have been generated and are stored in app state (Session 4)

All four of these are required for Session 5 to work correctly.
