# Day 1 Student Pre-Session File: AI Interview Prep Dashboard

## What We Are Building

In this 8-day interview-prep phase, we will build one continuous project:

# AI Interview Prep Copilot

This app will help a student prepare for interviews using AI.

By the end of all sessions, the app will be able to:

- store your interview profile
- analyze job descriptions
- compare your profile with the JD
- generate interview questions
- evaluate your mock answers
- answer doubts using RAG-lite
- create a 7-day interview prep plan

## Day 1 Goal

In Day 1, we will build only the base dashboard.

The dashboard will collect:

- your name
- target role
- current skills
- project details
- weak areas
- job description

This data will become the context for future AI features.

## Day 1 Output

By the end of Day 1, you should have a working app where you can:

- enter your interview profile
- save your profile
- view your saved profile summary
- edit/update the profile
- keep the data even after refreshing the page

---

# Pre-Read

## Why Are We Building This?

In interviews, it is not enough to say:

“I used AI to build this.”

You should be able to explain:

- what problem the app solves
- who the user is
- what data the app collects
- how the app works
- how AI helped you build it
- what you tested
- what you would improve

This project will help you practice that.

## Simple App Flow

User enters profile details  
↓  
App saves the profile  
↓  
App shows a summary  
↓  
Future AI features use this profile as context

## Key Concepts to Revise

Before the session, revise these basic ideas:

- What is a web app?
- What is a form?
- What is user input?
- What is frontend?
- What is localStorage?
- What is a prompt?
- What is context in AI?
- Why does AI need clear instructions?

## Simple Explanation

A web app takes input from the user, stores or processes that input, and shows useful output.

In our app:

- the user is a student preparing for interviews
- the input is the student profile and JD
- the saved profile becomes context
- future AI features will use this context to give personalized output

---

# Prerequisites Before Session

## Mandatory Setup

Complete this before the live session:

1. Install Google Antigravity
2. Login with the required account
3. Make sure Antigravity opens properly
4. Create a folder named `ai-interview-prep-copilot`
5. Keep one sample job description ready
6. Keep your own profile/project details ready
7. Keep Chrome installed
8. Keep a stable internet connection
9. Keep this file open during the session

## Optional Setup

Useful but not mandatory:

- GitHub account
- basic Git installed
- VS Code as fallback editor
- Node.js installed, if needed by the generated project
- sample resume/profile text

## Important Rule

Do not spend the live session setting up tools.

If your setup does not work, follow the instructor screen and catch up after the session.

---

# Content to Prepare Before Class

Prepare this in a text file before class.

```text
Full Name:

Target Role:

Current Skills:

Project Details:

Weak Areas:

Job Description:
```

## Sample Student Profile

```text
Full Name:
Aarav Sharma

Target Role:
AI-assisted Junior Software Engineer

Current Skills:
Prompt engineering, HTML basics, UI building with AI tools, basic JavaScript understanding, no-code workflows, RAG basics

Project Details:
Built a travel planner prototype using AI tools. Created a basic workflow where user enters destination and budget, and the app generates itinerary suggestions.

Weak Areas:
Explaining code, debugging errors, APIs, JavaScript logic, technical interview confidence

Job Description:
We are hiring a Junior Software Engineer who can build web applications using AI-assisted development tools. The candidate should understand frontend basics, APIs, data handling, prompt engineering, AI feature integration, debugging, and product thinking. Experience with LLMs, automation tools, and rapid prototyping is preferred.
```

---

# Prompts for Day 1

Use these prompts during the session when instructed.

---

## Prompt 1: Base App Generation

```text
Create a simple web app called “AI Interview Prep Copilot”.

Goal:
This app will help students prepare for interviews using AI-assisted features. For Day 1, only build the base dashboard and profile form. Do not add actual AI features yet.

Build the following:

1. A clean dashboard layout
2. Header with app name: AI Interview Prep Copilot
3. Short subtitle: Build your interview profile and prepare using AI
4. A student profile form with these fields:
   - Full Name
   - Target Role
   - Current Skills
   - Project Details
   - Weak Areas
   - Job Description
5. Use textarea fields for Skills, Project Details, Weak Areas, and Job Description
6. Add a Save Profile button
7. After saving, show a Profile Summary section
8. Store the profile data in localStorage so that it remains after refresh
9. Add an Edit Profile button
10. Keep the UI simple, clean, and beginner-friendly
11. Do not add login, backend, database, or external APIs
12. Add basic empty field validation
13. Make it responsive for laptop and mobile view

Also add clear comments in the code explaining:
- where the form state is managed
- where localStorage is used
- how the profile summary is displayed
```

---

## Prompt 2: UI Improvement

```text
Improve the UI of the AI Interview Prep Copilot dashboard.

Keep the same functionality.

Make the layout more professional:
- Add a left or top navigation section with these future feature names:
  1. Profile
  2. JD Analyzer
  3. Match Score
  4. Question Generator
  5. Mock Evaluator
  6. RAG Doubt Solver
  7. Prep Plan Agent
- Only the Profile section should be functional for now.
- Add cards for “Profile Completion”, “Target Role”, and “Next Step”.
- Show a message: “Next: Analyze your Job Description in Day 2”.
- Keep the design clean and responsive.
- Do not add any new AI functionality yet.
```

---

## Prompt 3: Validation and Empty State

```text
Add better validation and empty states to the profile form.

Rules:
1. Full Name is required.
2. Target Role is required.
3. Job Description is required.
4. If required fields are missing, show a clear error message near the form.
5. If no profile is saved yet, show an empty state card saying:
   “No profile saved yet. Fill the form to create your interview prep profile.”
6. After saving, show a success message:
   “Profile saved successfully. This will be used as context for future AI features.”
7. Keep the UI simple and do not add any external libraries unless already used.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the current code of this app in beginner-friendly language.

Focus on:
1. What are the main parts/files?
2. Where is the form created?
3. Where is the profile data stored?
4. What happens when Save Profile is clicked?
5. How does localStorage work in this app?
6. How is the Profile Summary displayed?
7. Which part should I explain in an interview?

Do not rewrite the code. Only explain it clearly.
```

---

## Prompt 5: Debugging Prompt — Save Not Working

```text
The Save Profile button is not working correctly.

Please debug and fix the issue.

Expected behavior:
1. When I fill Full Name, Target Role, and Job Description, clicking Save Profile should save the data.
2. The saved data should appear in the Profile Summary section.
3. The data should remain after page refresh using localStorage.
4. If required fields are empty, show an error message.

Please explain what was wrong and what you changed.
```

---

## Prompt 6: Debugging Prompt — localStorage Not Working

```text
The profile data disappears after page refresh.

Please fix localStorage persistence.

Expected behavior:
1. When profile is saved, store it in localStorage.
2. When the app loads, check localStorage for saved profile data.
3. If saved data exists, display it in the Profile Summary.
4. The user should be able to edit and save updated data again.

Please explain the localStorage flow in simple language.
```

---

## Prompt 7: Interview Explanation Prompt

```text
Explain this app as if I am preparing for an interview.

Use this structure:
1. What problem does the app solve?
2. Who is the user?
3. What data does the app collect?
4. What happens when the user saves the profile?
5. Why is this profile important for future AI features?
6. What did I use AI for while building this?
7. What are the current limitations?
8. What will I add next?

Keep the explanation simple and interview-ready.
```

---

# What You Should Be Able to Explain After Day 1

By the end of the session, you should be able to answer:

1. What did you build?
2. Who is the user?
3. What data does the app collect?
4. What happens when Save Profile is clicked?
5. What is localStorage?
6. Why is this profile important for future AI features?
7. How did AI help you build faster?
8. Why should you still review AI-generated code?

## Final Day 1 Explanation

```text
I built the base version of an AI Interview Prep Copilot. The app collects the student’s target role, skills, project details, weak areas, and job description. This information is saved locally and will be used as context for future AI features like JD analysis, question generation, mock evaluation, and prep planning.
```
