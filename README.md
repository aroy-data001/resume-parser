# Resume Parser & Job Match Evaluator

A Python-based application that uses a large language model (LLM) to
extract structured information from resumes and evaluate candidates
against a dynamically supplied job description.

The project focuses on practical LLM application development: document
text extraction, prompt-based information extraction, structured outputs
with Pydantic, and batch processing.

**Current status:** The working implementation is a command-line Python
application. A FastAPI backend and React frontend are planned
extensions, not part of the current implementation.

## Features

-   **Dynamic job description input:** Paste a multiline job description
    into the terminal. The application sends it to the LLM and converts
    the requirements into a structured Pydantic model.
-   **PDF and DOCX support:** Extract text from PDF files with `pypdf`
    and from DOCX files with `python-docx`.
-   **Structured resume parsing:** Use an LLM to extract candidate
    information into a validated Pydantic model.
-   **Candidate evaluation:** Compare each parsed resume with the parsed
    job description and produce an overall match score with supporting
    textual details.
-   **Batch processing:** Process supported resume files placed in the
    local `resumes/` directory.

## Technology Stack

  Technology              Purpose
  ----------------------- --------------------------------------------------
  Python 3.14             Application logic
  Groq API                LLM inference
  `openai/gpt-oss-120b`   Configured LLM model
  Pydantic                Structured data models and validation
  `pypdf`                 PDF text extraction
  `python-docx`           DOCX text extraction
  `python-dotenv`         Load the Groq API key from environment variables
  `uv`                    Python dependency and environment management

## How It Works

``` text
                 Multiline Job Description
                           |
                           v
                 Groq LLM - JD Extraction
                           |
                           v
                 Structured JobD Model

Resume Files                |
(PDF / DOCX)                |
     |                      |
     v                      |
Text Extraction             |
(pypdf / python-docx)       |
     |                      |
     v                      |
Resume Text                 |
     |                      |
     v                      |
Groq LLM - Resume Parsing   |
     |                      |
     v                      |
Structured Resume Model    |
     |                      |
     +----------+-----------+
                |
                v
       Candidate Evaluation
                |
                v
      MatchScore (Pydantic)
                |
                v
       Score and Details
```

### Processing steps

1.  **Job description input:** Paste the complete job description into
    the terminal and enter `END` on a separate line to finish the input.
2.  **Job description parsing:** `parse_job_description()` sends the
    text to the configured Groq model. The response is parsed into the
    `JobD` Pydantic model.
3.  **Resume text extraction:** The application scans the `resumes/`
    directory and extracts text from supported `.pdf` and `.docx` files.
4.  **Resume parsing:** The extracted text is sent to the LLM and
    converted into a `Resume` Pydantic model.
5.  **Candidate evaluation:** The parsed job description and resume are
    passed to the evaluation function. The LLM returns a match score and
    supporting details, which are validated using the `MatchScore`
    model.
6.  **Batch output:** The application prints each candidate's score and
    details, then displays candidate summaries from the collected
    results.

## Project Structure

``` text
resume-parser/
│
├── app/
│   ├── __init__.py
│   ├── client.py              # Groq client and model configuration
│   ├── final_score.py         # Resume-to-job-description evaluation
│   ├── job_description.py     # Dynamic JD parsing and JobD schema
│   ├── main.py                # CLI workflow and batch processing
│   ├── resume_collect.py      # PDF and DOCX text extraction
│   ├── resume_parse.py        # LLM-based resume parsing
│   └── resume_structure.py    # Resume and match-score Pydantic models
│
├── resumes/                   # Local input resumes (not committed)
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

## Getting Started

### Prerequisites

-   Python 3.14
-   [`uv`](https://docs.astral.sh/uv/)
-   A Groq API key

### 1. Clone the repository

``` bash
git clone https://github.com/aroy-data001/resume-parser.git
cd resume-parser
```

### 2. Install dependencies

``` bash
uv sync
```

This creates or synchronizes the project virtual environment using the
dependencies declared in `pyproject.toml` and the lock file.

### 3. Configure the API key

Create a file named `.env` in the project root:

``` env
groq_api_key=your_groq_api_key_here
```

The application loads this variable in `app/client.py`.

Keep the `.env` file private. Do not commit your real API key to GitHub.

### 4. Add resume files

Place the resumes you want to evaluate inside the `resumes/` directory.

Supported formats:

-   `.pdf`
-   `.docx`

The repository's `.gitignore` excludes resume documents and files inside
`resumes/` so that personal candidate data is not accidentally
committed.

### 5. Run the application

From the repository root:

``` bash
uv run python -m app.main
```

### 6. Enter a job description

Paste the complete job description into the terminal. It can span
multiple lines.

When you have finished pasting, enter:

``` text
END
```

on a separate line and press Enter.

The application then parses the job description, processes the supported
resumes in `resumes/`, and prints the evaluation score and details for
each candidate.

## Data Models

The application currently uses Pydantic models to define the structure
of LLM outputs.

### Job description

The `JobD` model contains:

-   `role`
-   `required_skills`
-   `preferred_skills`
-   `minimum_education`
-   `minimum_experience`
-   `responsibilities`

### Resume

The `Resume` model contains:

-   `name`
-   `email`
-   `phone`
-   `total_education`
-   `total_experience`
-   `total_skills`
-   `total_duration`

Each experience entry includes fields for company, role, skills,
duration, and responsibility.

### Match evaluation

The `MatchScore` model currently contains:

-   `score`
-   `details`

The evaluation prompt asks the LLM to consider matching skills, missing
skills, experience requirements, and an overall verdict. These
explanations are currently represented through the `details` list rather
than separate typed fields.

## Current Scope and Limitations

This section describes the implementation as it exists today.

-   **Command-line application:** There is no web interface or HTTP API
    in the current repository.
-   **Local folder input:** Resume files are read from the `resumes/`
    directory; browser-based uploads are not available yet.
-   **Text-based PDF extraction:** The current PDF extraction uses
    `pypdf`. Scanned/image-only PDFs may not produce usable text because
    OCR is not implemented.
-   **LLM-dependent extraction and evaluation:** Results depend on the
    model response and may vary. Review extracted information and scores
    rather than treating them as definitive.
-   **Basic evaluation schema:** The current match result has an integer
    score and a list of textual details. Matching skills, missing
    skills, experience checks, and verdicts are not yet represented as
    dedicated Pydantic fields.
-   **No persistent candidate database:** Results are printed by the
    command-line workflow; there is no database or candidate history.
-   **No automated test suite documented yet:** Add tests for
    extraction, parsing, evaluation, and failure cases as the project
    evolves.
-   **No production deployment:** Authentication, API security, upload
    limits, monitoring, and deployment configuration are not part of the
    current implementation.

## Planned Improvements

The following items are planned and should not be considered implemented
features:

-   Build a FastAPI backend to expose resume parsing and evaluation
    through HTTP endpoints.
-   Build a React frontend for job description entry and resume uploads.
-   Support multiple resume uploads through the interface.
-   Improve the evaluation schema with explicit matched skills, missing
    skills, experience checks, and a candidate verdict.
-   Sort candidates reliably by match score and add candidate comparison
    views.
-   Add robust handling for malformed files, empty extraction results,
    and API failures.
-   Add automated tests and improve logging.
-   Add deployment and production-readiness features.

## Security and Data Handling

-   Store the Groq API key in `.env`; never hardcode or commit it.
-   Keep real resumes out of version control. Use synthetic or consented
    sample documents when sharing demonstrations.
-   Resume text is sent to the configured Groq API for parsing and
    evaluation. Do not process sensitive documents unless you are
    comfortable with the data handling of the configured API provider.
-   The current project does not provide authentication, access control,
    or a persistent secure file store.

## License

No license has been added to this repository yet. Until a license is
selected and committed, reuse and redistribution permissions are not
explicitly granted.
