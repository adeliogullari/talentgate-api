import re
from io import BytesIO
from typing import Any

import requests
from google import genai
from google.genai.types import GenerateContentConfig, ThinkingConfig

from config import get_settings

settings = get_settings()

schema = settings.docling_schema
host = settings.docling_host
port = settings.docling_port
url = f"{schema}://{host}:{port}/v1/convert/file"

client = genai.Client(api_key=settings.gemini_api_key)

CLEAN_PATTERNS = [
    (r"·(?=\s*$)", ""),
    (r"^\s*-\s*$", ""),
    (r"^\s*-\s+", "- "),
    (r"\n{3,}", "\n\n"),
    (r"\s+[a-zA-Z]\s*$", ""),
    (r"[\uE000-\uF8FF]", ""),
    (r"<!--\s*image\s*-->", ""),
]


def clean(contents: str) -> str:
    for pattern, repl in CLEAN_PATTERNS:
        contents = re.sub(pattern, repl, contents, flags=re.MULTILINE)

    return contents.strip()


def convert(file: bytes) -> Any:
    files = {
        "files": (
            "resume.pdf",
            BytesIO(file),
            "application/pdf",
        ),
    }

    data = {
        "to_formats": "md",
        "include_images": "false",
        "image_export_mode": "placeholder",
        "do_table_structure": "false",
        "do_ocr": "false",
        "force_ocr": "false",
        "md_page_break_placeholder": "",
        "extract_tables": "false",
        "abort_on_error": "true",
    }

    headers = {
        "Authorization": f"Bearer {settings.docling_api_key}",
    }

    response = requests.post(url=url, files=files, data=data, headers=headers)

    return response.json()["document"]["md_content"]


def parse(file: bytes, job_description: str) -> str | None:
    contents = convert(file)
    contents = clean(contents)

    prompt = f"""
    You are a structured data extraction and evaluation engine.

    Your task is to:
        - Extract structured information from the Resume.
        - Evaluate the candidate against the Job Description.

    CRITICAL RULES:
        - Return ONLY valid JSON.
        - If information is missing or unclear, return null.
        - Do NOT invent, assume, infer, or hallucinate information.
        - Use only information explicitly present in the Resume.

    -----------------------------------

    EVALUATION RULES:

    OVERVIEW:
        - Must be 1–2 short sentences.
        - Focus ONLY on job-critical strengths or gaps.

    -----------------------------------

    EDUCATION (weights):

    1. Degree relevance (0.60)
        - Alignment of degree with the job field.

    2. Education level (0.20)
        - Highest completed degree.

    3. Institution quality (0.10)
        - Reputation or recognition of the institution.

    4. Academic performance (0.10)
        - GPA, honors, distinctions, or awards.

    -----------------------------------

    EXPERIENCE (weights):

    1. Role relevance (0.50):
        - Total relevant experience
        - Alignment of titles and responsibilities.

    2. Skill alignment (0.50):
        - Match required and preferred skills.

    Important:
    - Use ONLY explicitly stated information from the resume.
    - Do NOT infer missing experience, skills, or impact.
    - If evidence is weak or unclear, reflect that in the score.

    -----------------------------------

    SCORING SCALE:

    9–10 = extremely strong match, minimal gaps
    7–8  = strong match with minor gaps
    5–6  = partial match, noticeable gaps
    3–4  = weak match
    0–2  = poor or irrelevant

    -----------------------------------

    WEIGHTED SCORES (round to 1 decimal):

    education_score =
        (degree_relevance × 0.60) +
        (education_level × 0.20) +
        (institution_quality × 0.10) +
        (academic_performance × 0.10)

    experience_score =
        (role_relevance × 0.50) +
        (skill_alignment × 0.50)

    overall_score =
        (education_score × 0.30) +
        (experience_score × 0.70)

    -----------------------------------

    JSON SCHEMA (STRICT):

    {{
      "applicant": {{
        "firstname": string | null,
        "lastname": string | null,
        "email": string | null,
        "phone": string | null,
        "address": {{
          "unit": string | null,
          "street": string | null,
          "city": string | null,
          "state": string | null,
          "country": string | null,
          "postal_code": string | null
        }},
        "links":[
          {{
            "type": "LINKEDIN" | "GITHUB" | "MEDIUM" | "OTHER" | null,
            "url": string | null
          }}
        ],
        "education": {{
          "institution": string | null,
          "degree": string | null,
          "field_of_study": string | null,
          "start_date": string | null,
          "end_date": string | null
        }},
        "experiences": [
          {{
            "title": string | null,
            "company": string | null,
            "description": string | null,
            "skills": string | null,
            "start_date": string | null,
            "end_date": string | null
          }}
        ]
      }},
      "summary": string | null,
      "evaluation": {{
        "education": {{
          "score": number | null
        }},
        "experience": {{
          "score": number | null
        }},
        "overview": string | null,
        "overall_score": number | null
      }}
    }}

    -----------------------------------

    JOB DESCRIPTION:
    {job_description}

    -----------------------------------

    RESUME:
    {contents}

    -----------------------------------

    Return ONLY the JSON result.
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=GenerateContentConfig(
            response_mime_type="application/json", temperature=0.0, thinking_config=ThinkingConfig(thinking_budget=-1)
        ),
    )

    return response.text
