import re
from io import BytesIO

import requests
from minio import Minio

minio_client = Minio(
    endpoint="localhost:9000",
    access_key="admin",
    secret_key="password",
    secure=False,
)

bucket = "talentgate"
object_name = "docs/AbdullahDeliogullariCV.pdf"

# Download file from MinIO
obj = minio_client.get_object(bucket, object_name)
file_bytes = obj.read()
obj.close()
obj.release_conn()

DOCLING_ENDPOINT = "http://localhost:5001/v1/convert/file"

files = {
    "files": (
        "example.pdf",
        BytesIO(file_bytes),
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

response = requests.post(DOCLING_ENDPOINT, files=files, data=data, timeout=300)

result = response.json()
markdown = result["document"]["md_content"]

markdown = re.sub(r"<!--\s*image\s*-->", "", markdown)

lines = markdown.splitlines()
deduped = []

for i, line in enumerate(lines):
    if i > 0 and line.startswith("## ") and lines[i - 1].startswith("## "):
        deduped.append(line.replace("## ", "**") + "**")
    else:
        deduped.append(line)

markdown = "\n".join(deduped)

markdown = markdown.replace(" ·", "")
markdown = re.sub(r"\s*·\s*", "", markdown)

clean_lines = []
for line in markdown.splitlines():
    stripped = line.strip()
    if stripped and all(not c.isalnum() for c in stripped):
        continue
    clean_lines.append(line)
markdown = "\n".join(clean_lines)

markdown = re.sub(r"[ ]{2,}", " ", markdown)
markdown = re.sub(r"(?m)^\s{2,}", "", markdown)

print(markdown)

