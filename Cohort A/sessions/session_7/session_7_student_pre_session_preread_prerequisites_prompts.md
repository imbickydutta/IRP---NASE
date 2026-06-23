# Session 7 Student Pre-Session File: Add AI Prep Plan Agent

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
- create a 7-day AI-powered interview prep plan

## Session 7 Goal

In Session 7, we will add the AI Prep Plan Agent.

The agent will take:

- your target role
- your weak topics (pre-filled from your saved profile)
- days until your interview
- daily available hours

And it will generate:

- a personalized 7-day preparation plan
- day-wise topics
- practice questions for each day
- a mock task for each day
- a final revision checklist

## Session 7 Output

By the end of Session 7, you should have a working feature where you can:

- enter your prep plan inputs (partially pre-filled)
- click Generate Plan and get a 7-day AI-powered plan
- view the plan as collapsible day cards inside the app
- expand each card to see that day's topic, questions, and task
- see a final revision checklist at the bottom of the plan

---

# Pre-Read

## Why Are We Building This?

Most students preparing for interviews struggle with:

- not knowing where to start
- having too many topics and too little time
- studying without structure
- not knowing what to practice each day

The AI Prep Plan Agent solves this directly. It takes your actual goals and time constraints and produces a structured, realistic daily roadmap — personalized to your weak areas and target role.

In interviews, when asked about this feature, you should be able to explain:

- what problem it solves
- what inputs the agent needs
- how the AI produces the plan
- why this is agent behavior and not just chatbot behavior
- how the output is structured and displayed in the app

## Simple App Flow

```
User enters profile in Session 1
↓
App saves profile in localStorage
↓
Session 2: JD Analyzer extracts key skills from the job description
↓
Session 3: Profile vs JD Match scores alignment between profile and JD
↓
Session 4: Interview Question Generator creates practice questions
↓
Session 5: Mock Answer Evaluator scores and gives feedback on student answers
↓
Session 6: RAG-Lite Doubt Solver answers concept questions from a knowledge base
↓
Session 7: AI Prep Plan Agent generates a personalized 7-day preparation roadmap
↓
Session 8: Full app review, polish, and mock interview demo
```

## Key Concepts to Revise

Before the session, revise these ideas:

1. **What is an AI agent?**
   An AI agent is a system that takes a goal and constraints, and produces a structured plan or set of actions — not just one response.

2. **What is the difference between an agent and a chatbot?**
   A chatbot responds to one message at a time. An agent plans across multiple steps to achieve a goal.

3. **What is a constraint in planning?**
   A constraint limits what is possible. Days until interview and daily hours are time and capacity constraints that shape the plan.

4. **What is structured output?**
   Structured output means the AI returns data in a defined format, like JSON, rather than plain text. This allows the app to parse and display the response programmatically.

5. **What is JSON?**
   JSON is a text-based format for storing structured data using key-value pairs. It is commonly used to pass data between AI and app code.

6. **What is pre-filling?**
   Pre-filling means automatically loading saved data into a form field. In Session 7, target role and weak topics are pre-filled from the localStorage profile saved in Session 1.

7. **What is a collapsible card?**
   A collapsible card is a UI element that shows a header and hides detail until the user clicks to expand it. It is used to display structured content without overwhelming the user.

8. **What is a revision checklist?**
   A revision checklist is a final list of key topics or actions to review at the end of a study period. In Session 7, AI generates this based on the student's weak areas and target role.

## Simple Explanation

An AI agent is like a smart planner.

You give it your goal: "I want to prepare for a data engineer interview."
You give it your constraints: "I have 7 days and 2 hours per day, and I am weak in SQL and system design."
The agent produces a structured plan: what to study on Day 1, Day 2, all the way to Day 7, with questions to practice and tasks to complete.

That is different from asking a chatbot: "What should I study for a data engineer interview?" The chatbot gives you a list. The agent gives you a personalized roadmap that accounts for your time and weaknesses.

---

# Prerequisites

## Mandatory Setup

Complete this before the live session:

1. Your app from Session 6 is working correctly
2. The RAG-Lite Doubt Solver from Session 6 is functional
3. Your profile is saved in localStorage (target role and weak areas must be filled)
4. Your AI tool (Antigravity or equivalent) is open and ready
5. You have read the Key Concepts above
6. You have your sample profile data ready (see Content to Prepare section below)
7. Chrome is installed
8. Stable internet connection is available
9. This file is open during the session

## Optional Setup

Useful but not mandatory:

- GitHub account to back up your app
- VS Code as a fallback editor
- Basic knowledge of JSON structure
- Have read about AI agents before the session

## Important Rule

Do not try to fix all previous sessions during Session 7.

If an earlier feature is broken, leave it for Session 8. In Session 7, focus only on getting the Prep Plan Agent working.

---

# Content to Prepare Before Class

Prepare this in a text file before class and keep it open during the session.

```text
Target Role:
[e.g. Junior Data Engineer / AI-assisted Software Developer / Backend Developer]

Weak Topics:
[e.g. SQL queries, system design, Python debugging, explaining code, APIs]

Days Until Interview:
[e.g. 7]

Daily Available Hours:
[e.g. 2]
```

## Sample Content

```text
Target Role:
AI-assisted Junior Software Engineer

Weak Topics:
explaining code, debugging errors, APIs, JavaScript logic, system design basics, technical interview confidence

Days Until Interview:
7

Daily Available Hours:
2
```

---

# Prompts for Session 7

Use these prompts during the session when instructed.

---

## Prompt 1: Main Build Prompt

```text
I am building an app called "AI Interview Prep Copilot".

Here is what has already been built in this app:
1. Session 1 — Base Profile Dashboard: A profile form that collects full name, target role, current skills, project details, weak areas, and job description. Data is saved in localStorage. A profile summary is displayed after saving.
2. Session 2 — JD Analyzer: Takes the saved job description and extracts required skills, responsibilities, role type, and interview topics using a structured AI prompt call.
3. Session 3 — Profile vs JD Match: Compares the saved student profile with the JD analysis results and shows a match score, strong areas, gap areas, and improvement suggestions.
4. Session 4 — Interview Question Generator: Generates role-specific interview questions based on the saved profile and JD analysis. Questions are displayed as a categorized list.
5. Session 5 — Mock Answer Evaluator: Student types a mock answer to a question, and AI evaluates it for clarity, accuracy, depth, and confidence. Shows a score and detailed feedback.
6. Session 6 — RAG-Lite Doubt Solver: Student types a concept question, and the app searches a local knowledge base to provide a relevant AI-assisted answer.

Now add a new section called "AI Prep Plan Agent" to this existing app.

Here is what this section should do:

Inputs (displayed as a form):
1. Target Role — text input, pre-filled from localStorage profile
2. Weak Topics — textarea, pre-filled from localStorage profile's weak areas
3. Days Until Interview — number input
4. Daily Available Hours — number input

Output:
1. A personalized 7-day interview preparation plan
2. Displayed as 7 collapsible day cards
3. Each day card must include:
   - Day number (e.g. Day 1, Day 2)
   - Topic for that day
   - 3 to 5 practice questions for that day
   - 1 mock interview task for that day
4. A Final Revision Checklist section after the 7 day cards, listing the most important topics to revise before the interview

UI Requirements:
- Show a loading message while the plan is being generated
- Show an empty state message if no plan has been generated yet: "No plan generated yet. Fill in the details above and click Generate Plan."
- If profile is not found in localStorage, show: "Please complete your profile first to generate a prep plan."
- Add a "Generate Plan" button
- Add a "Regenerate Plan" button after the first plan is shown
- Day cards should be collapsible — show day number and topic in the header, expand to show questions and task
- Keep the UI consistent with the rest of the app

Important constraints:
- Do not add n8n, webhooks, Google Sheets export, calendar sync, email notifications, or any external integration
- Do not add a database or backend
- Do not add deployment configuration
- Keep the plan generation entirely within the AI prompt call and the app UI

Also add clear comments in the code explaining:
- where the form inputs are pre-filled from localStorage
- where the AI prompt is constructed
- where the response is parsed into day objects
- how the day cards are rendered
- where the collapse and expand logic lives
```

---

## Prompt 2: UI Improvement Prompt

```text
Improve the UI of the AI Prep Plan Agent section.

Keep all the existing functionality.

Make these improvements:
1. Show the day number as a styled badge or pill (e.g. "Day 1" in a highlighted color)
2. Add a "Collapse All" and "Expand All" button at the top of the plan
3. Add a short summary header above the day cards saying: "Your 7-Day Prep Plan for [Target Role]"
4. Highlight the weak topics in the plan output with a colored badge or label
5. Add a subtle progress indicator showing how many days are in the plan (e.g. "7 of 7 days planned")
6. Style the Final Revision Checklist as a proper checklist with checkboxes
7. Make sure the layout is responsive on both laptop and mobile screens
8. Keep the design consistent with the rest of the app

Do not add any new AI functionality. Only improve the UI and UX of the existing Prep Plan section.
```

---

## Prompt 3: Debugging Prompt — Plan Not Generating

```text
The Generate Plan button in the AI Prep Plan Agent section is not working correctly.

Expected behavior:
1. When I fill in target role, weak topics, days until interview, and daily hours, clicking Generate Plan should trigger an AI call.
2. A loading state should appear while the plan is being generated.
3. The AI response should be parsed into 7 day objects.
4. The day cards should render with topic, questions, and mock task for each day.
5. The Final Revision Checklist should appear after the day cards.

Please debug and fix the issue.

Check:
- Whether the Generate Plan button is connected to the correct handler function
- Whether the prompt being sent to AI includes all four input values
- Whether the AI response is being parsed correctly into structured day data
- Whether the loading state is being shown and hidden at the right times
- Whether the day cards are rendering with the correct data

Please explain what was wrong and what you changed.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the AI Prep Plan Agent section of the current app in beginner-friendly language.

Focus on:
1. What are the main parts of this feature?
2. Where are the form inputs defined and pre-filled from localStorage?
3. Where is the AI prompt constructed and what does it contain?
4. How does the app send the request to AI?
5. How is the AI response parsed into structured day data?
6. How are the day cards rendered in the UI?
7. How does the collapse and expand logic work?
8. Where is the Final Revision Checklist rendered?
9. Which parts should I explain in an interview?

Do not rewrite the code. Only explain it clearly.
```

---

## Prompt 5: Interview Explanation Prompt

```text
Explain the AI Prep Plan Agent feature of the app as if I am preparing for an interview.

Use this structure:
1. What problem does this feature solve?
2. Who is the user and what do they need?
3. What are the four inputs the agent takes?
4. What does the AI produce as output?
5. How is the output displayed in the app?
6. Why is this feature called an agent rather than a chatbot?
7. What did I use AI for while building this?
8. What are the limitations of this feature?
9. What would I add next to improve it?

Keep the explanation simple, specific, and interview-ready. Use examples from the app.
```

---

## Prompt 6: Structured JSON Output Prompt

```text
The AI Prep Plan Agent currently returns the plan as plain text.

Modify the AI prompt so that it asks the AI to return the 7-day plan in this exact JSON structure:

{
  "plan": [
    {
      "day": 1,
      "topic": "string — the main topic for this day",
      "questions": [
        "string — practice question 1",
        "string — practice question 2",
        "string — practice question 3"
      ],
      "mockTask": "string — one mock interview task for this day"
    }
  ],
  "revisionChecklist": [
    "string — key topic 1 to revise before the interview",
    "string — key topic 2 to revise before the interview",
    "string — key topic 3 to revise before the interview"
  ]
}

After modifying the prompt:
1. Update the response parsing code to use this JSON structure.
2. Make sure the day cards render correctly using the new structured data.
3. Make sure the revision checklist renders using the revisionChecklist array.
4. Add error handling for cases where the AI does not return valid JSON — show a friendly error message.

Explain the changes you made.
```

---

## Prompt 7: Error and Empty State Prompt

```text
Add proper error and empty states to the AI Prep Plan Agent section.

Add the following:
1. If the student has not saved a profile in localStorage, show this message inside the Prep Plan section:
   "Please complete your profile first. Go to the Profile section and save your details before generating a prep plan."

2. If the student clicks Generate Plan without entering days until interview or daily hours, show a validation error:
   "Please fill in all required fields: Days Until Interview and Daily Available Hours."

3. If the AI call fails or returns an unexpected response, show this error:
   "Could not generate the plan. Please check your connection and try again."

4. If days until interview is entered as 0 or a negative number, show:
   "Please enter a valid number of days (minimum 1)."

5. If daily hours is entered as 0, show:
   "Please enter at least 1 hour of daily study time."

6. Before the first plan is generated, show an empty state card:
   "No plan generated yet. Fill in the details above and click Generate Plan to create your personalized 7-day prep roadmap."

Keep all existing functionality. Only add these validation and error state messages.
```

---

# What You Should Be Able to Explain After Session 7

By the end of the session, you should be able to answer these questions on your own — without reading notes:

1. What is the AI Prep Plan Agent and what problem does it solve?
2. What are the four inputs the agent takes and why does each one matter?
3. Why are target role and weak topics pre-filled from the saved profile?
4. What happens when the student clicks Generate Plan?
5. What is the difference between an AI agent and a chatbot?
6. Why is structured JSON output important for this feature?
7. How does the app render the AI response as collapsible day cards?
8. What is the Final Revision Checklist and how is it generated?
9. What edge cases or error states did you add to this feature?
10. How would you explain this feature to an interviewer in under one minute?

---

## Final Session 7 Explanation

```text
In Session 7, I added an AI Prep Plan Agent to the app. The student enters their target role, weak topics, days until the interview, and daily available hours. The app reads the saved profile for additional context, builds a structured prompt, and sends it to the AI. The AI returns a personalized 7-day preparation plan with day-wise topics, practice questions, and mock tasks, which the app displays as collapsible day cards. A final revision checklist is shown at the bottom. This feature demonstrates agent behavior because the AI uses the student's actual goals and constraints to produce a structured, multi-step action plan — not just a single conversational response.
```
