# Session 3 Instructor File: Add Profile vs JD Match

## Session Title

Add Profile vs JD Match

## Duration

2 hours

## Project

AI Interview Prep Copilot

## Session 3 Objective

By the end of Session 3, students should have a working match feature that reads the student profile saved in Session 1 and the JD analysis produced in Session 2, sends both to an AI with a structured comparison prompt, and displays a match report card showing: overall match band (Strong / Moderate / Weak), matched skills list, missing skills list, improvement suggestions, and interview risk areas.

This feature moves the app from data collection and analysis into personalized, explainable AI output — which is the most interview-relevant concept in the course.

## Session 3 Deliverable

Students will extend the existing AI Interview Prep Copilot to include:

1. A "Match Report" section in the dashboard
2. A "Check My Match" button that triggers the AI comparison
3. Match band display (Strong / Moderate / Weak)
4. Matched skills list
5. Missing skills list
6. Improvement suggestions (3–5 actionable items)
7. Interview risk areas
8. A clean report card layout

The feature should:

- read the student profile from localStorage
- read the JD analysis from app state (produced in Session 2)
- send both to the AI as a single comparison prompt with labeled context
- display the structured output in a readable report card
- handle the case where profile or JD analysis is missing

## Strict Scope Control

### Include

- Reading student profile from localStorage
- Reading JD analysis from app state
- Composing a labeled comparison prompt with both contexts
- AI call to generate match report
- Match band (Strong / Moderate / Weak) display
- Matched skills list
- Missing skills list
- Improvement suggestions (3–5 items)
- Interview risk areas section
- Loading state while AI is processing
- Empty state when profile or JD analysis is not available
- Error state if AI call fails
- Report card UI component

### Do Not Include

- ATS scores or hiring probability percentages presented as facts
- Resume upload or resume rewriting
- Integration with job boards or external HR platforms
- Claiming any specific hiring decision or prediction
- Backend APIs or database storage
- User authentication
- Percentage-based match scores presented without explanation
- Sending or sharing the report card externally
- Complex resume parsing

Session 3 is only about using two saved contexts to generate an explainable AI comparison.

---

# Instructor Framing

## Opening Message

In Session 1 we built the profile. In Session 2 we analyzed the job description and extracted structured output. Now, in Session 3, we will connect those two pieces of information and ask AI a very specific question: How well does this student's profile match this job description?

This is not a guess. This is a structured AI comparison with labeled context and explainable output. That is a skill that very few developers understand — and it is exactly what interviewers will ask about.

Today's feature produces a match report card that shows not just a result but a reason. That is what explainable AI means.

## Key Philosophy

Students are not expected to code everything from scratch.

They are expected to:

- understand why two contexts need to be labeled before sending to AI
- understand what a match band is and why it is more honest than a percentage
- guide AI with a clear structured comparison prompt
- inspect and explain the generated report card code
- test the feature with their own profile and JD
- explain the AI concept in interview language

## Repeated Instructor Line

AI can compare two pieces of context, but you are responsible for understanding why the result came out that way and explaining it to an interviewer.

---

# Session Flow

## 0–10 min: Opening and Recap of Session 2 — JD Analyzer

### Instructor Goal

Reconnect students to the full project journey and set up why today's feature depends on both previous sessions.

### Recap Session 2

Ask students to recall what Session 2 produced:

- a JD analysis output with required skills extracted
- responsibilities list
- role type
- important interview topics
- difficulty level

This analysis is currently stored in the app state after the JD Analyzer runs.

### Set Up Today

Explain that in Session 3, we are not throwing away Session 2's output. We are feeding it into a new AI call alongside the student profile. This is the first time in the course that students will send two separate pieces of information to AI in a single prompt.

### Ask Students

What do you think AI needs to compare the profile with the JD?

Expected answers:

- the profile (name, skills, experience, target role)
- the JD analysis (required skills, responsibilities, role type)

Confirm: exactly. Both pieces must be present, labeled, and structured. If we send them unlabeled, the AI comparison will be vague or incorrect.

### Frame Today's Goal

By the end of this session, clicking "Check My Match" will produce a full match report card in under 10 seconds.

---

## 10–20 min: Product Breakdown Before Prompting

### Instructor Goal

Teach students to plan the feature output before writing the AI prompt or generating code.

### Ask Students

What should the match report card show?

Walk through these expected sections:

1. Overall match band — Strong, Moderate, or Weak
2. Matched skills — skills the student has that the JD needs
3. Missing skills — skills the JD needs that the student does not have
4. Improvement suggestions — 3 to 5 actionable steps the student can take
5. Interview risk areas — topics where the student is likely to struggle in the interview

### Explain the Match Band

A match band (Strong / Moderate / Weak) is not the same as a percentage score.

A percentage like "72% match" sounds precise but is not explainable. It is a black-box number.

A match band like "Moderate — you have core skills but are missing cloud deployment and system design" is explainable. It tells the student what to do.

In explainable AI, every result must come with a reason. Students should understand this principle.

### Convert into Feature List

1. "Check My Match" button
2. Loading state while AI is processing
3. Match band badge (Strong / Moderate / Weak)
4. Matched skills section
5. Missing skills section
6. Improvement suggestions section
7. Interview risk areas section
8. Empty state if profile or JD analysis is missing
9. Error state if AI call fails

### Instructor Control Rule

Do not let students add a percentage score. If a student asks "can we add a percentage?", explain that AI-generated percentages are not factual and would be misleading. The match band is deliberately qualitative to be honest.

---

## 20–35 min: Generate Add Profile vs JD Match Feature in AI Tool

### Instructor Goal

Use the main build prompt to generate the match feature on top of the existing app.

### What to Watch For in Generated Output

- Does the code read from localStorage for the student profile?
- Does it read the JD analysis from app state?
- Is the comparison prompt clearly labeled with two contexts?
- Does the AI call (Gemini 1.5 Flash via @google/generative-ai — free tier) return match band, matched skills, missing skills, suggestions, and risk areas?
- Is there a loading state?
- Is there an empty state when profile or JD is missing?
- Is the report card displayed cleanly?

### Instructor Walk-Through While Generation Runs

While the AI tool generates code, explain to students:

The most important part of today's prompt is how we label the two contexts. We do not just paste the profile and the JD together. We label them:

```
STUDENT PROFILE:
[profile content here]

JD ANALYSIS:
[JD analysis content here]
```

This labeling is what lets AI understand which information belongs to which context. Without labels, AI may mix them up or give a vague output.

### Instructor Control Rule

Use only the main build prompt for this segment. Do not let students add extra features during generation. First get the match report working correctly.

---

## 35–50 min: Instructor Walkthrough of Generated Feature

### Instructor Goal

Help students understand every significant part of the generated match feature code.

### Walkthrough Areas

1. Where the profile is read from localStorage
2. Where the JD analysis is read from app state
3. How the comparison prompt is composed — especially the labeling of two contexts
4. Where the AI call is made
5. How the AI response is parsed into match band, matched skills, missing skills, suggestions, and risk areas
6. How the report card component renders each section
7. Where the loading state is controlled
8. Where the empty state / error state is handled

### Ask During Walkthrough

- Which variable holds the student profile?
- Which variable holds the JD analysis?
- What does the comparison prompt look like before it is sent to AI?
- How does the app know the AI response is complete?
- Where is the match band stored after the AI responds?
- What happens if the student profile is empty when the user clicks "Check My Match"?

### Simple Explanation

The session 2 JD analyzer produced structured output. Session 3 takes that output and the profile, combines them with clear labels, sends a single AI call with a comparison instruction, and shows the result in a structured UI. This is the core pattern of multi-context AI features.

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students run the main build prompt on their existing app (which should already have the profile dashboard from Session 1 and the JD analyzer from Session 2) and build the match feature.

### Instructor Support Areas

Help students with:

- prompt paste issues
- JD analysis not being in app state (student may not have completed Session 2 correctly)
- profile reading from localStorage returning null
- AI call not triggering on button click
- match band not rendering
- report card sections not showing
- loading state not clearing after AI responds

### If Student Has Incomplete Session 2

If a student does not have the JD analyzer output in their app state, do not rebuild Session 2 during this session. Instead:

- let the student use a hardcoded sample JD analysis object for today
- instruct them to fix Session 2 after class
- do not block the class

### If Student Setup Fails Entirely

The student should:

- follow instructor screen and understand the feature conceptually
- pair with another student
- use the shared completed Session 3 code after class

---

## 65–80 min: Improve and Refine

### Instructor Goal

Once the basic match feature is working, improve the visual presentation of the report card.

### Expected Improvements

- color-coded match band badge (green for Strong, amber for Moderate, red for Weak)
- icon-separated sections for matched vs missing skills
- numbered list for improvement suggestions
- highlighted warning style for interview risk areas
- a message at the bottom: "This report is AI-generated. Use it as a guide, not a guarantee."

### Disclaimer Explanation

Walk students through why the disclaimer matters.

Explain: AI is comparing text. It does not know the hiring manager's exact criteria. A match band is a useful guide — it shows gaps and strengths — but it is not a hiring decision. Including a disclaimer is responsible AI design.

### Instructor Control Rule

The disclaimer is mandatory. Students should not remove it. This protects both the user and the student in interview discussion.

---

## 80–95 min: Edge Cases and Error States

### Instructor Goal

Teach students to think about failure scenarios, not just the happy path.

### Edge Cases to Implement

1. Student profile is empty (not saved yet) — show message: "Please complete your profile first before checking your match."
2. JD analysis is not available (JD Analyzer not run) — show message: "Please run the JD Analyzer first before checking your match."
3. AI call fails due to network or API error — show message: "Unable to generate match report. Please try again."
4. AI returns an incomplete response (missing sections) — handle gracefully, show what is available
5. Student has no skills listed in profile — match band should be Weak, missing skills should list all JD required skills

### Ask Students

What is the worst thing that could happen if we don't handle these edge cases?

Expected answers:

- app crashes
- user sees a blank screen
- user thinks the feature is broken
- user loses trust in the app

Confirm: handling edge cases is not optional polish. It is the difference between a demo and a real product.

---

## 95–105 min: Concept Pause — Context Management and Explainable AI Output

### Instructor Goal

Convert the implementation into interview-ready understanding of the AI concept.

### Explain Context Management

Context management is the practice of deciding what information to send to an AI model, how to label it, and how to structure the prompt so the AI can reason about multiple pieces of information correctly.

In today's feature:

- Context 1: the student profile (name, skills, target role, weak areas)
- Context 2: the JD analysis (required skills, responsibilities, role type, interview topics)

Both contexts are labeled clearly in the prompt. Without labeling, AI cannot distinguish between what belongs to the student and what belongs to the job.

### Explain Explainable AI Output

Explainable AI means every result must come with a reason.

A match band like "Moderate" without explanation is not explainable. It is just a label.

A match band like "Moderate — you have frontend skills but are missing cloud deployment and REST API design" is explainable. The user can act on it.

When we design the AI output schema for this feature, we force the AI to return:

- the band AND the reason
- matched skills AND the reason they match
- missing skills AND why they matter for the role
- suggestions AND what problem each suggestion solves
- risk areas AND why they are risky for this specific role

That structure is called explainable output design.

### Ask the Student Writing Task

Ask every student to write a 2–3 line answer:

Why does the match report show a band instead of a percentage?

Expected answer:

A percentage score from AI is not based on a verified formula. It would be misleading. A match band like Strong, Moderate, or Weak is qualitative and honest. It clearly communicates where the student stands without pretending to be a precise measurement.

---

## 105–115 min: Interview Discussion and Viva Practice

### Instructor Goal

Prepare students to speak confidently about the match feature and the AI concept behind it.

Use the interview questions section below.

Pick 3–5 questions per student if time allows.

Encourage students to answer in full sentences, not one-word answers.

---

## 115–120 min: Wrap-Up and Session 4 Preview

### Instructor Closing

Today we connected two pieces of saved context — the student profile and the JD analysis — and produced a structured, explainable match report. This is the first time in the app that AI is comparing information, not just extracting it.

Next session — Session 4 — we will add the Interview Question Generator. The app will use the JD analysis and the match report to generate interview questions targeted at the student's weak areas and missing skills. That will make the questions truly personalized.

---

# Instructor Notes

## What to Emphasize

Session 3 is the first session where students feel the real power of context management.

Emphasize:

- the difference between one-context AI calls (Session 2) and two-context AI calls (Session 3)
- why labeling both contexts is essential, not optional
- why match bands are more honest than percentages
- why the disclaimer "this is AI-generated, use it as a guide" must be present
- why explainable output has a reason attached to every result
- that the JD analysis from Session 2 is not discarded — it becomes an input for Session 3
- that students are building a pipeline, not isolated features

## Common Student Mistakes

1. Sending the raw JD text to the match prompt instead of the structured JD analysis from Session 2
2. Sending profile and JD analysis without labels — AI produces confused or mixed output
3. Asking AI for a percentage match score and displaying it as a fact
4. Not reading from localStorage for the profile — using hardcoded sample data instead
5. Building the report card before verifying the AI call returns correct data
6. Skipping the loading state — user sees a blank screen while AI processes
7. Not handling the case where profile or JD analysis is missing
8. Removing the disclaimer from the report card
9. Displaying raw AI output text instead of rendering structured sections
10. Trying to add resume upload or job board integration during this session

## How to Control the Session

Use this rule:

If a feature is not needed to display the match report card, do not add it in Session 3.

Session 3 only needs: profile read, JD analysis read, comparison prompt, AI call, and structured report card display.

## Setup Rule

Students must have a working Session 2 output before Session 3.

If a student's JD analyzer is broken, they should use a sample JD analysis object provided by the instructor and fix Session 2 after class.

Do not delay Session 3 to fix Session 2 live.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### Q1. What feature did you add in Session 3?

Expected answer:

In Session 3, I added a Profile vs JD Match feature to the AI Interview Prep Copilot. The feature reads the student profile saved in Session 1 and the JD analysis produced in Session 2, sends both to an AI with a structured comparison prompt, and displays a match report card. The report card shows the overall match band (Strong, Moderate, or Weak), matched skills, missing skills, improvement suggestions, and interview risk areas.

### Q2. What is a match band and why did you choose it over a percentage?

Expected answer:

A match band is a qualitative label — Strong, Moderate, or Weak — that summarizes how well a student's profile aligns with a job description. I chose a match band instead of a percentage because an AI-generated percentage is not based on a verified formula. It would be misleading to show "72% match" as if it were a precise measurement. A match band combined with reasons and specific gap areas is more honest and more actionable for the student.

### Q3. Where does the match feature get its input data from?

Expected answer:

The match feature reads two inputs. The student profile is read from localStorage, where it was saved in Session 1. The JD analysis — including required skills, responsibilities, role type, and interview topics — is read from the app state, where it was stored after the JD Analyzer ran in Session 2.

### Q4. What does the match report card display?

Expected answer:

The match report card displays five sections: the overall match band (Strong, Moderate, or Weak), a list of matched skills (skills the student has that the JD requires), a list of missing skills (skills the JD needs that the student does not have), three to five improvement suggestions with specific actionable steps, and a list of interview risk areas that highlight where the student may struggle in an interview for this role.

### Q5. Why did you add a disclaimer to the report card?

Expected answer:

The disclaimer reads: "This report is AI-generated. Use it as a guide, not a guarantee." I added it because AI is comparing text — it does not have access to the hiring manager's actual criteria or the company's internal evaluation rubric. The match report gives useful guidance on gaps and strengths, but it is not a hiring decision. Including the disclaimer is responsible AI design and protects the user from over-relying on the AI output.

---

## App Flow Questions

### Q6. Walk me through what happens when the user clicks "Check My Match".

Expected answer:

When the user clicks "Check My Match", the app first checks whether a saved student profile exists in localStorage and whether a JD analysis is available in app state. If either is missing, it shows an appropriate message asking the user to complete the missing step first. If both are available, the app composes a labeled comparison prompt with the profile under a "STUDENT PROFILE" heading and the JD analysis under a "JD ANALYSIS" heading. It sends this prompt to the AI and displays a loading state. When the AI responds, the app parses the structured output and renders the report card with the match band, matched skills, missing skills, suggestions, and risk areas.

### Q7. What happens if the student profile is missing when the user tries to check their match?

Expected answer:

If the student profile is not found in localStorage — meaning the user has not completed Session 1's profile form — the app displays a message: "Please complete your profile first before checking your match." The match report is not generated. This prevents the AI from receiving an empty profile and producing a meaningless or confusing result.

### Q8. What happens if the JD analysis is not available?

Expected answer:

If the JD analysis is not in the app state — meaning the user has not run the JD Analyzer from Session 2 — the app shows a message: "Please run the JD Analyzer first before checking your match." The feature depends on the structured JD analysis output, not just the raw job description text. Without the analyzed output, the comparison would be less structured and less useful.

### Q9. How is the AI response turned into the report card sections?

Expected answer:

The AI is prompted to return its response in a specific structured format — either as labeled sections or as a JSON object — with separate fields for match band, matched skills, missing skills, improvement suggestions, and risk areas. The app then parses this structured response and maps each field to the corresponding UI section in the report card. If a section is missing in the response, the app handles it gracefully rather than crashing.

### Q10. What happens when the AI call fails due to a network error?

Expected answer:

If the AI call fails due to a network issue or API error, the app clears the loading state and shows an error message: "Unable to generate match report. Please try again." The report card is not shown in an incomplete state. This prevents the user from seeing a blank or broken card and gives them a clear action to take.

---

## AI Topic Questions: Context Management and Explainable AI Output

### Q11. What is context management in AI applications?

Expected answer:

Context management is the practice of deciding what information to include in an AI prompt, how to label it, and how to structure it so the AI model can reason about multiple pieces of information correctly. In Session 3, context management means combining two inputs — the student profile and the JD analysis — into a single prompt with clear labels for each. This allows the AI to understand which information belongs to the student and which belongs to the job, and to compare them accurately.

### Q12. Why does the comparison prompt label the two contexts separately?

Expected answer:

Without labels, AI treats all text in the prompt as a single undifferentiated block of information. If we paste the profile and the JD analysis together without labels, the AI may mix up which skills belong to the student and which are required by the job. By labeling the two contexts — with headings like "STUDENT PROFILE:" and "JD ANALYSIS:" — we give the AI clear structure to follow. This is a fundamental principle of multi-context prompt design.

### Q13. What does explainable AI mean, and how did you implement it in this feature?

Expected answer:

Explainable AI means that every output should come with a reason, not just a result. In this feature, the match band is not a standalone label. It is accompanied by specific matched skills that explain why the band is what it is. The missing skills list explains the gap. The improvement suggestions explain what the student should do about the gap. The risk areas explain where the gap creates interview risk. Every section answers both "what" and "why". That is the implementation of explainable AI output.

### Q14. What is the difference between a one-context AI call and a two-context AI call?

Expected answer:

A one-context AI call sends a single piece of information to the AI for processing. For example, in Session 2, we sent the raw job description to the JD Analyzer and asked it to extract skills and responsibilities. A two-context AI call sends two separate pieces of information — each labeled — and asks the AI to reason about the relationship between them. In Session 3, we send the student profile as Context 1 and the JD analysis as Context 2, and ask the AI to produce a structured comparison. Two-context calls require more careful prompt design because the AI must understand both pieces and their relationship.

### Q15. If a recruiter asks: "How accurate is your match report?", how do you answer?

Expected answer:

The match report is an AI-assisted analysis, not a verified recruitment metric. It is based on comparing the text of the student profile with the text of the JD analysis. AI identifies overlaps and gaps in skills and responsibilities as described in both documents. It does not access the hiring manager's private criteria, the company's internal scoring rubric, or any external HR database. The match band — Strong, Moderate, or Weak — is a qualitative guide to help the student understand where they need to improve. It is not a prediction of hiring outcome. That is why we include a disclaimer on every report card.

---

# Session 3 Completion Checklist

Students should complete the following by the end of the session:

- [ ] "Check My Match" button is visible in the app
- [ ] App reads student profile from localStorage correctly
- [ ] App reads JD analysis from app state correctly
- [ ] Comparison prompt labels both contexts separately
- [ ] AI call is triggered on button click
- [ ] Loading state is shown while AI is processing
- [ ] Match band (Strong / Moderate / Weak) is displayed in the report card
- [ ] Matched skills section is displayed
- [ ] Missing skills section is displayed
- [ ] Improvement suggestions (3–5 items) are displayed
- [ ] Interview risk areas section is displayed
- [ ] Disclaimer is present on the report card
- [ ] Empty state message shows when profile is missing
- [ ] Empty state message shows when JD analysis is missing
- [ ] Error state shows when AI call fails
- [ ] Student can explain the AI concept (context management and explainable output) in 2 minutes

---

# Instructor Backup Plan

If the AI tool generation fails or student setup issues take too long:

1. Instructor continues live build on screen using the main build prompt.
2. Students follow conceptually and take notes on the match report sections.
3. Share the final Session 3 code after the session.
4. Students use the provided prompts later to regenerate or fix their app.
5. Do not sacrifice the Concept Pause or the interview discussion section — these are the most important parts for placement readiness.
6. If AI is generating but slowly, use the wait time to walk through the comparison prompt structure on the whiteboard or shared screen and explain context labeling in detail.

### Gemini API Key Troubleshooting

If a student's AI calls are failing, check these in order:

- Confirm the `.env` file exists in the project root (same folder as `package.json`) and contains `VITE_GEMINI_API_KEY=...` with no extra spaces or quotes around the key
- Confirm the student restarted the Vite dev server after creating or editing the `.env` file — changes to `.env` are not picked up automatically
- Confirm the student installed the package: `npm install @google/generative-ai` must have been run in the project folder
- If the student hits a rate limit error: the free tier allows 15 requests per minute — ask the student to wait 1 minute and try again
- If the key itself is invalid: the student should return to aistudio.google.com, copy the key again, and paste it fresh into the `.env` file
