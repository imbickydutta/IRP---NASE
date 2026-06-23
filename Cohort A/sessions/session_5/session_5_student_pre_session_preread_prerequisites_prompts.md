# Session 5 Student Pre-Session File: Add Mock Answer Evaluator

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

## What Has Been Built So Far

- Session 1: Base Profile Dashboard — profile form, target role, skills, weak areas, job description, localStorage persistence
- Session 2: JD Analyzer — extracts required skills, responsibilities, role type, and interview topics from the job description
- Session 3: Profile vs JD Match — compares the student profile with the JD and generates a match report with gaps
- Session 4: Interview Question Generator — uses the profile and JD to generate a categorized list of likely interview questions (generated questions available in app state)

## Session 5 Goal

In Session 5, we will add the Mock Answer Evaluator.

This feature lets a student:

- select a question from the Session 4 generated list, or type a custom question
- type their answer in a text area
- submit the answer for AI evaluation
- receive a structured feedback card

## Session 5 Output

By the end of Session 5, your app should have a working evaluator where you can:

- pick a question from the dropdown or type your own
- write your answer
- click Submit for Evaluation
- see a feedback card with score, strengths, missing points, improved answer, and a follow-up question

---

# Pre-Read

## Why Are We Building This Feature?

In interviews, most students practice answering questions — but they have no way to know if their answers are good.

They either:

- ask a friend who is not an expert
- read model answers without comparing their own
- guess based on their confidence level

The Mock Answer Evaluator gives structured, criteria-based feedback instantly. It does not replace expert mentorship. But it gives students a consistent mirror to test and improve their answers before the actual interview.

In an interview, you should be able to explain:

- what the evaluator does
- how you designed the AI prompt to produce structured feedback
- why the five-component feedback card is more useful than a vague opinion
- what the limitations of AI evaluation are
- how you would improve the evaluator if you had more time

## Simple App Flow

User enters profile and saves  
↓  
JD Analyzer extracts skills and topics from the job description  
↓  
Profile vs JD Match generates a gap report  
↓  
Question Generator creates a list of likely interview questions  
↓  
User selects a question from the list or types a custom one  
↓  
User types their answer in the text area  
↓  
App builds a rubric-based evaluation prompt  
↓  
AI evaluates the answer and returns structured feedback  
↓  
App displays the feedback card with score / strengths / missing points / improved answer / follow-up question

## Key Concepts to Revise

Before the session, revise or read about these ideas:

- What is a rubric? — A rubric is a set of specific criteria used to evaluate something. A rubric defines what to score and how much each criterion is worth.
- What is structured output from AI? — When you ask AI to return output in a specific format (JSON or labeled sections) rather than free-flowing text
- What is a feedback loop? — A cycle where a user gets feedback, improves based on it, and tries again. This evaluator creates a feedback loop for interview practice.
- What is prompt engineering? — Writing AI instructions carefully so the output matches exactly what you need
- What is state in a web app? — The data your app is currently holding in memory. In our case, the Session 4 generated questions are in state.
- What is a dropdown (select element)? — A UI component that lets the user pick from a list of options
- What is a text area? — A multi-line input field where users can type longer text
- What is an API call? — A request your app sends to an external service (like an AI model) and waits for a response

## Simple Explanation

When you ask a human examiner to evaluate an interview answer, they use their experience and standards. They think about whether the answer is correct, clear, complete, and well-structured.

When we ask AI to evaluate an interview answer, we need to give it those standards explicitly. We write them into the prompt. This is called rubric-based prompting.

Our prompt tells AI:
- what the question was
- what the student answered
- what criteria to score on (correctness, clarity, depth, examples, completeness)
- what format to return the result in (score, strengths, missing points, improved answer, follow-up question)

AI then follows those instructions and produces a structured evaluation. The app takes that structured output and displays it as a clean feedback card.

---

# Prerequisites Before Session

## Mandatory Setup

Complete this before the live session:

1. Make sure your AI Interview Prep Copilot app from Sessions 1 through 4 is working
2. Confirm that Session 4's Question Generator is working and generating questions
3. Have the app open and ready before class starts
4. Set up the Gemini API for your React app (required for this session):
   - Run in your project folder: `npm install @google/generative-ai`
   - Create a `.env` file in your project root (same folder as `package.json`) and add: `VITE_GEMINI_API_KEY=your_key_here`
   - Get your free API key at: aistudio.google.com (free Google account, no credit card needed)
   - Replace `your_key_here` with the key you copied from AI Studio
   - Restart your dev server (`npm run dev`) after adding the `.env` file
   - Verify setup: temporarily add `console.log(import.meta.env.VITE_GEMINI_API_KEY)` at the top of your main component and check the browser console — you should see your key printed
   - Remove that console.log line after confirming it works
5. Prepare 2–3 sample answers to interview questions (one short answer, one detailed answer, one incorrect or incomplete answer — this helps you test the evaluator properly)
6. Keep a sample interview question ready for manual entry testing
7. Have your AI coding tool (Antigravity or equivalent) open and ready
8. Keep this pre-session file open during the session for reference

## Optional Setup

Useful but not mandatory:

- Review the Session 4 code to understand how generated questions are stored in state
- Think about what makes a good interview answer for your target role
- Look up one or two sample strong answers to common interview questions in your field

## Important Rule

Do not spend the live session debugging your Sessions 1–4 app.

If your previous sessions are not working, follow the instructor screen and use the provided code fallback. Keep the focus on Session 5.

---

# Content to Prepare Before Class

Prepare this in a text file before class. You will use this to test your Mock Answer Evaluator.

```text
Sample Question 1 (Basic):
Tell me about yourself.

Your Answer to Q1:
[Write a 3-5 sentence answer here. Keep it honest and based on your actual profile.]

Sample Question 2 (Technical):
[Pick a technical question relevant to your target role — e.g., "Explain how a REST API works" or "What is the difference between SQL and NoSQL?"]

Your Answer to Q2:
[Write your answer here. Try to write the best answer you can so you can compare it with the AI evaluation.]

Sample Question 3 (Weak Answer Test):
[Use the same technical question as Q2.]

Weak Answer for Q3:
[Write a very short or incomplete answer intentionally — e.g., just one sentence. This helps you test how the evaluator handles poor answers.]
```

---

# Prompts for Session 5

Use these prompts during the session when instructed.

---

## Prompt 1: Main Build Prompt

```text
I am building a web app called "AI Interview Prep Copilot".

Here is what has already been built across Sessions 1 through 4:

Session 1 — Base Profile Dashboard:
- Profile form with fields: Full Name, Target Role, Current Skills, Project Details, Weak Areas, Job Description
- Save Profile button with localStorage persistence
- Profile summary display
- Edit profile functionality

Session 2 — JD Analyzer:
- Takes the job description from the profile
- Sends it to AI with a structured prompt
- Displays extracted: Required Skills, Responsibilities, Role Type, Interview Topics

Session 3 — Profile vs JD Match:
- Compares the saved profile with the JD analysis
- Generates a match report showing matched skills, missing skills, and improvement suggestions
- Displays a match percentage or readiness score

Session 4 — Interview Question Generator:
- Uses the profile and JD analysis as context
- Sends a structured prompt to AI
- Generates a categorized list of interview questions (Technical, Behavioral, Role-Specific)
- Questions are stored in app state as an array and displayed in the UI

Now add Session 5 — Mock Answer Evaluator.

Build the following feature and integrate it into the existing app:

1. A question input section with two options:
   - A dropdown (select element) populated from the Session 4 generated questions array in app state
   - A manual/custom question text input for questions not in the list
   - The user should be able to use either option to set the question for evaluation

2. An answer text area:
   - Multi-line text area labeled "Your Answer"
   - Placeholder text: "Type your answer here..."
   - Minimum height of 150px

3. A Submit for Evaluation button:
   - Validates that both a question and an answer are present before submitting
   - If either is empty, show a validation error message
   - When both are present, trigger the evaluation function

4. A loading state:
   - Show a loading indicator while waiting for the AI response
   - Disable the Submit button during loading

5. A feedback card that displays after evaluation with these five sections:
   - Score: out of 10, displayed prominently
   - Strengths: what the student did well in their answer
   - Missing Key Points: what was absent or underdeveloped in the answer
   - Improved Answer: a better version of the student's answer
   - Follow-Up Question: one follow-up question an interviewer might ask based on this answer

6. Use the Gemini API to send the evaluation prompt to AI:
   - Package: @google/generative-ai (already installed in setup)
   - API key: import.meta.env.VITE_GEMINI_API_KEY
   - Model: gemini-1.5-flash
   - Import: import { GoogleGenerativeAI } from "@google/generative-ai"
   - Init: const genAI = new GoogleGenerativeAI(import.meta.env.VITE_GEMINI_API_KEY)
   - Get model: const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" })
   - Call: const result = await model.generateContent(prompt); const text = result.response.text()
   - For the structured JSON output version (Prompt 6), add generationConfig: { responseMimeType: "application/json", temperature: 0 }

7. The evaluation function should build and send this rubric-based prompt to the AI:

"You are an expert interview coach evaluating a candidate's answer to an interview question.

Question: [insert selected question here]

Candidate's Answer: [insert student's answer here]

Evaluate this answer using the following rubric:
- Correctness and accuracy (0-3 points)
- Clarity and structure (0-2 points)
- Depth and completeness (0-2 points)
- Use of relevant examples (0-2 points)
- Professional terminology (0-1 point)

Return your evaluation in this exact format:

Score: [total out of 10]

Strengths:
[list 2-3 specific things the candidate did well]

Missing Key Points:
[list 2-4 things that were missing or underdeveloped]

Improved Answer:
[write a better version of the answer in 3-5 sentences]

Follow-Up Question:
[write one follow-up question an interviewer would ask based on this answer]"

8. An empty state when no evaluation has been submitted yet:
   - Show a message: "Submit your answer above to see your evaluation feedback."

9. Do NOT add:
   - Voice input or voice output
   - Timed interview mode
   - Multi-question sequential interview flow
   - Answer history saved to a database
   - Any feature not listed above

Add clear comments in the code explaining:
- where the question dropdown is populated from Session 4 state
- where the rubric prompt is constructed
- how the AI response is parsed into five sections
- where the feedback card is rendered
```

---

## Prompt 2: UI Improvement Prompt

```text
Improve the UI of the Mock Answer Evaluator feature in the AI Interview Prep Copilot.

Keep all existing functionality. Make the following improvements:

1. Score display:
   - Show the score in a large, bold circle or badge
   - Color code: green for 7-10, yellow for 4-6, red for 1-3

2. Feedback card sections:
   - Add a clear header label for each of the five sections
   - Use icons or colored left borders to distinguish sections visually
   - Make the Improved Answer section stand out with a slightly different background

3. Add a "Try Again" button below the feedback card:
   - Clears the feedback card
   - Resets the answer text area to empty
   - Keeps the selected question so the student can refine their answer

4. Add a header at the top of the feedback card showing:
   - "Evaluation for: [question text]"
   - This reminds the student which question was evaluated

5. Improve the question input area:
   - Add a label above the dropdown: "Select a question from your generated list"
   - Add a separator or divider between the dropdown and the manual entry option
   - Add a label: "Or type a custom question"

6. Keep the overall layout consistent with the rest of the app.

Do not add voice, timing, or answer history features.
```

---

## Prompt 3: Debugging Prompt — Feedback Card Not Displaying

```text
The Mock Answer Evaluator is not displaying the feedback card after I submit my answer.

The Submit for Evaluation button is clicked, the loading state appears briefly, but then either nothing is shown or only raw text appears instead of the five-section feedback card.

Please debug and fix this issue.

Expected behavior:
1. Student selects a question and types an answer.
2. Student clicks Submit for Evaluation.
3. A loading indicator appears.
4. After the AI response arrives, the feedback card should display with five clearly labeled sections:
   - Score out of 10
   - Strengths
   - Missing Key Points
   - Improved Answer
   - Follow-Up Question
5. Each section should be rendered separately in the UI, not as one block of raw text.

Please check:
- Whether the AI response is being received correctly
- Whether the parsing logic is splitting the response into the five sections
- Whether the feedback card component is receiving the parsed data
- Whether the state update after the AI response triggers a re-render

Explain what was wrong and what you changed.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the current code of the Mock Answer Evaluator feature in beginner-friendly language.

Focus on:
1. Where is the question dropdown created and how is it populated from Session 4 state?
2. Where is the rubric prompt constructed? Show me that section of code.
3. What exactly is sent to the AI API when Submit is clicked?
4. How is the AI response parsed into five separate sections?
5. How is the feedback card rendered — which component or section of code handles this?
6. What is the loading state doing?
7. What validation happens before the API call is made?
8. Which parts of this code should I be able to explain in an interview?

Do not rewrite the code. Only explain it clearly in plain language.
```

---

## Prompt 5: Interview Explanation Prompt

```text
Help me explain the Mock Answer Evaluator feature as if I am preparing for a technical interview.

Use this structure:
1. What feature did I build in Session 5?
2. What problem does it solve for the user?
3. What are the inputs and outputs of the feature?
4. What is a rubric-based evaluation prompt and why did I use one?
5. How does the app construct the prompt before sending it to AI?
6. How does the app parse the AI response into five sections?
7. What are the limitations of AI scoring?
8. What did I use AI for while building this feature?
9. What would I improve if I had more time?

Keep the explanation simple, interview-ready, and around 3-5 sentences per question.
```

---

## Prompt 6: Structured JSON Output Prompt

```text
Modify the Mock Answer Evaluator to request a structured JSON response from AI instead of plain text.

Update the evaluation prompt sent to AI to request this exact JSON schema:

{
  "score": <number between 1 and 10>,
  "strengths": [<string>, <string>, <string>],
  "missing_key_points": [<string>, <string>, <string>],
  "improved_answer": "<string with improved answer in 3-5 sentences>",
  "follow_up_question": "<string with one follow-up question>"
}

Then update the parsing logic to:
1. Parse the returned JSON string into a JavaScript object
2. Map each field directly to the corresponding section of the feedback card
3. Handle the case where JSON parsing fails — if the AI does not return valid JSON, fall back to displaying the raw text in a single block with a note saying "Structured display unavailable. Raw feedback shown below."

Also add a comment in the code explaining why JSON output is more reliable for structured feedback cards than trying to parse plain text.
```

---

## Prompt 7: Error and Empty State Prompt

```text
Add proper error handling and empty states to the Mock Answer Evaluator feature.

Handle these specific cases:

1. Empty answer submission:
   - If the answer text area is empty when Submit is clicked, show an inline error message: "Please type your answer before submitting."
   - Do not make the API call.

2. Empty question:
   - If no question is selected from the dropdown and the custom question field is also empty, show: "Please select or type a question before submitting."

3. No questions in dropdown:
   - If the Session 4 question generator has not been run and the questions array is empty, show a message inside the dropdown area: "No questions generated yet. Go to Question Generator first, or type a custom question below."

4. API call failure:
   - If the AI API call fails for any reason, show an error message: "Evaluation failed. Please try again. If the problem continues, check your connection."
   - Reset the loading state so the student can try again.

5. Before any evaluation is submitted:
   - Show an empty state placeholder: "Submit your answer above to see your evaluation feedback."

6. Loading state:
   - Show a spinner or loading message: "Evaluating your answer..."
   - Disable the Submit button while loading to prevent duplicate submissions.

Keep all existing functionality. Do not add voice or timed features.
```

---

# What You Should Be Able to Explain After Session 5

By the end of the session, you should be able to answer these questions on your own. Do not look at the answers — practice explaining them independently.

1. What is the Mock Answer Evaluator and what problem does it solve?
2. How does the question dropdown get populated from Session 4's generated questions?
3. What happens step by step when the student clicks Submit for Evaluation?
4. What is a rubric-based evaluation prompt and how is it different from asking AI for general feedback?
5. What are the five components of the feedback card and why was each one included?
6. How does the app parse the AI response into five separate sections?
7. What are three limitations of AI scoring that a student should be aware of?
8. What happens if the answer text area is empty when Submit is clicked?
9. Why is structured output (JSON or labeled sections) important for a feature like this?
10. How would you explain this feature in one minute to an interviewer who has never seen the app?

## Final Session 5 Explanation

```text
In Session 5, I added the Mock Answer Evaluator to the AI Interview Prep Copilot. A student can select an interview question from the list generated in Session 4, or type a custom question, then type their answer and submit it for evaluation. The app sends a rubric-based prompt to AI that specifies scoring criteria and forces a structured response. The feedback card displays a score out of 10, strengths, missing key points, an improved answer, and one follow-up question — giving the student actionable feedback rather than a vague impression.
```

---

# Session 6 Preview

In Session 6 — Add RAG-Lite Doubt Solver — we will add a feature that lets you type a specific doubt or question and get an AI answer grounded in your own profile, JD analysis, and session context.

This is a simplified version of Retrieval-Augmented Generation (RAG): instead of AI answering from general knowledge alone, it uses your stored context as source material to give more accurate, personalized answers.

Make sure your Session 5 Mock Answer Evaluator is working before Session 6. Session 6 builds on the same running app.
