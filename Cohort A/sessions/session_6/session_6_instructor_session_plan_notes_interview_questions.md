# Session 6 Instructor File: Add RAG-Lite Doubt Solver

## Session Title

Add RAG-Lite Doubt Solver

## Duration

2 hours

## Project

AI Interview Prep Copilot

## Session 6 Objective

By the end of Session 6, students should have a working RAG-Lite Doubt Solver feature added to their AI Interview Prep Copilot app.

The feature allows a student to type a doubt or question. The app searches a predefined knowledge base using keyword matching, finds the most relevant note, and generates an answer grounded only in that retrieved note. The response shows the answer, the source note title used, and a fallback message if no relevant note is found.

This feature introduces the core concept of Retrieval Augmented Generation in a way students can understand and explain without any production complexity.

## Session 6 Deliverable

Students will add a RAG-Lite Doubt Solver that:

1. Maintains a predefined knowledge base as a JavaScript array of 10–15 note objects with title and content fields
2. Accepts a student's typed doubt or question as input
3. Searches the knowledge base using keyword matching to find the most relevant note
4. Sends the retrieved note as context inside the AI prompt
5. Returns an answer grounded in that note
6. Displays the answer, the source note title used, and a fallback message when no relevant note is found

The app should allow the student to:

- type a doubt or question in a text input
- click a button to search and generate an answer
- see the answer grounded in a specific note
- see the source note title that was used
- receive a clear fallback message if no match is found

## Strict Scope Control

### Include

- Predefined knowledge base as a JavaScript array of note objects with title and content fields
- 10–15 notes covering AI, interview, and technical topics
- Keyword-based search to find the most relevant note
- AI call with the retrieved note passed as context in the prompt
- Display of answer, source note title, and fallback message when no match is found
- Integration with the existing app that already has profile dashboard, JD analyzer, profile vs JD match, interview question generator, and mock answer evaluator

### Do Not Include

- PDF upload or file import of any kind
- Vector database or embeddings API
- Semantic search or cosine similarity
- Dynamic knowledge base management or CRUD operations on notes
- Cloud storage, file system access, or server-side storage
- Pinecone, Weaviate, Chroma, or any external vector store
- Dynamic note creation by users
- Multiple retrieval results or ranked lists
- Fine-tuning or custom model usage

Session 6 is only about demonstrating the RAG concept with static data, keyword search, and source attribution.

---

# Instructor Framing

## Opening Message

We have now built five features in this app. The profile dashboard stores the student's context. The JD Analyzer extracts structured insight from a raw job description. The Match Report compares the student's profile with the JD. The Question Generator creates targeted interview questions. The Mock Evaluator assesses answers with structured feedback.

Today we add the Doubt Solver. But this is not just a simple Q&A feature. We are going to build it in a specific way that introduces one of the most important patterns in modern AI engineering: Retrieval Augmented Generation, which everyone in the field shortens to RAG.

The idea is simple. Instead of asking AI to answer from whatever it knows — which can lead to hallucinated or incorrect answers — we first search a knowledge base for a relevant note, and then ask AI to answer using only that note. The AI becomes grounded. The answer becomes verifiable. And we can tell the user exactly which source was used.

## Key Philosophy

Students are not expected to understand vector databases or embeddings today.

They are expected to:

- understand why grounded answers are better than hallucinated answers
- understand the three steps of RAG: retrieve, augment, generate
- know what a knowledge base looks like in simple code
- know how to pass retrieved context into an AI prompt
- understand why source attribution matters in AI products
- explain the RAG concept clearly in an interview

## Repeated Instructor Line

RAG is not a database technology. RAG is a pattern: find the right context first, then ask AI to answer using only that context.

---

# Session Flow

## 0–10 min: Opening and Recap of Session 5 — Add Mock Answer Evaluator (complete evaluation flow built)

### Instructor Goal

Ground students in what they have already built and create a clear connection between Session 5 and Session 6.

### Recap Questions to Ask

Ask the class:

- What did we build in Session 5?
- What does the Mock Evaluator take as input?
- What does it produce as output?
- Where does the evaluation prompt send the student's answer?
- Why did we use structured output in the evaluator?

### Expected Recap Answers

Session 5 added the Mock Answer Evaluator. The student enters an interview question and writes a mock answer. The app sends both to the AI with a structured evaluation prompt. The AI returns a score, specific feedback, and suggested improvements. The output is displayed clearly on screen.

### Bridge to Session 6

Now we have a student who can look at their profile, analyze a JD, see their match score, get interview questions, and evaluate their mock answers. But what if they have a conceptual doubt? What if they do not understand a term or concept mentioned in the questions? Today we build the Doubt Solver for exactly that situation. And we will build it the right way — using RAG.

### Set Expectations

Tell students: Today involves one new concept — RAG — and one new pattern — passing retrieved context into a prompt. The code itself is straightforward. The understanding is what we will focus on.

---

## 10–20 min: Product Breakdown Before Prompting

### Instructor Goal

Before generating any code, help students think through the feature requirements clearly.

### Ask Students

What does the Doubt Solver need to do?

Guide them toward:

- It needs a knowledge base to search
- It needs to accept a user's question as input
- It needs to find the most relevant note from the knowledge base
- It needs to pass that note to the AI as context
- It needs to show the answer plus which note was used
- It needs to handle cases where no relevant note is found

### Break Down the Feature into Parts

1. Knowledge base: a JavaScript array of objects with title and content
2. Keyword search function: loops through notes, matches keywords from the user's question
3. Retrieve best match: pick the note with the highest keyword overlap
4. AI call: pass the retrieved note's content as context in the prompt (Gemini 1.5 Flash via @google/generative-ai — free tier)
5. Display: answer, source note title, and fallback message

### Instructor Explanation

This is the product thinking step. Before asking AI to build, we need to understand what we want. A vague prompt like "add a doubt solver" will give us something generic. Our specific breakdown will give us a feature that demonstrates RAG clearly and correctly.

---

## 20–35 min: Generate Add RAG-Lite Doubt Solver Feature in AI Tool

### Instructor Goal

Use the main build prompt to generate the complete RAG-Lite Doubt Solver feature.

### Walk Students Through the Prompt Before Pasting

Point out the key sections in Prompt 1:

- The list of already-built features (so AI understands the existing app)
- The knowledge base specification (10–15 notes, JavaScript array, title and content)
- The keyword matching requirement (no embeddings, no cosine similarity)
- The prompt construction instruction (retrieved note content goes into the AI prompt)
- The display requirements (answer, source note title, fallback)
- The explicit exclusions (PDF, vector DB, embeddings, Pinecone)

### What to Watch For in the Generated Output

- Does the knowledge base contain 10–15 meaningful notes on AI, interview, and technical topics?
- Does the search function loop through notes and match keywords?
- Does the AI call (Gemini 1.5 Flash via @google/generative-ai — free tier) receive the retrieved note's content as part of the prompt?
- Does the prompt instruct the AI to answer only from the provided note?
- Is the source note title displayed alongside the answer?
- Is there a fallback message when no note matches?

### Instructor Control Rule

Do not let students start customizing the knowledge base or adding more notes during generation. First verify the core flow works end-to-end. Customization happens later.

---

## 35–50 min: Instructor Walkthrough of Generated Feature

### Instructor Goal

Help students understand what AI generated, function by function.

### Walkthrough Areas

1. The knowledge base array — show the structure of each note object (title, content)
2. The keyword search function — explain how it tokenizes the user's question and loops through notes
3. The scoring/ranking logic — how the note with the most keyword matches is selected
4. The AI prompt construction — show exactly where the retrieved note's content is inserted
5. The prompt instruction — point out the line that tells AI to answer only from the provided note
6. The response display — show where answer, source title, and fallback are rendered
7. The overall data flow — from user input to retrieved note to AI call to displayed answer

### Ask During Walkthrough

- Where does the knowledge base live in the code?
- What does one note object look like?
- What happens when the user types a question and clicks Submit?
- How does the app decide which note is most relevant?
- Where does the retrieved note go in the AI prompt?
- What does the AI prompt say about how to use the note?
- What happens if no note scores above zero?

### Simple Explanation

AI generated this code, but in interviews you will need to explain what it does. So we always read the generated output and understand the data flow before moving on.

---

## 50–65 min: Student Follow-Along Build

### Student Task

Students paste Prompt 1 and build their version of the RAG-Lite Doubt Solver in their own app.

### Instructor Support Areas

Help students with:

- prompt paste issues or formatting problems
- knowledge base not being recognized as a valid JavaScript array
- search function returning null or undefined instead of a note object
- AI call failing because the note content is not inserted correctly into the prompt
- fallback message not appearing when no note is found
- source title not displaying alongside the answer
- the feature not integrating cleanly with the existing app tabs or navigation

### If Student Build Fails

Do not block the class. The student should:

- follow the instructor screen
- note which step broke
- pair with another student for troubleshooting
- use the shared completed code after class and regenerate using the debug prompt

---

## 65–80 min: Improve and Refine

### Instructor Goal

Improve the knowledge base quality and the display of results so the feature feels polished.

### Expected Improvements

- Expand the knowledge base to 12–15 notes with meaningful, interview-relevant content
- Improve the source note display — show the note title in a styled callout or card
- Add a character count or hint near the input field
- Make the fallback message more helpful (e.g., suggest rewording the question)
- Improve keyword matching to handle plural forms or partial matches

### Instructor Explanation

The first version gave us working functionality. This round is about making the feature feel like a real product feature and reinforcing that the knowledge base quality directly affects the quality of the answers. This is a real insight: in production RAG systems, curating the knowledge base well is just as important as the retrieval mechanism.

---

## 80–95 min: Edge Cases and Error States

### Instructor Goal

Teach students to think about what can go wrong, which is essential for both robust apps and interview discussions.

### Edge Cases to Cover

1. User submits an empty question — app should show a validation message, not crash
2. User types a very short question (one word) — keyword matching may return a low-quality match; discuss threshold handling
3. User types a question using different terminology than the notes — no match found, fallback message displays
4. Knowledge base array is empty or undefined — app should not crash, should show appropriate error
5. AI call fails or times out — show an error message rather than a blank screen
6. Retrieved note content is very long — discuss how this affects the prompt and token usage

### Instructor Explanation

Every production AI system needs error handling. If the knowledge base is empty, the app should not crash. If the AI call fails, the user should see a clear message. Good AI products are not just about the happy path — they are about every path.

---

## 95–105 min: Concept Pause — RAG (Retrieval Augmented Generation)

### Instructor Goal

Convert what students just built into a clear, interview-ready conceptual understanding of RAG.

### Explain RAG in Plain Language

Ask the class: what is the problem with asking AI a question directly?

Expected answer: AI might hallucinate. It answers from its training data, which may be outdated, incorrect, or not specific to our context.

Now explain: RAG solves this by doing three things first — before generating the answer.

Step 1: Retrieve — Search a knowledge base and find the most relevant piece of information for the user's question.

Step 2: Augment — Add the retrieved information to the AI prompt as context. The prompt now contains both the question and the relevant source material.

Step 3: Generate — Ask the AI to answer using only the provided context. This grounds the answer in a real source and prevents hallucination.

### Draw the Three-Step Flow

User types a question  
↓  
App searches the knowledge base (keyword matching)  
↓  
App finds the most relevant note  
↓  
App builds a prompt: question + retrieved note content  
↓  
App sends the augmented prompt to the AI  
↓  
AI generates an answer grounded only in the retrieved note  
↓  
App displays the answer + source note title  
↓  
If no note found: App shows a fallback message

### Why Source Attribution Matters

Source attribution means telling the user: this answer came from this specific source. It builds trust. It allows the user to verify. It prevents the app from appearing to make things up.

In production RAG systems like document Q&A, customer support bots, and enterprise search tools, source attribution is a core requirement. Our simple implementation demonstrates this principle clearly.

### Student Writing Task

Ask every student to write a 2–3 line answer:

What is RAG, and how did we use it in the Doubt Solver?

Expected answer:

RAG stands for Retrieval Augmented Generation. In the Doubt Solver, we first search the knowledge base for a note relevant to the user's question, then pass that note as context in the AI prompt, and ask AI to answer only from that source. This prevents hallucination and allows us to show the user exactly which source was used.

---

## 105–115 min: Interview Discussion and Viva Practice

### Instructor Goal

Prepare students to speak about the RAG-Lite Doubt Solver clearly and confidently in an interview setting.

Use the interview questions section below.

Run 2–3 questions as a group discussion, then ask each student to answer one question individually.

---

## 115–120 min: Wrap-Up and Session 7 Preview

### Instructor Closing

Today we built the RAG-Lite Doubt Solver. The app now has a knowledge base, a retrieval mechanism, and an AI call that is grounded in retrieved context. You can explain RAG without mentioning a single vector database.

Next session — Session 7 — Add AI Prep Plan Agent. The app will analyze the student's profile, weak areas, target role, and JD match score, and generate a personalized 7-day interview preparation plan using an agent-style prompt.

This is the most complex feature of the series. It combines everything we have built so far and demonstrates the concept of an AI agent that reasons across multiple inputs and produces a structured, actionable plan.

---

# Instructor Notes

## What to Emphasize

Session 6 is primarily a concept session. The code itself is not complex — it is a JavaScript array, a loop, and an AI prompt. What matters is that students understand:

- why we retrieve before generating
- how retrieved context becomes part of the prompt
- why this is better than asking AI to answer from memory
- what source attribution means and why it matters
- how to explain RAG without jargon

## Common Student Mistakes

1. Asking AI to use embeddings or vector search even though the prompt explicitly excludes it — remind students to re-read the scope before generating
2. Not checking whether the keyword search actually returns the correct note for a test question — students should manually test 2–3 questions against the knowledge base
3. Not displaying the source note title alongside the answer — the source attribution is the key learning, do not let this be skipped
4. Having a knowledge base with only 3–4 vague notes — the notes should be specific and substantive enough for keyword matching to work
5. Forgetting the fallback message for when no note matches — every AI feature needs an empty or no-result state
6. Not reading the AI prompt that was generated — students must be able to explain how the prompt tells the AI to use only the retrieved note
7. Treating this as a search feature rather than a RAG feature — emphasize that the search is only Step 1 and the AI generation grounded in the note is the whole point
8. Adding a feature where users can create or edit notes — this is out of scope and creates complexity we do not need for this session
9. Not testing the fallback case — students should test with a question that has no matching keywords in the knowledge base
10. Confusing keyword matching with semantic search — explicitly clarify that keyword matching is simpler, sufficient for this demo, and avoids the need for embeddings

## How to Control the Session

Use this rule:

If a feature requires an external API, a cloud service, file uploads, or dynamic data management, it is out of scope for Session 6.

Session 6 only needs a static JavaScript array, a keyword search function, an AI call with retrieved context, and three display elements: answer, source title, fallback.

## Setup Rule

Do not spend more than 5 minutes of live class on setup or environment issues.

If the existing app from Session 5 is not loading, students should use a clean project with a fresh paste of the main build prompt.

---

# Questions to Discuss: Interview Perspective

## Basic Project Questions

### Q1. What did you build in Session 6?

Expected answer:

In Session 6, I added a RAG-Lite Doubt Solver to the AI Interview Prep Copilot. The feature allows a student to type any doubt or question. The app searches a predefined knowledge base of 10–15 notes using keyword matching, finds the most relevant note, and asks the AI to generate an answer grounded only in that note. The response displays the answer, the title of the source note that was used, and a fallback message if no relevant note is found in the knowledge base.

### Q2. What is the knowledge base in this feature?

Expected answer:

The knowledge base is a JavaScript array of note objects. Each note has two fields: a title and a content field. The title is a short label like "What is RAG?" or "What is prompt engineering?" The content is a paragraph or two of information on that topic. The app has 10–15 such notes covering AI concepts, interview preparation tips, and technical topics. This array is hardcoded in the app as a static data source.

### Q3. How does the app find the relevant note?

Expected answer:

The app uses keyword-based search. When the student submits a question, the app splits the question into individual words and checks each note in the knowledge base for how many of those words appear in the note's title or content. The note with the highest number of matching keywords is selected as the most relevant note. This is a simple but effective approach for a small, static knowledge base.

### Q4. What does the app display after a question is submitted?

Expected answer:

The app displays three things. First, it shows the generated answer from the AI, which is grounded only in the retrieved note. Second, it shows the title of the source note that was used to generate the answer, so the user knows which piece of the knowledge base was referenced. Third, if no note in the knowledge base matches the user's question at all, the app displays a fallback message telling the user that no relevant note was found and suggesting they try rephrasing the question.

### Q5. Why is this feature useful in an interview prep app?

Expected answer:

When preparing for interviews, students frequently encounter terms, concepts, or topics they do not understand. Rather than leaving the app and searching the web, the Doubt Solver provides quick answers grounded in a curated knowledge base specifically relevant to interview preparation. The source attribution tells the student exactly where the answer came from, which builds trust. The fallback message is also useful because it tells the student when the app does not have an answer rather than generating something incorrect.

---

## App Flow Questions

### Q6. Walk me through the complete data flow of the Doubt Solver from user input to displayed answer.

Expected answer:

The student types a question in the text input and clicks the Submit button. The app takes the question text and passes it to the keyword search function. The search function splits the question into words, loops through every note in the knowledge base array, and counts how many question words appear in each note's title and content. The note with the highest keyword match count is selected. If no note scores above zero, the app sets a fallback state and displays the no-match message. If a note is found, the app builds an AI prompt that includes the user's original question and the full content of the retrieved note. The prompt instructs the AI to answer only using the provided note. The app sends this prompt to the AI API, receives the generated answer, and displays the answer along with the source note's title.

### Q7. How is the retrieved note passed to the AI?

Expected answer:

The retrieved note's content is inserted directly into the AI prompt as a string. The prompt typically says something like: "Use only the following information to answer the question. Do not use any outside knowledge. Information: [note content here]. Question: [user's question]." This is how retrieval augments the generation step — the prompt now carries both the user's question and the relevant source material. The AI uses that source material to produce a grounded, verifiable answer.

### Q8. What is source attribution and where does it appear in the app?

Expected answer:

Source attribution means identifying which source was used to generate a given answer. In our app, after the AI response is displayed, we also show the title of the note that was retrieved and used in the prompt. For example, if the student asked about prompt engineering and the app retrieved a note titled "What is prompt engineering?", the display will show the answer followed by a line like "Source: What is prompt engineering?" This allows the user to know exactly which note in the knowledge base the answer was drawn from, which makes the answer trustworthy and verifiable.

### Q9. What happens when no note matches the user's question?

Expected answer:

When the keyword search scores all notes in the knowledge base and none of them have any matching keywords from the user's question, the app does not call the AI at all. Instead, it displays a fallback message. The fallback message tells the user that no relevant note was found in the knowledge base for their question and may suggest they try rephrasing or using different keywords. This is important because calling the AI without any retrieved context would defeat the entire purpose of RAG — the AI would answer from general knowledge and potentially hallucinate.

### Q10. How does this feature connect to the rest of the app?

Expected answer:

The Doubt Solver is the sixth tab or section in the app. It uses the same navigation structure as all previous features. The knowledge base is static and self-contained — it does not pull from the student profile or the JD. However, the notes in the knowledge base were curated to be relevant to the same topics the app already works with: AI concepts, interview preparation, prompt engineering, and technical interview topics. This makes the Doubt Solver a natural support tool for the student using the other features in the app.

---

## AI Topic Questions — RAG (Retrieval Augmented Generation)

### Q11. What is RAG? Explain it in plain language.

Expected answer:

RAG stands for Retrieval Augmented Generation. It is a pattern where, instead of asking AI to answer a question from its general training knowledge, you first retrieve a relevant piece of information from a specific knowledge base, and then provide that retrieved information to the AI as context in the prompt. The AI then generates an answer grounded in that specific context rather than using its general knowledge. The three steps are: retrieve the relevant source, augment the prompt with that source, and then generate the answer. RAG is used widely in production AI applications to reduce hallucination and make AI answers verifiable.

### Q12. Why is RAG better than asking AI directly without any context?

Expected answer:

When you ask AI a question without any context, it answers from its training data. This can lead to hallucination — the AI confidently generates incorrect or outdated information. With RAG, you first find a relevant, verified piece of source material and give it to the AI as context. The AI is then constrained to answer from that source. This produces more accurate, verifiable, and trustworthy answers. It also allows source attribution — you can tell the user exactly which document or note the answer came from. In enterprise and production AI products, this reliability is critical.

### Q13. What is the difference between RAG and fine-tuning?

Expected answer:

Fine-tuning means training an AI model on new data so that knowledge becomes part of the model's weights. This is expensive, time-consuming, and requires retraining whenever the knowledge changes. RAG, on the other hand, keeps the model unchanged and instead provides relevant knowledge dynamically at query time through the prompt. RAG is much faster to implement, cheaper, and easier to update — you just update the knowledge base rather than retraining the model. For most business applications, RAG is preferred because it is practical, updatable, and does not require deep ML engineering.

### Q14. What is a knowledge base in the context of RAG?

Expected answer:

A knowledge base is a collection of documents, notes, or records that the retrieval step searches through. In production systems, a knowledge base might be thousands of PDF documents, support tickets, internal wiki pages, or product manuals stored in a vector database. In our app, the knowledge base is a simple JavaScript array of note objects with a title and content field. The principle is the same regardless of scale: the knowledge base is the curated source of truth that the AI uses to answer questions, rather than generating answers from its general training knowledge.

### Q15. How would you implement RAG in a production system compared to what we built today?

Expected answer:

In our app, we used a small static JavaScript array and keyword-based search, which works well for demonstrating the concept. In a production RAG system, the knowledge base would typically be stored in a vector database like Pinecone, Weaviate, or Chroma. Each document in the knowledge base would be converted into a numerical vector using an embeddings model, which captures the semantic meaning of the text. When a user asks a question, that question is also converted into a vector, and the system finds the document vectors that are closest in meaning using cosine similarity. This semantic search is much more powerful than keyword matching and works even when the user uses different terminology than the documents. The rest of the flow — augmenting the prompt and generating a grounded answer — is the same. The core concept we learned today maps directly to how production RAG systems work.

---

# Session 6 Completion Checklist

Students should complete the following by the end of the session:

- [ ] Doubt Solver tab or section is visible in the app navigation
- [ ] Knowledge base array contains 10–15 note objects with title and content fields
- [ ] Notes cover AI, interview preparation, and technical topics
- [ ] Text input field is present for the student to type a question
- [ ] Submit or Ask button is present and functional
- [ ] Keyword search function loops through the knowledge base and scores each note
- [ ] Most relevant note is selected and passed into the AI prompt
- [ ] AI prompt instructs the AI to answer only from the retrieved note
- [ ] Generated answer is displayed clearly on screen
- [ ] Source note title is displayed alongside the answer
- [ ] Fallback message appears when no note matches the question
- [ ] Student can explain what RAG means in plain language and how the app uses it

---

# Instructor Backup Plan

If the AI tool fails to generate the feature correctly or student setup issues cause significant delays:

1. Instructor demonstrates the full working feature live on screen.
2. Students follow conceptually, noting the knowledge base structure, search function, and prompt construction.
3. Share the final Session 6 code after the session.
4. Students use Prompt 1 and Prompt 3 (debugging prompt) to regenerate or fix their own version after class.
5. Do not sacrifice the Concept Pause segment — the RAG explanation is the most important learning of this session.
6. If time runs short, skip the improvement round (65–80 min) and go directly to Concept Pause after the walkthrough.

## Gemini API Key Troubleshooting

If AI calls fail during the session:

- Check that the `.env` file exists in the project root (same folder as `package.json`) and contains the line: `VITE_GEMINI_API_KEY=your_key_here`
- Remind students to restart the Vite dev server after adding or editing the `.env` file — environment variables are not hot-reloaded
- Confirm the import in the component uses `import.meta.env.VITE_GEMINI_API_KEY` (not `process.env`)
- Free tier limit is 15 RPM (requests per minute) — if a student hits the rate limit, wait 1 minute and try again
- Keys are obtained free at aistudio.google.com with a standard Google account — no credit card required
