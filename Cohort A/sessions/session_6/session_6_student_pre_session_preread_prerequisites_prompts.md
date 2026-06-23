# Session 6 Student Pre-Session File: Add RAG-Lite Doubt Solver

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
- answer doubts using a RAG-Lite knowledge base
- create a 7-day personalized interview prep plan

## What Has Been Built So Far

By Session 5, the app already has:

- Session 1: Base Profile Dashboard — profile form, target role, skills, weak areas, job description, localStorage persistence
- Session 2: JD Analyzer — takes raw job description, extracts required skills, responsibilities, role type, and interview topics
- Session 3: Profile vs JD Match — compares your profile with the analyzed JD, produces a structured match report with gap analysis
- Session 4: Interview Question Generator — generates targeted interview questions based on your profile and the JD
- Session 5 — Add Mock Answer Evaluator (complete evaluation flow built): accepts an interview question and your answer, evaluates it with score, specific feedback, and suggestions

## Session 6 Goal

In Session 6, we will add the RAG-Lite Doubt Solver.

This feature allows you to type any doubt or question. The app searches a predefined knowledge base — a JavaScript array of 10–15 notes on AI, interview, and technical topics — using keyword matching, finds the most relevant note, and asks the AI to answer using only that note.

The feature introduces one of the most important concepts in modern AI engineering: Retrieval Augmented Generation (RAG).

## Session 6 Output

By the end of Session 6, you should have a working Doubt Solver where you can:

- type a doubt or question
- get an AI-generated answer grounded in a specific knowledge base note
- see the source note title that was used to produce the answer
- receive a clear fallback message if no relevant note is found

---

# Pre-Read

## Why Are We Building This Feature?

In interviews, you will be asked about how your app handles knowledge and information. If your AI just answers from general knowledge, it can hallucinate — generate confident but incorrect answers. The Doubt Solver demonstrates that you know how to prevent this by using a better pattern: retrieve a verified source first, then generate an answer grounded in that source.

Being able to explain RAG clearly — without mentioning a single vector database — is a skill that separates a basic AI app builder from someone who understands AI engineering concepts.

This feature also teaches you:

- what a knowledge base is and how to structure one
- how to search a knowledge base using simple code
- how to pass retrieved information into an AI prompt
- why source attribution matters in AI products
- how to handle the case when no relevant information is found

## Simple App Flow

User enters profile details  
↓  
App saves the profile  
↓  
JD Analyzer extracts key information from the job description  
↓  
Profile vs JD Match compares your profile with the JD  
↓  
Question Generator creates targeted interview questions  
↓  
Mock Evaluator assesses your practice answers  
↓  
Doubt Solver searches the knowledge base for the relevant note  
↓  
App passes the retrieved note to the AI as context  
↓  
AI generates an answer grounded only in that note  
↓  
App displays answer + source note title (or fallback message)  
↓  
Session 7 — Add AI Prep Plan Agent

## Key Concepts to Revise

Before the session, revise or read about these ideas:

- What is a knowledge base? (A curated collection of information a system can search and reference)
- What is retrieval? (Finding the most relevant piece of information from a collection based on a query)
- What is context in an AI prompt? (Additional information passed into the prompt so the AI can use it to answer)
- What is hallucination in AI? (When AI generates confident but incorrect or fabricated information)
- What is keyword matching? (Finding matches by checking whether specific words from a query appear in a document)
- What is source attribution? (Telling the user which specific source an answer was derived from)
- What is a JavaScript array of objects? (A list where each item is an object with properties, e.g., title and content)
- What is RAG? (Retrieval Augmented Generation — retrieve context first, augment the prompt with it, then generate a grounded answer)

## Simple Explanation

Imagine you have a folder with 15 printed notes on topics like "What is RAG?", "What is prompt engineering?", "How do LLMs work?", and "What is the difference between fine-tuning and RAG?".

A student asks: "What is prompt engineering?"

Instead of making up an answer, you:

1. Look through the folder for the note most relevant to the question
2. Find the note titled "What is prompt engineering?"
3. Read that note to the student as the basis for your answer

That is RAG. You retrieved the relevant note. You augmented your response with its content. You generated a grounded answer based on it.

In our app:

- the folder is the JavaScript array of note objects
- looking through the folder is the keyword search function
- reading the note to form an answer is the AI call with the note passed as context
- the source attribution is telling the student: "this answer came from the note titled X"

---

# Prerequisites Before Session

## Mandatory Setup

Complete this before the live session:

1. Have the AI Interview Prep Copilot app from Session 5 open and working
2. Verify that the app loads correctly in the browser
3. Verify that at least the Profile Dashboard and Mock Evaluator from Session 5 are functional
4. Have Google Antigravity or your AI coding tool open and ready
5. Keep this file open during the session
6. Have a stable internet connection
7. Have at least 3 test questions ready to type into the Doubt Solver during the session

## Optional Setup

Useful but not mandatory:

- A text file with 5–6 sample doubts you want to test (e.g., "What is RAG?", "How does keyword matching work?", "What is the difference between fine-tuning and RAG?")
- Notes from Session 5 if you need to remind yourself of the existing app structure
- A list of 2–3 topics you think should be in the knowledge base

## Important Rule

Do not spend the live session on setup or fixing the previous session's app.

If Session 5's app has issues, use a fresh project and paste the full main build prompt. The prompt includes the full context of all previous features.

---

# Content to Prepare Before Class

Prepare this in a text file before class. You will use it during the session to test the Doubt Solver.

```text
Sample Doubts to Test:

1. What is RAG?
2. What is prompt engineering?
3. How do large language models work?
4. What is the difference between fine-tuning and RAG?
5. What is hallucination in AI?
6. What is a vector database?
7. How should I prepare for a technical interview?
8. What is a knowledge base?
9. What is source attribution?
10. What is context in an AI prompt?

Topics to include in the knowledge base:
- RAG (Retrieval Augmented Generation)
- Prompt engineering
- How LLMs work
- Fine-tuning vs RAG
- Hallucination in AI
- Vector databases (basic concept)
- Technical interview preparation
- Interview communication tips
- What is an API?
- What is a REST API?
- What is localStorage?
- What is frontend development?
- What is a JavaScript array?
- What is source attribution?
- What is context in AI prompting?
```

---

# Prompts for Session 6

Use these prompts during the session when instructed.

---

## Prompt 1: Main Build Prompt

```text
I am building an AI Interview Prep Copilot web app.

The app already has these features built and working:
1. Session 1 — Base Profile Dashboard: profile form with full name, target role, current skills, project details, weak areas, and job description. Data is saved in localStorage.
2. Session 2 — JD Analyzer: takes the saved job description and extracts required skills, responsibilities, role type, and interview topics using a structured AI prompt.
3. Session 3 — Profile vs JD Match: compares the saved student profile with the analyzed JD and generates a structured match report with a match percentage, strengths, gaps, and recommendations.
4. Session 4 — Interview Question Generator: uses the student profile and the JD analysis to generate a list of targeted interview questions organized by category.
5. Session 5 — Mock Answer Evaluator: accepts an interview question and the student's typed answer, sends both to the AI with a structured evaluation prompt, and returns a score out of 10, specific feedback, and suggested improvements.

Now add Session 6 — RAG-Lite Doubt Solver.

This feature should work as follows:

Step 1 — Knowledge Base:
Create a JavaScript array called knowledgeBase containing 12–15 note objects.
Each note object must have exactly two fields:
- title: a short descriptive label for the topic (e.g., "What is RAG?")
- content: a paragraph or two of information on that topic

Include notes on these topics at minimum:
- What is RAG (Retrieval Augmented Generation)?
- What is prompt engineering?
- How do large language models work?
- What is the difference between fine-tuning and RAG?
- What is hallucination in AI?
- What is a vector database (basic concept only)?
- How to prepare for a technical interview?
- What is source attribution in AI?
- What is context in an AI prompt?
- What is an API?
- What is a REST API?
- What is localStorage?
- What is frontend development?

Step 2 — Keyword Search Function:
Create a function called findRelevantNote(question, knowledgeBase) that:
- takes the user's question as a string
- converts it to lowercase and splits it into individual words
- loops through every note in the knowledgeBase array
- for each note, counts how many of the question's words appear in the note's title or content (case-insensitive)
- returns the note with the highest keyword match count
- returns null if no note scores above zero

Step 3 — Doubt Solver UI:
Add a new section or tab called "Doubt Solver" to the app navigation.
In this section, include:
- A text input field labeled "Type your doubt or question"
- A button labeled "Find Answer"
- A results area that shows:
  a. The AI-generated answer
  b. A label showing the source note title used (e.g., "Source: What is RAG?")
  c. A fallback message if no relevant note was found (e.g., "No relevant note found in the knowledge base. Please try rephrasing your question.")

Step 4 — AI Call:
When a relevant note is found:
- Build a prompt in this format:
  "You are a helpful assistant. Use only the information provided below to answer the student's question. Do not use any outside knowledge or add information that is not in the provided note. Note Title: [note title]. Note Content: [note content]. Student Question: [user's question]. Answer:"
- Send this prompt to the AI API
- Display the response as the answer

When no relevant note is found:
- Do not call the AI
- Display the fallback message

Do not add:
- PDF upload
- Vector database or embeddings API
- Semantic search or cosine similarity
- Dynamic note creation or editing by users
- Pinecone, Weaviate, Chroma, or any external vector store
- Cloud storage or file system access

Add clear comments in the code explaining:
- where the knowledge base array is defined
- how the keyword search function works
- where the retrieved note is inserted into the AI prompt
- where the source note title is displayed
- where the fallback message is triggered
```

---

## Prompt 2: UI Improvement Prompt

```text
Improve the UI of the RAG-Lite Doubt Solver section in the AI Interview Prep Copilot.

Keep the same functionality — do not change the knowledge base, search function, or AI call logic.

Make these UI improvements:
1. Add a character counter below the question input field.
2. Display the source note title in a styled card or callout box, not just as plain text.
3. Add a label above the answer section that says "Answer grounded in knowledge base:".
4. Style the fallback message with a different background color (light yellow or light red) to make it visually distinct.
5. Add a "Clear" button that resets the input and results area.
6. Show a loading indicator while the AI is generating the answer.
7. Keep the design consistent with the rest of the app's existing UI style.

Do not change the knowledge base content, the search function logic, or the AI prompt structure.
```

---

## Prompt 3: Debugging Prompt — Keyword Search Returns Wrong Note or No Note

```text
The RAG-Lite Doubt Solver in my AI Interview Prep Copilot is not working correctly.

Issue: The keyword search is returning the wrong note or returning null even when I type a clearly relevant question.

Please debug and fix the findRelevantNote function.

Expected behavior:
1. When I type "What is RAG?", the note titled "What is RAG?" or the most relevant RAG note should be returned.
2. When I type "tell me about prompt engineering", the note on prompt engineering should be returned.
3. When I type something completely unrelated to all notes (like "pizza recipe"), null should be returned and the fallback message should appear.
4. The search should be case-insensitive.
5. Common short words (like "is", "a", "the", "what", "how", "me", "tell") should be filtered out or ignored to avoid false matches.

Please also check:
- whether the knowledgeBase array is properly defined and accessible to the function
- whether the function handles null or empty questions gracefully
- whether the function correctly compares the question words against both the note title and content

Explain what was wrong and what you changed.
```

---

## Prompt 4: Code Explanation Prompt

```text
Explain the current code of the RAG-Lite Doubt Solver feature in plain language.

Focus on:
1. What does the knowledgeBase array look like? What is the structure of each note object?
2. How does the findRelevantNote function work step by step?
3. Where is the retrieved note inserted into the AI prompt?
4. What does the AI prompt say and why is it written that way?
5. Where is the source note title displayed?
6. Where is the fallback message triggered and displayed?
7. What is the data flow from when the student types a question to when the answer appears on screen?
8. Which part of this code should I explain in an interview about RAG?

Do not rewrite the code. Only explain it clearly in beginner-friendly language.
```

---

## Prompt 5: Interview Explanation Prompt

```text
Help me explain the RAG-Lite Doubt Solver feature as if I am in an interview.

Use this structure:
1. What is the feature and what problem does it solve?
2. What is RAG and how did I use it in this feature?
3. What is the knowledge base in my app?
4. How does the app find the relevant note?
5. How does the retrieved note get passed to the AI?
6. What is source attribution and where does it appear in my app?
7. What happens when no relevant note is found?
8. What are the limitations of my current approach?
9. How would I improve this in a production system?
10. What AI concept did I demonstrate with this feature?

Keep the explanation simple, clear, and interview-ready. Use plain language. Avoid jargon.
```

---

## Prompt 6: Structured JSON Output Prompt

```text
Modify the RAG-Lite Doubt Solver so that the AI returns its response as structured JSON instead of plain text.

The AI response should follow this exact JSON schema:

{
  "answer": "the generated answer text",
  "confidence": "high | medium | low",
  "source_note_title": "title of the note that was used",
  "answer_grounded": true,
  "suggestion": "optional string: one suggestion for the user to explore further, or null if none"
}

Instructions:
1. Update the AI prompt to instruct the AI to respond only in valid JSON matching the above schema.
2. Parse the JSON response in the app code.
3. Display each field separately:
   - Show "answer" as the main answer text
   - Show "source_note_title" as the source label
   - Show "confidence" as a badge (e.g., "Confidence: High")
   - Show "suggestion" if it is not null
4. If the JSON parsing fails, fall back to displaying the raw response as plain text.
5. Keep all existing fallback behavior for when no note is found.

Explain the changes you made in comments.
```

---

## Prompt 7: Error and Empty State Prompt

```text
Add proper error handling and empty states to the RAG-Lite Doubt Solver feature.

Handle these cases:

1. Empty question submitted:
   - If the student clicks "Find Answer" without typing a question, show a validation message: "Please type a question before searching."
   - Do not call the search function or the AI.

2. Question too short (less than 3 characters):
   - Show a message: "Your question is too short. Please type a more complete question."

3. No note found in the knowledge base:
   - Show the fallback message: "No relevant note found for your question. Try rephrasing or using different keywords."
   - Do not call the AI.

4. AI call fails (network error or API error):
   - Show an error message: "Could not get an answer right now. Please check your internet connection and try again."
   - Do not show a blank screen.

5. Knowledge base is empty or undefined:
   - Show an error message: "The knowledge base is not available. Please contact support."
   - Do not crash the app.

6. Response is loading:
   - Show a loading indicator while waiting for the AI response.
   - Disable the "Find Answer" button while loading to prevent duplicate requests.

Add these error and empty states without changing the core search function or AI prompt logic.
```

---

# What You Should Be Able to Explain After Session 6

By the end of the session, you should be able to answer these questions independently. Practice these before your interview.

1. What is RAG and what do the three letters stand for?
2. How does your Doubt Solver use RAG?
3. What is the knowledge base in your app and how is it structured?
4. How does the keyword search function work?
5. How is the retrieved note passed to the AI?
6. What does source attribution mean and where does it appear in your app?
7. What happens when no note matches the user's question?
8. Why is it better to ground AI answers in a specific source rather than letting AI answer from general knowledge?
9. What are the limitations of keyword matching compared to semantic search?
10. How would you build this feature in a production system?

## Final Session 6 Explanation

```text
In Session 6, I added a RAG-Lite Doubt Solver to my AI Interview Prep Copilot. The app has a predefined knowledge base — a JavaScript array of 12–15 note objects, each with a title and content. When a student types a doubt, the app searches the knowledge base using keyword matching to find the most relevant note, then passes that note as context in the AI prompt, asking the AI to answer only from that source. The response shows the generated answer, the source note title that was used, and a fallback message if no relevant note is found. This demonstrates the core RAG concept: retrieve relevant context first, augment the prompt with it, and generate a grounded, verifiable answer.
```
