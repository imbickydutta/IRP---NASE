# Session 4 Instructor File: Add Interview Question Generator

## Session Title

Add Interview Question Generator

## Duration

2 hours

## Project

AI Interview Prep Copilot

## Session 4 Objective

By the end of Session 4, students should have a working Interview Question Generator that reads the JD analysis, student profile, and match report from app state and produces a categorized set of targeted interview questions.

Students should understand how prompt chaining works in practice — how one feature's output becomes the next feature's input — and be able to explain this concept clearly in an interview setting.

## Session 4 Deliverable

Students will add an Interview Question Generator feature to the existing app that:

1. Reads JD analysis output from Session 2
2. Reads student profile from Session 1
3. Reads match report from Session 3 (match band, missing skills, risk areas)
4. Builds a chained context prompt from all three sources
5. Generates 5 technical questions
6. Generates 3 project-based questions
7. Generates 2 HR questions
8. Generates 2 scenario-based questions
9. Displays all 12 questions in clearly labelled, collapsible sections
10. Adds a copy button for each category
11. Stores generated questions in app state for use in Session 5

## Strict Scope Control

### Include

- Read JD analysis, student profile, and match report from app state
- Build a chained context prompt combining all three sources
- Generate 12 questions across 4 labelled categories
- Display questions in collapsible sections with category headers
- Copy button for each category
- Regenerate button
- Store generated questions in app state
- Loading state during generation
- Empty state when no profile or JD is available
- Session 5 navigation label visible

### Do Not Include

- Full mock interview room
- Question bank database
- Voice input or output
- Answer evaluation (that is Session 5)
- Timed interview mode
- AI voice features
- External question APIs
- Answer suggestions or hints
- Difficulty rating system
- Question filtering or sorting
- User-added custom questions

Session 4 is only about generating and displaying the questions. Evaluating answers is Session 5.

---

# Instructor Framing

## Opening Message

In Sessions 1, 2, and 3, we built three separate pieces. Today those pieces stop being separate. The question generator we build in Session 4 will read the JD analysis from Session 2, the student profile from Session 1, and the match report from Session 3 — and combine them into a single rich prompt that generates 12 targeted interview questions.

This is prompt chaining. One feature's output becomes the next feature's input. That is how real AI products work.

## Key Philosophy

Students are not expected to write the question generation logic by hand.

They are expected to:

- understand how context accumulates across features
- construct a chained prompt that includes all prior outputs
- verify that the generated questions are targeted, not generic
- test all four question categories
- explain prompt chaining in their own words during a viva

## Repeated Instructor Line

The more context you give AI, the more personalized and useful its output becomes. That is what prompt chaining achieves.

---

# Session Flow

## 0–10 min: Opening and Recap of Session 3 — Add Profile vs JD Match

### Instructor Goal

Reorient students, confirm all prior work is in place, and connect today's feature to what has already been built.

### Ask the Class

Ask three quick questions before moving forward:

- What does the JD Analyzer output? (skills, responsibilities, role type, topics)
- What does the Match Report output? (match band, missing skills, risk areas)
- Where is all this data stored? (app state, localStorage)

If students cannot answer these confidently, spend an extra two minutes reviewing the match report UI before proceeding.

### Recap Diagram

Draw or show this on screen:

Session 1 → Profile (name, role, skills, projects, weak areas, JD)
Session 2 → JD Analysis (skills required, role type, topics)
Session 3 → Match Report (match band, missing skills, risk areas)
Session 4 → Question Generator reads all of the above and generates targeted questions

### Set Today's Goal

By the end of this session, the app will generate 12 interview questions — technical, project-based, HR, and scenario-based — that are specific to this student's profile and this job description, not generic.

---

## 10–20 min: Product Breakdown Before Prompting

### Instructor Goal

Teach students to think like a product designer before they touch the prompt. This prevents vague generation and scope creep.

### Ask Students

If you had to prepare interview questions for a student manually, what information would you need?

Expected answers:

- the job description
- the student's skills and projects
- which skills the student is missing
- which areas are risky

### Convert Into Feature Components

Walk through this list with the class:

1. Input source: JD analysis (from app state, not re-entered)
2. Input source: student profile (from app state)
3. Input source: match report — match band, missing skills, risk areas (from app state)
4. Context block: combine all three into one structured prompt
5. Output: 5 technical questions
6. Output: 3 project-based questions
7. Output: 2 HR questions
8. Output: 2 scenario-based questions
9. UI: collapsible sections per category
10. UI: copy button per category
11. State: store output for Session 5

### Key Instructor Point

The reason our questions will be better than any generic question list is that we are giving AI the student's actual profile, their actual JD, and their actual gaps. That is context-aware generation — and it is only possible because we built the earlier features first.

---

## 20–35 min: Generate Add Interview Question Generator Feature in AI Tool

### Instructor Goal

Use Prompt 1 from the student file to generate the Interview Question Generator feature.

### Run the Main Build Prompt

Use the prompt prepared in the pre-session file. The prompt includes:

- full recap of what is already built
- where JD analysis is stored in app state
- where match report is stored
- what to generate (12 questions, 4 categories)
- how to display them (collapsible sections, copy button)
- what NOT to add (no answer evaluation, no voice, no database)
- comment requirements

### What to Watch For

- Does the feature read from existing app state rather than asking the user to re-enter data?
- Are all four categories present: Technical, Project-Based, HR, Scenario-Based?
- Does each category have the correct count (5, 3, 2, 2)?
- Is there a collapsible section for each category?
- Is there a copy button?
- Is there a regenerate button?
- Are the generated questions actually tied to the JD and profile, not generic?
- Is the loading state shown during generation?

### Instructor Control Rule

Do not let students add features that are not in the scope list. If AI generates answer evaluation, scoring, or voice features, tell students to ask AI to remove those immediately.

---

## 35–50 min: Instructor Walkthrough of Generated Feature

### Instructor Goal

Help students understand what AI generated and how it uses context.

### Walkthrough Areas

1. Where is the context assembled from app state
2. How the chained prompt is constructed (show the actual prompt string being built)
3. Where the AI call is made
4. How the response is parsed into four categories
5. How collapsible sections are rendered
6. Where the copy button logic lives
7. Where the questions are stored in app state

### Ask During Walkthrough

- Where does the app read the JD analysis? Point to that line.
- Where does the app read the match report? Point to that line.
- What does the combined prompt look like? Can you read it in the code?
- Why do we store questions in app state? (For Session 5 to use them)
- What would happen if the student had not saved a profile? (Empty state should handle it)

### Key Instructor Point

Make sure students see the actual combined prompt string in the code. This is the most important part of the session. Students need to see that the prompt is built by concatenating multiple pieces of stored data — that is the prompt chain.

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students run the main build prompt in their own environment and add the Interview Question Generator feature to their existing app.

### Instructor Support Areas

Help students with:

- app state not carrying JD analysis or match report from previous sessions
- questions not separated into four categories
- copy button not functioning
- collapsible sections not toggling
- AI generating generic questions (context not passed correctly)
- regenerate button not triggering a new call

### If Student App State Is Missing Prior Data

This is the most common blocker in Session 4. If a student did not complete Sessions 2 or 3, their app state will not have JD analysis or match report data. Handle this by:

- giving the student a hardcoded sample state object to paste in
- having them use the instructor's built app for reference
- not blocking the rest of the class

### If Student Setup Fails

The student should:

- follow instructor screen
- pair with another student
- use the shared Session 4 code after class

---

## 65–80 min: Improve and Refine

### Instructor Goal

Move from a working feature to a well-structured feature that feels like part of a real product.

### Expected Improvements

- polish collapsible section headers with question counts (e.g., "Technical Questions (5)")
- add a progress message: "Questions generated based on your profile and JD match"
- add a small context summary above the questions: "Generated for: [role] | Match: [band] | Missing: [n] skills"
- make the regenerate button prominent
- ensure copy button shows a brief confirmation ("Copied!")
- ensure the section is scrollable if many questions are displayed

### Ask Students to Test

Before moving on, every student should verify:

- Do the questions mention topics from their JD?
- Do the project-based questions reference their actual project names?
- Do the HR questions reference their target role?
- Does copy work on each category?

---

## 80–95 min: Edge Cases and Error States

### Instructor Goal

Teach students to think about failure modes and incomplete data states.

### Must Handle

1. No profile saved — show message: "Please complete your profile before generating questions."
2. No JD saved — show message: "Please enter a job description before generating questions."
3. No match report available — show message: "Please run the Profile vs JD Match before generating questions."
4. AI call fails — show message: "Question generation failed. Please try again."
5. Partial context — warn user that questions may be less targeted if match report is missing
6. Empty question category — show placeholder rather than empty collapsed section

### Ask the Class

What would happen if a student skips Session 3 and tries to use the question generator directly?

Expected answer: The app should detect that match report data is missing and show a helpful warning rather than crashing or generating with incomplete context.

### Instructor Explanation

Edge cases make an app professional. An app that only works for perfect inputs is not a real product. Handling missing context gracefully is as important as the happy path.

---

## 95–105 min: Concept Pause — Prompt Chaining and Contextual Question Generation

### Instructor Goal

Convert implementation into interview-ready conceptual understanding.

### Explain the Flow

User completes profile in Session 1
↓
JD Analyzer extracts skills and topics in Session 2
↓
Match Report identifies gaps and risk areas in Session 3
↓
Question Generator reads all three outputs
↓
Builds a single chained context prompt
↓
AI generates questions specific to this student and this JD
↓
Questions stored in app state for Session 5 answer evaluator

### Plain Language Explanation

Before today, each feature was independent. The JD analyzer analyzed the JD. The match report compared profile and JD. But neither of those results was feeding into anything else.

Today we connected them. The question generator does not start from scratch. It inherits everything we have already computed. That is prompt chaining — each feature passes its output forward so the next feature can work with richer context.

This is important in interviews because it shows you understand how AI products are designed. You are not just using AI once. You are building a pipeline where AI outputs accumulate and improve each next step.

### Student Writing Task

Ask every student to write a 2–3 line answer:

What is prompt chaining and how does it work in this app?

Expected answer:

Prompt chaining means using one feature's output as input for the next feature. In this app, the JD analysis and match report outputs are combined with the student profile to build a rich context prompt for the question generator. This makes the generated questions specific to this student's situation rather than generic.

---

## 105–115 min: Interview Discussion and Viva Practice

### Instructor Goal

Prepare students to speak confidently about Session 4 in technical and HR interview settings.

Use the questions in the Interview Questions section below.

Run at least 5 questions with the full class. Pick one or two students for live viva practice.

Encourage students to answer in 3–5 sentences, not one-liners.

---

## 115–120 min: Wrap-Up and Session 5 Preview — Add Mock Answer Evaluator

### Instructor Closing

Today we added the Interview Question Generator. This feature does not just generate questions — it generates questions that are specific to your profile, your JD, and your skill gaps. That is the power of prompt chaining.

In Session 5, we will add the Mock Answer Evaluator. The user will type an answer to one of the generated questions, and the app will evaluate it using AI — giving a score, identifying what was good, and pointing out what was missing.

The questions we stored in app state today will be the input for Session 5. The chain continues.

---

# Instructor Notes

## What to Emphasize

Session 4 is not about generating more AI content. It is about making AI content smarter by giving it richer context.

The key shift students need to understand:

- generic questions come from no context
- targeted questions come from combining profile, JD, and gap data
- this is only possible because Sessions 1, 2, and 3 built that context first

Emphasize the moment students see questions that mention their actual role, their actual project, and their actual missing skills. That is the most powerful teaching moment of the session.

## Common Student Mistakes

1. Re-entering profile data into the question generator manually instead of reading it from app state
2. Generating only one category of questions instead of all four
3. Missing the exact question counts (5 technical, 3 project, 2 HR, 2 scenario)
4. Adding answer evaluation inside Session 4 (must stay out of scope)
5. Not checking whether questions are actually personalized to the JD and profile
6. Forgetting to store generated questions in app state for Session 5
7. Not adding a loading state while the AI call is in progress
8. Not handling the edge case where match report is missing
9. Spending too much time customizing question categories instead of getting the core working first
10. Asking AI to add a question bank or database (outside scope — questions are always generated fresh)

## How to Control the Session

Use this rule:

If a feature is not needed for Session 5, do not build it in Session 4.

Session 4 only needs to generate and display the 12 questions and store them in app state.

If students ask about adding difficulty levels, topic filters, or voice features, note them as Session 7 or later enhancements and move on.

## Setup Rule

Do not spend more than 5 minutes troubleshooting missing app state from prior sessions.

If a student's app is missing JD analysis or match report data, give them a hardcoded sample object and move forward.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### Q1. What did you build in Session 4?

Expected answer:

In Session 4, I added an Interview Question Generator to the AI Interview Prep Copilot. This feature reads the JD analysis, student profile, and match report from app state, combines them into a chained context prompt, and generates 12 interview questions across four categories: 5 technical questions, 3 project-based questions, 2 HR questions, and 2 scenario-based questions. The questions are displayed in collapsible sections with a copy option and are stored in app state for the Session 5 answer evaluator.

### Q2. What is the input to the question generator?

Expected answer:

The input is not user-entered data at this stage. The question generator reads three pieces of data already stored in app state: the student profile saved in Session 1 (name, role, skills, projects, weak areas), the JD analysis output from Session 2 (required skills, role type, topics), and the match report from Session 3 (match band, missing skills, risk areas). All three are combined into a single context-rich prompt before the AI call is made.

### Q3. Why are the generated questions better than a generic question list?

Expected answer:

Because they are built from the student's actual profile, their actual job description, and their actual skill gaps. A generic question list is the same for everyone. Our generated questions reference the student's target role, the specific skills required in their JD, the projects they have listed, and the areas where they scored low in the match report. That specificity makes the questions far more useful for actual interview preparation.

### Q4. Why do we have four separate categories of questions?

Expected answer:

Because different parts of an interview require different types of questions. Technical questions test domain knowledge. Project-based questions test what the student actually built and how they think. HR questions test communication, motivation, and culture fit. Scenario-based questions test judgment and problem-solving under real-world conditions. Separating them helps the student prepare each area deliberately rather than treating all questions the same.

### Q5. Why do we store the generated questions in app state?

Expected answer:

Because Session 5 needs them. The Mock Answer Evaluator in Session 5 will show the student one question at a time and evaluate their typed answer. It reads the questions directly from app state rather than regenerating them each time. Storing them here ensures continuity across sessions and prevents unnecessary repeated AI calls.

---

## App Flow Questions

### Q6. How does the chained context prompt get built in this feature?

Expected answer:

The app reads three separate pieces of stored data from app state: the student profile, the JD analysis, and the match report. It then assembles them into a single structured prompt string. The prompt includes context blocks for each data source — the student's name, role, and skills; the JD's required skills and role type; and the match band, missing skills, and risk areas from the match report. The prompt also specifies the exact output format: 12 questions in four labelled categories. This assembled string is then sent to the AI in one call.

### Q7. What happens if the match report is not available when the user tries to generate questions?

Expected answer:

The app checks app state before making the AI call. If the match report data is missing, it shows a clear message telling the user to run the Profile vs JD Match first. It does not crash or generate with incomplete context. This is an important edge case because users might try to use Session 4 without having completed Session 3, and the app needs to guide them gracefully rather than breaking silently.

### Q8. What is the loading state and why is it needed?

Expected answer:

The loading state is a visual indicator shown while the AI call is in progress. It typically shows a spinner or message like "Generating your questions..." The loading state is needed because AI calls take a few seconds and the app must not appear frozen or unresponsive during that time. Without a loading state, users may click the generate button multiple times thinking it is not working, which could cause duplicate calls or unexpected behavior.

### Q9. How does the copy button work in this feature?

Expected answer:

Each question category has its own copy button. When clicked, it reads the list of questions for that category and copies them to the clipboard using the browser's clipboard API. The button then briefly changes its label to "Copied!" as visual confirmation before returning to its default state. This makes it easy for students to paste the generated questions into a notes document or study sheet without manually selecting text.

### Q10. What is the difference between this feature and a question bank?

Expected answer:

A question bank is a pre-stored collection of fixed questions that all users draw from. Our question generator creates questions fresh each time using the specific context of that student. No two students will get the same set of questions because their profiles, JDs, and match reports are different. This is the core advantage — the questions are generated, not retrieved. They adapt to the context rather than being one-size-fits-all.

---

## AI Topic Questions — Prompt Chaining and Contextual Question Generation

### Q11. What is prompt chaining?

Expected answer:

Prompt chaining is a technique where the output of one AI prompt is used as input for the next. Instead of making one large AI call with all context upfront, you build context progressively — each step in the app adds more information that the next step can use. In our app, the JD analyzer produces structured output in Session 2, the match report adds gap analysis in Session 3, and the question generator combines both with the student profile in Session 4. Each output feeds the next prompt, creating a chain of context-rich AI interactions.

### Q12. Why is accumulated context better than a single flat prompt?

Expected answer:

A single flat prompt has to do everything at once: analyze the JD, compare the profile, identify gaps, and generate questions. That is too much for one prompt and makes it harder to debug when something goes wrong. Accumulated context breaks the work into focused steps. Each step is easier to test and verify. By the time we reach the question generator, the context is already structured and validated from prior steps. The AI call in Session 4 only has to do one job: generate questions from a clean, pre-processed context block.

### Q13. How would you explain prompt chaining in a technical interview?

Expected answer:

I would say: prompt chaining is a design pattern where each AI call in an application is informed by the output of previous calls or user interactions. Instead of giving AI all context upfront in one call, you accumulate it step by step. In my app, the student profile is collected first, then the JD is analyzed, then the gap is calculated — and by the time we generate interview questions, we have a rich context object that makes the generated output specific and accurate. This mirrors how pipelines work in software engineering — data is processed in stages and each stage feeds the next.

### Q14. What is the difference between a generic AI prompt and a context-aware AI prompt?

Expected answer:

A generic prompt gives AI minimal or no context about the specific user. For example: "Generate 10 interview questions for a software engineer." The output will be broad and applicable to anyone. A context-aware prompt includes the user's specific profile, JD, and skill gaps. For example: "Given that this student is applying for a Junior AI Engineer role, has experience in React and prompt engineering, is missing backend skills, and has been flagged as medium risk in data structures — generate 5 technical questions targeting those gaps." The second prompt produces questions that are directly useful for this student's actual interview.

### Q15. How would you explain this feature if an interviewer asks: "Tell me about a feature that uses AI intelligently, not just as a black box"?

Expected answer:

I would say: in my AI Interview Prep Copilot, the Interview Question Generator uses AI with accumulated context rather than a single isolated call. By the time the question generator runs, it already has the student's profile, the JD analysis, and the match report. It uses all three to build a structured prompt that asks AI to generate questions targeting the student's specific skill gaps and experience. The questions are categorized into technical, project-based, HR, and scenario types. This is not AI being used as a black box — it is AI being used as a structured reasoning engine with rich, deliberate input. I can explain what goes into the prompt, what comes out, how it is parsed, and how it is stored for the next feature.

---

# Session 4 Completion Checklist

Students should complete the following by the end of the session:

- [ ] Question Generator reads JD analysis from app state (not re-entered manually)
- [ ] Question Generator reads student profile from app state
- [ ] Question Generator reads match report from app state
- [ ] Combined context prompt is constructed from all three sources
- [ ] 5 technical questions are generated and displayed
- [ ] 3 project-based questions are generated and displayed
- [ ] 2 HR questions are generated and displayed
- [ ] 2 scenario-based questions are generated and displayed
- [ ] Each category is displayed in a collapsible section with a label
- [ ] Copy button works for each category
- [ ] Loading state is visible during AI call
- [ ] Generated questions are stored in app state for Session 5

---

# Instructor Backup Plan

If AI tool generation fails or setup issues take too long:

1. Instructor continues the live build on screen.
2. Students follow conceptually and note the prompt structure.
3. Instructor walks through the context assembly logic manually.
4. Share the final Session 4 code after the session.
5. Students use the prompts later to regenerate or fix their version.
6. Do not sacrifice the concept pause or interview discussion sections — the conceptual understanding of prompt chaining is non-negotiable for this session.
