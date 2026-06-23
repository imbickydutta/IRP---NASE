# Session 7 Instructor File: Add AI Prep Plan Agent

## Session Title

Add AI Prep Plan Agent

## Duration

2 hours

## Project

AI Interview Prep Copilot

## Session 7 Objective

By the end of Session 7, students should have a working AI Prep Plan Agent inside the app. The agent takes the student's target role, weak topics, days until interview, and daily available hours, then generates a personalized 7-day interview preparation plan with day-wise topics, specific practice questions, and a mock task for each day, plus a final revision checklist — all displayed in the app as collapsible day cards.

Students should also be able to explain the difference between an AI agent and a chatbot, and articulate how AI uses goals and constraints to produce structured multi-step plans.

## Session 7 Deliverable

Students will add a new section to the existing AI Interview Prep Copilot app with:

1. An AI Prep Plan Agent input form
2. Target Role input (pre-filled from saved profile)
3. Weak Topics input (pre-filled from saved profile weak areas)
4. Days Until Interview input
5. Daily Available Hours input
6. Generate Plan button
7. 7 collapsible day cards displaying topic, questions, and mock task per day
8. A Final Revision Checklist section at the bottom of the plan

---

## Strict Scope Control

### Include

Inputs: target role, weak topics, days until interview, daily hours. Output: 7-day plan displayed in the app UI as day cards with topic, questions, and task. All rendered inside the app.

- Prep Plan input form with 4 inputs
- Pre-fill target role and weak topics from saved localStorage profile
- Generate 7-day plan using a structured AI prompt call
- Display plan as 7 collapsible day cards in the app UI
- Each day card: day number, topic for the day, 3–5 practice questions, 1 mock task
- Final revision checklist rendered inside the app
- Loading state while plan is being generated
- Empty state if no plan has been generated yet
- Basic error handling if generation fails

### Do Not Include

Mandatory n8n or webhook integration, mandatory Google Sheets export, external calendar sync, email notifications, deployment — these can be shown as instructor demo or optional stretch only.

- Mandatory n8n integration
- Mandatory webhook or external API setup beyond the AI call
- Mandatory Google Sheets export
- External calendar sync
- Email notifications
- Deployment
- Multi-user support
- Backend database storage of the plan
- Audio or voice features
- PDF export (can be shown as optional stretch or instructor demo)

Session 7 is only about building the plan generation and the collapsible day card display inside the app.

---

# Instructor Framing

## Opening Message

In the last session we added the RAG-Lite Doubt Solver. The app can now answer concept questions from a knowledge base. Today we add the most strategic feature of the entire app: the AI Prep Plan Agent.

This is not a chatbot. A chatbot responds to one message. An agent takes your goals and constraints, thinks through the full problem, and produces a structured multi-step action plan. Today's feature is a real-world example of AI acting as a planner, not just a responder.

Students will also practice the most important interview distinction in AI product building: agent versus chatbot.

## Key Philosophy

Students are not expected to code a planner algorithm from scratch.

They are expected to:

- design the inputs and outputs clearly before prompting
- write a structured prompt that gives the AI enough context to generate a useful plan
- understand what the generated feature does
- test the plan output
- debug issues using AI
- explain agent behavior in interview language

## Repeated Instructor Line

AI can generate the plan, but you are responsible for understanding, testing, and explaining it.

---

# Session Flow

## 0–10 min: Opening and Recap of Session 6 — Add RAG-Lite Doubt Solver

### Instructor Goal

Connect Session 6 to Session 7, and frame today's feature as a natural next step in the app.

### Recap Session 6

Ask two students:

- What did we add in Session 6?
- How does the RAG-Lite Doubt Solver work?

Expected answers:

- We added a Doubt Solver that takes a student question and searches a local knowledge base to give an answer.
- The student types a question, the app finds the most relevant content from a set of topic summaries, and AI returns an answer based on that context.

### Bridge to Session 7

After building a Doubt Solver, the natural question is: "What should I study, and in what order?" Today we build a feature that answers exactly that. The student enters their target role, weak areas, time available, and the AI produces a structured plan — not one response, but a complete 7-day roadmap.

### Instructor Energy Check

Ask students:

- How many of you have a real interview coming up?
- How many of you would use this feature for actual prep?

This warms the room and makes the session personal.

---

## 10–20 min: Product Breakdown Before Prompting

### Instructor Goal

Teach students to define the inputs and outputs of a feature before writing a single prompt.

### Ask Students: What Does a Study Plan Need as Input?

Expected answers:

- what role you are preparing for
- what topics you are weak in
- how many days you have
- how many hours you can give per day

### Ask Students: What Should the Plan Output?

Expected answers:

- a day-by-day topic list
- practice questions for each day
- a task or exercise for each day
- something to revise at the end

### Convert Into Feature Spec

Write this on the board or share on screen:

Inputs:
1. Target role — from profile
2. Weak topics — from profile
3. Days until interview
4. Daily hours available

Outputs:
1. 7 day cards with: topic, 3–5 questions, 1 mock task per day
2. Final revision checklist

UI:
- Collapsible cards so the plan is not overwhelming
- Pre-filled inputs from localStorage profile

### Instructor Explanation

Before writing any prompt, we know exactly what to ask the AI to build. A vague prompt gives a vague plan. A defined spec gives a usable feature.

---

## 20–35 min: Generate Add AI Prep Plan Agent Feature in AI Tool

### Instructor Goal

Use Prompt 1 (Main Build Prompt) to generate the full feature.

### What to Watch For

- Does the form show 4 inputs?
- Are Target Role and Weak Topics pre-filled from localStorage?
- Does clicking Generate Plan send the request to AI?
- Is the output structured as 7 day cards?
- Does each card show topic, questions, and mock task?
- Is the final revision checklist rendered?
- Is there a loading state while plan generates?

### Instructor Control Rule

Do not let students adjust the UI style or add extra features before the base feature works. The rule is: generate first, verify second, improve third.

### If AI Generates Too Little

If the output is only a text block and not structured day cards, show students how to add a follow-up prompt to restructure the output into collapsible cards.

### If AI Generates Too Much

If AI adds email export, n8n, or calendar sync, use the scope control prompt to trim the output.

---

## 35–50 min: Instructor Walkthrough of Generated Feature

### Instructor Goal

Help students understand what the generated code is doing before they build it themselves.

### Walkthrough Areas

1. The form and its 4 input fields
2. How target role and weak topics are pre-filled from localStorage
3. The Generate Plan button and its click handler
4. The AI prompt being sent — show students the actual prompt string in the code
5. How the AI response is parsed into 7 day objects
6. How the day cards are rendered in the UI
7. The collapse/expand logic for each day card
8. The final revision checklist rendering

### Ask During Walkthrough

- Where does the app read the saved profile from?
- What does the prompt sent to AI look like?
- How does the app decide which day gets which topic?
- Where is the response parsed into day-by-day data?
- What triggers the card to expand or collapse?

### Simple Explanation

The AI is not writing the plan randomly. The prompt tells it: here is the role, here are the weak areas, here is the time constraint. The AI produces a structured output, and our code displays that output as day cards. We wrote the container; AI filled the content.

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students run Prompt 1 in their own AI tool and add the Prep Plan Agent feature to their existing app.

### Instructor Support Areas

Help students with:

- profile data not pre-filling in the form inputs
- Generate Plan button not triggering the AI call
- AI response not parsing into structured day cards
- Day cards not collapsing or expanding
- Final revision checklist not rendering

### If Student Setup Fails

Do not block the class.

The student should:

- follow the instructor screen closely
- note the key steps
- pair with another student who has the feature running
- use the prompts to regenerate after class

---

## 65–80 min: Improve and Refine

### Instructor Goal

Upgrade the feature from a basic implementation to a polished, interview-ready one.

### Expected Improvements

- Add a loading spinner or message while plan is generating
- Improve day card styling — show day number as a badge
- Add a "Collapse All / Expand All" button
- Add a "Regenerate Plan" option
- Show a short summary header above the plan: "Your 7-Day Plan for [Role]"
- Highlight weak topics in the plan with a badge or color

### Use Prompt 2 for UI Improvements

Walk through the UI improvement prompt as a class, then let students apply it.

### Instructor Explanation

A feature that works is good. A feature that works and communicates clearly to the user is interview-ready. Show students how small UX improvements are also product-thinking signals in interviews.

---

## 80–95 min: Edge Cases and Error States

### Instructor Goal

Teach students to think about what happens when things go wrong.

### Must Handle

1. User clicks Generate Plan without filling in days or hours — show a validation error
2. AI returns a malformed or unexpected response — show a fallback error message
3. Profile is not saved in localStorage — show a prompt to complete profile first
4. Daily hours is 0 or extremely small — show a friendly note that the plan may be compressed
5. Days until interview is 1 or less — show a message: "Only 1 day left — here is a focused final revision plan"

### Instructor Explanation

Good apps handle failure gracefully. In interviews, the ability to identify edge cases shows you think like an engineer, not just a builder. Students who can list edge cases always impress interviewers.

### Ask Students

What else could go wrong with this feature?

Expected answers:

- internet is down and AI call fails
- user enters 0 hours and plan makes no sense
- user enters a very unusual role and AI gives generic output
- user regenerates and the plan changes completely each time

---

## 95–105 min: Concept Pause — AI Agents and Planning

### Instructor Goal

Convert the built feature into a clear, explainable AI concept for interviews.

### Explain the Agent vs Chatbot Distinction

A chatbot:
- waits for one input
- gives one response
- has no memory of goals across turns
- does not structure a multi-step output

An agent:
- receives a goal and constraints
- breaks the goal into steps
- produces a structured multi-step output
- can take actions based on the output
- acts more like a planner than a responder

### Explain the Flow

Student enters: role, weak topics, days, hours  
↓  
App reads saved profile from localStorage  
↓  
App constructs a structured prompt with goals and constraints  
↓  
AI agent receives the prompt  
↓  
Agent plans: what topics to cover, in what order, with what tasks  
↓  
Agent outputs a structured 7-day plan  
↓  
App parses the response and renders day cards  
↓  
Student gets a personalized, actionable prep roadmap

### Ask Students to Recall

What is the difference between asking AI: "What should I study for a software interview?" versus what we built today?

Expected answer: The chatbot question gives a generic answer. Our agent feature uses the student's actual role, actual weak areas, actual time constraints, and produces a structured plan with day-wise actions. That is the agent difference — context plus structure plus actionable output.

### Student Writing Task

Ask every student to write 2–3 lines:

What makes our Prep Plan feature an agent and not just a chatbot?

Expected answer:

Our Prep Plan feature is agent-like because it takes goals (prepare for this role) and constraints (these weak areas, this many days, this many hours), and uses them to produce a structured multi-step plan. A chatbot would only respond to one question at a time without planning across multiple steps.

---

## 105–115 min: Interview Discussion and Viva Practice

### Instructor Goal

Prepare students to speak confidently about this feature in an interview.

Use the interview questions section below.

Run 3–4 questions as a live viva. Pick different students for each question.

---

## 115–120 min: Wrap-Up and Session 8 Preview

### Instructor Closing

Today we added the most strategic feature of the app: an AI Prep Plan Agent that takes goals and constraints and produces a full structured prep roadmap. Students can now walk into an interview and say: "I built a feature where AI acts as a planning agent."

Next session is Session 8: Debug, Test, Polish, and Interview Demo. We will review the full app from Session 1 to Session 7, fix any broken features, polish the UI, and run a full mock interview demo where students present and explain their project from end to end.

Make sure your full app is working before Session 8.

---

# Instructor Notes

## What to Emphasize

Session 7 is the conceptual peak of the cohort.

Emphasize:

- The agent vs chatbot distinction is one of the most asked questions in AI-adjacent interviews right now
- Today's feature is a real-world agent pattern: goal + constraints + structured output + multi-step plan
- Students should be able to explain this without code
- Pre-filling inputs from localStorage shows that the app is a connected product, not isolated features
- Collapsible day cards show UI/UX thinking, not just AI call thinking
- Every student should be able to say: "My app generates a personalized 7-day prep plan using the student's saved profile as context"

## Common Student Mistakes

1. Sending a vague prompt to generate the plan ("make a study plan") without including role, weak topics, days, and hours — results in a generic and unusable output
2. Not pre-filling the form inputs from localStorage — the app feels disconnected from the profile
3. Treating the AI response as a raw text block instead of parsing it into structured day objects — day cards cannot be rendered
4. Forgetting to add a loading state — the app appears frozen while the AI call is processing
5. Adding more than 7 days — scope creep, not needed for this session
6. Skipping validation — user submits with 0 days or empty weak topics and the plan is nonsensical
7. Collapsible cards not being implemented — student renders all content flat, which is hard to read
8. Forgetting the final revision checklist — it is part of the deliverable
9. Not reading the generated plan — student clicks Generate but never reviews whether the output makes sense
10. Confusing agent with automation — students say "it uses n8n" when the agentic behavior here is entirely in the structured prompt and output parsing

## How to Control the Session

Use this rule:

If the feature generates a 7-day plan with collapsible day cards and a revision checklist, move on. Do not keep adding improvements until the core is verified.

Session 7 only needs a working Prep Plan Agent with structured day card output. Polish in Session 8.

## Setup Rule

Do not spend more than 5 minutes on setup issues.

If the app from Session 6 is broken, students should open a clean version of their app and add only the Prep Plan section to it. Do not try to fix all previous sessions during Session 7.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### Q1. What did you build in Session 7?

Expected answer:

In Session 7, I added an AI Prep Plan Agent to the app. It takes the student's target role, weak topics, days until interview, and daily available hours as inputs, and generates a personalized 7-day interview preparation plan. The plan is displayed in the app as collapsible day cards, each showing the topic for the day, 3 to 5 practice questions, and one mock task. There is also a final revision checklist at the end of the plan.

### Q2. What problem does the AI Prep Plan Agent solve?

Expected answer:

Most students preparing for interviews do not know where to start. They have limited time and multiple weak areas. The Prep Plan Agent solves this by taking all the student's constraints and goals and generating a structured, day-wise roadmap so the student knows exactly what to study, in what order, and what to practice each day. It removes the guesswork from interview preparation.

### Q3. What are the four inputs the agent takes?

Expected answer:

The four inputs are: target role, which tells the agent what kind of interview the student is preparing for; weak topics, which tells the agent which areas need the most attention; days until interview, which is the time constraint; and daily available hours, which is the capacity constraint. Together these four inputs give the AI enough information to generate a relevant and realistic preparation plan.

### Q4. Why are target role and weak topics pre-filled from the profile?

Expected answer:

The student already entered their target role and weak areas in Session 1 when they built the base profile. Pre-filling these inputs from localStorage means the student does not have to re-enter data they already provided. It also shows that the app works as a connected product where each feature builds on the same profile context, rather than a set of isolated tools.

### Q5. What is a collapsible day card and why did you use it?

Expected answer:

A collapsible day card is a UI element that shows a summary header — in our case the day number and topic — and expands when clicked to reveal the full content: practice questions and mock task. We used collapsible cards because displaying all 7 days with all questions and tasks at once would be overwhelming. Collapsible cards give the user control over what they see, which makes the plan easier to navigate and use.

---

## App Flow Questions

### Q6. What happens when the student clicks Generate Plan?

Expected answer:

When the student clicks Generate Plan, the app first validates that all four inputs are filled. If validation passes, the app reads the saved profile from localStorage to enrich the context, then constructs a structured prompt that includes the target role, weak topics, days available, and hours per day. This prompt is sent to the AI. While the AI is processing, the app shows a loading state. When the response arrives, the app parses it into 7 day objects and renders them as collapsible day cards with topics, questions, and tasks. The final revision checklist is rendered below the cards.

### Q7. How does the app get the saved profile data to pre-fill the inputs?

Expected answer:

The app reads from localStorage, which is where the profile was saved in Session 1. When the Prep Plan section loads, the app calls localStorage.getItem with the profile key, parses the JSON, and uses the saved target role and weak areas values to pre-fill the corresponding form inputs. This means if the student already has a complete profile, they only need to enter the days and hours, and they can generate a plan immediately.

### Q8. What does the prompt sent to AI look like for this feature?

Expected answer:

The prompt sent to AI includes all the context needed for the plan. It tells the AI: the student is preparing for this specific role, these are their weak topics, they have this many days left, and they can study for this many hours per day. The prompt also instructs the AI to return the plan in a structured format — 7 day objects, each with a day number, topic, list of practice questions, and a mock task. It also asks for a final revision checklist. A structured prompt like this is what makes the output usable for rendering day cards in the app.

### Q9. How does the app parse the AI response into day cards?

Expected answer:

The AI is instructed to return the plan in structured JSON format, where each day is an object with fields for day number, topic, questions, and task. When the response arrives, the app parses this JSON and maps over the 7 day objects to render a day card for each one. If the AI returns plain text instead of structured JSON, the app either falls back to a text display or prompts the user to try again. Instructing AI to return structured JSON is the key step that makes the response renderable in the UI.

### Q10. What happens if the student has not saved a profile yet?

Expected answer:

If the student has not saved a profile in Session 1, the app cannot pre-fill the target role or weak topics. In this case, the app shows a message in the Prep Plan section asking the student to complete their profile first, with a link or button to go to the profile section. This prevents the student from generating a plan without proper context, which would result in a generic and unhelpful output. It also shows that the app is designed with connected state in mind.

---

## AI Topic Questions

### Q11. What is the difference between an AI agent and a chatbot?

Expected answer:

A chatbot receives one input, gives one response, and has no awareness of goals or constraints across multiple steps. An agent receives a goal and a set of constraints, breaks the goal into structured steps, and produces a multi-step action plan or output. In our app, if the student simply asked: "What should I study for a software interview?" that would be a chatbot interaction — one question, one answer. Our Prep Plan Agent, on the other hand, takes the student's role, weak areas, days, and hours, and produces a complete 7-day structured plan with day-wise topics, questions, and tasks. That multi-step, goal-directed, constraint-aware output is what makes it agent-like behavior.

### Q12. How does an AI agent use constraints to produce a plan?

Expected answer:

A constraint is something that limits the solution space. In our feature, the constraints are: the number of days available (time constraint) and the number of hours per day (capacity constraint). The AI uses these constraints to decide how much content to fit per day, which topics to prioritize based on the weak areas, and how to sequence the plan so that the student covers the most important topics first. Without constraints, the AI would produce a generic or unrealistic plan. With constraints, the output is bounded and practical. This is exactly how human planners work too — they use goals and constraints together to produce actionable plans.

### Q13. Why is structured output important for agent behavior?

Expected answer:

Agent behavior is useful only if the output can be acted upon. A plain text paragraph response from AI is readable but not actionable for a computer — the app cannot automatically render day cards from unstructured text. Structured output, in our case JSON with defined fields like day number, topic, questions, and task, allows the app to parse the response programmatically and display each day's content in the correct card. Structured output is what bridges the gap between AI generating something and the app displaying it usefully. This is why prompting for structured JSON output is a critical skill in building AI features.

### Q14. Can you explain agentic AI in simple language to a non-technical interviewer?

Expected answer:

Agentic AI means AI that acts more like a planner or an assistant than a simple answering machine. Instead of just replying to one question, it takes your goal — for example, prepare for an interview in 7 days — and your situation — you are weak in databases and have 2 hours per day — and it produces a complete action plan for you. It figures out what you should do on Day 1, Day 2, Day 3, all the way to Day 7, based on what you told it. It is like having a personal coach who listens to your constraints and gives you a structured roadmap, rather than just answering one question at a time.

### Q15. How would you explain the AI Prep Plan Agent to an interviewer in one minute?

Expected answer:

In Session 7 of the AI Interview Prep Copilot, I built a Prep Plan Agent. The student enters their target role, weak topics, days until the interview, and daily hours available. The app reads the student's saved profile for additional context, constructs a structured prompt with all this information, and sends it to an AI. The AI returns a personalized 7-day preparation plan in structured JSON format. The app parses this response and displays it as collapsible day cards, each showing the topic for the day, practice questions, and a mock task. There is also a final revision checklist. This feature demonstrates agent behavior because the AI is not just answering one question — it is using goals and constraints to produce a structured, multi-step preparation roadmap.

---

# Session 7 Completion Checklist

Students should complete the following by the end of the session:

- [ ] AI Prep Plan Agent section is visible in the app
- [ ] Input form has all 4 fields: target role, weak topics, days until interview, daily hours
- [ ] Target role and weak topics are pre-filled from saved profile in localStorage
- [ ] Generate Plan button triggers the AI call
- [ ] Loading state is shown while plan is being generated
- [ ] AI response is parsed into structured 7-day data
- [ ] Plan is displayed as 7 collapsible day cards
- [ ] Each day card shows: day number, topic, practice questions, and mock task
- [ ] Final revision checklist is rendered below the day cards
- [ ] Empty state is shown when no plan has been generated yet
- [ ] Basic validation prevents generating with empty required inputs
- [ ] Student can explain the agent vs chatbot distinction in 2–3 sentences

---

# Instructor Backup Plan

If AI tool generation fails or produces an unusable output for this session:

1. Instructor continues the live build on screen.
2. Students follow conceptually and note the key steps.
3. Share the final Session 7 code after the session.
4. Students use the prompts to regenerate or fix their app after class.
5. Do not sacrifice the Concept Pause or Interview Discussion sections — the agent vs chatbot explanation is the most important takeaway.
6. If the full plan generation fails, show a hardcoded 7-day plan as a static example so students can still build the day card UI and understand the output structure.
