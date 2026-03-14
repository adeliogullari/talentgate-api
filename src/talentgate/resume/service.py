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


def parse(file: bytes) -> str | None:
    contents = convert(file)
    contents = clean(contents)

    job_description = """

    About us

    Are you looking for an exciting opportunity to join a fast-growing fintech company that is revolutionizing the payment industry? Do you want to work with cutting-edge technologies and a talented team of professionals? If yes, then Wallester AS might be the perfect place for you!
    Wallester AS is an Estonian licensed payment service provider that develops financial digital technology and issues VISA cards. Since 2018, we have been an official Visa partner and Visa FinTech Fast Track Member issuing physical and virtual cards of any type: debit cards, credit cards, prepaid cards, and cards for business. Our distinctive advantage is a unique REST API created by our in-house development team. Easily integrated with any platform, it allows you to launch your card program in no time!
    We are looking for passionate and driven individuals who share our vision of creating truly high-quality and profitable products for our clients.


    About the role

    As the QA Team Lead at Wallester, you will guide and manage a team of QA engineers, ensuring the consistent delivery of high-quality software. Your role involves planning, organizing, and supervising the entire quality assurance process to meet deadlines and uphold standards. You will work closely with cross-functional teams and stakeholders to achieve key QA objectives and performance metrics.
    In addition, you’ll play a crucial role in shaping the team’s practices—whether by introducing new procedures, refining workflows, developing training initiatives, updating role definitions, or setting measurable performance goals.
    If you're passionate about fintech and payment technologies, excel in quality assurance, and thrive in a dynamic, fast-paced environment, we invite you to bring your expertise to our team.


    Location

    We are seeking QA Team Lead specialists to join Wallester’s headquarters in Tallinn (Golden Gate, Rotermanni Quarter) and our Latvian office in Riga (Jupiter Tower).


    Technology stack

    Python
    pytest
    Appium
    Postman/Apidog
    TestRail
    JSON REST API
    PostgreSQL
    AWS infrastructure
    Microservice Architecture
    …but don’t worry we don’t expect you to know everything!


    What will you do?

    Directly manage and lead QA team members.
    Assign tasks and projects based on team skills and capacity.
    Mentor and guide Junior, Mid-level, and Senior QA engineers.
    Ensure deadlines are met and deliverables maintain high quality.
    Develop and oversee detailed test plans and test cases.
    Manage and monitor execution of test cases (manual and automated).
    Oversee bug lifecycle management and defect triage.
    Ensure testing coverage for all scenarios and use cases.
    Implement, enforce, and improve QA processes and standards.
    Maintain and update test documentation.
    Manage and maintain QA tools and platforms.
    Train team members on QA tools and practices.
    Identify training needs and upskilling opportunities.
    Track and report on QA metrics (coverage, defect rates, automation progress, etc.).
    Lead continuous improvement initiatives for QA processes.
    Represent QA in cross-functional and project-level discussions.
    Advocate for QA needs and resources across the organization.
    Collaborate with development, product, and business stakeholders to integrate quality throughout the SDLC.
    Participate in agile ceremonies (planning, retrospectives, reviews).
    Stay up-to-date with testing methodologies, tools, and industry standards.


    What you'll need

    5+ years of experience in QA, with focus on software testing.
    1+ years of proven experience in team leadership or management.
    Strong understanding of QA best practices, processes, and methodologies.
    Hands-on experience with a variety of QA tools and platforms.
    Excellent communication, organizational, and interpersonal skills.Ability to manage deadlines and deliver high-quality outcomes.
    Capable of working independently while fostering team collaboration.


     We offer

    Competitive salary
    Development and career opportunities
    Medical Insurance upon the completion of the probationary period
    Supportive and caring Leadership
    A modern office in the center of Tallinn
    A chance to work as part of a highly motivated and talented team
    Referral program
    Team building and Company Events
    Free parking

    """

    prompt = f"""
    Return ONLY valid JSON.
    Do not include explanations outside JSON.
    If a field is missing, return null.
    Do NOT invent, assume, or hallucinate information.

    You are evaluating the resume AGAINST the provided Job Description.

    Format:
    {{
      "summary": string | null,

      "education": {{
          "institution": string | null,
          "degree": string | null,
          "field_of_study": string | null,
          "start_date": string | null,
          "end_date": string | null
      }},
      "experiences": [
        {{
          "company": string | null,
          "title": string | null,
          "description": string | null,
          "skills": string | null,
          "start_date": string | null,
          "end_date": string | null,
        }}
      ],

      "evaluation": {{
        "education": {{
          "score": number,
        }},
        "experience": {{
          "score": number,
        }},
        "skills": {{
          "score": number,
        }},
        "overall_score": number
      }}
    }}

    -----------------------------------
    Strict Skill Extraction Rules:
    - Include only skills that are explicitly stated or clearly demonstrated through specific actions or tasks.
    - Do NOT add generic soft skills unless they are explicitly mentioned.
    - Do NOT assume familiarity with tools, technologies, or methodologies unless directly referenced.
    - Select up to 3 of the most relevant and clearly supported skills.

    -----------------------------------
    Evaluation Rules (Against Job Description):

    Score each category from 0 to 10.

    Weights:
    - experience: 0.60
    - skills: 0.30
    - education: 0.10

    overall_score =
    (experience_relevance_to_job × 0.60) +
    (skills_match_to_job × 0.30) +
    (education_match × 0.10)

    Round overall_score to 1 decimal place.

    Scoring Guidelines:
    9-10 = extremely strong match, minimal gaps
    7-8  = strong match with minor gaps
    5-6  = partial match, noticeable gaps
    3-4  = weak match
    0-2  = poor or irrelevant

    -----------------------------------

    Job Description:
    {job_description}

    Resume:
    {contents}
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=GenerateContentConfig(
            response_mime_type="application/json", temperature=0.0, thinking_config=ThinkingConfig(thinking_budget=-1)
        ),
    )

    return response.text
