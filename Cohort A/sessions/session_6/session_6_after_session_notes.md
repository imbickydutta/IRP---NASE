# Session 6 After-Session Notes: Add RAG-Lite Doubt Solver

## What We Built Today

Today we added the RAG-Lite Doubt Solver to the AI Interview Prep Copilot.

The feature includes:

- A predefined knowledge base: a JavaScript array of 12–15 note objects, each with a title and content field
- A keyword search function that scores every note in the knowledge base against the user's question and returns the most relevant note
- An AI call that receives the retrieved note's content as context inside the prompt, with explicit instructions to answer only from that source
- A results display that shows the generated answer, the source note title used, and a fallback message when no note matches

The Doubt Solver is now the sixth active feature in the app. Students can type any doubt or question related to AI, interviews, or technical topics and receive a grounded, source-attributed answer.

This session builds directly on Session 5 — Add Mock Answer Evaluator (complete evaluation flow built), which introduced structured AI evaluation. In Session 7 — Add AI Prep Plan Agent, we will combine all six features into a personalized prep plan.

---

# Why This Feature Matters

This feature is not just a Q&A widget. It demonstrates a critical AI engineering pattern.

When AI is asked a question without any context, it answers from its general training knowledge. This leads to hallucination — AI confidently generating incorrect, outdated, or fabricated information. In a professional product, this is unacceptable.

RAG (Retrieval Augmented Generation) is the pattern that solves this. By retrieving a relevant source first and grounding the AI's response in that source, the app produces answers that are:

- more accurate and verifiable
- traceable to a specific source
- constrained to known, curated information

Source attribution — showing the user exactly which note was used — is also a core feature of trustworthy AI products. In enterprise tools like document Q&A systems, customer support bots, and internal knowledge assistants, source attribution is a standard requirement.

Building this feature demonstrates that the student understands not just how to use AI, but how to build AI-powered products responsibly.

---

# App Flow

The complete flow from Session 1 through Session 6:

User enters and saves interview profile (name, target role, skills, project details, weak areas, JD)  
↓  
App stores profile in localStorage  
↓  
JD Analyzer takes the saved job description and extracts required skills, responsibilities, role type, and interview topics  
↓  
Profile vs JD Match compares saved profile with the JD analysis and produces match percentage, strengths, gaps, and recommendations  
↓  
Interview Question Generator uses the profile and JD analysis to generate targeted questions by category  
↓  
Mock Answer Evaluator accepts a question and a student's typed answer, evaluates it with a score, specific feedback, and suggestions  
↓  
Doubt Solver accepts a student's typed doubt or question  
↓  
App keyword-searches the predefined knowledge base and retrieves the most relevant note  
↓  
App builds an AI prompt with the retrieved note as context  
↓  
AI generates an answer grounded only in the retrieved note  
↓  
App displays answer + source note title  
↓  
If no note matches: App displays fallback message (no AI call made)  
↓  
Session 7 — Add AI Prep Plan Agent

---

# What is RAG (Retrieval Augmented Generation)?

RAG is a pattern used in AI systems where, instead of asking AI to answer from its general training knowledge, you first retrieve a relevant piece of information from a specific knowledge source and then provide that information to the AI as context in the prompt.

The name describes the three steps precisely. Retrieval means finding the most relevant source material from a knowledge base. Augmented means adding that retrieved material to the AI prompt so the AI has something specific to reference. Generation means the AI produces its answer based on that provided context rather than from general knowledge.

The key benefit is grounding. A grounded answer is one that is derived from a known, verifiable source. When you also display which source was used — this is source attribution — the user can verify the answer, build trust in the system, and understand where the information came from. Hallucination is reduced because the AI is explicitly instructed to answer only from the provided note, not from its general knowledge.

In our app, the knowledge base is a JavaScript array of note objects with a title and content field. The retrieval step is a keyword matching function that loops through all notes and scores them by how many words from the user's question appear in each note. The augmentation step is inserting the retrieved note's content into the AI prompt. The generation step is the AI call that produces the answer. The source attribution is displaying the source note's title alongside the answer.

This is the same fundamental concept used in production RAG systems. The difference is scale and retrieval quality. Production systems use vector databases and embeddings to enable semantic search across thousands of documents. Our app demonstrates the concept clearly without that complexity.

---

# What Students Should Understand

Students should understand:

1. What RAG stands for and what each word in the name means
2. Why grounded AI answers are more reliable than ungrounded answers
3. The structure of the knowledge base: a JavaScript array of objects with title and content fields
4. How the keyword search function works: it loops through notes, counts matching words, returns the highest-scoring note
5. How the retrieved note is inserted into the AI prompt as context
6. Why the AI prompt explicitly says "answer only from the provided note" — this is the grounding instruction
7. What source attribution means and why it is important in AI products
8. What happens when no note matches: the fallback message appears and no AI call is made
9. The difference between our keyword matching approach and production semantic search using embeddings
10. How to explain this entire feature in 3–4 sentences without jargon

---

# Interview-Ready Explanation

Use this explanation:

```text
In Session 6, I added a RAG-Lite Doubt Solver to my AI Interview Prep Copilot. The app has a predefined knowledge base — a JavaScript array of 12 to 15 note objects, each with a title and content field covering AI, interview, and technical topics. When a student types a doubt, the app runs a keyword search to find the most relevant note, passes that note's content into the AI prompt as context, and asks the AI to answer only from that source. The response displays the answer and the source note title used, with a fallback message if no matching note is found. This feature demonstrates the core RAG pattern: retrieve relevant context, augment the prompt with it, and generate a grounded, verifiable answer.
```

---

# What Happens When a Student Types a Question and Clicks Find Answer?

Expected answer:

```text
When the student types a question and clicks Find Answer, the app first validates that the question is not empty. It then passes the question to the keyword search function, which splits the question into individual words, loops through every note in the knowledge base, and counts how many question words appear in each note's title and content. The note with the highest keyword match count is selected as the most relevant note. If no note scores above zero, the app skips the AI call and displays a fallback message. If a note is found, the app constructs an AI prompt that includes the retrieved note's content and the student's question, and instructs the AI to answer only from the provided note. The AI response is then displayed as the answer, along with the title of the source note that was used.
```

---

# What AI Was Used For

AI was used to help generate:

- the knowledge base content (12–15 well-written notes on relevant topics)
- the keyword search function structure
- the AI prompt construction that grounds the response in the retrieved note
- the display logic for answer, source note title, and fallback message
- the error and empty state handling

But students still need to:

- test whether the keyword search returns the correct note for different types of questions
- verify that the source note title appears correctly in the results
- confirm the fallback message appears when a question has no matching note
- understand the data flow from question input to AI response to displayed output
- be able to explain what RAG is, why it matters, and how their app demonstrates it
- explain the difference between keyword matching and semantic search
- be able to explain what would change in a production implementation

---

# Common Issues and Fixes

## Issue 1: Keyword search always returns the same note or an incorrect note

Possible reasons:

- Common short words like "is", "a", "the", "what", "how" are being matched and causing false scores
- The search function is only checking the note title, not the content
- The comparison is case-sensitive and not finding matches

What to ask AI:

```text
The keyword search in my RAG-Lite Doubt Solver is returning incorrect or irrelevant notes. Please fix the findRelevantNote function so that:
1. It filters out common stop words like "is", "a", "the", "what", "how", "me", "tell", "explain" before scoring.
2. It searches both the note title and the note content, not just the title.
3. The comparison is case-insensitive.
4. It returns null if no note scores above zero meaningful matches.
Explain what was wrong and what you changed.
```

## Issue 2: Source note title is not displayed with the answer

Possible reasons:

- The retrieved note object is being passed to the AI call but not stored in state for display
- The UI is only rendering the AI response text and not the source title field
- The source title display is conditional and the condition is not being met

What to ask AI:

```text
In my RAG-Lite Doubt Solver, the AI answer is showing correctly but the source note title is not appearing. Please fix the display logic so that the title of the retrieved note is shown below or above the answer in a clearly labeled section, for example: "Source: What is RAG?". The source title should appear every time a valid note is retrieved and an answer is generated.
```

## Issue 3: App crashes or shows a blank screen when no note is found

Possible reasons:

- The AI call is being made even when the search function returns null
- The UI is trying to render properties of the note object when the note is null
- There is no conditional check before the AI call

What to ask AI:

```text
My RAG-Lite Doubt Solver crashes or shows a blank screen when the keyword search returns no matching note. Please add a proper null check after the findRelevantNote call. If the result is null, the app should skip the AI call entirely and instead display the fallback message: "No relevant note found in the knowledge base. Please try rephrasing your question." Make sure the app does not crash when note is null and explain the changes you made.
```

---

# Key Takeaways

1. RAG is a pattern, not a technology. The core idea is always the same: retrieve a relevant source, augment the prompt with it, and generate a grounded answer. Whether you use a JavaScript array and keyword matching or a vector database and embeddings, the principle is identical.

2. Source attribution is not optional. Showing the user which source was used is a design requirement for trustworthy AI products. It allows verification, builds trust, and distinguishes grounded answers from hallucinated ones.

3. The fallback state is as important as the success state. A well-designed AI feature handles the case where the knowledge base does not have a relevant answer. Calling the AI with no context and hoping for the best is not acceptable in a production product.

4. Students who can explain RAG in plain language stand out. Most people who use AI tools cannot explain why grounded answers matter or what retrieval means in an engineering context. Being able to explain this clearly — using your own app as an example — is a significant interview differentiator.

---

# Session 7 Preview

In Session 7, we will add the final AI feature:

# AI Prep Plan Agent

The app will analyze the student's full profile, including their target role, weak areas, job description match score, and identified skill gaps, and generate a personalized 7-day interview preparation plan.

This is the most complex feature of the series. The AI will act as an agent that reasons across multiple inputs — everything collected and analyzed across the previous six sessions — and produces a structured, day-by-day action plan with specific tasks, focus areas, and resources for each day.

Main AI concept:

Agent-style prompting, multi-input reasoning, and structured plan generation.

Session 7 will bring together all the context we have built and demonstrate how a well-designed AI agent prompt can produce a complete, actionable output from a rich user context.
