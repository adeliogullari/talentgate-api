import re
from typing import TypedDict, List

import requests
from io import BytesIO
from google import genai
from google.genai.types import GenerateContentConfig

from config import get_settings
from src.talentgate.resume.models import Resume

settings = get_settings()

docling_schema = settings.docling_schema
docling_host = settings.docling_host
docling_port = settings.docling_port
docling_endpoint = f"${docling_schema}://${docling_host}:${docling_port}"

client = genai.Client(api_key=settings.gemini_api_key)

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Explain how AI works in a few words",
    config=GenerateContentConfig(response_mime_type="application/json", response_schema=Resume),
)

print(response.parsed)


def convert(file: bytes):
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
        "abort_on_error": "false",
    }

    headers = {
        "Authorization": f"Bearer {settings.docling_api_key}",
    }

    response = requests.post(
        f"${docling_endpoint}/v1/convert/file", files=files, data=data, headers=headers, timeout=30000
    )

    return response.json()


def parse() -> Resume:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents="Explain how AI works in a few words",
        config=GenerateContentConfig(response_mime_type="application/json", response_schema=Resume),
    )

    return response.parsed


def evaluate():

    pass


DOCLING_ENDPOINT = "http://localhost:5001/v1/convert/file"

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
    "abort_on_error": "false",
}

response = requests.post("http://localhost:5001/v1/convert/file", files=files, data=data, timeout=300)

result = response.json()
markdown = result["document"]["md_content"]

markdown = re.sub(r"<!--\s*image\s*-->", "", markdown)
