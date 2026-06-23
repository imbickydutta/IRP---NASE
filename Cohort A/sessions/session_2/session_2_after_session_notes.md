# Session 2 After-Session Notes: Add JD Analyzer

## What We Built Today

Today we added the JD Analyzer feature to the AI Interview Prep Copilot.

The app can now:

- Accept a raw job description from the user via a text area
- Send the job description to AI with a structured prompt
- Receive a JSON response with five extracted fields
- Parse and display the extracted data as organized result cards
- Store the extracted JD data in app state for use in Session 3

The five extracted fields are:

- Required Skills — list of technical and soft skills mentioned in the JD
- Key Responsibilities — list of main job responsibilities
- Role Type — categorized as Frontend, Full-Stack, AI-ML, or Backend
- Top 5 Interview Topics — five most important topics to prepare based on the JD
- Difficulty Level — Entry, Mid, or Senior

---

# Why This Feature Matters

A job description is just paragraphs of text. On its own, it is hard to act on.

The JD Analyzer turns that unstructured text into structured, actionable data. A student can now see immediately:

- what skills they need
- what they would do in the role
- how hard the interview is likely to be
- exactly what topics to prepare

More importantly, the extracted data feeds the next feature. In Session 3, the app will compare the student's skills from their profile against the required skills from the JD Analyzer. That comparison only works because Session 2 extracted and stored the JD data in a usable format.

This is how a real product is built — each session's output becomes the next session's input.

---

# App Flow

The complete flow from Session 1 — Base Profile Dashboard through Session 2:

User fills in profile form (Name, Target Role, Skills, Project Details, Weak Areas, Job Description)
↓
User clicks Save Profile
↓
App validates required fields
↓
App saves profile to localStorage
↓
App displays Profile Summary
↓
User navigates to JD Analyzer section
↓
User pastes raw job description into text area
↓
User clicks Analyze JD
↓
App validates input is not empty
↓
App shows loading state
↓
App sends JD text + structured prompt to AI
↓
AI returns JSON object with five keys
↓
App strips any markdown formatting from AI response
↓
App parses JSON using JSON.parse()
↓
App stores extracted data in app state
↓
App hides loading state
↓
App renders five result cards: Required Skills, Key Responsibilities, Role Type, Interview Topics, Difficulty Level
↓
Session 3 — Add Profile vs JD Match — will read this stored JD data to run Profile vs JD Match

---

# What is Structured Prompting and JSON Output?

When we give AI a question, the answer it gives depends heavily on how we phrased the question. This is true for humans too, but it is especially important with AI because the app needs to use that answer in code.

If we ask: "What are the skills in this job description?" — AI will write a sentence or a paragraph. That is natural language. We cannot easily split it into a list, sort it, or render it in separate UI cards. We would need to guess where one skill ends and another begins.

Structured prompting solves this by asking AI to format its answer in a specific way. We tell AI: return your answer as a JSON object with these exact keys. We list the keys, the expected value types — array of strings, or one of these specific options — and we tell AI not to add anything else to the response. The result is a clean, predictable, machine-readable output every time.

JSON output is particularly useful because JavaScript applications can directly parse JSON using JSON.parse(). Once parsed, the data is a regular JavaScript object. We can access response.requiredSkills, response.roleType, response.difficultyLevel just like accessing any variable. We can then map each value to a UI component.

The concept of structured prompting goes beyond this app. Any time a developer wants AI to participate in a data pipeline — extract information, classify input, generate options, return decisions — structured prompting is the approach that makes the AI output usable in code. It is a foundational pattern in modern AI product development.

---

# What Students Should Understand

Students should understand:

1. The JD Analyzer feature sends a raw text input to AI and receives structured JSON output
2. The structured prompt inside the code is what causes AI to return JSON instead of prose
3. The prompt must specify the exact keys, value types, and allowed values expected in the JSON
4. JSON.parse() converts the AI response string into a usable JavaScript object
5. AI sometimes wraps its JSON response in markdown code fences — the app must strip these before parsing
6. The extracted JD data is stored in app state so other features in the same app can access it
7. A loading state is needed because AI calls are asynchronous — they take time to respond
8. Error handling for JSON parsing is required — AI can occasionally return an unexpected format
9. Displaying structured data as cards is a product design decision — it makes the extracted information scannable and actionable
10. The JD Analyzer output directly enables Session 3's Profile vs JD Match feature

---

# Interview-Ready Explanation

```text
In Session 2, I added a JD Analyzer to the AI Interview Prep Copilot. The user pastes a raw job description and the app uses structured prompting to ask AI for a JSON response with five specific fields: required skills, key responsibilities, role type, interview topics, and difficulty level. The app parses the JSON and displays each field as a result card. The extracted data is also saved in app state so the next feature — Profile vs JD Match — can compare it against the student's profile.
```

---

# What Happens When Analyze JD Is Clicked?

Expected answer:

```text
When Analyze JD is clicked, the app first checks whether the text area has any content. If it is empty, an error message is shown asking the user to paste a job description. If there is content, the app sets a loading state to disable the button and show a loading indicator. It then sends the job description text to the AI along with a structured prompt that asks for a JSON response with five specific keys. When the AI responds, the app strips any markdown formatting from the response string and then parses it using JSON.parse(). If parsing succeeds, the extracted data is stored in app state and five result cards are rendered. If parsing fails, an error message is shown asking the user to try again.
```

---

# What AI Was Used For

AI was used to help:

- Generate the JD Analyzer section within the existing app layout
- Write the initial structured prompt that asks for JSON output
- Create the logic to strip markdown code fences from AI responses
- Build the result card components for each of the five extracted fields
- Add loading state and error state handling
- Write the JSON parsing logic with try-catch

But students still need to:

- Test the feature with a real job description — not a placeholder
- Verify that all five cards appear with actual data
- Check that the JSON keys match what the app expects
- Test the error state by clicking Analyze JD with an empty input
- Verify the extracted data is accessible in state for future features
- Understand what the structured prompt says and why it produces JSON
- Be able to explain the feature flow in an interview without reading notes

---

# Common Issues and Fixes

## Issue 1: Analyze JD button clicks but nothing appears

Possible reasons:
- The button is not connected to the analyze function
- The AI function is not being called
- The prompt is missing or malformed
- The response is not being handled or stored

What to ask AI:

```text
The Analyze JD button is not producing any results. Please check whether the button is correctly connected to the analyze function, whether the AI function is being called with the JD text, whether the prompt is properly structured, and whether the response is being parsed and stored in state. Fix the issue and explain what was wrong.
```

## Issue 2: JSON parse error — AI returned unexpected format

Possible reasons:
- AI wrapped the JSON in markdown code fences (```json ... ```)
- AI returned a partial JSON with missing closing brackets
- AI added extra explanation text before or after the JSON
- The prompt did not explicitly tell AI to return only JSON

What to ask AI:

```text
The JD Analyzer is throwing a JSON parse error. The AI response may be wrapped in markdown code fences or contain text before or after the JSON. Please add logic to strip any markdown formatting from the AI response before parsing. Also update the prompt to explicitly say: return only the JSON object with no explanation text and no markdown code fences. Show me the updated prompt and the updated parsing logic.
```

## Issue 3: Result cards appear but some fields are empty or missing

Possible reasons:
- The AI JSON used different key names than the app expects
- The prompt did not list the exact key names clearly
- One of the required keys was not returned in the response
- The app is accessing the wrong key when rendering the card

What to ask AI:

```text
Some result cards in the JD Analyzer are empty or showing undefined. Please check whether the key names in the AI response match the key names the app uses when rendering the cards. Check the prompt to make sure it specifies exactly these key names: requiredSkills, keyResponsibilities, roleType, interviewTopics, difficultyLevel. Also add a fallback so that if a key is missing, the card shows "Not available" instead of breaking.
```

---

# Key Takeaways

1. Structured prompting is a design decision, not just a coding trick

The way you write the prompt determines what kind of output you get from AI. Asking for JSON is a deliberate engineering choice that makes AI output usable in application code. This is a pattern you will use throughout your career in AI-powered product development.

2. JSON.parse() bridges AI output and application logic

AI returns a string. Your app needs an object. JSON.parse() is the step in between. Always wrap it in a try-catch — AI responses are not always perfectly formatted, and a crash in this step breaks the whole feature.

3. Storing extracted data in state enables feature chaining

The JD Analyzer does not just display results. It stores them. That stored data is what allows Session 3's Profile vs JD Match to function. Every session in this project is designed so the output of one session becomes the input of the next. This is how a real product is architected.

4. Good UI on structured data is a product skill

Displaying required skills as chips instead of a paragraph, using colored badges for role type and difficulty level, and separating input from results with clear layout — these are product decisions. They make the structured data actually useful to the user. Interviewers notice when students can talk about both the technical implementation and the user experience reasoning.

---

# Session 3 Preview

In Session 3 — Add Profile vs JD Match — we will add the Profile vs JD Match feature.

The app will compare the student's skills from their saved profile against the required skills extracted by the JD Analyzer today.

The result will be:

- a match score or percentage
- matched skills — skills the student already has
- missing skills — skills the JD requires that the student does not have
- a simple recommendation based on the gap

Main AI concept for Session 3:

Comparative prompting — sending two sets of data to AI and asking it to compare them and return a structured result.

Session 3 will use the JD data you extracted today. Make sure your Session 2 feature is working and the extracted JD data is stored in app state before Session 3 starts.
