# Session 3 After-Session Notes: Add Profile vs JD Match

## What We Built Today

Today we added the Profile vs JD Match feature to the AI Interview Prep Copilot.

This session built on the outputs of Session 2 — JD Analyzer (JD analysis output with required skills, responsibilities, role type, interview topics available in app state).

The app can now:

- read the student profile saved in Session 1 from localStorage
- read the JD analysis produced in Session 2 — JD Analyzer from app state
- compose a labeled comparison prompt with both contexts
- send that prompt to AI and receive a structured match result
- display a match report card showing:
  - overall match band (Strong / Moderate / Weak)
  - matched skills list
  - missing skills list
  - improvement suggestions (3–5 actionable items)
  - interview risk areas

---

# Why This Feature Matters

A job description and a student profile are two separate pieces of information. Neither one alone tells you whether the student is ready for the role.

The match feature connects them.

It takes what the student has and what the role needs, sends both to AI as labeled context, and produces an output that explains the gap clearly — not as a black-box number, but as a structured, reasoned comparison.

This is the first feature in the app where AI is comparing two contexts rather than analyzing one. That shift is significant. It teaches:

- how to design prompts that handle multiple inputs
- why labeling context is not optional — it changes the quality of AI output
- why AI results need reasons attached, not just labels
- how to present AI output honestly using bands instead of misleading percentages

---

# App Flow

The complete flow from Session 1 through Session 3:

User opens app  
↓  
User fills profile form (Session 1)  
↓  
App validates required fields  
↓  
User clicks Save Profile  
↓  
App saves profile to localStorage as "studentProfile"  
↓  
App displays profile summary  
↓  
User pastes job description and clicks "Analyze JD" (Session 2)  
↓  
App sends raw JD text to AI  
↓  
AI extracts required skills, responsibilities, role type, interview topics, difficulty level  
↓  
JD analysis stored in app state as jdAnalysis  
↓  
App displays JD analysis panel  
↓  
User clicks "Check My Match" (Session 3)  
↓  
App reads studentProfile from localStorage  
↓  
App reads jdAnalysis from app state  
↓  
App checks: is profile available? Is JD analysis available?  
↓  
App composes labeled comparison prompt with both contexts  
↓  
App sends prompt to AI  
↓  
Loading state shown  
↓  
AI returns: match band, matched skills, missing skills, suggestions, risk areas  
↓  
App parses structured response  
↓  
Match report card displayed  
↓  
Session 4: App uses match report and JD analysis to generate targeted interview questions

---

# What is Context Management and Explainable AI Output?

Context management is the practice of deciding what information to include in an AI prompt, how to structure it, and how to label it so that the AI model can reason about multiple pieces of information correctly.

In Session 3, the app manages two contexts at once. The first context is the student profile — what the student knows, has built, and finds difficult. The second context is the JD analysis — what the role requires in terms of skills, responsibilities, and interview preparation. These two pieces of information are labeled separately in the comparison prompt, using headings like "STUDENT PROFILE:" and "JD ANALYSIS:", so the AI knows precisely which information belongs to which side of the comparison. Without this labeling, AI may confuse the student's skills with the job's requirements or produce vague output that is not actionable.

Explainable AI output means that every result from the AI must come with a reason, not just a verdict. A match band of "Moderate" on its own tells the student very little. A match band of "Moderate — you have strong prompting and UI skills but are missing REST API integration and debugging depth" tells the student exactly where to focus. In Session 3, the report card is designed to enforce this principle: every section has both a result and an explanation. The match band comes with a reason. The missing skills come with context about why they matter for the role. The improvement suggestions are specific and actionable. The risk areas explain where gaps create the most interview difficulty. This is how responsible AI features are built — not just displaying AI output, but designing it to be useful.

---

# What Students Should Understand

Students should understand:

1. Why two input contexts need to be labeled separately in the prompt
2. What a match band is and why it is preferred over a percentage score
3. What context management means in the design of AI prompts
4. What explainable AI output means — every result must have a reason attached
5. How the match feature reads from two sources: localStorage and app state
6. Why the disclaimer "AI-generated — use as a guide, not a guarantee" is necessary and not optional
7. How loading states, empty states, and error states protect the user experience
8. Why the JD analysis from Session 2 is used rather than the raw job description text
9. How AI output structure is designed in the prompt before the AI call is made
10. Why this feature cannot be called an ATS score or a hiring prediction

---

# Interview-Ready Explanation

Use this explanation:

```text
In Session 3, I added a Profile vs JD Match feature to the AI Interview Prep Copilot. The feature reads two inputs: the student profile from localStorage and the JD analysis from the previous session's app state. It combines both as labeled context in a single AI comparison prompt. The AI returns a structured match result with an overall match band — Strong, Moderate, or Weak — along with matched skills, missing skills, improvement suggestions, and interview risk areas. The report card is designed following explainable AI principles: every result comes with a reason, not just a label. I also included a disclaimer because AI comparisons are guides based on text analysis, not verified hiring metrics.
```

---

# What Happens When the User Clicks "Check My Match"?

Expected answer:

```text
When the user clicks "Check My Match", the app first checks whether a saved student profile exists in localStorage and whether a JD analysis is available in app state. If the profile is missing, the app shows: "Please complete your profile first before checking your match." If the JD analysis is missing, the app shows: "Please run the JD Analyzer first before checking your match." If both are available, the app composes a labeled comparison prompt — with the student profile under the heading "STUDENT PROFILE:" and the JD analysis under the heading "JD ANALYSIS:" — and sends it to the AI. A loading state is shown while the AI processes the request. When the AI responds, the app parses the structured output and renders the match report card with the match band (colored badge), matched skills, missing skills, improvement suggestions, and interview risk areas. A disclaimer is shown at the bottom of the card.
```

---

# What AI Was Used For

AI was used to:

- compare the student profile text with the JD analysis text
- identify overlapping skills between what the student has and what the role requires
- identify skill gaps
- generate 3–5 specific improvement suggestions based on those gaps
- identify interview risk areas given the student's weak areas and the role's requirements
- assign a qualitative match band (Strong / Moderate / Weak) with a justification

But students still need to:

- design the labeled comparison prompt structure
- decide what goes into the "STUDENT PROFILE:" and "JD ANALYSIS:" sections
- choose to use a match band instead of a misleading percentage score
- parse and map the AI response to the correct report card sections
- implement loading, empty, and error states independently
- add the disclaimer and understand why it is necessary
- test the feature with their own real profile and JD data
- explain the context management and explainable output concepts in interview language

---

# Common Issues and Fixes

## Issue 1: Match report is blank or the AI call does not trigger

Possible reasons:

- the profile key "studentProfile" in localStorage does not match what the code is reading
- the jdAnalysis state variable is empty when the button is clicked
- the comparison prompt is not being composed before the AI call
- the AI call function is not connected to the button click handler

What to ask AI:

```text
The "Check My Match" button does not trigger the AI call or the match report is blank. Please check: (1) Is the profile being read from localStorage using the correct key "studentProfile"? (2) Is the jdAnalysis state variable available and non-empty when the button is clicked? (3) Is the comparison prompt being composed correctly before the AI call? (4) Is the AI call function connected to the button click event? Fix the issue and explain what was wrong.
```

## Issue 2: Match band displays but matched/missing skills are empty

Possible reasons:

- the AI response was parsed only for the match band and the parsing logic for other sections was not completed
- the AI returned a different section format than expected and the parser failed
- the response was truncated and skills sections were cut off

What to ask AI:

```text
The match band is showing correctly but the matched skills, missing skills, improvement suggestions, and risk areas sections are empty. Please check the AI response parsing logic. The AI response should contain all five sections. Verify that the parser is reading all sections from the response and mapping them to the correct display variables. If the AI response format is inconsistent, update the prompt to enforce a clearer structure for each section.
```

## Issue 3: The app crashes when profile or JD analysis is missing

Possible reason:

- the code is trying to access properties of a null or undefined object when localStorage returns null or jdAnalysis is not yet set

What to ask AI:

```text
The app crashes when either the student profile or the JD analysis is missing. Please add null checks before reading from localStorage and before accessing the jdAnalysis state variable. If either is missing, display the appropriate message: "Please complete your profile first" or "Please run the JD Analyzer first". Do not attempt the AI call if either input is missing. Explain where you added the null checks and why.
```

---

# Key Takeaways

## 1. Labeling contexts changes the quality of AI output

When we send two pieces of information to AI without labels, the AI cannot distinguish between them and may produce confused or blended output.

By labeling "STUDENT PROFILE:" and "JD ANALYSIS:" separately, we give AI a clear structure to follow.

## 2. Match bands are more honest than percentages

An AI-generated percentage like "72% match" is not based on a verified formula. It is a numerical label that sounds precise but is not.

A match band like "Moderate — strong prompting skills but missing API integration" is qualitative, explainable, and actionable.

Choosing a match band is a deliberate design decision that makes the app more responsible.

## 3. Explainable AI output requires designing the output structure before the call

Explainable output does not happen automatically. It must be asked for in the prompt.

By instructing AI to return a reason alongside every result — a reason for the match band, context for missing skills, specific improvement steps, and risk justifications — we design the output to be useful rather than just decorative.

## 4. Every AI feature needs edge case handling

The happy path (profile exists, JD analysis exists, AI responds correctly) is only one scenario.

Building for empty state, missing inputs, and AI failure is what separates a working demo from a production-quality feature.

---

# Session 4 Preview — Add Interview Question Generator

In Session 4, we will add the Interview Question Generator.

## Interview Question Generator

The app will use the JD analysis from Session 2 and the match report from Session 3 — specifically the missing skills and interview risk areas — to generate a targeted set of interview questions.

Because the questions are generated using the student's specific gap areas, they will be more personalized than a generic question list.

Main AI concept:

Conditional prompt construction — using application state to decide what gets included in an AI prompt, so the output changes based on who the user is and what their gaps are.

Session 4 will use the JD analysis and match report already available in app state.
