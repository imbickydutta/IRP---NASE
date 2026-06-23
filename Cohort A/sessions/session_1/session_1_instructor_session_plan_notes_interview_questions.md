# Day 1 Instructor File: AI Interview Prep Dashboard

## Session Title

Build the Base App: AI Interview Prep Dashboard

## Duration

2 hours

## Project

AI Interview Prep Copilot

## Day 1 Objective

By the end of Day 1, students should have a working base dashboard where they can enter and save their interview-prep profile.

This profile becomes the base context for all future AI features:

- JD Analyzer
- Profile vs JD Match
- Interview Question Generator
- Mock Answer Evaluator
- RAG-lite Doubt Solver
- AI Prep Plan Agent

## Day 1 Deliverable

Students will build a simple web app with:

1. Student Profile
2. Target Role
3. Skills
4. Project Details
5. Weak Areas
6. Job Description
7. Saved Profile Summary

The app should allow the student to:

- fill the profile form
- save the profile
- view the saved profile summary
- edit/update the profile
- persist the data locally

## Strict Scope Control

### Include

- Base dashboard
- Profile form
- Save Profile button
- Profile summary
- localStorage persistence
- basic validation
- future navigation labels

### Do Not Include

- login/signup
- database
- backend APIs
- authentication
- deployment
- AI API integration
- JD analysis
- resume scoring
- voice features
- complex UI design
- advanced React/state theory

Day 1 is only about creating the foundation.

---

# Instructor Framing

## Opening Message

Over the next 8 sessions, we are not building 8 separate projects. We are building one AI Interview Prep Copilot. Every day we will add one useful AI feature to the same app.

Today we will build the base dashboard. This dashboard will store the student’s interview profile, which becomes the context for all future AI features.

## Key Philosophy

Students are not expected to code everything from scratch.

They are expected to:

- guide AI with clear prompts
- understand what AI generated
- test the generated feature
- debug issues using AI
- explain the app flow in interview language

## Repeated Instructor Line

AI can generate code, but you are responsible for understanding, testing, and explaining it.

---

# Session Flow

## 0–10 min: Opening and Project Framing

### Instructor Goal

Set the direction and establish the running-project model.

### Explain Final Project Vision

Final app will include:

- student profile
- JD analyzer
- profile/JD match
- interview question generator
- mock answer evaluator
- RAG-lite doubt solver
- AI prep plan agent

### Day 1 Deliverable

By the end of today, your app should accept your interview profile and display a saved summary.

---

## 10–20 min: Product Breakdown Before Prompting

### Instructor Goal

Teach students not to blindly ask AI to “build an app.”

### Ask Students

What does this app need to collect?

Expected answers:

- name
- target role
- skills
- project details
- weak areas
- job description

### Convert into Feature List

1. Dashboard title
2. Profile form
3. Job description text area
4. Save button
5. Saved profile summary
6. Edit/update support
7. Local storage persistence

### Instructor Explanation

Before asking AI to build, we should know what we want. A vague prompt gives a vague app. A clear feature list gives a usable app.

---

## 20–35 min: Generate the Base App in Antigravity

### Instructor Goal

Use the first main prompt to generate the base app.

### What to Watch For

- Does the app have all required fields?
- Does Save Profile work?
- Is localStorage implemented?
- Is a Profile Summary displayed?
- Is the UI simple enough?

### Instructor Control Rule

Do not let students customize too much at this point. First get the basic app working.

---

## 35–50 min: Instructor Walkthrough of Generated App

### Instructor Goal

Help students understand what AI generated.

### Walkthrough Areas

1. Main app file
2. Form fields
3. State/data object
4. Save button logic
5. Profile summary rendering
6. localStorage logic
7. Basic validation

### Ask During Walkthrough

- Where is the profile data stored?
- What happens when Save Profile is clicked?
- What happens after page refresh?
- Which fields are required?
- Where is the summary displayed?

### Simple Explanation

AI generated the code, but in interviews you need to explain what it created. So we will always read the generated output.

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students run the main prompt and build their version.

### Instructor Support Areas

Help students with:

- prompt paste issues
- preview not loading
- missing save button
- localStorage not working
- UI breaking on smaller screen

### If Student Setup Fails

Do not block the class.

The student should:

- follow instructor screen
- pair with another student
- use the shared completed code after class

---

## 65–80 min: Improve App Structure

### Instructor Goal

Make the app feel like the base of a real product, not only a form.

### Expected Improvements

- simple navigation
- future feature labels
- dashboard cards
- next-step message

### Instructor Explanation

We are adding future navigation now so every upcoming session feels like adding one feature into the same product.

---

## 80–95 min: Add Validation and Empty States

### Instructor Goal

Teach edge-case thinking.

### Must Add

1. Required fields
2. Error message
3. Empty state
4. Success message
5. No profile saved message

### Instructor Explanation

Good apps do not only work for ideal inputs. They handle empty fields and guide the user.

---

## 95–105 min: Concept Pause

### Instructor Goal

Convert implementation into interview understanding.

### Explain the Flow

User enters profile details  
↓  
App stores the values in state  
↓  
User clicks Save  
↓  
App validates required fields  
↓  
App saves data to localStorage  
↓  
App shows profile summary  
↓  
Future AI features will use this saved data as context

### Student Writing Task

Ask every student to write a 2–3 line answer:

What happens when I click Save Profile?

Expected answer:

When I click Save Profile, the app checks whether required fields are filled. If valid, it stores the profile data in localStorage and displays the saved profile summary.

---

## 105–115 min: Interview Discussion and Viva Practice

### Instructor Goal

Prepare students to speak about the project.

Use the interview questions section below.

---

## 115–120 min: Wrap-Up and Day 2 Preview

### Instructor Closing

Today we built the base profile dashboard. Next session, we will add the first real AI feature: JD Analyzer. The app will take a raw job description and extract skills, responsibilities, role type, and interview topics using structured prompting.

---

# Instructor Notes

## What to Emphasize

Day 1 is not about teaching coding syntax.

Day 1 is about teaching students how to:

- convert a product idea into a build prompt
- guide an AI coding tool
- inspect generated code
- understand app flow
- test a feature
- explain what the app does
- prepare for interview discussion

## Common Student Mistakes

1. Asking vague prompts like “Build interview app”
2. Adding too many features on Day 1
3. Trying to add login/database immediately
4. Not checking if save works
5. Not testing refresh persistence
6. Not reading generated code
7. Spending too much time on colors/design
8. Not preparing their own JD/profile content

## How to Control the Session

Use this rule:

If a feature is not needed for Day 2, do not build it on Day 1.

Day 1 only needs a clean base profile dashboard.

## Setup Rule

Do not spend more than 5 minutes of live class on setup.

If setup fails, the student follows along and catches up later.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### 1. What did you build today?

Expected answer:

I built the base dashboard of an AI Interview Prep Copilot. It collects the student’s target role, skills, project details, weak areas, and job description.

### 2. Who is the user of this app?

Expected answer:

The user is a student or fresher preparing for interviews, especially for AI-assisted or new-age software engineering roles.

### 3. What problem does this app solve?

Expected answer:

It helps students organize their interview-prep context in one place so AI features can later generate more personalized preparation support.

### 4. Why do we collect the job description?

Expected answer:

The job description tells us what the company expects. Later, the app can use it to analyze required skills, generate interview questions, and compare the student profile with the role.

### 5. Why do we collect weak areas?

Expected answer:

Weak areas help the app personalize practice questions, feedback, and preparation plans.

---

## App Flow Questions

### 6. What happens when the user clicks Save Profile?

Expected answer:

The app validates required fields, stores the entered profile data locally, and displays the saved profile summary.

### 7. Where is the data stored in Day 1?

Expected answer:

For Day 1, the data is stored in localStorage so it stays available after page refresh.

### 8. Why are we using localStorage instead of a database?

Expected answer:

Day 1 is focused on building the base app quickly. localStorage is simple and enough for storing one user’s profile locally. A database can be added later if multiple users or persistent server-side storage is needed.

### 9. What is the limitation of localStorage?

Expected answer:

It stores data only in the user’s browser. It is not suitable for sensitive data, multi-user systems, or production-level storage.

### 10. What is the difference between form input and saved profile summary?

Expected answer:

The form input is where the user enters or edits data. The saved profile summary displays the saved version of that data.

---

## AI-Assisted Building Questions

### 11. How did AI help you build faster?

Expected answer:

AI helped generate the initial app structure, form fields, localStorage logic, validation, and UI layout based on a clear prompt.

### 12. Why should you not blindly trust AI-generated code?

Expected answer:

AI can miss requirements, create bugs, overcomplicate the app, or generate code I do not understand. I need to test, review, and explain the generated code.

### 13. What makes a good prompt for building this app?

Expected answer:

A good prompt clearly mentions the app goal, required fields, expected behavior, what to include, what not to include, and how the output should behave.

### 14. What did you check after AI generated the app?

Expected answer:

I checked whether all fields were present, Save Profile worked, validation worked, data stayed after refresh, and the profile summary displayed correctly.

### 15. How would you explain this project in one minute?

Expected answer:

I built the base version of an AI Interview Prep Copilot. It collects the student’s target role, skills, project details, weak areas, and job description. This information is saved locally and will be used as context for future AI features like JD analysis, question generation, mock evaluation, and prep planning.

---

# Day 1 Completion Checklist

Students should complete the following by the end of the session:

- App opens successfully
- App has title and dashboard layout
- Form has all required fields
- Save Profile button works
- Required field validation works
- Profile Summary appears after saving
- Data remains after refresh
- Edit Profile works
- Future navigation is visible
- No unnecessary AI feature is added
- Student can explain the app in 1 minute

---

# Instructor Backup Plan

If Antigravity generation fails or setup issues take too long:

1. Instructor continues live build on screen.
2. Students follow conceptually.
3. Share the final Day 1 code after session.
4. Students use the prompts later to regenerate/fix their app.
5. Do not sacrifice the interview explanation section.
