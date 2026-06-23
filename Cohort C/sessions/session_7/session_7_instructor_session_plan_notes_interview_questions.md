# Session 7 Instructor File: Vision/OCR Mini Module

## Session Title

Vision/OCR Mini Module — Gemini Multimodal Image Understanding

## Duration

2 hours

## Portfolio Module

vision-module

## Session 7 Objective

By the end of Session 7, students will have built a standalone vision-language module that uses Gemini 1.5 Flash to process an image (invoice, receipt, or ID card), extract structured data from it, and save the result as a JSON file. Students will understand how vision-language models differ from traditional OCR tools, how to design multimodal prompts, and why confidence notes and human verification are essential in production document AI.

## Deliverable

- `vision_ocr_module.py` — main Python script with `analyze_image(image_path)` function
- `sample_image.png` — a pre-built or ASCII-art-generated sample document image included in the repo
- `ocr_output.json` — structured JSON output saved after running the script

---

## Strict Scope Control

### Include

- `vision_ocr_module.py` with `analyze_image(image_path)` as the core function
- Gemini 1.5 Flash multimodal API call using `google-generativeai` library
- Image loading via `PIL.Image.open()` passed directly to Gemini
- One sample image file (invoice or receipt style) included in the repo
- Structured JSON output prompt requiring: `extracted_text`, `document_type`, `key_fields` dict, `confidence_notes`
- `ocr_output.json` result saved to disk
- `confidence_notes` field explicitly required in the Gemini prompt
- Basic error handling for missing file, API failure, and malformed JSON response
- Environment variable for `GEMINI_API_KEY` loaded via `python-dotenv` or `os.environ`
- Clear inline code comments explaining each function and design choice

### Do Not Include

- Image upload UI, file picker, or any GUI
- Batch image processing or folder scanning
- Vision agent or multi-step agentic loop
- Production document parser (no PDF parsing, no multi-page handling)
- Complex image preprocessing (no OpenCV, no image resizing pipelines)
- pytesseract or any traditional OCR library (Gemini handles this)
- Paid vision APIs (Gemini 1.5 Flash handles vision for free on the same API key)
- FastAPI endpoint or any web server
- React or any frontend code
- Embedding generation for this session (not needed — this is a vision module)
- ChromaDB for this session (RAG is already done in Sessions 4 and 5)

---

# Instructor Framing

## Opening Message

Show the portfolio folder at the start. Point to each script already built:

- Session 1: `structured_output_engine.py` — the foundation of structured AI output
- Session 2: `llm_logger.py` — tracking and evaluating LLM calls
- Session 3: `ai_handler.py` — serverless-style function design
- Session 4: `rag_pipeline.py` — RAG with ChromaDB and sentence-transformers
- Session 5: `rag_evaluator.py` — RAG evaluation and improvement
- Session 6: Simple Agent Router — `agent_router.py` with tool routing

Then say: "Today we go beyond text. We give Gemini an image and ask it to read and understand it. This is called multimodal AI, and it is the basis of document AI products used in banking, insurance, healthcare, and logistics. We will build `vision_ocr_module.py`."

Emphasize the portfolio framing: this module is standalone, but it uses the same Gemini API key, the same structured output thinking from Session 1, and the same confidence/evaluation mindset from Session 2 and 5. Vision is a natural extension of what students already know.

## Key Philosophy

Vision-language models do not "scan" images like a flatbed scanner. They interpret images the same way they interpret text — using learned patterns and contextual understanding. This means they can be brilliant (understanding a complex invoice layout) and brittle (hallucinating a blurry date field). Students need to understand both sides and design their systems accordingly.

Students are not expected to become computer vision engineers. They are expected to understand how to use Gemini's vision capability, design a multimodal prompt, handle its limitations, and communicate this clearly in an interview.

## Repeated Instructor Line

Gemini can read the image. Your job is to design the prompt, validate the output, and document when it should not be trusted.

---

# Session Flow

## 0–10 min: Opening, Portfolio Recap, Show Existing Scripts

Open the portfolio folder on screen. Walk through all 6 scripts built so far. Show the file sizes — each script is small and standalone. Reinforce that the portfolio is a collection of modules, not one giant app.

Introduce today's module: "We will add a seventh module — vision_ocr_module.py. This script takes an image and returns structured data about what is in the image."

Show a real-world context: document AI in banking KYC, insurance claim processing, healthcare record extraction, logistics invoice parsing. These are roles AI engineers are hired for. This module makes that connection concrete.

Ask the class: "How do you think Gemini processes an image differently from how it processes a text string?" Accept 2-3 answers. This surfaces the intuition before the explanation.

Tell students: today's deliverables are three files — `vision_ocr_module.py`, `sample_image.png`, and `ocr_output.json`. All three go into the portfolio folder. The session is done when all three exist and the script runs cleanly.

## 10–20 min: Concept Explanation — Vision-Language Models and Why They Matter

Explain the core concept in plain language first: a Vision-Language Model (VLM) is a model that can receive both image and text as input and generate a text response. Gemini 1.5 Flash is a VLM. The same API call that accepts a text prompt can also accept an image object alongside the text.

Draw or display this flow on screen:
`Image file → PIL.Image.open() → passed to Gemini along with text instruction → Gemini returns structured text → parse to JSON → save to ocr_output.json`

Explain why this is different from traditional OCR (Tesseract, Google Vision API, AWS Textract): Traditional OCR engines pattern-match pixel regions to character codes. VLMs understand semantic context — they can infer that "INV-2024-0045" is an invoice number even if the field label is partially obscured, because they understand document structure from training data.

Explain the risk side: VLMs can hallucinate fields that do not exist in the image, especially when image quality is poor or when prompted too broadly. This is why the `confidence_notes` field in the output is not optional — it is a design requirement.

Briefly mention the production trade-off: VLMs are slower and more expensive than traditional OCR at scale, but they handle layout variability, multilingual text, and complex document types far better. For high-value documents (loan applications, medical records), VLMs are worth the cost. For high-volume commodity scanning (supermarket receipts at millions per day), traditional OCR pipelines are still preferred.

## 20–35 min: Build the Module Using Claude Code or Cursor

Have the instructor run Prompt 1 from the student pre-session file in Claude Code or Cursor. Do this live on screen.

After the prompt runs, show the generated `vision_ocr_module.py` on screen. Do a quick sanity check before walking through it:
- Does the file import `google.generativeai`, `PIL.Image`, `json`, `os`?
- Is the `analyze_image(image_path)` function defined?
- Does the prompt to Gemini ask for `extracted_text`, `document_type`, `key_fields`, and `confidence_notes`?
- Is the output saved to `ocr_output.json`?

If any of these are missing, use the improvement prompt live. Do not fix it manually — show students how to prompt the AI coding tool to fix the gap.

Also generate or show the `sample_image.png`. The simplest approach for classroom use is to programmatically generate a fake invoice using Python's `Pillow` library with text drawn on a white background. This removes the need to source an external image and gives students a reproducible artifact. If Pillow drawing is too slow, use the provided ASCII-art invoice approach: save a `.txt` file as a `.png` via Pillow's `ImageDraw`.

## 35–50 min: Walk Through Generated Code — Explain Every Function

Walk through `vision_ocr_module.py` line by line. Cover every major section.

Section 1 — Imports and API setup: `google.generativeai` is configured with the API key. `PIL.Image` is used to open the image file. `json`, `os`, `re` are used for output handling.

Section 2 — `generate_sample_image()` function (if included): Show how Pillow's `ImageDraw` can create a fake invoice image programmatically. Explain why this is better for a classroom setting than downloading an external file — it makes the module self-contained.

Section 3 — `analyze_image(image_path)` function: This is the core function. It opens the image with `PIL.Image.open(image_path)`, constructs a multimodal prompt (text instruction + image object), calls `model.generate_content([prompt_text, image])`, and parses the response.

Section 4 — Prompt design: Walk through the exact prompt string. Show how it asks Gemini for JSON output and explicitly requires `confidence_notes`. Ask students: "Why is `confidence_notes` in the prompt, not just in our post-processing?" Answer: If it is not in the prompt, Gemini will not produce it — it only produces what is asked for.

Section 5 — JSON parsing and error handling: Show the `try/except` block. Explain that Gemini sometimes wraps JSON in markdown code fences (` ```json ... ``` `). Show the regex or string stripping needed to clean this. This is a real issue students will encounter in the wild.

Section 6 — `save_output(data, filepath)` function: Saves the parsed dict to `ocr_output.json` with `json.dump(..., indent=2)`.

Section 7 — `main()` block: Show the `if __name__ == "__main__"` entry point. Explain why this pattern matters — it allows the module to be imported by other scripts (like a future agent that calls `analyze_image`) without immediately running.

## 50–65 min: Student Follow-Along Build

Students run Prompt 1 from their pre-session file in their own Claude Code or Cursor instance. Instructor circulates (or monitors student screens if remote) to check:

- Is the `GEMINI_API_KEY` set in the environment?
- Did the script generate without syntax errors?
- Does `sample_image.png` exist in the folder?
- Does running `python vision_ocr_module.py` produce output on the terminal?

The most common issue at this stage is the API key not being set. Have a standard fix ready: `export GEMINI_API_KEY="your_key_here"` in terminal, or a `.env` file with `python-dotenv`. Walk one student through it on screen so the rest can follow.

Second most common issue: Pillow not installed. Fix: `pip install Pillow`. Third: `google-generativeai` version conflict. Fix: `pip install --upgrade google-generativeai`.

Do not let students spend more than 3 minutes on any single setup issue during follow-along. If they are blocked, have them use the instructor's generated code and continue conceptually.

## 65–80 min: Test with Sample Inputs, Inspect Output Files

Every student should now run `python vision_ocr_module.py` and open `ocr_output.json`.

Walk the class through reading the JSON output together. Project one student's (or the instructor's) `ocr_output.json` on screen. Ask:
- "What did Gemini extract as `document_type`?"
- "What is in the `key_fields` dict? Are those the right fields for an invoice?"
- "What is in `confidence_notes`? Did Gemini note any uncertainty?"
- "Does `extracted_text` match what you see in the image?"

Introduce the concept of output validation here: in production, you would not just log the JSON — you would check that `key_fields` contains the required fields and that none of them are null. Show a simple validation snippet: check that `amount` and `date` exist in `key_fields` and are non-empty strings.

Have students intentionally pass a low-quality or ambiguous image (e.g., a very small image, or a screenshot of blurry text) and re-run. Show how the `confidence_notes` field changes. This makes the limitation concrete and memorable.

## 80–95 min: Edge Cases, Error Handling, Failure Modes

Run Prompt 7 (Edge Case and Failure Mode Prompt) from the student file. Walk through the improvements added by the AI coding tool.

Cover these specific failure modes for this module:

1. Image file not found: `FileNotFoundError` when `PIL.Image.open()` is called with a bad path. Fix: check `os.path.exists(image_path)` before opening.

2. Gemini returns non-JSON text: The model sometimes returns a conversational response instead of JSON, especially if the prompt is ambiguous. Fix: wrap JSON parsing in `try/except json.JSONDecodeError` and log the raw response for debugging.

3. Gemini wraps JSON in markdown code fences: The response looks like ` ```json\n{...}\n``` `. Fix: use `re.sub(r'```json\n?|```', '', response_text).strip()` before parsing.

4. API rate limit (429 error): On the free tier, Gemini 1.5 Flash allows 15 requests per minute. If the class runs 20 students simultaneously, some will hit this. Fix: exponential backoff with `time.sleep()`, or stagger student runs.

5. Image too large: Very large images (>4MB) can cause the API call to fail or time out. Fix: add a check on file size and a resize step using `image.thumbnail((1024, 1024))` if needed.

6. `key_fields` is missing expected keys: Gemini may not extract all fields if the image is unclear. Fix: in the output, use `.get()` with defaults rather than direct key access — `key_fields.get("amount", "NOT_FOUND")`.

7. `GEMINI_API_KEY` not set: The `google.generativeai.configure()` call will fail with an authentication error. Fix: check for the env variable at startup and raise a clear `ValueError` with a helpful message.

8. PIL ImportError: Pillow is not always installed by default. Fix: add it to `requirements.txt` and show the install command.

Show each of these in the code and explain how to communicate them in an interview: "I handled the case where Gemini returns markdown-wrapped JSON by stripping the code fences before parsing. I also added a check for missing API key at startup."

## 95–105 min: Concept Pause — VLMs, Multimodal Prompting, OCR Limitations, Human Verification

Stop coding. Close the editor. Explain the conceptual layer.

Vision-Language Models process images by encoding them into a sequence of visual tokens (patch embeddings) that are combined with text tokens in the transformer architecture. Gemini 1.5 Flash uses a multimodal encoder that maps image patches to a representation space shared with text. When you pass `[prompt_text, image]` to `generate_content()`, both inputs flow through this shared space.

This is fundamentally different from traditional OCR: Traditional OCR (Tesseract, AWS Textract) works by finding character-shaped regions in a binarized image and mapping them to Unicode codepoints using trained classifiers. It is fast and deterministic. VLM-based OCR is slower and probabilistic — the same image can produce slightly different outputs on repeated calls. The advantage is robustness: VLMs handle varied fonts, rotated text, mixed languages, and complex layouts that would require extensive preprocessing for traditional OCR.

The hallucination risk is real. If you ask Gemini "what is the invoice total?" and the image is blurry, Gemini may confidently return a plausible-looking number that is wrong. This is not a bug — it is the nature of probabilistic generation. The `confidence_notes` field in the output is the design response to this risk: it gives the model a designated place to communicate uncertainty, which an application can surface to a human reviewer.

Ask students: "What would you do in production if `confidence_notes` says 'date field is partially obscured, extraction uncertain'?" Expected direction: flag the document for human review, send it to a review queue, or block automatic downstream processing until a human confirms the date.

Gemini vs GPT-4 Vision: both are capable VLMs. GPT-4 Vision has historically shown slightly higher accuracy on dense text extraction benchmarks. Gemini 1.5 Flash is faster, cheaper, and has a 1M token context window which allows passing very large images or multiple images in one call. For this portfolio, Gemini 1.5 Flash is the right choice — it is free tier accessible and uses the same API key as the text calls students have been making since Session 1.

## 105–115 min: Interview Discussion and Viva Practice

Use the interview questions from the section below. Run through at least 5 of them. Recommended sequence: Q1, Q3, Q6, Q9, Q13.

Ask each question out loud. Give students 60 seconds to form an answer, then call on one. Correct or extend the answer. Have the student repeat the improved answer.

For Q13 (production scaling), push students to think about cost, latency, and error rate — not just whether the code works.

Remind students: "In an interview, you do not need to memorize these answers. You need to understand the concept well enough to reconstruct the answer. If you built this module and can explain every line of code, the answer comes naturally."

## 115–120 min: Wrap-Up, Show Output Files, Preview Session 8

Show the portfolio folder now with 7 scripts. Highlight the three new files from today: `vision_ocr_module.py`, `sample_image.png`, `ocr_output.json`.

Tell students: "You have now built a portfolio that covers structured output, logging, serverless functions, RAG, RAG evaluation, agent routing, and vision/OCR. Each module is independent, each is explainable, and each maps to a real product use case."

Preview Session 8: "In the final session, we will do a complete system design walkthrough. You will be asked to design a document AI pipeline that could use several of these modules together. We will also do mock interview practice covering the full portfolio. Come prepared to explain any of the 7 modules."

---

# Instructor Notes

## What to Emphasize

This session has a higher concept density than previous sessions because vision is newer territory for most students. The implementation is actually simpler than Sessions 4 and 5 (no vector DB, no embeddings, no chunking) — but the conceptual understanding of why VLMs behave the way they do is deeper.

Emphasize that the API call for vision is the same pattern as text generation — `model.generate_content(...)` — but the content list contains both a text string and a PIL Image object. This sameness is important: it means students can extend any existing Gemini text module to handle images with minimal changes.

Emphasize the `confidence_notes` requirement repeatedly. This is the most interview-differentiating concept in this session. Most junior candidates know how to call a vision API. Very few think about designing the output to surface uncertainty explicitly.

Emphasize that `ocr_output.json` is a first-pass extraction, not ground truth. Human verification is a feature requirement, not an afterthought.

## Common Student Mistakes — Specific to This Module

1. Passing the image path as a string to `generate_content()` instead of a PIL Image object. The Gemini SDK requires the actual image object, not the file path. Error: `google.generativeai.types.generation_types.StopCandidateException` or silent failure with no image understanding in the response.

2. Forgetting to call `PIL.Image.open(image_path)` and passing the raw path string. Fix: always open the image first and pass the returned `PIL.Image` object.

3. Not stripping markdown code fences from the Gemini response before calling `json.loads()`. Error: `json.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`. Students must handle the ` ```json ` wrapper.

4. Asking Gemini to return JSON without specifying the exact keys in the prompt. Gemini will invent its own field names, which breaks the downstream parsing. The prompt must explicitly list `extracted_text`, `document_type`, `key_fields`, and `confidence_notes` as required keys.

5. Not setting `GEMINI_API_KEY` as an environment variable and hardcoding the key in the script. This is a security issue and will cause problems if the student shares the script. Fix: always use `os.environ.get("GEMINI_API_KEY")` or `python-dotenv`.

6. Using the wrong `google-generativeai` method for multimodal input. Some students try `model.generate_content(prompt)` with a concatenated string that includes the image filename, thinking Gemini will "find" the image. It will not. The image object must be in the content list.

7. Not handling the case where `json.loads()` succeeds but the returned dict is missing expected keys (e.g., `key_fields` is present but `amount` is absent because the image was unclear). Fix: always use `.get()` with a default value when accessing nested keys.

8. Generating a `sample_image.png` that is entirely blank or too small to be readable by Gemini. If the image has no text, Gemini will return an empty `extracted_text` and a `confidence_notes` about the image being blank. This is actually a good teaching moment — show it happening and discuss what it means.

9. Expecting Gemini to be 100% accurate on the sample image and being confused when `key_fields.amount` returns a slightly different format than expected (e.g., "1,250.00" vs "1250.00"). Explain that output normalization (stripping currency symbols, standardizing date formats) is always needed in production.

10. Running the script multiple times quickly and hitting the 15 requests/minute rate limit on the free tier. Error: `google.api_core.exceptions.ResourceExhausted: 429 Quota exceeded`. Fix: add a `time.sleep(4)` between calls in test loops, or implement exponential backoff.

## How to Control the Session

The biggest time sink in this session is environment setup. Students who do not complete the pre-session checklist will spend 15-20 minutes installing Pillow, setting up their API key, and troubleshooting imports. Enforce the pre-session setup requirement strictly.

Do not let any single student's debug session consume class time after the 2-minute mark. Have a fallback: share the instructor's working script and `sample_image.png` so the student can run the instructor's version and continue participating conceptually.

The concept pause at 95-105 min is non-negotiable. Do not compress it to make room for more coding. The interview value of this session is in the conceptual understanding, not the code volume.

If students start asking about building a batch processing pipeline or a web UI for image upload, redirect firmly: "That is Session 8 planning territory. Today we are only building `analyze_image(image_path)` as a clean, standalone function."

---

# Questions to Discuss: Interview Perspective

## Basic Module Questions

### Q1. What did you build in Session 7?

Expected answer:
I built `vision_ocr_module.py`, a standalone Python module that uses Gemini 1.5 Flash as a vision-language model to analyze a document image and extract structured information from it. The module defines an `analyze_image(image_path)` function that opens the image with PIL, passes it along with a structured text prompt to Gemini's multimodal API, and returns a parsed JSON object containing `extracted_text`, `document_type`, `key_fields` such as amount, date, and name, and `confidence_notes`. The result is also saved to `ocr_output.json`. The module is a portfolio artifact demonstrating multimodal AI prompting, structured output design, and responsible handling of uncertain extractions.

### Q2. What is the difference between this module and a traditional OCR tool like pytesseract?

Expected answer:
Pytesseract and other traditional OCR tools work by binarizing the image, detecting character-shaped pixel regions, and mapping them to Unicode characters using a trained classifier. The output is raw text with positional metadata. Gemini 1.5 Flash, as a vision-language model, encodes the entire image into visual tokens and reasons about it in context — it understands that an invoice has a header, line items, and a total, even if the layout is non-standard. The practical difference is that Gemini can handle layout variability, partial occlusion, and semantic inference (for example, inferring that "INV-0045" is an invoice number even without an explicit "Invoice Number" label), while pytesseract requires clean, well-formatted input and extensive preprocessing. The trade-off is that Gemini is slower, costs API credits, and can hallucinate — pytesseract is deterministic and free to run locally.

### Q3. Why is `confidence_notes` a required field in the output?

Expected answer:
Vision-language models are probabilistic — they do not scan pixels the way a scanner does; they generate output based on learned patterns, which means they can produce plausible-looking but incorrect values when the image is ambiguous, blurry, or contains partially visible text. `confidence_notes` is a required field in the prompt design so that Gemini has a designated location to surface its own uncertainty. If Gemini is unsure whether a date field reads "01/06" or "01/08" due to image quality, it should express that in `confidence_notes` rather than silently returning a guess. In a production pipeline, `confidence_notes` is read by downstream logic to decide whether to auto-approve the extraction or route it to a human reviewer. This is the difference between a prototype and a responsible production system.

### Q4. How do you pass an image to Gemini 1.5 Flash using the `google-generativeai` library?

Expected answer:
The `google-generativeai` library's `generate_content()` method accepts a list of content parts. To include an image, you open the file using `PIL.Image.open(image_path)` and include the resulting PIL Image object as one element of the content list, alongside the text instruction string. The call looks like: `model.generate_content([prompt_text, pil_image])`. The SDK handles the internal encoding of the PIL image into the multimodal format Gemini expects. This is the same `model.generate_content()` call used for text-only prompts — the multimodal capability is accessed simply by including a non-text object in the list, which is why the learning curve from text to vision is intentionally low with this library.

### Q5. What does `ocr_output.json` contain and why is it saved to disk?

Expected answer:
`ocr_output.json` contains the structured result of running `analyze_image()` on the sample document image. It is a JSON object with four top-level keys: `extracted_text` (the full text Gemini read from the image), `document_type` (e.g., "invoice", "receipt", "ID card"), `key_fields` (a nested dictionary with specific fields like `amount`, `date`, `vendor_name`, `invoice_number`), and `confidence_notes` (a string or list describing any uncertainty in the extraction). It is saved to disk rather than only printed to the console for two reasons: first, it makes the module's output a persistent, inspectable artifact that is part of the portfolio; second, in a real pipeline, downstream processes would read this JSON file or its equivalent rather than re-running the vision model on every request.

## Technical Deep-Dive Questions

### Q6. Why might `json.loads()` fail on the Gemini response even when the model was asked to return JSON?

Expected answer:
Gemini, like most language models, sometimes wraps its JSON output in markdown code fences (` ```json\n{...}\n``` `) rather than returning raw JSON. This happens because the model was likely trained on documents where JSON examples appear in code blocks. When `json.loads()` receives a string starting with ` ``` `, it throws a `json.JSONDecodeError` because backticks are not valid JSON. The fix is to strip the code fences before parsing, using either a regex like `re.sub(r'```json\n?|```', '', response_text).strip()` or a simple string replacement. A robust implementation also wraps the entire parse step in a `try/except json.JSONDecodeError` block and logs the raw response text when parsing fails, so the engineer can inspect what Gemini actually returned.

### Q7. What happens in `analyze_image()` from input to output? Walk through the execution steps.

Expected answer:
First, the function checks whether the file at `image_path` exists using `os.path.exists()`; if not, it raises a `FileNotFoundError` with a clear message. Then it opens the image using `PIL.Image.open(image_path)`, which returns a PIL Image object. It constructs a multimodal prompt string that specifies the required JSON output format with all four required keys. It calls `genai.GenerativeModel("gemini-1.5-flash").generate_content([prompt_text, pil_image])` to get the model's response. It extracts the text from `response.text`, strips any markdown code fences, and calls `json.loads()` on the cleaned string inside a `try/except` block. If parsing succeeds, it returns the dict. If parsing fails, it returns a fallback dict with `extracted_text` set to the raw response and an error message in `confidence_notes`. Finally, the `main()` block calls `analyze_image()` and writes the result to `ocr_output.json` using `json.dump(..., indent=2)`.

### Q8. Why does the prompt explicitly list the required JSON keys rather than just saying "return JSON"?

Expected answer:
If the prompt says "return the extracted information as JSON" without specifying keys, Gemini will invent its own schema — which may vary between runs, use different key names (e.g., "total" vs "amount", "date_issued" vs "date"), or omit fields entirely for images where those fields are not obviously present. Downstream code that accesses `result["key_fields"]["amount"]` will break with a `KeyError` if Gemini used "total_amount" instead. By specifying the exact key names in the prompt — and instructing Gemini to use null or "NOT_FOUND" for keys that cannot be extracted — we enforce a deterministic output schema. This is the same structured output principle used in Session 1's `structured_output_engine.py`, now applied to multimodal input.

### Q9. What are the Gemini 1.5 Flash free tier rate limits and how do you handle them in this module?

Expected answer:
As of mid-2024, Gemini 1.5 Flash on the free tier allows 15 requests per minute and 1500 requests per day. When this limit is exceeded, the API returns an `HTTP 429 ResourceExhausted` error, which the `google-generativeai` SDK raises as `google.api_core.exceptions.ResourceExhausted`. In this module, which processes a single image per run, rate limiting is unlikely in normal use. However, if the module is extended to process multiple images in a loop, an exponential backoff strategy should be implemented: catch the `ResourceExhausted` exception, wait (starting at 1 second and doubling on each retry up to a max of 60 seconds), and retry the call. The `tenacity` library provides a clean decorator-based way to implement this: `@retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5), retry=retry_if_exception_type(ResourceExhausted))`.

### Q10. How would you validate the output of `analyze_image()` before using it downstream?

Expected answer:
Output validation should happen in a separate step after parsing. At minimum, check that the returned dict contains all four required top-level keys (`extracted_text`, `document_type`, `key_fields`, `confidence_notes`) using `isinstance(result, dict) and all(k in result for k in required_keys)`. Then validate the `key_fields` sub-dict: check that expected fields are present and non-null, for example `result["key_fields"].get("amount")` should not be `None` or `"NOT_FOUND"` for an invoice. If `confidence_notes` is non-empty, flag the record for human review rather than auto-processing it. In a production system, this validation layer would also normalize field formats — strip currency symbols from amounts, parse dates into ISO 8601 format, convert all strings to lowercase for document_type. This validation logic is intentionally separate from `analyze_image()` so that the extraction and validation concerns are decoupled.

## Production and System Design Questions

### Q11. How would you build a production document processing pipeline using this module as the foundation?

Expected answer:
A production pipeline would add several layers around the core `analyze_image()` function. First, an ingestion layer to accept document uploads from a file system, S3 bucket, or email attachment and normalize them to a standard image format. Second, a pre-processing step to check image quality (DPI, contrast, file size) and reject or flag documents that fall below a threshold, rather than sending bad images to the expensive VLM API. Third, the `analyze_image()` call itself, wrapped in retry logic for rate limiting and with a timeout to prevent hanging on slow API responses. Fourth, a validation layer that checks the output schema and flags records with non-empty `confidence_notes` for human review. Fifth, a storage layer that writes the JSON output to a database (PostgreSQL with JSONB columns, or a document store like MongoDB). Sixth, a monitoring layer that tracks extraction accuracy over time by sampling completed records and comparing VLM output against ground truth. The module built in Session 7 is the core extraction unit in step three of this pipeline.

### Q12. What would you monitor in production for this vision OCR pipeline?

Expected answer:
The key metrics to monitor are: extraction accuracy rate (percentage of documents where all required fields are extracted successfully without `confidence_notes` flags), hallucination rate (percentage of documents where extracted values differ from ground truth, measured by periodic spot-checking), API latency percentiles (P50, P95, P99 response times for the Gemini API call), API error rate (429 rate limit errors, 500 server errors, timeout rate), human review queue depth (the number of documents flagged by `confidence_notes` that are waiting for human verification — a rising queue indicates degrading image quality in the input stream or a model regression), and cost per document (number of API calls times cost per call). For the free tier portfolio module, latency and error rate are the practical metrics to track. In production, accuracy drift over time is the most critical signal — if the model starts hallucinating more frequently on a document type, it likely means the input distribution has shifted (e.g., a new invoice template not seen in training).

### Q13. What breaks when you scale this module from processing one image to processing 10,000 images per day?

Expected answer:
Several things break at scale. Rate limiting becomes the first bottleneck: the free tier allows 1500 requests per day, so 10,000 images per day requires a paid tier. Even on a paid tier, parallel calls will hit per-minute rate limits, requiring a job queue (Celery, AWS SQS, or a simple `concurrent.futures` ThreadPoolExecutor with rate limiting). Memory becomes an issue: loading 10,000 PIL Image objects without streaming will exhaust RAM; images must be processed in batches and garbage-collected. The current `analyze_image()` function is synchronous and blocking, so at scale it needs to be wrapped in async logic or run as a worker pool. The single `ocr_output.json` file breaks immediately — at scale, each document needs its own output record in a database with a document ID, timestamp, and processing status. Error handling becomes more complex: a single failed extraction should not block the entire batch. Finally, cost management becomes important: at scale, you would add a cheapness filter to skip the VLM for documents that traditional OCR can handle reliably (clear, machine-printed text) and only use Gemini for complex cases.

### Q14. How would you compare Gemini 1.5 Flash vision against GPT-4 Vision for this use case, and when would you choose one over the other?

Expected answer:
Both are capable multimodal models. GPT-4 Vision (gpt-4-turbo or later) has historically shown slightly higher accuracy on dense, structured document extraction benchmarks, particularly for complex layouts like medical records and financial tables. Gemini 1.5 Flash has a significantly larger context window (1 million tokens), which allows passing multiple images or very high-resolution images in a single call — a meaningful advantage for multi-page documents. Gemini 1.5 Flash is substantially faster and cheaper than GPT-4 Vision at equivalent accuracy for straightforward document types (invoices, receipts). For this portfolio, Gemini 1.5 Flash is the right choice because it uses the same `google-generativeai` API key the student has been using since Session 1, it is free tier accessible, and it handles the module's scope (single-image invoice/receipt extraction) with more than sufficient accuracy. The code structure for GPT-4 Vision would be nearly identical — the same multimodal pattern applies, with the image encoded as base64 in the message rather than as a PIL object — making the architectural knowledge transferable across providers without requiring students to learn a second SDK.

### Q15. Why do you need human verification in a document AI pipeline even when accuracy is 95%?

Expected answer:
A 95% accuracy rate sounds high, but at scale it means 1 in 20 documents has an incorrect extraction. For a pipeline processing 10,000 invoices per day, that is 500 incorrectly processed documents per day. In high-stakes domains like financial transactions, healthcare records, or legal documents, a single incorrect extraction can cause a wrong payment, a treatment error, or a compliance violation — each of which has costs that far exceed the cost of human review. The `confidence_notes` field in this module is the mechanism that enables risk-stratified human verification: documents where the model flags uncertainty go to a human reviewer; documents where the model is confident and the output passes schema validation can be auto-processed. This is not an admission of model failure — it is a responsible system design pattern called "human-in-the-loop." The goal is not to replace human judgment but to reduce the volume of documents requiring it from 100% to 5-10%, while ensuring the highest-risk cases always get human attention.

---

# Session 7 Completion Checklist

Students should verify all of the following by the end of the session:

- [ ] `vision_ocr_module.py` exists in the portfolio folder and runs without import errors
- [ ] `sample_image.png` exists in the portfolio folder and is a readable document image (invoice/receipt style)
- [ ] Running `python vision_ocr_module.py` completes without an unhandled exception
- [ ] `ocr_output.json` is created after running the script and contains valid, parseable JSON
- [ ] `ocr_output.json` contains all four required keys: `extracted_text`, `document_type`, `key_fields`, `confidence_notes`
- [ ] `key_fields` contains at least three extracted fields (e.g., amount, date, vendor name)
- [ ] `confidence_notes` is populated (either with actual uncertainty notes or with "extraction appears complete and confident")
- [ ] `analyze_image(image_path)` function is defined and callable independently (can be imported from another script)
- [ ] `GEMINI_API_KEY` is loaded from an environment variable, not hardcoded in the script
- [ ] Gemini API rate limit (429) is handled gracefully with a caught exception and a meaningful error message, not an unhandled crash
- [ ] The script handles a missing or incorrect `image_path` with a clear error message rather than a raw Python traceback
- [ ] Student can explain, without reading the code, what `analyze_image()` does, what `confidence_notes` is for, and why VLM-based OCR differs from pytesseract

---

# Instructor Backup Plan

## If Gemini Rate Limit Hits During Class

If multiple students run the script simultaneously and several hit 429 errors:
1. Pause the class and explain the rate limit — this is itself a teaching moment about free tier constraints in production AI.
2. Stagger student runs: have students run in groups of 5, waiting 60 seconds between groups.
3. The instructor's already-generated `ocr_output.json` should be visible on screen so students who are rate-limited can still follow the output discussion.
4. If rate limiting persists, switch to showing the output analysis section using the instructor's saved `ocr_output.json` and have students catch up on their own script execution after class.

## If a Student's Setup Fails (Pillow, google-generativeai, or API key issues)

1. Do not spend more than 2 minutes debugging any individual student issue during class.
2. Pair the blocked student with a neighbor who has a working setup.
3. Share the instructor's completed `vision_ocr_module.py` and `sample_image.png` via chat or shared folder at the 50-minute mark so that blocked students can run the instructor's version.
4. The student should follow the instructor screen for all conceptual sections and catch up on their own build after class using the prompts in the pre-session file.
5. Ensure every student leaves with the `ocr_output.json` file — even if they ran the instructor's version — so they have the portfolio artifact.

## If Gemini Returns Unexpected Output Format Consistently

If the JSON parsing fails for most students because Gemini is returning an unexpected format:
1. Show the raw `response.text` on screen — this is a teachable debugging moment.
2. Run the improvement prompt live to add more robust parsing (regex strip + fallback dict).
3. If Gemini is consistently returning non-JSON responses, modify the prompt to add "IMPORTANT: Return ONLY the JSON object. Do not include any explanation text before or after the JSON. Do not use markdown code fences."
