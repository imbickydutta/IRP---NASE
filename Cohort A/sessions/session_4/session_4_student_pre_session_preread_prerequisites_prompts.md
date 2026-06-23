# Session 4 Student Pre-Session File: Add Interview Question Generator

## What We Are Building

In this 8-session interview-prep phase, we are building one continuous project:

# AI Interview Prep Copilot

This app helps a student prepare for interviews using AI.

By the end of all sessions, the app will be able to:

- store your interview profile
- analyze job descriptions
- compare your profile with the JD
- generate interview questions
- evaluate your mock answers
- answer doubts using RAG-lite
- create a 7-day interview prep plan

## What We Have Built So Far

Before Session 4, the app already has:

- Session 1: Base Profile Dashboard — profile form, target role, skills, projects, weak areas, job description, localStorage persistence
- Session 2: JD Analyzer — structured extraction of required skills, role type, responsibilities, and interview topics from the JD
- Session 3 — Add Profile vs JD Match: match band (strong/moderate/weak), missing skills list, and risk areas identified by comparing profile to JD analysis

## Session 4 Goal

In Session 4, we will add the Interview Question Generator.

This feature reads the JD analysis, student profile, and match report that are already stored in app state — and uses all three to generate a targeted set of 12 interview questions.

## Session 4 Output

By the end of Session 4, the app will:

- read JD analysis from app state (Session 2 output)
- read student profile from app state (Session 1 data)
- read match report from app state (Session 3 output)
- build a combined context prompt from all three sources
- generate 5 technical questions
- generate 3 project-based questions
- generate 2 HR questions
- generate 2 scenario-based questions
- display all 12 questions in labelled, collapsible sections
- provide a copy button for each category
- store the questions in app state so Session 5 can use them

---

# Pre-Read

## Why Are We Building This Feature?

In interviews, an interviewer does not ask random questions. They ask questions based on the job role, your skills, and your gaps. If you walk into an interview with only generic preparation, you are not ready.

This feature solves that. Instead of asking you to guess which questions might come up, it reads everything the app already knows about you — your profile, your JD, your match gaps — and generates questions tailored specifically to your situation.

This is also why Sessions 1, 2, and 3 mattered. Without the JD analysis and the match report, this feature would have no useful context to work from.

You should be able to explain:

- what problem this feature solves
- where the input data comes from
- what prompt chaining means
- how the questions are categorized
- why context-aware questions are better than generic ones
- how AI was used and what you tested

## Simple App Flow

Session 1: User enters profile → App saves profile to localStorage
↓
Session 2: User enters JD → App extracts skills, role type, topics → Saved to app state
↓
Session 3: App compares profile vs JD → Match band, missing skills, risk areas → Saved to app state
↓
Session 4: App reads all three → Builds chained context prompt → AI generates 12 targeted questions → Questions saved to app state
↓
Session 5 — Add Mock Answer Evaluator: App reads questions → User answers → AI evaluates answers

## Key Concepts to Revise

Before the session, revise these ideas:

- What is app state and why is it different from localStorage?
- What is a prompt in the context of AI?
- What does it mean to pass context to an AI model?
- What is a structured AI output (JSON categories)?
- What is prompt chaining?
- What does "context-aware generation" mean?
- What is a collapsible UI section?
- Why do apps accumulate state across features rather than re-asking the user each time?

## Simple Explanation

Prompt chaining means using the output of one AI step as the input for the next.

In this app, by Session 4 we have already computed two AI outputs: the JD analysis and the match report. Instead of asking the user to fill in all that information again, the question generator reads it from app state and adds it to the prompt automatically.

This is how real AI products work. Each feature builds on what the previous feature produced. The more context the app accumulates, the more personalized the AI output becomes.

Think of it like briefing a colleague. If you give them no information, they give you generic advice. If you give them your resume, the JD, and your skill gaps — they give you exactly the preparation you need.

---

# Prerequisites Before Session

## Mandatory Setup

Complete this before the live session:

1. Your Session 1, 2, and 3 app must be working
2. Your profile must be saved (Session 1)
3. Your JD Analyzer must have run and produced output (Session 2)
4. Your Profile vs JD Match must have run and produced a match report (Session 3)
5. Open your existing app in your AI coding tool (Antigravity or equivalent)
6. Have your profile data and JD text ready for testing
7. Keep this file open during the session
8. Keep a stable internet connection
9. Keep Chrome or your default browser open for testing

## Optional Setup

Useful but not mandatory:

- a second browser tab with your existing app open for comparison
- your Session 3 notes or output screenshot
- a notepad for writing down your 2–3 line concept explanation during the concept pause

## Important Rule

Do not try to rebuild Sessions 1, 2, or 3 during this session.

If your prior sessions are incomplete or missing data, tell your instructor before the session starts so they can give you a sample state object to use.

---

# Content to Prepare Before Class

Prepare this in a text file before class so you can paste it into prompts quickly.

```text
My Profile (from Session 1):
Full Name:
Target Role:
Current Skills:
Project Details:
Weak Areas:
Job Description:

JD Analysis Output (from Session 2):
Required Skills:
Role Type:
Key Responsibilities:
Important Interview Topics:

Match Report Output (from Session 3):
Match Band (Strong / Moderate / Weak):
Missing Skills:
Risk Areas:
```

## Sample Data for Session 4

```text
My Profile (from Session 1):
Full Name: Aarav Sharma
Target Role: Junior AI Engineer
Current Skills: Prompt engineering, React basics, HTML, CSS, localStorage, basic JavaScript, API calls, no-code tools, RAG basics
Project Details: Built an AI Interview Prep Copilot with features including profile dashboard, JD analyzer, and profile vs JD match using AI-assisted development tools.
Weak Areas: Backend development, system design, database concepts, debugging complex JavaScript, confidence in live coding

Job Description:
We are hiring a Junior AI Engineer who can build AI-powered web applications. The candidate should understand LLMs, prompt engineering, API integration, React, data handling, debugging, and product thinking. Experience with AI tools, automation, and rapid prototyping is a strong advantage.

JD Analysis Output (from Session 2):
Required Skills: LLMs, prompt engineering, React, API integration, data handling, debugging, product thinking, automation, rapid prototyping
Role Type: Junior AI Engineer — frontend-heavy with AI integration
Key Responsibilities: Build and maintain AI-powered web features, integrate LLM APIs, debug AI-generated code, collaborate on product design
Important Interview Topics: LLM fundamentals, prompt design, React state management, API calls, debugging strategies, product trade-offs

Match Report Output (from Session 3):
Match Band: Moderate
Missing Skills: Backend development, system design, complex debugging
Risk Areas: System design questions, backend API questions, database-related questions
```

---

# Prompts for Session 4

Use these prompts during the session when instructed.

---

## Prompt 1: Main Build Prompt

```text
I am building an AI Interview Prep Copilot. This is a web app that helps students prepare for interviews using AI features.

Here is what has already been built in the app:

Session 1 — Base Profile Dashboard:
- Student profile form with fields: Full Name, Target Role, Current Skills, Project Details, Weak Areas, Job Description
- Save Profile button with validation
- Profile summary display
- localStorage persistence for the profile data

Session 2 — JD Analyzer:
- Takes the saved Job Description from the profile
- Calls AI to extract: Required Skills, Role Type, Key Responsibilities, Important Interview Topics
- Displays the analysis in a structured format
- Saves the JD analysis output to app state

Session 3 — Profile vs JD Match:
- Reads the student profile and JD analysis from app state
- Calls AI to compare them
- Outputs: Match Band (Strong / Moderate / Weak), Missing Skills list, Risk Areas list
- Displays the match report in a card format
- Saves the match report to app state

Now add Session 4 — Interview Question Generator:

Feature behavior:
1. Read the following from app state (do NOT ask the user to re-enter any data):
   - Student profile: Full Name, Target Role, Current Skills, Project Details, Weak Areas
   - JD analysis: Required Skills, Role Type, Important Interview Topics
   - Match report: Match Band, Missing Skills list, Risk Areas list
2. Build a chained context prompt that combines all three data sources into a single structured prompt
3. Call AI with this chained prompt and ask it to generate:
   - 5 technical questions (based on required skills and role type)
   - 3 project-based questions (based on the student's listed projects)
   - 2 HR questions (based on target role and profile)
   - 2 scenario-based questions (based on risk areas and missing skills)
4. Parse the AI response and display questions in four clearly labelled collapsible sections:
   - Technical Questions (5)
   - Project-Based Questions (3)
   - HR Questions (2)
   - Scenario-Based Questions (2)
5. Add a copy button for each section that copies all questions in that category to clipboard
6. Add a Regenerate Questions button that calls AI again with the same context
7. Show a loading state while the AI call is running
8. Show a context summary above the questions: "Generated for: [Target Role] | Match: [Match Band] | Gaps: [count] missing skills"
9. Store the generated questions in app state as an object with four keys: technical, projectBased, hr, scenarioBased

Do NOT add:
- Answer evaluation or scoring (that is Session 5)
- Voice input or output
- External question bank or database
- Timed interview mode
- Difficulty levels or filters

Add clear comments in the code explaining:
- where the context data is read from app state
- how the chained prompt is assembled
- where the AI call is made
- how the response is parsed into four categories
- where the questions are stored in app state

Keep the UI clean and consistent with the existing app style.
```

---

## Prompt 2: UI Improvement Prompt

```text
Improve the UI of the Interview Question Generator in the AI Interview Prep Copilot.

Keep the same functionality and do not change any logic.

Improvements to make:
1. Add a clear section heading: "Your Personalized Interview Questions"
2. Add a context banner above the questions showing:
   "Generated for: [Target Role] | Match: [Match Band] | [n] missing skills identified"
3. Make each collapsible section header bold and use a clear icon or indicator for open/closed state
4. Add the question count in the section header, e.g., "Technical Questions (5)"
5. Style each question as a numbered list inside the collapsed section
6. Change the copy button to show "Copy Questions" and briefly show "Copied!" after clicking
7. Make the Regenerate button clearly visible and labeled "Regenerate Questions"
8. Add a subtle divider between sections
9. If questions have not been generated yet, show a prompt message: "Click Generate Questions to get your personalized set."
10. Keep the design responsive and consistent with the rest of the app.

Do not change any state management, AI call logic, or data handling.
```

---

## Prompt 3: Debugging Prompt — Questions Are Generic and Not Personalized

```text
The Interview Question Generator is producing generic questions that do not reference my specific profile, job description, or skill gaps.

Expected behavior:
1. Technical questions should reference the specific required skills from my JD analysis.
2. Project-based questions should reference my actual project details from my profile.
3. HR questions should reference my target role specifically.
4. Scenario-based questions should reference my risk areas and missing skills from the match report.

The issue is likely one of the following:
- The context from app state is not being read correctly before the AI call
- The chained prompt is not including the profile, JD analysis, or match report data
- The prompt is too generic and not specifying which data to use for each question category

Please:
1. Check how the context data is read from app state before the AI call
2. Show me the assembled prompt string before it is sent to AI
3. Fix the prompt assembly so it includes: student name, target role, skills, projects, required skills from JD, role type, match band, missing skills, and risk areas
4. Confirm the fix by showing the updated prompt and explaining what changed
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the Interview Question Generator code in beginner-friendly language.

Focus on:
1. Where does the app read the JD analysis from app state?
2. Where does the app read the match report from app state?
3. How is the combined context prompt assembled?
4. Where is the AI call made and what does it receive?
5. How is the AI response parsed into four separate categories?
6. How do the collapsible sections work?
7. How does the copy button work?
8. Where are the generated questions stored in app state?
9. What happens if the match report or JD analysis is not available?
10. Which parts should I explain during a technical interview?

Do not rewrite the code. Only explain it clearly.
```

---

## Prompt 5: Interview Explanation Prompt

```text
Explain the Interview Question Generator feature of my AI Interview Prep Copilot as if I am preparing for a job interview.

Use this structure:
1. What problem does this feature solve?
2. Where does the input data come from?
3. What is prompt chaining and how does this feature use it?
4. How are the questions categorized and why?
5. Why are these questions better than generic interview questions?
6. What did I use AI for in building this feature?
7. What edge cases does this feature handle?
8. What does this feature pass to Session 5?
9. What are the current limitations?
10. What would I improve with more time?

Keep the explanation clear, confident, and interview-ready.
```

---

## Prompt 6: Structured JSON Output Prompt

```text
Update the Interview Question Generator to request a structured JSON response from AI instead of plain text.

The AI response should follow this exact JSON schema:

{
  "technical": [
    "Question 1",
    "Question 2",
    "Question 3",
    "Question 4",
    "Question 5"
  ],
  "projectBased": [
    "Question 1",
    "Question 2",
    "Question 3"
  ],
  "hr": [
    "Question 1",
    "Question 2"
  ],
  "scenarioBased": [
    "Question 1",
    "Question 2"
  ]
}

Changes needed:
1. Update the AI prompt to explicitly ask for a JSON response with the above schema
2. Parse the JSON response after the AI call
3. Use the parsed object to populate each collapsible section
4. Add error handling in case the JSON is malformed or incomplete
5. Store the parsed JSON object in app state as the questions data

Add a comment explaining why JSON parsing is used instead of plain text parsing.
```

---

## Prompt 7: Error and Empty State Prompt

```text
Add proper error and empty states to the Interview Question Generator feature.

Handle the following cases:

1. No profile saved:
   Show message: "Please complete your profile in the Profile section before generating questions."
   Add a button: "Go to Profile"

2. No JD analysis available:
   Show message: "Please run the JD Analyzer first so we can generate relevant technical questions."
   Add a button: "Go to JD Analyzer"

3. No match report available:
   Show message: "Please run the Profile vs JD Match first. The match report helps us target your weak areas."
   Add a button: "Go to Match Report"

4. AI call fails:
   Show message: "Question generation failed. This may be a temporary issue. Please try again."
   Add a Retry button that re-runs the AI call with the same context.

5. Partial context (profile exists but JD analysis is missing):
   Show a warning banner: "Generating with partial context. Run JD Analyzer for more targeted questions."
   Still allow generation to proceed.

6. Empty question category returned by AI:
   Show placeholder: "No questions generated for this category. Try regenerating."

Keep all existing functionality intact. Only add these state-handling cases.
```

---

# What You Should Be Able to Explain After Session 4

By the end of the session, you should be able to answer these questions on your own — without looking at notes:

1. What does the Interview Question Generator do?
2. Where does the input data come from — does the user re-enter anything?
3. What is prompt chaining and how does this feature use it?
4. What are the four question categories and how many questions are in each?
5. Why are context-aware questions more useful than generic questions?
6. What happens if the match report is not available when the user tries to generate questions?
7. Where are the generated questions stored, and why does that matter for Session 5?
8. How does the copy button work?
9. What did you use AI for and what did you verify yourself?
10. How would you explain this feature in one minute to a hiring manager?

## Final Session 4 Explanation

```text
In Session 4, I added an Interview Question Generator to the AI Interview Prep Copilot. The feature reads the student profile, JD analysis, and match report from app state — data that was already computed in Sessions 1, 2, and 3 — and combines them into a single context-rich prompt. This is called prompt chaining: using one feature's output as the next feature's input. The AI generates 12 targeted questions across four categories — technical, project-based, HR, and scenario-based — that are specific to the student's profile and job description, not generic. The questions are displayed in collapsible sections with a copy option and stored in app state for the Session 5 answer evaluator.
```
