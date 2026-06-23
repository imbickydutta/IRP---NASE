# Session 3 Student Pre-Session File: Add Profile vs JD Match

## What We Are Building

In this 8-session interview-prep phase, we are building one continuous project:

# AI Interview Prep Copilot

This app will help a student prepare for interviews using AI.

By the end of all sessions, the app will be able to:

- store your interview profile
- analyze job descriptions
- compare your profile with the JD
- generate interview questions
- evaluate your mock answers
- answer doubts using RAG-lite
- create a 7-day interview prep plan

## What We Have Built So Far

### Session 1: Base Profile Dashboard

- student profile form (name, target role, skills, project details, weak areas, job description)
- Save Profile button
- profile summary display
- localStorage persistence

### Session 2: JD Analyzer

- JD Analyzer section
- "Analyze JD" button
- AI call that extracts required skills, responsibilities, role type, important interview topics, and difficulty level from the raw job description
- structured output displayed in the JD Analysis panel
- JD analysis stored in app state for use in later features

## Session 3 Goal

In Session 3, we will add the Profile vs JD Match feature.

This feature takes the profile you saved in Session 1 and the JD analysis produced in Session 2, sends both to an AI together with a structured comparison prompt, and produces a match report card.

## Session 3 Output

By the end of Session 3, you should have a working app where:

- clicking "Check My Match" reads your profile and JD analysis
- the app sends both to AI as labeled context
- the AI returns a structured comparison result
- the app displays a match report card showing:
  - overall match band (Strong / Moderate / Weak)
  - matched skills list
  - missing skills list
  - improvement suggestions (3–5 actionable items)
  - interview risk areas

---

# Pre-Read

## Why Are We Building This Feature?

In interviews, it is not enough to say:

"I uploaded my profile and the app gave me a score."

You should be able to explain:

- how the app read two separate pieces of context
- why those contexts were labeled differently in the prompt
- what a match band is and why it is more honest than a percentage
- how the app turned raw AI output into a structured report card
- what explainable AI output means and why every result comes with a reason
- what happens when the profile or JD analysis is missing
- what the disclaimer on the report card means and why it is necessary

This feature teaches you the most interview-relevant AI engineering concept in the course: sending multiple contexts to AI and designing output that explains itself.

## Simple App Flow

User fills profile in Session 1  
↓  
App saves profile to localStorage  
↓  
User pastes JD and clicks "Analyze JD" in Session 2  
↓  
App extracts required skills, responsibilities, role type, interview topics  
↓  
JD analysis stored in app state  
↓  
User clicks "Check My Match" in Session 3  
↓  
App reads profile from localStorage  
↓  
App reads JD analysis from app state  
↓  
App composes labeled comparison prompt with both contexts  
↓  
App sends prompt to AI  
↓  
AI returns match band, matched skills, missing skills, suggestions, risk areas  
↓  
App displays match report card  
↓  
Session 4 — Add Interview Question Generator: App uses match report and JD analysis to generate targeted interview questions

## Key Concepts to Revise

Before the session, think about these ideas:

1. What is context in AI? What information does an AI model use to generate its output?
2. What happens if you send two different pieces of information to AI without labeling which is which?
3. What does "structured output" mean? Why is a JSON object easier to display than raw text?
4. What is the difference between a qualitative label (Strong / Moderate / Weak) and a quantitative score (72%)?
5. What does "explainable AI" mean? Why should every AI result come with a reason?
6. What is a prompt template? Why do we use placeholders that get filled with real data at runtime?
7. What is a loading state? Why is it important when an async AI call is running?
8. What is app state? How is it different from localStorage?

## Simple Explanation

In Session 2, the app used AI to analyze a job description and extract structured information about what the role needs.

In Session 3, the app reads two things: what the student has (from the profile) and what the role needs (from the JD analysis). It sends both to AI together, with clear labels, and asks: "How well does this student match this role?"

AI returns a structured comparison — not just a number, but a band with reasons. The app then displays this comparison as a report card that the student can read and act on.

The key idea is this: AI is useful not just for extracting from one document, but for comparing across two documents when both are provided as labeled context.

---

# Prerequisites Before Session 3

## Mandatory Setup

Complete this before the live session:

1. Your Session 1 app (profile dashboard) must be working
2. Your Session 2 app (JD analyzer) must be working and producing JD analysis output
3. Your student profile must already be saved in the app (name, target role, skills, weak areas, JD)
4. The JD Analyzer must have successfully run at least once and produced output
5. You should be able to open the app and see both the profile summary and the JD analysis
6. Keep your app file open in the AI tool
7. Keep this pre-session file open during the session
8. Keep a stable internet connection

### Gemini API Setup (required for Session 3)

Session 3 calls the Gemini API directly from the browser. Complete these steps before class:

1. Install the package: run `npm install @google/generative-ai` in your project folder
2. Get a free API key from aistudio.google.com (free Google account, no credit card required)
3. Create a `.env` file in your project root (same folder as `package.json`) and add this line:
   ```
   VITE_GEMINI_API_KEY=your_key_here
   ```
   Replace `your_key_here` with the key you copied from aistudio.google.com
4. Restart your Vite dev server after adding the `.env` file (`npm run dev`)
5. Verify the key is loading: temporarily add this line at the top of your main component and check the browser console:
   ```
   console.log(import.meta.env.VITE_GEMINI_API_KEY)
   ```
   You should see your key printed. Remove this line after verifying.

Note: the `VITE_` prefix is required for Vite to expose the variable to the browser. This is acceptable for classroom use. Do not use this pattern in production apps.

## Optional Setup

Useful but not mandatory:

- a second sample JD ready in case you want to test the match with a different role
- notes from Session 2 on what the JD analysis output looks like (fields and structure)
- a list of 5–8 skills you have and 5–8 skills the target role requires, for quick testing

## Important Rule

If your Session 2 JD analyzer is not working, do not try to fix it during the live Session 3 class.

Instead, use the sample JD analysis object that the instructor will provide. Fix Session 2 after class.

Do not block your Session 3 progress because of a Session 2 issue.

---

# Content to Prepare Before Class

Prepare your own match test data in a text file before class.

```text
My Profile (what I already have):

Name:
Target Role:
My Skills (list each skill):
My Projects:
My Weak Areas:

JD Analysis from Session 2 (what the role requires):

Required Skills (list each):
Responsibilities (list key ones):
Role Type:
Interview Topics:
Difficulty Level:
```

## Sample Match Test Data

```text
My Profile:

Name: Aarav Sharma
Target Role: AI-assisted Junior Software Engineer
My Skills: prompt engineering, HTML basics, UI building with AI tools, basic JavaScript, no-code workflows, RAG basics
My Projects: travel planner prototype using AI tools — user enters destination and budget, app generates itinerary suggestions
My Weak Areas: explaining code, debugging errors, REST APIs, JavaScript logic, technical interview confidence

JD Analysis from Session 2:

Required Skills: frontend development, JavaScript, REST APIs, data handling, prompt engineering, AI feature integration, debugging, product thinking, LLMs, automation tools, rapid prototyping
Responsibilities: build web applications using AI-assisted tools, integrate AI features into product, debug and test features, collaborate with product team
Role Type: Junior Software Engineer (AI-assisted track)
Interview Topics: JavaScript basics, API integration, frontend state management, prompt engineering, AI feature design, debugging approach
Difficulty Level: Entry to mid-level

Expected Match Band: Moderate
Expected Matched Skills: prompt engineering, UI building with AI tools, RAG basics, rapid prototyping, LLMs
Expected Missing Skills: REST APIs, JavaScript logic, debugging, data handling, system design basics
```

---

# Prompts for Session 3

Use these prompts during the session when instructed.

---

## Prompt 1: Main Build Prompt

```text
I am building an AI Interview Prep Copilot web app.

Here is what is already built:

Session 1 — Base Profile Dashboard:
- Student profile form with fields: Full Name, Target Role, Current Skills, Project Details, Weak Areas, Job Description
- Save Profile button with validation
- Profile Summary section that shows saved profile
- Data stored in localStorage under the key "studentProfile"
- Edit Profile button

Session 2 — JD Analyzer:
- JD Analyzer section with a textarea for raw job description
- "Analyze JD" button that sends the JD text to an AI
- AI returns structured output: required skills, responsibilities, role type, important interview topics, difficulty level
- JD analysis is displayed in a panel
- JD analysis is stored in app state as a variable called jdAnalysis

Now add Session 3: Profile vs JD Match feature.

Build the following:

1. A new "Match Report" section in the dashboard
2. A "Check My Match" button
3. When clicked, the button should:
   a. Read the student profile from localStorage using the key "studentProfile"
   b. Read the JD analysis from the existing jdAnalysis state variable
   c. If the profile is missing, show a message: "Please complete your profile first before checking your match."
   d. If the JD analysis is missing, show a message: "Please run the JD Analyzer first before checking your match."
   e. If both are available, compose a labeled comparison prompt like this:

   STUDENT PROFILE:
   Name: [name]
   Target Role: [target role]
   Skills: [skills]
   Projects: [projects]
   Weak Areas: [weak areas]

   JD ANALYSIS:
   Required Skills: [required skills]
   Responsibilities: [responsibilities]
   Role Type: [role type]
   Interview Topics: [interview topics]
   Difficulty: [difficulty level]

   Task: Compare the student profile with the JD analysis. Return your response with these exact sections:
   - MATCH BAND: (Strong / Moderate / Weak) with a 1-2 sentence reason
   - MATCHED SKILLS: list of skills the student has that the JD requires
   - MISSING SKILLS: list of skills the JD requires that the student does not have
   - IMPROVEMENT SUGGESTIONS: 3 to 5 specific actionable steps the student can take
   - INTERVIEW RISK AREAS: 2 to 4 specific topics where the student may struggle in interviews for this role

4. Show a loading state ("Generating match report...") while the AI is processing
5. When the AI responds, parse the output and display it in a styled match report card with separate sections for each part
6. Display the match band as a colored badge: green for Strong, amber for Moderate, red for Weak
7. Add a disclaimer at the bottom of the report card:
   "This report is AI-generated. Use it as a guide, not a guarantee."
8. Show an error message if the AI call fails: "Unable to generate match report. Please try again."

Use the following for the AI call:
- Use the Gemini API via the @google/generative-ai npm package
- API key from: import.meta.env.VITE_GEMINI_API_KEY
- Model: gemini-1.5-flash
- For JSON output use responseMimeType: "application/json" in generationConfig

Do NOT add:
- ATS scores or hiring percentage numbers
- Resume upload feature
- Job board integration
- Backend database
- Login or authentication
- Any feature not described above

Add clear comments in the code explaining:
- where the profile is read from localStorage
- where the JD analysis is read from app state
- how the comparison prompt is composed with labeled contexts
- where the AI call is made
- how the response is parsed into report sections
```

---

## Prompt 2: UI Improvement Prompt

```text
Improve the visual design of the match report card in the AI Interview Prep Copilot.

Keep the same functionality. Do not change the AI call logic.

Improve the following:

1. The match band badge should be larger and clearly visible at the top of the card
2. Use distinct icons or colors to separate matched skills (positive) from missing skills (gap)
3. Display improvement suggestions as a numbered list with bold action words
4. Display interview risk areas with a warning-style highlight (amber or red background)
5. Add a header to the report card: "Your Match Report — [Target Role]"
6. Add a subtle divider between each section
7. Make the disclaimer text smaller and italicized
8. Keep the overall design consistent with the rest of the app

Do not add new features. Only improve the visual design of the existing report card.
```

---

## Prompt 3: Debugging Prompt — Match Report Not Generating

```text
The "Check My Match" feature is not generating a match report correctly.

Please debug and fix the issue.

Expected behavior:
1. Clicking "Check My Match" should read the student profile from localStorage.
2. It should read the JD analysis from the jdAnalysis state variable.
3. It should compose a labeled comparison prompt with both contexts.
4. It should send the prompt to the AI and show a loading state.
5. When the AI responds, it should parse the output and display the report card with match band, matched skills, missing skills, improvement suggestions, and interview risk areas.

Possible issues to check:
- Is the profile being read from localStorage correctly using the key "studentProfile"?
- Is the jdAnalysis state variable populated when the button is clicked?
- Is the comparison prompt being composed before the AI call?
- Is the loading state being cleared after the AI responds?
- Is the AI response being parsed into the expected sections?

Please explain what was wrong and what you changed.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the Profile vs JD Match feature code in beginner-friendly language.

Focus on:
1. How does the app read the student profile from localStorage?
2. How does the app read the JD analysis from app state?
3. How is the comparison prompt composed? Why are the two contexts labeled separately?
4. Where is the AI call made and what does it send?
5. How is the AI response parsed into match band, matched skills, missing skills, suggestions, and risk areas?
6. How is the loading state controlled?
7. How are empty states handled when profile or JD analysis is missing?
8. Which parts should I explain in an interview about context management?

Do not rewrite the code. Only explain it clearly.
```

---

## Prompt 5: Interview Explanation Prompt

```text
Explain the Profile vs JD Match feature as if I am preparing for an interview.

Use this structure:
1. What does this feature do?
2. What inputs does it use and where do they come from?
3. How does the app send two contexts to AI in a single prompt?
4. What is context management and why does it matter here?
5. What is a match band and why is it more honest than a percentage score?
6. What is explainable AI output and how is it implemented in this feature?
7. What happens when the profile or JD analysis is missing?
8. What are the limitations of this feature?
9. What would I improve if given more time?

Keep the explanation simple, interview-ready, and confident.
```

---

## Prompt 6: Structured JSON Output Prompt

```text
Modify the AI call in the Profile vs JD Match feature to request a structured JSON response instead of plain text.

Use this JSON schema for the AI output:

{
  "matchBand": "Strong" or "Moderate" or "Weak",
  "matchBandReason": "1-2 sentence explanation of why this band was assigned",
  "matchedSkills": ["skill1", "skill2", "skill3"],
  "missingSkills": ["skill1", "skill2", "skill3"],
  "improvementSuggestions": [
    "Suggestion 1: specific action",
    "Suggestion 2: specific action",
    "Suggestion 3: specific action"
  ],
  "interviewRiskAreas": [
    "Risk area 1: explanation",
    "Risk area 2: explanation"
  ]
}

Update the prompt to ask the AI to return only valid JSON in this exact schema.
Update the parsing logic to parse the JSON response and map each field to the correct report card section.
If the JSON is malformed or incomplete, fall back to an error state with the message: "Unable to parse match report. Please try again."

Add a comment explaining the JSON parsing logic.
```

---

## Prompt 7: Error and Empty State Prompt

```text
Improve the error and empty state handling in the Profile vs JD Match feature.

Handle these cases:

1. If the student profile is not found in localStorage, show a clear message:
   "Your profile is not saved yet. Please go to the Profile section and save your profile first."
   Add a link or button that navigates the user to the profile form.

2. If the JD analysis is not available in app state, show a clear message:
   "JD analysis is not available. Please go to the JD Analyzer section and run the analysis first."
   Add a link or button that navigates the user to the JD Analyzer section.

3. If the AI call fails due to a network error, show:
   "Unable to reach AI service. Please check your connection and try again."
   Show a "Retry" button.

4. If the AI call returns an empty or malformed response, show:
   "Match report could not be generated. Please try again."

5. If the user has no skills listed in their profile, include a note in the missing skills section:
   "No skills were found in your profile. The match accuracy may be low."

Keep all other functionality unchanged.
```

---

# What You Should Be Able to Explain After Session 3

By the end of the session, you should be able to answer these questions on your own. These do not have printed answers here — practice answering them yourself.

1. What is the Profile vs JD Match feature and what does it display?
2. Where does the feature get its two inputs from?
3. Why do we label both contexts separately in the comparison prompt?
4. What is a match band and why is it more useful than a percentage score?
5. What is context management in AI applications?
6. What is explainable AI output and how did you implement it in this feature?
7. What happens if the student profile is missing when the user clicks "Check My Match"?
8. What happens if the JD analysis is not available in app state?
9. Why is the disclaimer important on the report card?
10. What would you improve in this feature if you had more time?

---

## Final Session 3 Explanation

```text
In Session 3, I added a Profile vs JD Match feature to the AI Interview Prep Copilot. The feature reads the student profile from localStorage and the JD analysis from the app state, combines both as labeled context in a single comparison prompt, and sends it to AI. The AI returns a structured match report with an overall match band (Strong, Moderate, or Weak), matched skills, missing skills, improvement suggestions, and interview risk areas. The report card is designed to be explainable — every result comes with a reason — because AI comparisons should guide the user, not just label them.
```
