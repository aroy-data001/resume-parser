# Resume Parser & Job Match Evaluator

A Python-based resume parsing and job matching project that uses an LLM to extract structured information from resumes and compare candidates against a job description.

## Features

- Extract text from PDF and DOCX resumes.
- Parse resume information into structured Pydantic models.
- Extract structured requirements from a job description using an LLM.
- Compare parsed resumes with the parsed job description and generate a match score with supporting details.
- Process multiple resumes from a local folder.

## Tech Stack

- Python 3.14
- Groq API (`openai/gpt-oss-120b`)
- Pydantic
- `pypdf`
- `python-docx`
- `python-dotenv`
- `uv` for dependency and environment management

## Project Structure

```text
resume-parser/
├── app/
│   ├── __init__.py
│   ├── client.py              # Groq client and model configuration
│   ├── final_score.py         # Resume vs. job-description scoring
│   ├── job_description.py     # Job-description extraction and schema
│   ├── main.py                # Batch-processing entry point
│   ├── resume_collect.py      # PDF/DOCX text extraction
│   ├── resume_parse.py        # LLM-based resume parsing
│   └── resume_structure.py    # Pydantic data models
├── resumes/                   # Local resumes to process (not committed)
├── .env                       # API key (not committed)
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

## How It Works

1. **Job description extraction:** The job description currently defined in `app/job_description.py` is sent to the LLM and converted into structured data.
2. **Resume text extraction:** PDF files are processed with `pypdf`; DOCX files are processed with `python-docx`.
3. **Resume parsing:** Extracted text is sent to the LLM and mapped to the Pydantic resume model.
4. **Candidate evaluation:** The parsed resume is compared with the structured job description. The LLM returns a score and supporting details.
5. **Batch processing:** The application iterates through supported files in the local `resumes/` folder and prints evaluation results.

## Setup

### Prerequisites

- Python 3.14
- [uv](https://docs.astral.sh/uv/) installed
- A Groq API key

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd resume-parser
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure the API key

Create a `.env` file in the project root:


```env
groq_api_key=your_groq_api_key_here
```

Keep your real API key private. Do not commit `.env`.


### 4. Add resumes

Place PDF or DOCX files in the `resumes/` folder. Resume files are ignored by Git to help prevent accidental publication of personal data.

### 5. Run the application

From the project root:


```bash
uv run python -m app.main
```

The program processes each supported resume in `resumes/` and prints its match score and evaluation details.

## Current Limitations

- The job description is currently defined in the source code rather than entered through a UI or command-line interface.
- Processing is local and folder-based; there is no web interface or API yet.
- Evaluation output is currently a score and supporting details, rather than a fully detailed candidate report.
- LLM results may vary between runs and should be reviewed rather than treated as a definitive hiring decision.
- Scanned/image-based PDFs may not yield extractable text with the current extraction pipeline.

## Future Improvements

- Accept job descriptions through a file, CLI, or web interface.
- Improve structured scoring output with explicit matched skills, missing skills, experience checks, and verdict fields.
- Add robust handling for malformed documents and API failures so one file does not stop a batch.
- Add candidate ranking and exportable reports.
- Add automated tests for extraction, parsing, and scoring.
- Build a web interface and deploy the application.

## License

Choose and add a license before publishing if you want others to reuse the project. No license is currently specified.
