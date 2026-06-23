# Session 8 Instructor File: Debug, Test, Polish, and Interview Demo

## Session Title

Debug, Test, Polish, and Interview Demo

## Session Navigation

**Previous session:** Session 7 — Add AI Prep Plan Agent (complete app with all 7 features built)

**Next session:** None — this is the final session

## Duration

2 hours

## Project

AI Interview Prep Copilot

## Session 8 Objective

By the end of Session 8, students should have a fully polished AI Interview Prep Copilot that is portfolio-ready, demo-ready, and interview-explainable.

This session does not add a new AI feature. It adds production-level polish to all 7 features already built:

- Loading states on every AI call button
- Error messages when AI calls fail
- Empty input validation on every form
- Fallback text when AI returns no content
- A project README
- A manual test checklist covering all 7 features
- A 2-minute demo script
- Viva preparation

## Session 8 Deliverable

Students will finish this session with:

1. A polished, error-handled version of the complete AI Interview Prep Copilot
2. A project README written using AI
3. A manual test checklist covering all 7 features
4. A 2-minute spoken demo script
5. A set of practiced viva answers

The app should:

- show loading spinners on every AI button while waiting for a response
- show a user-friendly error message if any AI call fails
- prevent empty submissions across all 7 features
- show fallback text if AI returns an empty or unclear response
- be explainable confidently in a job interview

## Strict Scope Control

### Include

- Loading spinner on all AI buttons
- Error state messages for failed AI calls
- Empty input validation for all forms across all 7 features
- Fallback text when AI returns no useful content
- Minor UI consistency polish across sections
- Project README generated using AI
- Manual test checklist for all 7 features
- 2-minute demo script generated using AI
- Viva prep: top 15 likely interview questions with model answers

### Do Not Include

- Any new AI feature not built in Sessions 1–7
- Redesign of the full UI or layout
- Deployment to production or any hosting platform
- Authentication or login system
- Database or backend integration
- New pages that were not part of Sessions 1–7 planning
- Spending the full session only on CSS or animations
- New API integrations

Session 8 is the polish and packaging session. The feature set is already complete.

---

# Instructor Framing

## Opening Message

Over the last 7 sessions, we built a complete AI Interview Prep Copilot. We added a profile dashboard, JD analyzer, profile-JD match report, interview question generator, mock answer evaluator, RAG-lite doubt solver, and an AI prep plan agent.

Today we do something equally important: we make that app interview-ready.

Any real product engineer knows that building the feature is only 70% of the job. The other 30% is error handling, polish, testing, documentation, and communication. That is what Session 8 is about.

By the end of today, you will have an app you can open in front of an interviewer and walk through confidently.

## Key Philosophy

Students are not expected to code everything from scratch.

They are expected to:

- use AI to find gaps in their own code
- add production-level polish with AI assistance
- write documentation using AI and understand it
- test every feature deliberately
- explain the entire app in interview language
- demonstrate the project as a portfolio piece

## Repeated Instructor Line

Building the feature is only half the job. Polishing, testing, and explaining it is what separates a student project from a portfolio product.

---

# Session Flow

## 0–10 min: Opening and Recap of Session 7 — Add AI Prep Plan Agent (complete app with all 7 features built)

### Instructor Goal

Celebrate the completion of all 7 features and set the tone for the final session.

### Recap of Session 7

In Session 7, students added the AI Prep Plan Agent. This feature reads the student's profile, weak areas, target role, and available days and generates a day-by-day structured interview preparation plan using a structured AI prompt.

That was the last new AI feature. The full feature set is now complete.

### Transition to Session 8

Ask students: "Is your app ready to demo to a recruiter right now?"

Common responses will be: "Not sure," "Probably yes," "It has some bugs."

Explain: Most apps built quickly with AI have gaps — missing loading states, no error messages, inputs that break when empty, no documentation. Today we fix all of that.

### What Today Looks Like

Today we will use AI to audit our own AI-built code and make it portfolio-ready. We will write tests, README, and a demo script. We will also practice explaining the project confidently.

This is how professional engineers close a sprint.

---

## 10–20 min: Product Breakdown Before Prompting

### Instructor Goal

Before running any prompt, teach students to audit their own app like a QA engineer would.

### Ask Students

Go through each of the 7 features and ask: "What breaks in this feature if the input is empty?"

Expected answers per feature:

- Profile Dashboard: form submits with blank name or role
- JD Analyzer: crashes or returns nothing with empty JD
- Profile vs JD Match: returns empty match if either side is missing
- Question Generator: generates questions without any role or JD context
- Mock Answer Evaluator: evaluates an empty answer field
- RAG-Lite Doubt Solver: sends an empty question to the AI
- AI Prep Plan Agent: generates a plan without any weak areas or days

### Next Question for Students

"What happens in your app if the AI call takes 5 seconds? Does the button freeze? Does the user see a loading message?"

### Build the Audit List

Together, create a checklist on the board or shared screen:

1. Which buttons have loading states?
2. Which forms have empty validation?
3. Which AI calls show error messages on failure?
4. Which sections show fallback text if AI returns nothing?
5. Is there a README?
6. Is there a test checklist?
7. Is there a demo script?

### Instructor Explanation

We are not guessing what to fix. We are auditing the product before prompting AI. This is how real engineers approach a pre-release bug bash. A clear audit gives a focused prompt.

---

## 20–35 min: Generate Debug, Test, Polish, and Interview Demo Feature in AI Tool

### Instructor Goal

Use the main polish prompt to review and improve the full app in one structured pass.

### What to Watch For

- Does AI identify specific missing loading states across all 7 buttons?
- Does AI add consistent error message handling?
- Does AI validate empty inputs in all forms?
- Does AI add fallback text when AI output is missing?
- Does the code remain organized and not break existing features?
- Does the README include all 7 features with descriptions?
- Does the demo script follow a clear 2-minute spoken flow?

### Instructor Control Rule

Do not let students run UI redesign prompts at this point. The focus is functional polish only. If a student asks about animations or complete UI overhaul, say: "We can do that after the session. Right now we are fixing functionality."

### What to Show Students

Run the main prompt from the student file (Prompt 6: UI Polish Prompt) live on the instructor screen first. Walk through what AI produces before students run their own version.

---

## 35–50 min: Instructor Walkthrough of Generated Feature

### Instructor Goal

Help students understand what the polish pass added to each part of the app.

### Walkthrough Areas

1. Loading state logic on each AI button — where is the loading variable set, where is the spinner shown, where is it cleared
2. Error state handling — where is the try/catch or error variable, what message shows on failure
3. Empty input validation — which fields now block submission when empty
4. Fallback text rendering — where does AI check for empty output and show a default message
5. README structure — which sections cover features, tech stack, setup, and usage
6. Test checklist — how is each feature covered in the manual test list
7. Demo script — what is the spoken flow for a 2-minute walkthrough

### Ask During Walkthrough

- Where does the loading spinner appear for the JD Analyzer?
- What happens now if the Mock Answer Evaluator receives an empty answer field?
- Where is the fallback text shown for the Question Generator?
- What does the README say about how to run the app?
- Which step in the demo script covers the prep plan agent?

### Simple Explanation

AI helped us add polish, but in an interview you need to explain every part of this app. So we read what was generated. We do not skip this step.

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students run their polish prompt, review the generated changes, and apply them to their own app.

### Instructor Support Areas

Help students with:

- Generated code breaking an existing feature
- Loading state not clearing after AI call finishes
- Error message showing even when the call succeeds
- README being too short or missing features
- Test checklist missing one or more of the 7 features
- Demo script being too long or too technical

### If Student App Is Broken Before This Session

Do not spend more than 3 minutes debugging a single student's broken app during this segment.

The student should:

- use the instructor screen as reference
- note which feature is broken
- run the debugging prompt (Prompt 7) after the session
- focus on understanding the polish changes being made

---

## 65–80 min: Improve and Refine

### Instructor Goal

Push the output beyond the first AI generation pass and teach students to iterate.

### What to Improve in This Segment

1. Review the README and ask: "Does this explain the app to someone who has never seen it?"
2. Review the test checklist and ask: "Is every AI call in the app covered in this list?"
3. Review the demo script and ask: "Can I actually speak this in 2 minutes comfortably?"
4. Ask students to read the demo script aloud once. Time it.

### Iteration Prompts to Run

- If the README is weak, run the README Generation Prompt (Prompt 3) again with more specific instructions
- If the test checklist is incomplete, ask AI to add the missing feature test cases
- If the demo script is too long, ask AI to shorten it to 120 words

### Instructor Explanation

The first AI output is never the final output. You prompt, review, and refine. This iteration mindset is what separates students who use AI well from students who just paste the output.

---

## 80–95 min: Edge Cases and Error States

### Instructor Goal

Push students to think like QA engineers and find the remaining edge cases.

### Edge Case Scenarios to Walk Through

1. What happens if the user pastes a 10,000-character JD into the JD Analyzer?
2. What happens if the AI returns a response that contains only whitespace?
3. What happens if the user clicks the Question Generator button 5 times in rapid succession?
4. What happens if localStorage is full?
5. What happens if the Prep Plan Agent is called with no weak areas and no target date?

### Instructor Explanation

Great apps handle the unhappy path, not just the happy path. You do not have to fix all of these today. But you should be able to explain what might go wrong and what you would do to fix it.

### Ask Students to Add One Edge Case Fix

Each student picks one edge case and asks AI to handle it. Examples:

- Disable the button while loading to prevent multiple calls
- Trim whitespace before validating empty inputs
- Show a "Content too long" message if JD exceeds a limit
- Show a specific message if AI returns only whitespace

### Why This Matters in Interviews

Interviewers frequently ask: "What happens if the user does X incorrectly?" A student who has thought about edge cases answers confidently. A student who never tested the app cannot answer.

---

## 95–105 min: Concept Pause — AI-Assisted Code Review, Testing, and Portfolio Explanation

### Instructor Goal

Convert all the technical work of this session into interview-ready conceptual understanding.

### Explain the AI-Assisted Code Review Concept

AI does not only help you build features. It can also review the code you already built and find problems.

In this session, we used AI to:

- audit our app for missing loading states, error messages, and validation
- generate a test checklist to check every feature manually
- write a README that explains the project to someone unfamiliar with it
- create a demo script so we can speak about the app confidently

This is called AI-assisted code review. Instead of a senior engineer reviewing your code, you use AI as a reviewer to find gaps.

### The Key Distinction

Using AI as a reviewer is different from using AI as a builder. When AI builds, it generates new code. When AI reviews, it reads existing code and suggests improvements or finds missing pieces.

Both skills matter. But for a final session, the review and polish pass is the most important.

### Explain What Makes a Project Portfolio-Ready

A portfolio project must:

- work without crashing on normal use
- handle errors gracefully
- have a README that explains what it does
- be demonstrable in 2 minutes
- be explainable without reading the code out loud

### Full App Concept Flow

User opens the app  
↓  
Fills profile (Session 1 — base dashboard, localStorage)  
↓  
Pastes a JD → AI extracts skills and topics (Session 2 — JD Analyzer)  
↓  
App compares profile with JD → match score and gap report (Session 3 — Profile vs JD Match)  
↓  
App generates interview questions based on JD and role (Session 4 — Question Generator)  
↓  
User types a mock answer → AI evaluates and gives feedback (Session 5 — Mock Answer Evaluator)  
↓  
User asks a doubt → AI answers using their profile as context (Session 6 — RAG-Lite Doubt Solver)  
↓  
AI builds a day-by-day prep plan from weak areas and target date (Session 7 — Prep Plan Agent)  
↓  
All buttons show loading states, all forms validate, errors are handled (Session 8 — Polish)  
↓  
README, test checklist, and demo script are complete  
↓  
App is portfolio-ready and interview-ready

### Student Writing Task

Ask every student to write a 3-line answer:

"How did you use AI to review the code you built with AI?"

Expected answer:

I ran a code review prompt that asked AI to check every feature for missing loading states, error handling, and empty input validation. AI identified the gaps in each of the 7 features and generated the fixes. I reviewed the output, tested it manually, and refined the parts that did not work correctly.

---

## 105–115 min: Interview Discussion and Viva Practice

### Instructor Goal

Prepare students to speak confidently about the complete project.

Use the interview questions section below. Focus especially on the AI Topic Questions (Q11–Q15) which are about AI-assisted code review, testing, and portfolio explanation.

### Viva Practice Method

1. Pair students up.
2. One student asks a question, the other answers without reading notes.
3. Rotate roles after 5 minutes.
4. Instructor selects 2–3 questions to ask the full class.

### Key Message

In an interview, you will not read your README. You will speak from understanding. That is why we practice explaining the project in words, not documents.

---

## 115–120 min: Wrap-Up and Final Demo Preparation and Portfolio Packaging

### Instructor Closing

Today we completed the final session of the AI Interview Prep Copilot.

Over 8 sessions you built a real product:

- Session 1: Profile Dashboard
- Session 2: JD Analyzer
- Session 3: Profile vs JD Match
- Session 4: Interview Question Generator
- Session 5: Mock Answer Evaluator
- Session 6: RAG-Lite Doubt Solver
- Session 7: AI Prep Plan Agent
- Session 8: Polish, Test, Document, Demo

This app is now portfolio-ready. You can add it to your GitHub, explain it in interviews, and walk a recruiter through it in 2 minutes.

### Final Instructions to Students

1. Save the final code to a named folder or GitHub repository.
2. Save the README as a file in the project folder.
3. Save the test checklist as a separate document.
4. Save the demo script as a text file or note.
5. Practice the demo script at least twice before any interview.

---

# Instructor Notes

## What to Emphasize

Session 8 is not a throwaway session.

Polish, testing, documentation, and demo prep are real engineering skills.

Session 8 is about teaching students:

- how to use AI to review code you built with AI
- how to add error handling and loading states to an existing app
- how to write documentation with AI assistance
- how to create a test plan for an AI-assisted app
- how to present and explain a project in interview language

## Common Student Mistakes

1. Thinking Session 8 is just about making things look pretty and rushing through it.
2. Running the polish prompt and not reading what AI changed.
3. Not testing the loading states — just assuming they work.
4. Writing a README that only lists the tech stack without explaining the features.
5. Creating a demo script that is too long to speak in 2 minutes.
6. Skipping the viva practice segment to spend more time on code.
7. Trying to add a new feature in Session 8 because they feel the app is incomplete.
8. Not handling the case where an AI call returns an empty or whitespace-only response.
9. Applying the polish prompt but not verifying that existing features still work after the change.
10. Not saving the README, test checklist, and demo script as separate files for portfolio use.

## How to Control the Session

Use this rule:

If it adds a new feature, it is out of scope for Session 8.

Session 8 only polishes, tests, documents, and demos the 7 features already built.

If a student's app is still missing a Session 1–7 feature, treat that as a separate fix using the debugging prompt, not as a new addition to scope.

## Setup Rule

Students should arrive at Session 8 with a working app from Session 7.

If an app is completely broken, do not rebuild it live during Session 8.

Share the instructor's completed Session 7 code as a baseline and have the student apply Session 8 polish on top of that.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### 1. What is the AI Interview Prep Copilot?

Expected answer:

The AI Interview Prep Copilot is a web app that helps students prepare for interviews using a series of AI-powered features. The app collects the student's profile, analyzes job descriptions, compares the profile with the JD, generates interview questions, evaluates mock answers, answers doubts using a context-aware approach, and builds a personalized day-by-day preparation plan.

### 2. How many features does the final app have, and what are they?

Expected answer:

The final app has 7 AI-powered features built across 7 sessions. They are: the base profile dashboard that stores the student's interview context, a JD analyzer that extracts structured information from a job description, a profile versus JD match report that shows alignment and gaps, an interview question generator, a mock answer evaluator, a RAG-lite doubt solver, and an AI prep plan agent that builds a day-by-day preparation schedule.

### 3. What does polishing an app mean in the context of this project?

Expected answer:

Polishing the app means adding the finishing layer that makes it production-ready. This includes adding loading states so the user knows an AI call is in progress, adding error messages so the user knows when something fails, adding input validation so the app does not crash on empty input, adding fallback text so the user sees something useful even if AI returns an empty response, and adding documentation so anyone can understand and run the app.

### 4. Why did you write a README for this project?

Expected answer:

A README is the first thing a recruiter or interviewer reads when they look at a project on GitHub or in a portfolio. Without a README, the project looks unfinished. The README explains what the app does, what features it has, what technologies were used, and how to run it. Writing a good README shows that I can communicate about my own work, which is an important engineering skill.

### 5. What is a manual test checklist and why did you create one?

Expected answer:

A manual test checklist is a list of specific steps to verify that each feature of the app works correctly. I created one that covers all 7 features. For each feature, the checklist specifies what to input, what button to click, and what output to expect. This helped me verify that loading states, error handling, and validation all work before the app goes into a portfolio. It also shows an interviewer that I know how to test an app, not just build it.

---

## App Flow Questions

### 6. Walk me through the complete flow of the app from start to finish.

Expected answer:

The user starts by filling in their interview profile: name, target role, skills, project details, weak areas, and job description. This is saved to localStorage. Then the user can analyze the JD to extract required skills and topics. The app compares the profile against the JD and shows a match score with identified gaps. The user can then generate interview questions based on the role and JD. They can type a mock answer and receive AI evaluation feedback. If they have a specific doubt, they can ask the RAG-lite doubt solver which uses their profile as context. Finally, the prep plan agent generates a day-by-day preparation schedule based on weak areas and available days. In Session 8, all of these steps now include loading states, error handling, and validation.

### 7. What happens if an AI call fails in the final polished app?

Expected answer:

In the polished version of the app, every AI call is wrapped in error handling logic. If an AI call fails, the loading state is cleared and an error message is shown to the user. The message is friendly and specific, such as "Question generation failed. Please check your input and try again." The user can then retry. Before Session 8, many of these cases were unhandled and the app would simply freeze or show nothing.

### 8. What happens if a user submits an empty form in any of the 7 features?

Expected answer:

After Session 8 polish, every form in all 7 features has empty input validation. If required fields are empty when the user clicks an AI button, the app shows a validation error message and does not make the AI call. This prevents wasted API calls and confusing empty outputs. For example, if the user clicks Generate Questions without a job description, they see a message like "Please enter a job description before generating questions."

### 9. How does the app handle an AI response that contains no useful content?

Expected answer:

After the polish pass, the app checks whether the AI response is empty or contains only whitespace before rendering it. If the AI returns an empty or minimal response, the app shows a fallback message to the user such as "AI was unable to generate content. Please refine your input and try again." This prevents the user from seeing a blank output section without understanding why.

### 10. How is localStorage used across all 7 features?

Expected answer:

LocalStorage stores the user's base profile from Session 1. Every AI feature in Sessions 2 through 7 reads from this saved profile to provide personalized context. For example, the question generator uses the saved target role and JD, the mock evaluator uses the saved role and skills as evaluation context, and the prep plan agent uses the saved weak areas. This means the user only needs to fill their profile once, and all features use that data automatically.

---

## AI Topic Questions

### 11. How did you use AI to review code that you also built with AI?

Expected answer:

I used AI to audit the complete app by running a structured code review prompt. The prompt asked AI to look at all 7 features and identify which buttons were missing loading states, which forms lacked empty validation, which AI calls had no error handling, and which sections showed nothing when AI returned an empty response. AI returned a list of gaps along with suggested fixes. I then reviewed those fixes, applied the ones that made sense, and tested each change manually. This is an iterative process of using AI as a reviewer rather than only as a builder.

### 12. What are the limitations of using AI to review your own code?

Expected answer:

AI can miss context-specific logic errors that require understanding the full app flow. It may suggest fixes that look correct in isolation but break other parts of the app. It cannot test the app — it only reads the code. It may hallucinate functions or variables that do not exist in the codebase. This is why after using AI for a review pass, the student must still manually test every feature to confirm the fixes actually work. AI review speeds up the process but does not replace verification.

### 13. How do you explain this project in an interview when someone asks if you actually coded it yourself?

Expected answer:

I say: "I built this project using AI-assisted development, which means I used AI tools to generate and refine code. However, I designed the feature structure, wrote the prompts, reviewed every piece of generated code, tested each feature manually, debugged issues, and can explain every part of the app in technical detail." This is an honest and confident answer. It shows that I understand AI-assisted development as a real engineering approach, not as cheating. I should then be ready to explain any feature in detail to prove my understanding.

### 14. What is the difference between using AI to build features and using AI to polish a finished app?

Expected answer:

When using AI to build features, I provide a detailed prompt describing what I want, and AI generates the initial implementation. I then integrate it, test it, and refine it. When using AI to polish a finished app, I paste the existing code and ask AI to review it for gaps such as missing loading states, unhandled errors, and empty input edge cases. The difference is that building is generative and polishing is analytical. Both require clear prompts, but polishing requires a better understanding of the existing code because I need to evaluate whether AI's suggestions actually fit what is already there.

### 15. How would you explain this project in a 2-minute interview demo?

Expected answer:

I would say: "I built an AI Interview Prep Copilot — a complete web app that helps students prepare for job interviews using a series of AI-powered features. Let me walk you through it. First, the user fills in their profile: their target role, skills, current projects, weak areas, and job description. The app saves this as their interview context. Then, the JD Analyzer extracts the required skills and topics from the job description. The Match Report compares their profile against those requirements and shows a score and gap list. The Question Generator uses the JD and role to generate likely interview questions. The Mock Answer Evaluator lets the student answer one question and get AI feedback. The RAG-Lite Doubt Solver answers specific prep doubts using the student's own context. Finally, the Prep Plan Agent builds a day-by-day study schedule. The app was built using AI-assisted development across 8 sessions, and I can explain any part of the code or design in detail."

---

# Session 8 Completion Checklist

Students should complete the following by the end of the session:

- [ ] Loading spinner is visible on all 7 AI call buttons while a response is pending
- [ ] Loading spinner clears after AI call completes or fails
- [ ] Error message is shown to the user if any AI call fails
- [ ] Empty input validation is active on all 7 feature forms
- [ ] Fallback text is shown when AI returns an empty or whitespace-only response
- [ ] Existing 7 features still work correctly after the polish changes
- [ ] Project README is written and includes: app description, feature list, tech stack, and how to run
- [ ] Manual test checklist covers all 7 features with specific input and expected output for each
- [ ] 2-minute demo script is written and the student has read it aloud at least once
- [ ] Student can explain the full app flow from Session 1 through Session 8 without reading notes
- [ ] Student can answer at least 5 of the viva questions without hesitation
- [ ] Final code is saved in a named folder or GitHub repository

---

# Instructor Backup Plan

If AI tool generation fails or the polish prompt breaks the existing app:

1. Instructor demonstrates the loading state, error handling, and validation changes manually on the instructor screen using a known-good code base.
2. Students follow conceptually and note which changes need to be made.
3. Share the instructor's polished version of the app after the session.
4. Students use Prompt 6 and Prompt 7 later to apply the same changes to their own app.
5. Do not sacrifice the viva practice, demo script, and README segments — these are the most important deliverables of Session 8.
6. If time runs short, prioritize: viva practice > README > demo script > polish code changes.
