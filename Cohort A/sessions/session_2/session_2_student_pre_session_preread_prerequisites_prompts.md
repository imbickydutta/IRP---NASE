# Session 2 Student Pre-Session File: Add JD Analyzer

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
- create a 7-day interview prep plan

## What Is Already Built

In Session 1, we built the base profile dashboard.

The app currently:

- collects Full Name, Target Role, Current Skills, Project Details, Weak Areas, and Job Description
- saves this profile to localStorage
- displays the saved profile as a summary
- supports editing and updating the profile
- shows future feature navigation labels

## Session 2 Goal

In Session 2, we will add the JD Analyzer feature.

The user will:

- paste a raw job description into a text area
- click Analyze JD
- receive AI-extracted structured data shown as cards

## Session 2 Output

By the end of Session 2, your app should have a working JD Analyzer section that:

- accepts raw job description text as input
- sends the text to AI with a structured prompt
- displays the following as result cards:
  - Required Skills (list)
  - Key Responsibilities (list)
  - Role Type (Frontend / Full-Stack / AI-ML / Backend)
  - Top 5 Interview Topics (list)
  - Difficulty Level (Entry / Mid / Senior)
- stores the extracted data in app state for use in Session 3
- shows an empty state before analysis
- shows an error if the input is empty

---

# Pre-Read

## Why Are We Building This Feature?

A job description is written in natural language. It has paragraphs, buzzwords, requirements mixed with nice-to-haves, and a lot of text to read. Most students read it once and move on.

The JD Analyzer solves this by extracting only the most useful information in a structured format. Now a student can see at a glance: what skills are required, what the role involves, how hard the interview is likely to be, and exactly what topics to prepare.

But here is the deeper reason we are building this:

In interviews, you will be asked how your app uses AI.

You need to be able to explain that you did not just call AI and display text. You asked AI for structured output. You defined what keys you wanted. You parsed the response. You built UI from it. That is a real engineering decision, and interviewers respect it.

## Simple App Flow

Session 1 — Base Profile Dashboard:

User fills profile form
↓
App saves profile to localStorage
↓
App shows saved profile summary

Session 2 — JD Analyzer added:

User fills profile form
↓
App saves profile to localStorage
↓
App shows saved profile summary
↓
User pastes raw job description into JD Analyzer
↓
User clicks Analyze JD
↓
App sends JD + structured prompt to AI
↓
AI returns JSON with five extracted fields
↓
App parses JSON and stores data in state
↓
App displays Required Skills, Responsibilities, Role Type, Interview Topics, Difficulty Level as cards
↓
Session 3 — Add Profile vs JD Match — will use this extracted JD data to compare with the student profile

## Key Concepts to Revise

Before the session, revise these ideas:

1. What is a prompt in AI context? — A prompt is the instruction we give to the AI. It decides what the AI responds with.
2. What is JSON? — JSON stands for JavaScript Object Notation. It is a way of representing structured data using key-value pairs. Example: { "name": "Aarav", "role": "Engineer" }.
3. What is JSON.parse()? — It is a function that converts a JSON string into a usable JavaScript object so the app can access each value.
4. What is structured output? — Instead of asking AI to give a prose answer, structured output means asking AI to format the answer in a specific way — like JSON with named keys.
5. What is app state? — State is a variable that holds data the app is currently working with. When state updates, the UI re-renders to reflect the new data.
6. What is an API call in this context? — When the app sends the job description to AI and waits for a response, that is an API call. It is asynchronous, meaning it takes some time and the app needs a loading state.
7. What is a loading state? — A loading state is a UI indicator (spinner, message, or disabled button) that tells the user the app is processing something and they should wait.
8. What is an error state? — An error state is what the app shows when something goes wrong — like the user submitting an empty input or AI returning an invalid response.

## Simple Explanation

A job description is just a long block of unstructured text. It has no labels telling you "this part is the required skills" or "this part is the difficulty level."

AI can read that text and understand it. But if we ask AI to just describe the JD, we get another block of text. That is not useful in code.

Instead, we tell AI: here is the JD text, and here is the exact structure I want back. We give AI a template — a JSON schema — and ask it to fill it in.

When AI returns the filled-in JSON, our app can directly access each field:
- response.requiredSkills → array of skills → render in Required Skills card
- response.roleType → one string → render in Role Type badge
- response.difficultyLevel → one string → render in Difficulty Level badge

This is what makes today's feature more than just "paste text and get a summary." We are building something programmable from AI output.

---

# Prerequisites: Mandatory Setup

Complete this before the live session:

1. Make sure your Session 1 app is open and working
2. Confirm the profile form saves and shows the profile summary
3. Confirm localStorage is working (refresh the page and check if the profile stays)
4. Keep a real job description from any job site (LinkedIn, Naukri, Indeed) ready in a text file
5. Read the prompts below before the session starts — you do not need to memorize them, just read once
6. Keep this file open during the session
7. Ensure your internet connection is stable (AI calls need network access)

## Optional Setup

Useful but not mandatory:

- A second job description to test the feature with different input
- Notepad or notes app open to write your own explanation after the Concept Pause
- Browser console open to watch for JSON parse errors

## Important Rule

Do not add the JD Analyzer feature before the session.

If you try to build it yourself first and something breaks, you will spend the whole session debugging instead of learning the concept.

Come to the session with the Session 1 app working and wait for the live walkthrough.

---

# Content to Prepare Before Class

Prepare this in a text file before class. You will paste this into the JD Analyzer text area during the session.

```text
Sample Job Description to use during Session 2:

We are looking for a Software Engineer to join our product team.

Responsibilities:
- Build and maintain responsive web applications using React
- Integrate AI/ML APIs into product features
- Write clean, maintainable code with proper documentation
- Collaborate with design and product teams to deliver features
- Debug and troubleshoot production issues
- Participate in code reviews and technical discussions

Requirements:
- Strong knowledge of JavaScript and React
- Experience with REST APIs and async programming
- Understanding of frontend performance optimization
- Exposure to AI/ML tools or APIs is a plus
- Familiarity with version control using Git
- Good communication and problem-solving skills

Nice to have:
- Experience with prompt engineering or LLM APIs
- Knowledge of Node.js or backend frameworks
- Prior experience in a startup environment

We are a mid-stage startup. This is a mid-level role.
```

---

# Prompts for Session 2

Use these prompts during the session when instructed.

---

## Prompt 1: Main Build Prompt

```text
I am building an app called "AI Interview Prep Copilot".

What is already built:
- A base profile dashboard (Session 1)
- A profile form that collects: Full Name, Target Role, Current Skills, Project Details, Weak Areas, Job Description
- Save Profile button with validation
- Saved profile summary displayed after saving
- localStorage persistence so profile stays after page refresh
- Edit Profile button
- Basic navigation labels for future features

What I need to add now (Session 2):
Add a JD Analyzer feature to the existing app.

Feature requirements:

1. Add a new section to the app called "JD Analyzer"
2. Add a large text area with placeholder text: "Paste your job description here..."
3. Add a button labeled "Analyze JD"
4. When the user clicks Analyze JD:
   a. Show a loading state (disable the button, show a spinner or "Analyzing..." message)
   b. Send the pasted job description to AI with a structured prompt
   c. The AI prompt must ask for a JSON response with exactly these keys:
      - requiredSkills: array of strings
      - keyResponsibilities: array of strings
      - roleType: one of "Frontend", "Full-Stack", "AI-ML", "Backend"
      - interviewTopics: array of exactly 5 strings
      - difficultyLevel: one of "Entry", "Mid", "Senior"
   d. Parse the JSON response
   e. Store the parsed result in app state
   f. Show five result cards below the text area:
      - Required Skills card: display as bullet list
      - Key Responsibilities card: display as numbered list
      - Role Type card: display as a badge
      - Interview Topics card: display as numbered list
      - Difficulty Level card: display as a colored badge
5. Show an empty state message before any analysis: "Paste a job description above and click Analyze JD to extract key information."
6. Show an error message if the user clicks Analyze JD with an empty text area: "Please paste a job description before analyzing."
7. Handle the case where the AI response might be wrapped in markdown code fences — strip the fences before parsing JSON
8. Wrap the JSON parse in a try-catch and show a user-friendly error if parsing fails

Do not add:
- PDF upload
- File parsing
- Backend API
- Database
- Auto-resume matching
- ATS scoring
- Login or authentication

Keep the existing profile dashboard fully intact. Add the JD Analyzer below or alongside it.

Add clear code comments explaining:
- where the structured AI prompt is written
- what JSON schema the prompt asks for
- where the JSON is parsed
- where the extracted data is stored in state
```

---

## Prompt 2: UI Improvement Prompt

```text
Improve the visual presentation of the JD Analyzer result cards.

Current state:
The cards are showing the data but look plain.

Improvements needed:
1. Required Skills card: show each skill as a chip or tag, not a plain text list
2. Key Responsibilities card: show as a clean numbered list with good spacing
3. Role Type card: display as a colored pill badge — use blue for Frontend, purple for Full-Stack, orange for AI-ML, green for Backend
4. Interview Topics card: show as a numbered list with each topic on a separate line
5. Difficulty Level card: use a colored badge — green for Entry, amber for Mid, red for Senior
6. Add a subtle card border or shadow to separate each result card visually
7. Add an icon or emoji label to each card heading for quick scanning
8. Make sure the result section is clearly separated from the input section

Keep the same data and logic. Only improve the visual layout.
Do not add new features or change the data structure.
```

---

## Prompt 3: Debugging Prompt — Analyze JD Button Does Nothing

```text
The Analyze JD button is not working. When I click it, nothing happens.

Please debug this issue.

Expected behavior:
1. When I paste a job description and click Analyze JD, the app should show a loading state
2. The app should call the AI function with the pasted JD text
3. The AI function should send a structured prompt asking for JSON output
4. The result should appear as five cards: Required Skills, Key Responsibilities, Role Type, Interview Topics, Difficulty Level

Please check:
- Is the button connected to the correct function?
- Is the AI function being called?
- Is the prompt being sent correctly?
- Is the response being handled?
- Are there any console errors?

Fix the issue and explain what was wrong in simple language.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the JD Analyzer feature in this app in beginner-friendly language.

Focus on:
1. Where is the JD Analyzer section added in the app?
2. Where is the structured AI prompt written in the code?
3. What does the prompt tell AI to return?
4. How is the AI response received and parsed?
5. What happens if the JSON parsing fails?
6. Where is the extracted data stored?
7. How are the five result cards created from the parsed data?
8. Which part of this code is most important to explain in an interview?

Do not rewrite the code. Only explain it clearly.
```

---

## Prompt 5: Interview Explanation Prompt

```text
Explain the JD Analyzer feature as if I am describing it in a job interview.

Use this structure:
1. What does the JD Analyzer do?
2. Why is it useful for interview preparation?
3. How does the AI integration work?
4. What is structured prompting and why did I use it here?
5. How does the app handle errors in the AI response?
6. What data does the extracted result store and why does that matter for future features?
7. What would I improve if I had more time?

Keep the explanation simple, confident, and interview-ready.
Avoid technical jargon where possible.
```

---

## Prompt 6: Structured JSON Output Prompt

```text
I need to write an AI prompt that extracts structured information from a job description.

The prompt should:
1. Accept a raw job description as input
2. Ask the AI to analyze it and return a JSON object
3. The JSON must have exactly these keys:
   - requiredSkills: an array of strings listing the technical and soft skills mentioned
   - keyResponsibilities: an array of strings listing the main job responsibilities
   - roleType: a single string, one of "Frontend", "Full-Stack", "AI-ML", "Backend"
   - interviewTopics: an array of exactly 5 strings representing the most important topics to prepare
   - difficultyLevel: a single string, one of "Entry", "Mid", "Senior"
4. Tell AI to return only the JSON object with no extra explanation text
5. Tell AI not to wrap the JSON in markdown code fences

Write the full prompt template I can use in my application code.
Also show me an example of what a correct response would look like for a React developer job description.
```

---

## Prompt 7: Error and Empty State Prompt

```text
Add better error and empty states to the JD Analyzer feature.

Currently:
The app may not handle all edge cases gracefully.

Add these states:

1. Empty input state:
   - Before the user pastes anything, show: "Paste a job description above and click Analyze JD to extract key information."
   - If the user clicks Analyze JD with an empty text area, show a red error message: "Please paste a job description before analyzing."

2. Short input warning:
   - If the pasted text is fewer than 100 characters, show a warning: "This job description seems very short. Results may not be accurate. Consider pasting a more complete JD."

3. JSON parse error state:
   - If the AI response cannot be parsed as JSON, show: "AI returned an unexpected response. Please try again."

4. Incomplete JSON state:
   - If the parsed JSON is missing one or more expected keys, show: "Analysis returned incomplete data. Some sections may not display."

5. Success state:
   - After successful analysis, show a small success message: "Analysis complete. Review the results below."

Do not remove or change existing functionality. Only add these states.
```

---

# What You Should Be Able to Explain After Session 2

By the end of the session, you should be able to answer these questions on your own without reading notes:

1. What does the JD Analyzer feature do?
2. What are the five pieces of information it extracts from a job description?
3. What is the difference between asking AI for prose and asking AI for JSON?
4. What does the structured prompt inside the app code say?
5. Why do we need to parse the AI response as JSON?
6. What happens if the AI returns JSON wrapped in markdown code fences?
7. Why do we store the extracted JD data in app state instead of a local variable?
8. What error states did you add, and why are they important?
9. How does the JD Analyzer connect to the Profile vs JD Match feature in Session 3?
10. How would you explain structured prompting to an interviewer in two sentences?

---

## Final Session 2 Explanation

```text
In Session 2, I added a JD Analyzer feature to the AI Interview Prep Copilot. The user pastes a raw job description, and the app sends it to AI with a structured prompt that asks for a specific JSON format. The AI returns extracted data — required skills, responsibilities, role type, interview topics, and difficulty level — which the app parses and displays as organized cards. This taught me how to use structured prompting to get programmable output from AI instead of just readable text.
```
