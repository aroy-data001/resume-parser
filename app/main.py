from textwrap import indent
from pathlib import Path
import json
from app.job_description import parse_job_description
from app.resume_collect import resume
import time
from app.resume_parse import resumeParse
from app.final_score import final_score1

if __name__ == "__main__":
    print("Paste your job description below.")
    print("Type END on a separate line when finished.\n")

    jd_lines = []

    while True:
        line = input()

        if line.strip() == "END":
            break

        jd_lines.append(line)

    job_description = "\n".join(jd_lines)

    job_parsed = parse_job_description(job_description)

    print("\nJob Description Parsed Successfully!")
    print(job_parsed.model_dump_json(indent=2))

    resume_folder = Path("resumes")
    all_results = []
    for resume_path in resume_folder.iterdir():
        if resume_path.suffix.lower() not in [".pdf",".docx"]:
            continue
        print("\nProcessing:", resume_path.name)
        resume_text = resume(resume_path)
        parsed_resume = resumeParse(resume_text)
        time.sleep(5)

        refined_score = final_score1(job_parsed, parsed_resume)

        time.sleep(5)

        print("Score:", refined_score.score)
        print("Details:", json.dumps(refined_score.details, indent=2))
        all_results.append({
            "name": parsed_resume.name,
            "score": refined_score.score,
            "details": refined_score.details
        })
    top_2 = all_results[:2]
    worst_2 = all_results[-2:]


    print("TOP 2 CANDIDATES")
    for candidate in top_2:

        print(
            candidate["name"],
            "-",
            candidate["score"],
            "%"
        )

        print(candidate["details"])

    print("LOWEST 2 CANDIDATES")
    for candidate in worst_2:

        print(
            candidate["name"],
            "-",
            candidate["score"],
            "%"
        )
        print(candidate["details"])