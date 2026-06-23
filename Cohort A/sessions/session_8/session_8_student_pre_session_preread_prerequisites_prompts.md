# Session 8 Student Pre-Session File: Debug, Test, Polish, and Interview Demo

## Session Navigation

**Previous session:** Session 7 — Add AI Prep Plan Agent (complete app with all 7 features built)

**Next session:** None — this is the final session

## What We Are Building

Over 8 sessions, we are building one continuous project:

# AI Interview Prep Copilot

This app helps a student prepare for interviews using AI.

Here is everything the complete app can do:

- store your interview profile (Session 1)
- analyze job descriptions using AI (Session 2)
- compare your profile with the JD and show a match score (Session 3)
- generate interview questions based on your JD and role (Session 4)
- evaluate your mock answers and give structured feedback (Session 5)
- answer your prep doubts using your profile as context (Session 6)
- build a personalized day-by-day preparation plan (Session 7)
- handle errors, show loading states, and demo confidently (Session 8)

## Session 8 Goal

Session 8 does not add a new AI feature.

Instead, we make everything that was built in Sessions 1–7 work like a real, polished product.

We will:

- add loading states to every AI button
- add error messages when AI calls fail
- add empty input validation across all 7 forms
- add fallback text when AI returns no content
- write a project README
- build a manual test checklist for all 7 features
- write a 2-minute spoken demo script
- prepare for project viva questions

## Session 8 Output

By the end of Session 8, you should have:

1. A polished, error-handled version of the full AI Interview Prep Copilot
2. A project README file
3. A manual test checklist
4. A 2-minute spoken demo script
5. Practiced answers to likely viva questions

---

# Pre-Read

## Why Are We Building This?

In interviews, it is not enough to say:

"I built an AI-powered app."

You should be able to:

- open the app and demo it without it crashing
- explain what each feature does in plain language
- handle the case where the interviewer types something unexpected
- explain why you added loading states and error messages
- show a README that describes the project clearly
- walk through a 2-minute demo without reading your screen

Session 8 prepares you for all of that.

## Simple App Flow

User opens the app and fills their interview profile  
↓  
Profile is saved to localStorage (Session 1 — Base Profile Dashboard)  
↓  
User pastes a JD → AI extracts skills, topics, role type (Session 2 — JD Analyzer)  
↓  
App compares profile with JD → match score and gap report (Session 3 — Profile vs JD Match)  
↓  
App generates interview questions from JD and role (Session 4 — Question Generator)  
↓  
User types a mock answer → AI evaluates and gives feedback (Session 5 — Mock Answer Evaluator)  
↓  
User asks a doubt → AI answers using the profile as context (Session 6 — RAG-Lite Doubt Solver)  
↓  
AI builds a day-by-day prep plan from weak areas and available days (Session 7 — Prep Plan Agent)  
↓  
All buttons show loading states, all forms validate, all errors are handled (Session 8 — Polish)  
↓  
README, test checklist, and demo script are complete → App is portfolio-ready

## Key Concepts to Revise

Before Session 8, think about these ideas:

- What is a loading state? Why do apps show loading spinners?
- What is error handling? What should happen when an API call fails?
- What is input validation? Why do we prevent empty form submissions?
- What is a fallback? What should the UI show when AI returns no content?
- What is a README? What information does a good README include?
- What is a test checklist? How do you manually test a feature?
- What is a demo script? How long should a project demo be?
- What does "portfolio-ready" mean for a student project?

## Simple Explanation

A loading state is a temporary message or spinner that tells the user the app is working on something. Without it, the user does not know if the button click worked or if the app is frozen.

An error state is a message that appears when something goes wrong. For example, if the AI call fails because of a network issue, the app should show a message like "Could not generate questions. Please try again." Without this, the user sees a blank screen and does not know what happened.

Input validation is a check that runs before the app sends anything to AI. If the user clicks a button without filling in the required fields, the app should show a message like "Please enter a job description first" instead of sending an empty request to the AI and getting a confusing response.

Fallback text is what the app shows if AI returns an empty or very short response. Instead of showing nothing, the app shows a helpful message.

A README is a document that explains the project. It covers what the app does, what features it has, how to run it, and what technologies it uses. This is the first thing a recruiter reads when looking at your GitHub project.

---

# Prerequisites Before Session

## Mandatory Setup

Complete this before Session 8:

1. Your app from Session 7 should be open and working in Antigravity
2. All 7 features should be present in the app — profile, JD analyzer, match report, question generator, mock evaluator, doubt solver, prep plan
3. Test each feature once before the session to know which ones have bugs or missing states
4. Keep this pre-session file open during the session
5. Have your profile data filled and saved in the app
6. Have a sample JD pasted and saved in the JD analyzer

## Optional Setup

Useful but not mandatory:

- A GitHub account to push the final code
- A text editor like VS Code to review the generated code
- A notes document where you write your demo script and README
- A timer to practice your 2-minute demo

## Important Rule

Do not spend the live session setting up tools or rebuilding the app from scratch.

Session 8 assumes your Session 7 app is working. If it is not, inform the instructor before the session starts.

---

# Content to Prepare Before Class

Before Session 8, fill in this information in a text document. You will use it for your README, demo script, and viva answers.

```text
App Name:
AI Interview Prep Copilot

Your Name:

Target Role (from your profile):

List of all 7 features you built:
1.
2.
3.
4.
5.
6.
7.

One feature that is working well:

One feature that has a bug or missing state:

Technologies used (example: HTML, CSS, JavaScript, React, AI tool used):

How to run the app:

One sentence describing what the app does:
```

---

# Prompts for Session 8

Use these prompts during the session when instructed.

---

## Prompt 1: Code Review Prompt

Use this to ask AI to review your complete app for bugs, gaps, and missing states.

```text
You are a senior engineer reviewing a student project called AI Interview Prep Copilot.

The app has 7 features:
1. Base Profile Dashboard — collects name, target role, skills, project details, weak areas, and job description. Saves to localStorage.
2. JD Analyzer — takes a raw job description and extracts required skills, responsibilities, role type, and interview topics.
3. Profile vs JD Match — compares the saved student profile with the JD and returns a match score, aligned skills, and gaps.
4. Interview Question Generator — generates a list of likely interview questions based on the JD and target role.
5. Mock Answer Evaluator — takes a user's mock answer to a question and gives structured AI feedback.
6. RAG-Lite Doubt Solver — answers a student's specific prep doubt using the saved profile and JD as context.
7. AI Prep Plan Agent — generates a day-by-day preparation schedule based on weak areas, target role, and available days.

Please review the current code and identify:
1. Which AI call buttons are missing loading states?
2. Which forms are missing empty input validation?
3. Which AI calls are missing error state handling?
4. Which sections show a blank area if AI returns an empty response (missing fallback text)?
5. Any other obvious bugs or broken flows?

Return a checklist of issues found, not the fixed code yet.
```

---

## Prompt 2: Testing Checklist Prompt

Use this to generate a manual test checklist for all 7 features.

```text
Generate a manual test checklist for the AI Interview Prep Copilot app.

The app has 7 features:
1. Base Profile Dashboard (localStorage profile form)
2. JD Analyzer (AI extracts structured data from JD)
3. Profile vs JD Match (AI compares profile with JD)
4. Interview Question Generator (AI generates questions from JD and role)
5. Mock Answer Evaluator (AI evaluates a typed mock answer)
6. RAG-Lite Doubt Solver (AI answers a typed doubt using profile context)
7. AI Prep Plan Agent (AI builds a day-by-day prep schedule)

For each feature, create test cases that cover:
- the normal happy path (correct input, expected output)
- the empty input path (what happens when the user submits nothing)
- the AI failure path (what happens when the AI call fails)
- the edge case path (unusual but valid input)

Format as a checklist with checkboxes. Use plain language.
```

---

## Prompt 3: README Generation Prompt

Use this to generate a project README for the app.

```text
Write a project README for a web app called AI Interview Prep Copilot.

The app was built by a student using AI-assisted development tools across 8 sessions.

Include the following sections:

1. Project Title: AI Interview Prep Copilot
2. Short Description: A web app that helps students prepare for job interviews using 7 AI-powered features.
3. Features List: Describe each of the 7 features in 1–2 sentences:
   - Base Profile Dashboard
   - JD Analyzer
   - Profile vs JD Match Report
   - Interview Question Generator
   - Mock Answer Evaluator
   - RAG-Lite Doubt Solver
   - AI Prep Plan Agent
4. Tech Stack: List the technologies used (example: React, JavaScript, AI API, localStorage, CSS)
5. How to Run: Step-by-step instructions to run the app locally
6. How to Use: Step-by-step instructions for a user who opens the app for the first time
7. Project Status: Complete — all 7 features built and polished

Write it in clean Markdown format. Keep it beginner-friendly and professional.
```

---

## Prompt 4: Demo Script Prompt

Use this to generate a 2-minute spoken demo script for the full app.

```text
Write a 2-minute spoken demo script for a web app called AI Interview Prep Copilot.

The script should be used by a student during a job interview or portfolio presentation.

The app has 7 features:
1. Base Profile Dashboard — stores the student's name, target role, skills, projects, weak areas, and JD
2. JD Analyzer — extracts structured skills and topics from a job description
3. Profile vs JD Match — shows a match score and identifies skill gaps
4. Interview Question Generator — generates likely interview questions
5. Mock Answer Evaluator — evaluates mock answers with structured feedback
6. RAG-Lite Doubt Solver — answers prep doubts using the student's own profile as context
7. AI Prep Plan Agent — builds a day-by-day prep plan

The demo script should:
- take 2 minutes to read aloud at a comfortable pace
- walk through each feature in logical order
- explain what each feature does in plain language
- mention that AI was used to build it confidently
- end with a sentence about what the student learned

Do not use technical jargon. Write it as spoken language, not documentation.
```

---

## Prompt 5: Project Viva Preparation Prompt

Use this to generate 15 likely viva questions with model answers.

```text
I built a web app called AI Interview Prep Copilot for an interview prep course.

The app has 7 AI-powered features:
1. Base Profile Dashboard
2. JD Analyzer
3. Profile vs JD Match Report
4. Interview Question Generator
5. Mock Answer Evaluator
6. RAG-Lite Doubt Solver
7. AI Prep Plan Agent

I used AI-assisted development to build the app across 8 sessions using tools like Antigravity.

Generate 15 likely viva questions an interviewer might ask about this project, along with a model answer for each.

Cover:
- What the app does and why it was built
- How each major feature works
- How AI was used to build the app
- What I would improve or add next
- How I tested the app
- What I learned about AI-assisted development

Keep model answers to 3–5 sentences each. Use plain language.
```

---

## Prompt 6: UI Polish Prompt

Use this to add loading states, error states, input validation, and fallback text across the whole app.

```text
I have a complete web app called AI Interview Prep Copilot with 7 features.

Please add the following polish to every feature:

1. Loading State: For every button that makes an AI call, show a loading spinner or "Loading..." text while waiting for the AI response. Disable the button during loading to prevent multiple calls.

2. Error State: If an AI call fails for any reason, clear the loading state and show a user-friendly error message near the output section. Example: "Could not generate questions. Please check your input and try again."

3. Empty Input Validation: Before making any AI call, check that required input fields are filled. If they are empty, show a validation message and do not make the AI call. Example: "Please enter a job description before analyzing."

4. Fallback Text: After an AI call completes, check whether the response content is empty or only whitespace. If yes, show a fallback message. Example: "AI was unable to generate content. Please refine your input and try again."

5. Consistent UI: Make sure error messages and loading states look visually consistent across all 7 features.

Apply these changes to all 7 features: Profile Dashboard, JD Analyzer, Profile vs JD Match, Question Generator, Mock Evaluator, RAG-Lite Doubt Solver, and Prep Plan Agent.

Do not change the existing feature logic or UI layout. Only add these polish layers.

After making the changes, list each feature and confirm which polish items were added.

Explain what you changed in each feature after completing the update.
```

---

## Prompt 7: Debugging Prompt

Use this template when a specific feature is broken. Replace the placeholders with your actual details.

```text
One feature in my AI Interview Prep Copilot app is not working correctly.

Feature: [Name the feature — e.g., Mock Answer Evaluator]

What it should do:
[Describe the expected behavior — e.g., The user types a mock answer in the text area, clicks Evaluate Answer, and the app shows AI feedback with a score and improvement suggestions.]

What is actually happening:
[Describe the bug — e.g., The button does nothing when clicked. No loading state appears and no output is shown.]

What I have already tried:
[Describe anything you checked — e.g., I checked the button's onClick handler and it appears to be connected. The function runs but the AI response does not appear in the output section.]

Please:
1. Identify the likely cause of the issue.
2. Fix the issue without breaking other features.
3. Explain what was wrong and what you changed.
4. Tell me how to test that the fix works.
```

---

# What You Should Be Able to Explain After Session 8

By the end of the session, you should be able to answer these questions without reading notes:

1. What is the AI Interview Prep Copilot and what problem does it solve?
2. What are the 7 features of the app and what does each one do?
3. What is a loading state and why did you add it to every AI button?
4. What is an error state and what happens in your app when an AI call fails?
5. What is input validation and which forms does your app validate?
6. What is fallback text and when does it appear?
7. How did you use AI to review code that you also built with AI?
8. What is in your project README?
9. How would you demo this app in 2 minutes?
10. What would you improve or add if you had more time?

## Final Session 8 Explanation

```text
I built a complete AI Interview Prep Copilot across 8 sessions. The app has 7 AI-powered features: a profile dashboard, JD analyzer, profile-JD match report, question generator, mock answer evaluator, RAG-lite doubt solver, and a prep plan agent. In the final session, I used AI to review and polish the complete app by adding loading states, error handling, input validation, and fallback text across all features. The project is documented with a README and a manual test checklist, and I can walk through the full app in a 2-minute demo.
```
