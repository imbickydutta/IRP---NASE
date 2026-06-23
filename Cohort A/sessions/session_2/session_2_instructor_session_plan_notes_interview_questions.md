# Session 2 Instructor File: Add JD Analyzer

## Session Title

Add JD Analyzer

## Duration

2 hours

## Project

AI Interview Prep Copilot

## Session 2 Objective

By the end of Session 2, students should have a working JD Analyzer feature inside the existing AI Interview Prep Copilot app.

This feature takes a raw job description as input, sends it to AI with a structured prompt, and displays extracted data as organized cards showing:

- Required Skills
- Key Responsibilities
- Role Type
- Top 5 Interview Topics
- Difficulty Level

The extracted data is stored in app state so future sessions can use it.

## Session 2 Deliverable

Students will add to the existing profile dashboard app:

1. A JD Analyzer section with a large text area
2. An Analyze JD button
3. A loading state while AI processes the JD
4. Result cards for: Required Skills, Key Responsibilities, Role Type, Interview Topics, Difficulty Level
5. Extracted JD data stored in app state
6. Clear empty state when no JD has been analyzed yet
7. Error state if input is empty or AI fails to return valid JSON

The feature should feel like a natural extension of the existing dashboard — not a separate app.

## Strict Scope Control

### Include

- One JD text area input
- Analyze JD button
- Loading indicator while processing
- Required Skills result card
- Key Responsibilities result card
- Role Type result card (Frontend / Full-Stack / AI-ML / Backend)
- Top 5 Interview Topics result card
- Difficulty Level result card (Entry / Mid / Senior)
- Extracted JD data saved in app state
- Empty state message before analysis
- Error message for empty input
- Code comments explaining the structured prompt and JSON parsing

### Do Not Include

- PDF upload
- File parsing libraries
- Multiple JD comparison
- Backend API or server
- Database storage
- Auto-resume matching
- ATS scoring
- External NLP libraries
- Complex parsing logic
- User authentication
- Saving to external cloud

Session 2 adds one focused AI feature. Everything else waits for later sessions.

---

# Instructor Framing

## Opening Message

In Session 1, we built the base profile dashboard. Students saved their target role, skills, weak areas, and job description. That was the foundation.

Today we add the first real AI feature: JD Analyzer. The user pastes any job description into a text area, clicks Analyze JD, and the app uses AI to extract structured information from the raw text. The result appears as organized cards.

The key learning today is not just the feature — it is the concept of structured prompting. Instead of asking AI to describe a JD in prose, we ask AI to return specific JSON. That is a skill students will use throughout their careers.

## Key Philosophy

Students are not expected to write the AI prompt from scratch.

They are expected to:

- understand why structured output matters
- read the prompt and understand what it asks for
- read the returned JSON and understand how it is parsed
- test the feature with real and edge-case JDs
- explain the concept in interview language

## Repeated Instructor Line

AI returned structured data because we asked for structured data. The prompt is the design decision.

---

# Session Flow

## 0–10 min: Opening and Recap of Session 1 — Base Profile Dashboard

### Instructor Goal

Reconnect students to the app they built. Confirm everyone has the Session 1 app running before starting Session 2.

### Recap Questions to Ask Students

1. What does the profile dashboard store?
2. Where is the data saved?
3. What fields did we collect in the profile form?
4. Where will the job description come from in today's feature?

### Expected Recap Answers

- The dashboard stores name, target role, skills, project details, weak areas, and job description.
- Data is saved in localStorage.
- Job description was collected in the profile form.
- Today's JD Analyzer will use a dedicated text area — but the JD from the profile form can be pre-filled as a starting point.

### Instructor Setup Check

Before continuing, confirm every student can:

- open their Session 1 app
- see the profile dashboard
- see their saved profile summary

If any student's app is broken, pair them with another student or share the Session 1 base code. Do not let setup issues delay the whole class beyond 3 minutes.

### Bridge Statement

Today we take the raw job description — which is just unstructured text — and use AI to turn it into organized, usable data. That process is the feature we are building.

---

## 10–20 min: Product Breakdown Before Prompting

### Instructor Goal

Before touching the AI tool, make students think through the feature as a product designer would.

### Ask Students

What does a JD Analyzer need to do?

Expected answers:
- take a raw job description as input
- send it to AI
- get back extracted information
- display it clearly

### Break Down the Feature Step by Step

Write this on screen or whiteboard:

1. User sees a text area labeled "Paste Job Description Here"
2. User pastes a raw JD
3. User clicks Analyze JD
4. App sends the JD to AI with a specific prompt
5. AI returns structured JSON with required fields
6. App parses the JSON
7. App displays result cards

### Ask Students

What data do we want to extract from the JD?

Expected answers:
- required skills
- key responsibilities
- role type
- interview topics
- difficulty level

### Instructor Explanation

Notice we are extracting five specific pieces of data. This means our AI prompt must ask for exactly five things. If we ask AI to summarize the JD, we get prose. If we ask AI to return JSON with specific keys, we get structured data we can actually use in code. That difference is the core lesson of today.

### Convert into Feature List

1. JD text area input
2. Analyze JD button
3. Loading state
4. Required Skills card
5. Responsibilities card
6. Role Type card
7. Interview Topics card
8. Difficulty Level card
9. Empty state before analysis
10. Error state for empty input

---

## 20–35 min: Generate Add JD Analyzer Feature in AI Tool

### Instructor Goal

Run the main Session 2 build prompt to generate the JD Analyzer feature on top of the existing app.

### Before Running the Prompt

Remind students:
- The prompt builds on top of the existing profile dashboard
- We are not starting a new app
- The prompt includes what is already built so AI understands context
- The key part of this prompt is the section asking AI to return JSON output

### What to Watch For After Generation

- Does the JD text area appear in the app?
- Does the Analyze JD button call an AI function? (Gemini 1.5 Flash via @google/generative-ai — free tier)
- Does the AI prompt inside the code ask for JSON output with the correct keys?
- Does the app parse the returned JSON?
- Does each result card appear with data?
- Is there a loading state while processing?
- Are there comments in the code explaining the prompt structure?

### Instructor Control Rule

Do not let students ask AI to add PDF upload, ATS score, or backend storage during this step. The goal is one clean feature that works. Scope creep makes the app harder to explain in interviews.

---

## 35–50 min: Instructor Walkthrough of Generated Feature

### Instructor Goal

Help students understand what AI generated before they build their own version.

### Walkthrough Areas

1. Where is the JD Analyzer section added in the app layout?
2. Where is the JD input text area defined?
3. Where is the Analyze JD button and what function does it call?
4. Where is the structured AI prompt written in the code?
5. What JSON schema does the prompt ask for?
6. How is the JSON response parsed from the AI output?
7. How are the result cards rendered using the parsed data?
8. Where is the extracted JD data stored in app state?

### Ask During Walkthrough

- What would happen if the AI returned prose instead of JSON?
- What does the prompt say that makes AI return JSON?
- What happens if the JSON parsing fails?
- Where does the required skills list come from?
- Which part of the code creates each result card?

### Simple Explanation

Point to the prompt inside the code. Show students the line that says "return your answer as a JSON object" or similar. Explain: this single instruction is what makes the response structured instead of a paragraph. The rest of today is about understanding why that matters.

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students run the main Session 2 prompt in their own AI tool and add the JD Analyzer to their existing app.

### Instructor Support Areas

Help students with:

- prompt paste issues or errors
- preview not loading after generation
- Analyze JD button not triggering anything
- AI prompt inside the code not requesting JSON
- JSON parse errors in the console
- result cards not appearing
- loading state not showing or not disappearing

### If Student App Breaks

Do not block the class.

The student should:

- follow the instructor screen
- note the issue for after-class debugging
- use the shared completed Session 2 code after class

### Quick Diagnostic Question

Ask each student: "Run your app. Paste a JD. Click Analyze. What do you see?"

- If result cards appear: move on
- If nothing appears: check the AI function call and prompt
- If an error shows: check JSON parsing

---

## 65–80 min: Improve and Refine

### Instructor Goal

Make the JD Analyzer feature look and feel complete as part of the existing dashboard.

### Expected Improvements

- Result cards styled consistently with the existing profile dashboard
- Required Skills displayed as a bullet list or tag chips, not a paragraph
- Key Responsibilities displayed as a numbered list
- Role Type displayed as a highlighted badge (Frontend / Full-Stack / AI-ML / Backend)
- Difficulty Level displayed as a colored badge (Entry = green, Mid = amber, Senior = red)
- Clear separation between input section and results section
- Analyze JD button disabled during loading
- Option to clear results and analyze a different JD

### Instructor Explanation

The AI prompt is doing the heavy lifting. Our job is to display the structured output in a way that is easy to read. Good UI on structured data is part of product thinking, which interviewers value.

---

## 80–95 min: Edge Cases and Error States

### Instructor Goal

Teach students to think about what can go wrong with this feature.

### Edge Cases to Handle

1. User clicks Analyze JD without pasting anything — show error: "Please paste a job description before analyzing."
2. JD input is very short (less than 50 characters) — warn the user the JD may be too brief for accurate analysis.
3. AI returns incomplete JSON (missing one or more keys) — show a fallback message like "Analysis incomplete. Please try again."
4. AI returns a response that is not valid JSON at all — catch the parse error and show: "AI response was not in the expected format. Please try again."
5. User pastes the same JD twice — app should re-analyze and update results, not duplicate cards.
6. User clears the text area after analysis — decide whether to hide results or keep them until next analyze.

### Ask Students

Which of these edge cases is the most important to handle, and why?

Expected discussion: the JSON parse error is most critical because it determines whether the whole feature breaks or degrades gracefully.

### Instructor Explanation

A feature that fails silently is worse than one that shows a clear error. Handling edge cases is what separates a working prototype from a production-quality feature.

---

## 95–105 min: Concept Pause — Structured Prompting and JSON Output

### Instructor Goal

Convert what students built into clear interview-ready understanding of the AI concept.

### Explain the Concept

Structured prompting means writing a prompt that tells AI exactly what format to return the answer in.

Without structured prompting:
- User pastes a JD
- AI returns a paragraph describing the JD
- App cannot use a paragraph to create separate cards

With structured prompting:
- User pastes a JD
- Prompt tells AI: return a JSON object with keys requiredSkills, keyResponsibilities, roleType, interviewTopics, difficultyLevel
- AI returns parseable JSON
- App maps each key to a result card

### Show the Contrast on Screen

Bad prompt:
```
Here is a job description. Tell me what skills and responsibilities are mentioned.
```

Good prompt:
```
Here is a job description. Analyze it and return a JSON object with exactly these keys:
- requiredSkills: array of strings
- keyResponsibilities: array of strings
- roleType: one of "Frontend", "Full-Stack", "AI-ML", "Backend"
- interviewTopics: array of exactly 5 strings
- difficultyLevel: one of "Entry", "Mid", "Senior"
Return only the JSON object. No explanation text.
```

### Ask Students to Write

Ask every student to write a 2–3 line answer:

What is the difference between asking AI for prose and asking AI for JSON?

Expected answer:

When I ask AI for prose, I get a readable paragraph I cannot easily process in code. When I ask AI for JSON, I get structured data with specific keys I can map directly to UI components. Structured prompting is what makes AI output programmable.

### App Flow to Explain

User pastes raw job description into text area
↓
User clicks Analyze JD
↓
App sends JD + structured prompt to AI
↓
AI returns JSON with requiredSkills, keyResponsibilities, roleType, interviewTopics, difficultyLevel
↓
App parses the JSON
↓
App stores extracted data in state
↓
App displays five result cards with the extracted data
↓
Extracted JD data available for use in Session 3 (Profile vs JD Match)

---

## 105–115 min: Interview Discussion and Viva Practice

### Instructor Goal

Prepare students to speak about both the feature and the AI concept behind it.

Use the interview questions section below. Pick 4–5 questions and ask each student to answer verbally.

### Instructor Tip

Do not read the expected answers to students. Ask them to answer first. Then correct or build on their answer. Students learn more from attempting the explanation themselves.

---

## 115–120 min: Wrap-Up and Session 3 Preview

### Instructor Closing

Today we added the JD Analyzer. We took a raw, unstructured job description and used structured prompting to extract required skills, responsibilities, role type, interview topics, and difficulty level. Those results are now stored in the app.

In Session 3 — Add Profile vs JD Match — we will build the Profile vs JD Match feature. The app will compare the student's saved skills against the extracted JD requirements and generate a match score. That feature will use the data we extracted today — so what you built in Session 2 directly feeds Session 3.

Make sure your Session 2 feature works and the extracted JD data is accessible in app state before Session 3.

---

# Instructor Notes

## What to Emphasize

Session 2 introduces the first real AI call in the app. (Gemini 1.5 Flash via @google/generative-ai — free tier)

Students should understand:

- The AI prompt is inside the application code, not just a chat message
- The prompt design determines the output format
- JSON output is intentional — we ask for it explicitly
- Parsing JSON is a required step between AI output and UI display
- Error handling for AI responses is a product-quality skill

## Common Student Mistakes

1. Asking AI to add the JD Analyzer as a completely separate app instead of adding it to the existing dashboard.
2. Not including the JSON schema in the prompt — AI returns prose and the app breaks.
3. Forgetting to handle the case where AI returns JSON wrapped in markdown code fences (```json ... ```) which breaks JSON.parse().
4. Not storing the extracted JD data in state — future sessions need this data, so a local variable is not enough.
5. Spending all session time on result card styling instead of ensuring the JSON parsing works first.
6. Adding a PDF upload feature because they think it is cooler — this is out of scope and breaks the lesson focus.
7. Not testing with a real JD — using a placeholder like "good job description" does not exercise the full extraction.
8. Ignoring the loading state — clicking Analyze multiple times without a loading indicator creates duplicate calls.
9. Not adding the empty state — the section looks broken if nothing shows before the first analysis.
10. Assuming JSON.parse() always works — not wrapping it in a try-catch is a beginner mistake in AI feature development.

## How to Control the Session

Use this rule:

If a proposed addition does not help extract or display the five required JD fields, do not add it in Session 2.

The five fields are: Required Skills, Key Responsibilities, Role Type, Interview Topics, Difficulty Level.

Everything else — PDF upload, ATS scoring, backend, multiple JD comparison — comes after the course if at all.

## Setup Rule

Students must have the Session 1 base app working before Session 2 starts.

If a student does not have the Session 1 app, share the base code from Session 1 and let them open that. Do not spend live session time rebuilding Session 1.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### Q1. What feature did you add in Session 2?

Expected answer:

In Session 2, I added a JD Analyzer feature to the AI Interview Prep Copilot. The user can paste a raw job description into a text area, click Analyze JD, and the app extracts required skills, key responsibilities, role type, top 5 interview topics, and difficulty level. The results are displayed as structured cards below the input.

### Q2. Why is a JD Analyzer useful for interview preparation?

Expected answer:

Most students read job descriptions casually and miss what the company actually wants. A JD Analyzer breaks the JD into specific categories — required skills, responsibilities, and interview topics — so the student knows exactly what to prepare. It also identifies the difficulty level so the student can calibrate how much preparation is needed.

### Q3. Who are the users of the JD Analyzer feature?

Expected answer:

The users are students and freshers who are applying for jobs and want to prepare effectively. They may not know how to read between the lines of a job description. The analyzer does that work for them by extracting the most important information.

### Q4. What data does the JD Analyzer extract, and why did we choose those five fields?

Expected answer:

The JD Analyzer extracts required skills, key responsibilities, role type, top 5 interview topics, and difficulty level. We chose these five fields because they give a student the clearest picture of what a role demands. Required skills tell you what to have. Responsibilities tell you what you will do. Role type categorizes the position. Interview topics tell you what to study. Difficulty level sets expectations about experience needed.

### Q5. How does the JD Analyzer connect to Session 3?

Expected answer:

In Session 3, we build a Profile vs JD Match feature. That feature compares the student's saved skills from the profile with the required skills extracted by the JD Analyzer. Without the JD Analyzer running first and storing its results, the match feature would have nothing to compare against. So Session 2 output directly enables Session 3.

---

## App Flow Questions

### Q6. Walk me through what happens when a user clicks Analyze JD.

Expected answer:

When the user clicks Analyze JD, the app first checks whether the text area has content. If it is empty, an error message appears asking the user to paste a job description. If the text area has content, the app shows a loading state and sends the JD text to AI along with a structured prompt. The prompt instructs AI to return a JSON object with specific keys. The app receives the AI response, parses the JSON, stores the extracted data in app state, and renders five result cards: Required Skills, Key Responsibilities, Role Type, Interview Topics, and Difficulty Level.

### Q7. Where is the extracted JD data stored, and why does that matter?

Expected answer:

The extracted JD data is stored in the app's state. This matters because future features in the same app — like the Profile vs JD Match in Session 3 — need to access this data. If the data were only stored in a local variable inside the Analyze function, it would not be accessible to other components or features. Keeping it in state makes it available across the app.

### Q8. What is the role of the loading state in this feature?

Expected answer:

The loading state gives the user feedback that the app is working and prevents confusion when the AI call takes a few seconds to respond. Without a loading state, the user might think the button did not work and click it multiple times, which could trigger duplicate AI calls. The loading state disables the button and shows a spinner or message until the AI response is received and processed.

### Q9. What happens if the user pastes a very short or vague job description?

Expected answer:

If the user pastes a very short JD — for example, just a job title — the AI may not have enough information to extract meaningful data. The app can handle this in two ways: it can check the input length before sending to AI and warn the user, or it can send the short JD and display whatever AI extracts, even if the results are thin. In either case, the user should be guided to paste a more complete job description for better results.

### Q10. Why do we display the results as cards instead of a paragraph?

Expected answer:

Displaying results as cards makes each piece of extracted information visually distinct and easy to scan. A paragraph forces the user to read through everything to find one piece of information. Cards allow the user to jump directly to Required Skills, or Interview Topics, or Difficulty Level without reading the full output. Structured display is what makes structured data actually useful.

---

## AI Topic Questions — Structured Prompting and JSON Output

### Q11. What is structured prompting?

Expected answer:

Structured prompting is the practice of writing a prompt that tells AI exactly what format to use when returning the answer. Instead of asking an open-ended question and getting a natural-language paragraph, we give AI a specific structure — like a JSON schema with named keys and expected value types — and ask it to fill in that structure. The result is a response that code can directly parse and use, rather than a response that only a human can read.

### Q12. Why did we ask AI to return JSON instead of a text summary?

Expected answer:

We asked for JSON because the application needs to map specific pieces of extracted information to specific UI cards. If AI returns a paragraph saying "this role requires React, Node.js, and Python," the code has no reliable way to separate those skills into a list. If AI returns a JSON object with a key called requiredSkills containing an array of strings, the code can directly render that array as a list in the Required Skills card. JSON gives us programmable output, which is what applications need.

### Q13. What is the risk of not specifying the JSON schema in your prompt?

Expected answer:

If I do not specify the JSON schema, AI might return JSON with different key names, different data types, or inconsistent structure across different runs. For example, AI might call the field "skills" in one response and "requiredSkills" in another, or return a string where the app expects an array. By specifying the exact keys, value types, and allowed values in the prompt, I ensure the AI output is consistent and my JSON parsing logic does not break.

### Q14. What happens in the code when AI returns JSON wrapped in markdown code fences?

Expected answer:

When AI returns a JSON response, it sometimes wraps it in markdown code fences like triple backtick json. If the code tries to run JSON.parse() on that string directly, it will throw an error because the backticks and the word "json" are not valid JSON. A common fix is to strip the markdown wrapper before parsing — for example, by removing the first and last lines if they contain code fence markers, or by using a regular expression to extract only the JSON portion of the response.

### Q15. How would you explain structured prompting to a non-technical interviewer?

Expected answer:

I would say: when you ask a person a question, you can ask it in a way that gets you a useful answer or an unhelpful answer. If you ask "tell me about this job description," you get a summary. If you ask "please give me the required skills as a list, the responsibilities as a numbered list, and the role type as one word," you get exactly what you need. Structured prompting is the same idea applied to AI. We phrase the question precisely so the AI gives us a precise, usable answer instead of a general response.

---

# Session 2 Completion Checklist

Students should complete the following by the end of the session:

- [ ] Session 1 base app is open and working
- [ ] JD Analyzer section is visible in the app
- [ ] JD text area accepts input
- [ ] Analyze JD button is visible and clickable
- [ ] Loading state appears when Analyze JD is clicked
- [ ] AI prompt inside the code explicitly asks for JSON output with all five keys
- [ ] Required Skills card displays a list of skills
- [ ] Key Responsibilities card displays a list of responsibilities
- [ ] Role Type card displays one of: Frontend, Full-Stack, AI-ML, Backend
- [ ] Interview Topics card displays exactly 5 topics
- [ ] Difficulty Level card displays one of: Entry, Mid, Senior
- [ ] Extracted JD data is stored in app state
- [ ] Empty state message appears before first analysis
- [ ] Error message appears when Analyze JD is clicked on empty input
- [ ] Student can explain the structured prompting concept in 2–3 sentences

---

# Instructor Backup Plan

If the AI tool generation fails or the JSON parsing has major issues:

1. Instructor continues live build on screen.
2. Students follow conceptually and note the key prompt structure.
3. Share the final Session 2 code after the session.
4. Students use the prompts later to regenerate or fix their app.
5. Do not sacrifice the Concept Pause — structured prompting explanation is the most important learning of Session 2.
6. If AI keeps returning prose, demonstrate the prompt fix live: add "Return only the JSON object. Do not include any explanation or markdown formatting."
7. The interview explanation section must always run, even if the code is not fully working.

## Gemini API Troubleshooting

If AI calls are failing during the session:

- Check that the student's `.env` file exists in the project root (same folder as `package.json`) and contains `VITE_GEMINI_API_KEY=...` with a real key
- The Vite dev server must be restarted after adding or changing the `.env` file — stopping and re-running `npm run dev` is required
- Confirm the key is accessible: `console.log(import.meta.env.VITE_GEMINI_API_KEY)` in the component should print the key, not `undefined`
- Free tier limit is 15 RPM (requests per minute) — if a student hits the rate limit, wait 1 minute and try again
- If the key returns a 403 or "API key not valid" error, the student needs to generate a new key at https://aistudio.google.com
