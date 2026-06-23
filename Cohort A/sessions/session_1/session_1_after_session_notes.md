# Day 1 After-Session Notes: AI Interview Prep Dashboard

## What We Built Today

Today we built the base version of the AI Interview Prep Copilot.

The app collects and saves:

- Full Name
- Target Role
- Current Skills
- Project Details
- Weak Areas
- Job Description

This saved profile will be used as context for future AI features.

---

# Why This Base App Matters

Future AI features should not generate generic output.

They should use the student’s own context:

- target role
- job description
- skills
- projects
- weak areas

That is why Day 1 focused on collecting and saving this information.

---

# App Flow

The basic flow is:

User enters profile details  
↓  
App validates required fields  
↓  
User clicks Save Profile  
↓  
App saves data in localStorage  
↓  
App displays Profile Summary  
↓  
Future AI features use this saved profile as context

---

# What is localStorage?

localStorage is a browser feature that stores data locally on the user’s device.

In this app, localStorage is used so that the saved profile remains available even after refreshing the page.

## Important limitation

localStorage is not a production database.

It is useful for Day 1 because:

- it is simple
- it does not need backend setup
- it works for one-user local data
- it helps us focus on app flow

In a real production app, we may use a database instead.

---

# What Students Should Understand

Students should understand:

1. What the app does
2. What data it collects
3. Why that data matters
4. What happens when Save Profile is clicked
5. Why localStorage was used
6. How AI helped generate the app
7. Why AI-generated code must still be reviewed and tested

---

# Interview-Ready Explanation

Use this explanation:

```text
I built the base version of an AI Interview Prep Copilot. The app collects the student’s target role, skills, project details, weak areas, and job description. This information is saved locally using localStorage. In future sessions, this data will be used as context for AI features like JD analysis, profile matching, question generation, mock answer evaluation, and prep planning.
```

---

# What Happens When Save Profile is Clicked?

Expected answer:

```text
When Save Profile is clicked, the app first checks whether the required fields are filled. If the data is valid, it saves the profile in localStorage and displays the saved profile summary. If required fields are missing, it shows an error message.
```

---

# What AI Was Used For

AI was used to help generate:

- app layout
- profile form
- localStorage logic
- validation
- profile summary
- simple dashboard structure

But students still need to:

- test whether the app works
- check whether required fields exist
- verify whether data remains after refresh
- understand the generated code
- explain the app in interview language

---

# Common Issues and Fixes

## Issue 1: Save button does not work

Possible reasons:

- button is not connected to the save function
- validation blocks saving
- state is not updating correctly
- localStorage code is missing or incorrect

What to ask AI:

```text
The Save Profile button is not working. Please check the save function, validation, state update, and localStorage logic. Fix the issue and explain what was wrong.
```

## Issue 2: Data disappears after refresh

Possible reason:

- data is saved in state but not in localStorage
- app is not reading from localStorage on load

What to ask AI:

```text
The profile data disappears after refresh. Please add localStorage save and load logic. The saved profile should appear again when the app is reopened or refreshed.
```

## Issue 3: App has too many features

Possible reason:

- prompt was too broad
- AI added login/backend/AI features unnecessarily

What to ask AI:

```text
Simplify this app. For Day 1, keep only the profile dashboard, profile form, localStorage persistence, validation, and profile summary. Remove login, backend, database, and AI API features.
```

---

# Key Takeaways

## 1. Clear prompts create better apps

Bad prompt:

```text
Build an interview app.
```

Better prompt:

```text
Build a simple AI Interview Prep Copilot dashboard with profile form, job description input, localStorage save, profile summary, validation, and no backend.
```

## 2. Do not build everything at once

Day 1 is only the base dashboard.

AI features will be added one by one in later sessions.

## 3. Students must understand the app flow

Using AI to build is acceptable.

Not understanding the generated app is not acceptable.

## 4. Interviews test explanation

Students should be able to explain:

- what they built
- why they built it
- how it works
- what can go wrong
- what they will improve

---

# Day 2 Preview

In Day 2, we will add the first AI feature:

# JD Analyzer

The app will take a raw job description and extract:

- required skills
- responsibilities
- role type
- important interview topics
- difficulty level

Main AI concept:

Structured prompting and JSON output.

Day 2 will use the Job Description entered in Day 1.
