# AI Interview Prep Copilot — Interview Preparation Phase
## Cohort A

---

## Program Overview

This is an 8-session, hands-on interview preparation curriculum designed for non-tech students who have completed the AI / No-Code / GenAI program. The curriculum follows a single guiding principle: **students learn AI topics by building, not by reading theory.**

Each session takes the same running application — the AI Interview Prep Copilot — and adds one concrete, working feature to it. By the end of Session 8, students have a fully functional, portfolio-ready AI-powered tool they built themselves, one session at a time.

**Who this is for:** Students with no prior software development background who have completed the foundational AI / No-Code / GenAI program and are now preparing for job interviews.

**What makes this different:** Every AI concept (prompt chaining, RAG, agents, rubric evaluation) is introduced at the exact moment students need it to build the next feature. Theory follows practice, never the other way around.

---

## Running Project: AI Interview Prep Copilot

The AI Interview Prep Copilot is a single, evolving web application that students build across all 8 sessions. When complete, the app can:

- **Collect and store a student profile** — name, background, skills, projects, and experience saved in localStorage so no backend is required.
- **Analyze any job description** — paste a JD and the app extracts required skills, key responsibilities, and important topics using structured AI prompting.
- **Compare the student profile to the JD** — produce a match band (Strong / Moderate / Weak), list matched skills, identify missing skills, and highlight risk areas the student must address.
- **Generate a full interview question set** — produce 5 technical questions, 3 project-based questions, 2 HR questions, and 2 scenario-based questions tailored to the specific JD and student profile.
- **Evaluate mock answers** — the student types or speaks an answer; the app scores it on a rubric, identifies strengths and gaps, generates an improved model answer, and suggests a likely follow-up question.
- **Answer doubts from a knowledge base** — a RAG-Lite module grounds every answer in a predefined knowledge base so responses are accurate, cited, and not hallucinated.
- **Generate a personalized 7-day prep plan** — an AI agent reads the gap analysis and produces a day-by-day study and practice schedule with concrete daily tasks.

---

## 8-Session Overview Table

| # | Session Title | Feature Built | Main AI Topic |
|---|---|---|---|
| 1 | Build the Base App | Student profile dashboard with localStorage | Foundation setup |
| 2 | Add JD Analyzer | Extract skills, responsibilities, topics from JD | Structured prompting and JSON output |
| 3 | Add Profile vs JD Match | Match band, matched/missing skills, risk areas | Context management and explainable AI |
| 4 | Add Interview Question Generator | 5 technical + 3 project + 2 HR + 2 scenario questions | Prompt chaining |
| 5 | Add Mock Answer Evaluator | Score, strengths, gaps, improved answer, follow-up | Rubric-based AI evaluation |
| 6 | Add RAG-Lite Doubt Solver | Grounded answers from predefined knowledge base | RAG and grounded responses |
| 7 | Add AI Prep Plan Agent | Personalized 7-day prep plan with daily tasks | AI agents and planning |
| 8 | Debug, Test, Polish, Demo | Loading states, error states, README, demo script | AI code review and testing |

---

## Session-Wise Feature List

1. **Session 1 — Student Profile Dashboard:** Build the base application shell with a profile form that collects name, background, skills, projects, and experience. All data is saved to localStorage so the app works without a backend. This session establishes the project structure every future session builds on.

2. **Session 2 — JD Analyzer:** Add a Job Description input panel. When a JD is pasted, a structured AI prompt extracts required technical skills, key responsibilities, and important topics and returns them as a clean JSON object rendered on screen.

3. **Session 3 — Profile vs JD Match:** Add a gap analysis module that compares the stored student profile against the analyzed JD. The app produces a match band (Strong / Moderate / Weak), a list of matched skills, a list of missing skills, and a set of risk areas the student must address before the interview.

4. **Session 4 — Interview Question Generator:** Add a question generation panel. Using prompt chaining — the JD analysis feeds into the match analysis, which feeds into the question prompt — the app generates a balanced set of 5 technical, 3 project-based, 2 HR, and 2 scenario questions specific to this student and this JD.

5. **Session 5 — Mock Answer Evaluator:** Add an answer evaluation interface. The student selects a generated question, types or speaks their answer, and the app scores it against a rubric, identifies strengths and gaps, writes an improved model answer, and predicts a likely follow-up question the interviewer might ask.

6. **Session 6 — RAG-Lite Doubt Solver:** Add a doubt-solving chatbot grounded in a predefined knowledge base (common interview topics, HR questions, technical concepts). Answers are retrieved from the knowledge base first, then synthesized by the AI, preventing hallucination and ensuring accuracy.

7. **Session 7 — AI Prep Plan Agent:** Add an autonomous planning agent. The agent reads the student profile, the JD gap analysis, and the answer evaluation results, then generates a personalized 7-day preparation plan with specific daily tasks, topics to study, and practice activities.

8. **Session 8 — Debug, Test, Polish, Demo:** Add production-quality finishing touches: loading states for all AI calls, graceful error states, edge-case handling, a final README inside the app, and a demo script. Students use AI-assisted code review to find and fix bugs, then deliver a live demo.

---

## Final Project Vision

After Session 8, the AI Interview Prep Copilot is a complete, standalone, portfolio-ready application that a student can open on any device with a browser. The app:

- Requires no backend, no database, and no deployment — it runs entirely in the browser using localStorage and direct API calls.
- Guides a student from zero preparation to a structured, personalized interview readiness plan in a single session.
- Demonstrates mastery of five distinct applied AI techniques: structured prompting, context management, prompt chaining, RAG, and autonomous agent planning.
- Can be shown to a recruiter or hiring manager as a working product the student designed and built.
- Can be extended after the course to support additional JDs, multiple profiles, voice input, and more without changing the core architecture.

---

## Instructor Usage Guide

- **Read the instructor file before each session.** Every `session_N/instructor/` folder contains the session plan, the expected code state at the end of the session, common student errors, and suggested discussion prompts. Review it the evening before, not five minutes before class.
- **Use the end-state code as your reference, not your starting point.** The instructor files show what the app should look like after the session. Start the live build from the pre-session student file so students see every step taken.
- **Surface the AI concept only when the code demands it.** Each session introduces exactly one AI topic. Resist the temptation to explain future sessions' concepts early — the curriculum is sequenced so the concept lands when students have context for it.
- **Run the app yourself before class.** Open the pre-session file, confirm the API key works, and verify that the feature you are about to build produces the expected output. Do not discover broken prompts in front of students.
- **Use broken or unexpected outputs as teaching moments.** When the AI returns malformed JSON, an off-topic answer, or a weak match analysis, stop and diagnose it with the class. These moments teach prompt debugging better than any planned exercise.
- **Keep the session scope locked.** If a student asks about a feature from a future session, acknowledge it and add it to the "parking lot" — a visible list of ideas to revisit in Session 8. Do not build ahead; it breaks the scaffolding for students who miss a session.

---

## Student Usage Guide

- **Open the pre-session file before class.** Each `session_N/pre_session/` folder contains the starting code for that session. Load it in your editor or no-code tool before the instructor begins so you can follow along without falling behind.
- **Do not copy-paste the finished code.** The learning happens in the building. Use the pre-session file as your starting point and add each piece as the instructor explains it. Copy-pasting the end-state file means you miss the reasoning behind every decision.
- **Save your work to a personal folder after every session.** The sessions folder is shared. Copy your working file to a personal folder at the end of class so your progress is never overwritten.
- **Test the app with your own real profile and a real JD.** The app produces meaningfully better output when the inputs are genuine. Use your actual skills, your actual projects, and a JD you actually want to apply for.
- **When the AI output looks wrong, debug the prompt first.** Before asking the instructor for help, read the prompt that produced the bad output. Change one variable at a time — the input, the instruction, the output format — and observe what changes. This is the core skill the curriculum is building.
- **Bring your demo-ready app to every mock interview and placement session.** By Session 4 the app is already useful for real interview prep. Use it. The feedback loop between using the app and improving it is the fastest path to both interview readiness and AI fluency.

---

## Recommended Execution Rules

1. **One feature per session, no exceptions.** Each session is scoped to exactly one new feature. Attempting to build two features in one session compresses the learning and leaves students with incomplete code they cannot debug.
2. **Always start from the pre-session file.** Never start a session from the previous session's finished file without first verifying it matches the official pre-session baseline. Drift accumulates and breaks later sessions.
3. **Run the app at the start and end of every session.** A working app at the start of class confirms the baseline. A working app at the end confirms the feature was built correctly. If the app does not run at the end, do not close the session — diagnose the error together.
4. **Introduce the AI concept after the first working version of the feature.** Build a rough version first, show that it works, then explain the AI concept it demonstrates. Concept-first teaching does not work for this audience.
5. **Timebox student experimentation to 10 minutes per session.** After the main feature is built, give students 10 minutes to experiment with their own inputs. Set a visible timer. Experimentation is valuable; open-ended tinkering that eats the debrief is not.
6. **End every session with a one-sentence summary of the AI concept learned.** Ask a student to say it, not the instructor. This closes the loop between building and understanding.
7. **Log every unexpected AI output during class.** Keep a shared document where instructors record prompts that produced bad output. This log becomes the debugging exercise library for Session 8.
8. **Do not upgrade the AI model or change the API provider mid-cohort.** Model behavior changes between versions. Lock the model identifier at Session 1 and use the same identifier through Session 8 to ensure reproducible outputs.

---

## Scope Control Rules

1. **No feature that requires a backend is in scope.** All data lives in localStorage. Any student request that requires a server, database, or authentication is out of scope for this curriculum.
2. **No multi-JD or multi-profile support until Session 8.** The app is designed around one active profile and one active JD at a time. Supporting multiple is a valid extension but must not be attempted before the core app is complete.
3. **No UI redesign sessions.** Styling improvements are welcome in the final 10 minutes of Session 8 only. Spending session time on colors, fonts, or layout instead of AI features defeats the purpose of the curriculum.
4. **No switching AI providers mid-session.** If a student wants to try a different model or provider, note it as a post-course experiment. Switching mid-session breaks the shared instructor reference and wastes time on configuration.
5. **No adding features from future sessions into earlier sessions.** If Session 4's question generator seems easy and a student wants to add Session 5's evaluator early, decline. The evaluator depends on patterns established in Session 5. Building it early produces a fragile version that breaks when done correctly later.
6. **No skipping the debug-and-polish session.** Session 8 is not optional cleanup. Loading states, error handling, and the demo script are as important as any AI feature. A demo-ready app is the deliverable; Session 8 produces it.

---

## Folder Structure

```
sessions/
├── README.md
├── session_1/
│   ├── instructor/
│   │   ├── session_plan.md
│   │   ├── end_state_code/
│   │   └── common_errors.md
│   └── pre_session/
│       └── starter_code/
├── session_2/
│   ├── instructor/
│   │   ├── session_plan.md
│   │   ├── end_state_code/
│   │   └── common_errors.md
│   └── pre_session/
│       └── starter_code/
├── session_3/
│   ├── instructor/
│   │   ├── session_plan.md
│   │   ├── end_state_code/
│   │   └── common_errors.md
│   └── pre_session/
│       └── starter_code/
├── session_4/
│   ├── instructor/
│   │   ├── session_plan.md
│   │   ├── end_state_code/
│   │   └── common_errors.md
│   └── pre_session/
│       └── starter_code/
├── session_5/
│   ├── instructor/
│   │   ├── session_plan.md
│   │   ├── end_state_code/
│   │   └── common_errors.md
│   └── pre_session/
│       └── starter_code/
├── session_6/
│   ├── instructor/
│   │   ├── session_plan.md
│   │   ├── end_state_code/
│   │   └── common_errors.md
│   └── pre_session/
│       └── starter_code/
├── session_7/
│   ├── instructor/
│   │   ├── session_plan.md
│   │   ├── end_state_code/
│   │   └── common_errors.md
│   └── pre_session/
│       └── starter_code/
└── session_8/
    ├── instructor/
    │   ├── session_plan.md
    │   ├── end_state_code/
    │   └── common_errors.md
    └── pre_session/
        └── starter_code/
```

---

## Reuse Guide for Other Cohorts or Courses

This curriculum is designed to be reused across cohorts without rebuilding session content.

For Cohort B, Cohort C, or any adapted version of this course, edit the `SESSIONS_FOLDER` and `COHORT` constants at the top of the `generate-course-sessions` workflow script and re-run it. The script will scaffold a fresh sessions folder with the correct cohort label while keeping all session content, instructor files, pre-session starters, and scope rules identical.

No manual copying of session folders is required. The session content and structure remain the same across all cohorts; only the output path and cohort identifier change.

If the curriculum itself needs to be updated (new AI topics, revised features, different session count), make changes to the canonical session templates first, then re-run the generation script for all active cohorts to propagate the changes uniformly.
