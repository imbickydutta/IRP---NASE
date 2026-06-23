# Session 7 After-Session Notes: Vision/OCR Mini Module

## What We Built Today

Today we added the seventh module to the AI Systems Interview Portfolio:

- `vision_ocr_module.py` — Python script using Gemini 1.5 Flash multimodal to analyze a document image and return structured JSON output
- `sample_image.png` — a programmatically generated fake invoice image using Pillow's ImageDraw (self-contained, no external download needed)
- `ocr_output.json` — the structured extraction result saved to disk after running the script

The core function is `analyze_image(image_path)`. It opens an image file with PIL, constructs a multimodal prompt specifying the exact JSON output schema, calls Gemini 1.5 Flash with both the text prompt and the image object, parses the response, and returns a structured Python dict. The dict contains four required fields: `extracted_text`, `document_type`, `key_fields`, and `confidence_notes`.

---

# Why This Module Matters for AI Engineering Interviews

Document AI is one of the most active areas of AI engineering hiring. Companies across banking, insurance, healthcare, logistics, and legal services are actively building pipelines that extract structured data from documents at scale. The engineers who build these systems need to understand: how to pass images to a VLM, how to design a prompt that returns consistent structured output, why confidence scoring matters, and what the limitations of VLM-based extraction are compared to traditional OCR.

Most junior AI engineers know how to call a text generation API. Fewer know how to use the same API for vision input. Even fewer understand the design decisions that make a vision extraction module production-ready rather than a demo — specifically, the confidence notes pattern and the human review requirement.

This module positions you to discuss document AI fluently in an interview. It shows both practical skill (calling a multimodal API, parsing structured output, saving results) and conceptual depth (understanding hallucination risk, confidence tracking, human-in-the-loop design).

---

# Portfolio Module Map

```
Session 1: Structured Output Prompt Engine
    structured_output_engine.py + output_examples.json
    Status: DONE
    Key skill: JSON output design, prompt engineering
    Used by: Sessions 2, 3, 4, 5, 6, 7

Session 2: LLM Logging and Evaluation Tracker
    llm_logger.py + llm_logs.csv + eval_summary.json
    Status: DONE
    Key skill: tracking, evaluation, confidence scoring
    Used by: Sessions 5, 7 (confidence_notes concept)

Session 3: Serverless-Style AI Function
    ai_handler.py + .env.example
    Status: DONE
    Key skill: stateless function design, environment variables
    Used by: Session 7 (analyze_image is a stateless function)

Session 4: Basic RAG Pipeline     ←→     Session 5: RAG Evaluation
    rag_pipeline.py + chroma_db/              rag_evaluator.py + rag_eval_report.csv
    Status: DONE                              Status: DONE
    Key skill: retrieval, ChromaDB,           Key skill: before/after comparison,
    sentence-transformers                     retrieval quality metrics
    (Sessions 4 and 5 are linked)

Session 6: Simple Agent Router
    agent_router.py
    Status: DONE
    Key skill: intent classification, tool routing

Session 7: Vision/OCR Mini Module     ← COMPLETED TODAY
    vision_ocr_module.py
    sample_image.png
    ocr_output.json
    Status: DONE
    Key skill: multimodal prompting, VLM-based OCR, confidence notes

Session 8: Final System Design + Interview Demo
    Status: NEXT SESSION
    Goal: connect all 7 modules, mock interview practice, system design walkthrough
```

---

# Technical Deep-Dive: Vision-Language Models, Multimodal Prompting, OCR Limitations, and Human Verification

## How Vision-Language Models Process Images

A Vision-Language Model like Gemini 1.5 Flash processes an image by first dividing it into a grid of fixed-size patches (typically 16x16 or 32x32 pixels). Each patch is encoded into a high-dimensional vector called a patch embedding using a Vision Transformer (ViT) encoder. These patch embeddings are projected into the same representation space as text token embeddings and concatenated with the tokenized text prompt. The combined sequence — visual tokens from the image patches and text tokens from the prompt — is then processed by the transformer's attention mechanism, allowing the model to attend to both visual and textual information simultaneously when generating its response. This is why Gemini can "read" text in an image: it does not scan for character shapes like traditional OCR; it attends to the visual patterns in image patches and uses its language model knowledge to interpret what those patterns mean in context.

When you call `model.generate_content([prompt_text, pil_image])` in the `google-generativeai` library, the SDK handles the encoding of the PIL Image object into the patch embedding format and combines it with the tokenized prompt before sending to the API. From the developer's perspective, the call looks nearly identical to a text-only call — the only difference is that the content list contains an image object alongside the text string. This deliberate API design means that AI engineers who already know how to use Gemini for text generation can extend their existing code to handle images with minimal changes.

## Why VLM-Based OCR Differs from Traditional OCR and Why Both Still Exist

Traditional OCR engines (Tesseract, AWS Textract, Google Document AI in non-ML mode) work in a fundamentally different way: they binarize the image, detect contiguous pixel regions with character-like shapes, and match those regions to character codes using trained classifiers. This approach is fast (milliseconds per page), deterministic (the same image always produces the same output), and free to run locally (Tesseract is open source). However, it requires clean input: consistent fonts, adequate DPI, no rotation, minimal noise. When input quality degrades or document layouts vary significantly, traditional OCR accuracy drops sharply.

VLM-based OCR handles layout variability, mixed fonts, rotated text, multilingual content, and semantic inference that traditional OCR cannot do. For example, if an invoice uses "Amt." as an abbreviation for amount with no explicit "Amount:" label, traditional OCR will extract "Amt." as raw text with no semantic meaning. Gemini will infer that "Amt." refers to the total amount and place the corresponding value in `key_fields.amount`. This semantic understanding is the core advantage. The cost is that VLMs are slower (seconds per image rather than milliseconds), cost API credits, and — critically — can hallucinate. If a date field is partially smudged and reads ambiguously as "01/06" or "01/08", Gemini might confidently return one of the two values without indicating uncertainty unless the prompt explicitly asks for confidence notes. Traditional OCR would return the raw characters or low confidence scores from the character classifier — but it would not silently hallucinate a different date.

## The Confidence Notes Design Pattern and Human Verification

The `confidence_notes` field in this module is a deliberate design pattern, not an afterthought. In production document AI systems, extracted data is often used to trigger financial transactions, update medical records, or initiate legal processes. A single incorrect extraction in these contexts can cause a wrong payment, a treatment error, or a compliance violation. An accuracy rate of 95% sounds high, but at 10,000 documents per day it means 500 incorrect extractions daily. The solution is not to demand 100% VLM accuracy (which is not achievable) but to design the system to know when it does not know.

By requiring `confidence_notes` in the Gemini prompt, we give the model a structured place to surface uncertainty. Downstream logic reads this field and routes uncertain documents to a human review queue rather than auto-processing them. This "human-in-the-loop" pattern reduces the volume of documents requiring human attention from 100% to typically 5-15% (only the ambiguous ones), while ensuring that the highest-risk cases always receive human judgment. The `confidence_notes` field connects directly to the evaluation mindset introduced in Session 2's `llm_logger.py` and Session 5's `rag_evaluator.py` — in all three cases, the design question is the same: "How do we know when to trust the model's output?"

---

# What Students Should Understand

1. **The multimodal API call pattern**: `model.generate_content([prompt_text, pil_image])` — the content list can mix text and image objects. PIL Image object must be passed, not a file path string.

2. **Why structured output keys must be specified in the prompt**: If you ask Gemini to "return JSON" without specifying keys, it will invent its own schema that varies between runs, breaking downstream code. The explicit key list in the prompt enforces a contract between the model and your parser.

3. **Why markdown code fence stripping is a real engineering concern**: Gemini (like most LLMs trained on code-heavy data) sometimes wraps JSON output in ` ```json ... ``` ` fences, especially when the prompt implies a code context. The `re.sub(r'```json\n?|```', '', text).strip()` pattern is a practical fix used in production AI systems.

4. **The confidence_notes pattern**: It is a required prompt design decision, not an optional field. It exists because VLMs can hallucinate confidently. The field gives the model a designated place to express uncertainty and gives the application a structured signal to trigger human review.

5. **VLM vs traditional OCR trade-offs**: VLMs handle layout variability and semantic inference. Traditional OCR is faster, deterministic, and free. In production, both are often used: traditional OCR for high-volume, clean documents; VLMs for complex, variable-layout, or high-value documents.

6. **The `if __name__ == "__main__"` pattern enables module reuse**: Because `analyze_image()` is a standalone function and the `main()` block only runs when the script is executed directly, a future agent or pipeline module can import and call `analyze_image()` without triggering the full script execution.

7. **Rate limiting is a real free-tier constraint**: Gemini 1.5 Flash allows 15 requests per minute on the free tier. In a class of 20 students running the script simultaneously, some will hit 429 errors. Handling `ResourceExhausted` with retry logic is a practical skill, not a theoretical one.

8. **The `sample_image.png` is generated programmatically**: Using Pillow's `ImageDraw` to create a fake invoice image makes the module self-contained. No external file download is needed. This also demonstrates that portfolio modules should be fully reproducible — anyone who clones the repo can run the script from scratch.

9. **Output normalization is a separate concern**: Gemini might return "Rs. 2,655" or "2655" or "2,655 INR" for the same amount field. Standardizing field formats (stripping currency symbols, parsing dates to ISO 8601) is a post-extraction step that is intentionally separate from `analyze_image()`.

10. **This module maps to real product use cases**: KYC document verification in banking, insurance claim form extraction, healthcare prescription parsing, logistics invoice processing — all of these are products actively using VLM-based document extraction today.

---

# Interview-Ready Explanation

```text
In Session 7, I built vision_ocr_module.py — a Python module that uses Gemini 1.5 Flash as a vision-language model to extract structured information from a document image. The core function, analyze_image(), opens the image with PIL, passes it alongside a structured JSON prompt to Gemini's multimodal API using model.generate_content([prompt_text, pil_image]), and returns a parsed dict with four required fields: extracted_text, document_type, key_fields (a nested dict with amount, date, vendor name, and other document-specific fields), and confidence_notes (a string where the model documents any uncertainty or ambiguity in the extraction). The module saves results to ocr_output.json, and confidence_notes is a required design feature — not optional — because VLMs can hallucinate, and any non-empty confidence note triggers human review in a production pipeline rather than automatic processing.
```

---

# What Happens When `analyze_image(image_path)` Is Called

```text
Input: image_path = "sample_image.png"

Step 1: Check environment
    os.environ.get("GEMINI_API_KEY") → API key loaded from environment variable
    If key is None → raise ValueError("GEMINI_API_KEY is not set...")

Step 2: Check file existence
    os.path.exists("sample_image.png") → True
    If False → raise FileNotFoundError("Image file not found: sample_image.png...")

Step 3: Open image
    pil_image = PIL.Image.open("sample_image.png")
    Returns a PIL Image object in memory (not a file path, not raw bytes)

Step 4: Construct multimodal prompt
    prompt_text = """Analyze the document image and return a JSON object with exactly
    these keys: extracted_text, document_type, key_fields (with vendor_name,
    invoice_number, date, due_date, amount, bill_to), confidence_notes.
    Return ONLY the JSON object. Do not use markdown code fences."""

Step 5: Call Gemini multimodal API
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt_text, pil_image])
    Gemini processes the visual tokens from the image + text tokens from the prompt
    Returns a response object

Step 6: Extract response text
    raw_text = response.text
    → "```json\n{\n  \"extracted_text\": \"INVOICE\n...\", ...\n}\n```"
    (Gemini sometimes adds markdown fences even when instructed not to)

Step 7: Strip markdown code fences
    cleaned_text = re.sub(r'```json\n?|```', '', raw_text).strip()
    → "{\n  \"extracted_text\": \"INVOICE\n...\", ...\n}"

Step 8: Parse JSON
    result = json.loads(cleaned_text)
    Returns a Python dict with all four required keys
    If json.loads() fails → JSONDecodeError caught → return fallback dict with PARSE_ERROR

Step 9: Return result dict
    {
      "extracted_text": "INVOICE\nVendor: Acme Supplies Ltd.\n...",
      "document_type": "invoice",
      "key_fields": {
        "vendor_name": "Acme Supplies Ltd.",
        "invoice_number": "INV-2024-0045",
        "date": "15 June 2024",
        "due_date": "30 June 2024",
        "amount": "Rs. 2,655",
        "bill_to": "TechCorp Pvt. Ltd."
      },
      "confidence_notes": "Extraction complete. No ambiguities detected."
    }

Step 10 (in main()): Save to disk
    json.dump(result, open("ocr_output.json", "w"), indent=2)
    ocr_output.json created/updated in portfolio folder
```

---

# What AI Was Used For + What Engineers Must Still Do

## What Gemini AI Did

- Read and interpreted the document image using vision-language understanding
- Extracted all visible text from the image (`extracted_text`)
- Classified the document type (`document_type`)
- Identified and extracted specific named fields (`key_fields`)
- Generated a confidence assessment of its own extraction (`confidence_notes`)

## What AI Could Not Do — What You Must Still Do

- **Design the output schema**: You specified the exact JSON keys. Gemini only fills in the values.
- **Write the error handling**: Gemini does not know your application's error requirements. You wrote the `FileNotFoundError`, `ValueError`, `json.JSONDecodeError`, and rate limit handling.
- **Strip the code fences**: The `re.sub(r'```json\n?|```', ...)` pattern is an engineering fix for a known model behavior.
- **Validate the output**: Checking that all keys are present, that `key_fields` values are non-null, and deciding what to do when `confidence_notes` is non-empty — these are engineering decisions.
- **Make the module importable**: The `if __name__ == "__main__"` pattern, the function signature, and the module structure are engineering choices that determine how reusable `analyze_image()` is.
- **Test edge cases**: Passing a blank image, a corrupted file, or a non-document image requires your deliberate testing effort.
- **Decide when to trust the output**: Confidence notes are generated by Gemini, but the rule "non-empty confidence_notes triggers human review" is a product design decision you make.

---

# Common Issues and Fixes

## Issue 1: `json.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`

This means `json.loads()` received an empty string or a string that does not start with a JSON object. Gemini returned something other than the expected JSON — usually because the response started with markdown fences that were not fully stripped, or because Gemini added a preamble like "Here is the extracted information:".

What to ask AI:

```text
My vision_ocr_module.py is throwing json.JSONDecodeError on the Gemini response. First, add a debug print statement that prints the raw response.text before any parsing so I can see exactly what Gemini returned. Then add a more robust stripping step that uses re.search(r'\{.*\}', response_text, re.DOTALL) to find the JSON object even if it is surrounded by other text. If the JSON object cannot be found, return a fallback dict with document_type set to "PARSE_ERROR" and the raw response in the extracted_text field.
```

## Issue 2: `google.api_core.exceptions.ResourceExhausted: 429 Quota exceeded`

This is the Gemini free tier rate limit. On the free tier, Gemini 1.5 Flash allows 15 requests per minute. If you or your classmates are running scripts at the same time, you will hit this limit.

What to ask AI:

```text
My vision_ocr_module.py is hitting a 429 ResourceExhausted error from the Gemini API. Add retry logic to the generate_content() call in analyze_image(). Specifically: catch google.api_core.exceptions.ResourceExhausted, print a message saying "Rate limit reached. Waiting 60 seconds...", wait 60 seconds using time.sleep(60), and retry the call once. If the retry also fails with the same error, raise it with a message that says "Rate limit persists after retry. Try again in a few minutes." Show only the updated analyze_image() function.
```

## Issue 3: `AttributeError: module 'PIL.Image' has no attribute 'open'` or `ModuleNotFoundError: No module named 'PIL'`

Pillow is either not installed or the wrong package is installed. There is a common confusion between `PIL` (old, unmaintained) and `Pillow` (the maintained fork). You should always install `Pillow`, not `PIL`.

What to ask AI:

```text
I am getting ModuleNotFoundError: No module named 'PIL' when running vision_ocr_module.py. Tell me the correct pip install command for Pillow. Also check my import statement — should it be "import PIL" or "from PIL import Image"? Show the correct import and explain why "pip install PIL" does not work but "pip install Pillow" does.
```

---

# Limitations of This Module

This module is a portfolio prototype with intentional scope limits. In production, the following would need to be addressed:

**Single image only**: The module processes one image per call. A production pipeline would need a job queue (Celery, SQS, or similar) to process hundreds or thousands of images in parallel without hitting rate limits.

**No multi-page document support**: PDF files with multiple pages are not handled. In production, you would extract individual page images from a PDF (using `pdf2image` or `pypdf`) and call `analyze_image()` on each page, then merge the results.

**No image quality pre-screening**: The module sends any image to Gemini regardless of quality. A production system would pre-screen for minimum DPI, adequate contrast, and detectable text regions to avoid wasting API credits on unprocessable images.

**Non-deterministic output**: Running `analyze_image()` on the same image twice may produce slightly different `extracted_text` or different formatting in `key_fields` values. Production pipelines need output normalization (standardizing date formats, stripping currency symbols) to ensure consistency.

**`confidence_notes` is model-generated**: The confidence assessment comes from Gemini's self-report, not from an independent verification step. A model can hallucinate confidently and still produce an empty `confidence_notes`. In production, you would supplement model-generated confidence notes with independent validation (e.g., comparing extracted totals against line item sums, or cross-referencing vendor names against a known vendor list).

**No access control or audit trail**: The module reads any image file and writes output to disk without authentication, authorization, or audit logging. Production document AI systems require strict access control, especially for documents containing personal or financial data.

---

# Key Takeaways

1. **Multimodal prompting is the same pattern as text prompting, with image added to the content list.** The call `model.generate_content([prompt_text, pil_image])` is the only new pattern in Session 7. Everything else — structured output, error handling, JSON parsing, file I/O — is the same engineering you have been doing since Session 1.

2. **`confidence_notes` is not optional.** VLMs can hallucinate. The only way to catch this in production is to explicitly ask the model to report its uncertainty and to act on that report with human verification routing. A system that auto-processes every VLM output without a confidence gate is a liability, not a product.

3. **VLM-based OCR and traditional OCR are complementary, not competing.** Use traditional OCR (pytesseract, AWS Textract) for high-volume, clean, machine-printed documents where speed and cost matter most. Use VLM-based OCR for complex layouts, handwritten content, mixed-language documents, or any case where semantic inference (understanding what a field means) is required. The best production systems use both in a tiered approach.

4. **Portfolio modules are more valuable when they are importable, not just runnable.** The `if __name__ == "__main__"` pattern and the clean `analyze_image(image_path)` function signature mean that this module can be called from a future agent, pipeline, or evaluation harness. A module that can only be run as a standalone script has limited reuse value. A module with a clean function interface can be composed into larger systems — which is exactly what Session 8's system design discussion will explore.

---

# Session 8 Preview

Session 8 is the final session: Final System Design and Interview Demo.

You will not build a new module from scratch. Instead, you will:

1. Walk through a mock system design question: "Design a document processing pipeline for an insurance company that processes 10,000 claim forms per day." You will be expected to identify where each portfolio module fits — vision_ocr_module.py for extraction, rag_pipeline.py for policy document retrieval, agent_router.py for routing claim types, llm_logger.py for monitoring, rag_evaluator.py for quality tracking.

2. Do viva practice covering any of the 7 portfolio modules. You should be able to explain every module's purpose, design decisions, and production trade-offs in under 2 minutes each.

3. Review the complete portfolio together — 7 scripts, their inputs and outputs, and how they connect — so you can present it coherently as a single portfolio in interviews.

Come to Session 8 prepared to explain all 7 modules. The final interview demo will be stronger if you can draw connections across modules rather than explaining each one in isolation.
