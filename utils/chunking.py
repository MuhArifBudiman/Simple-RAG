import re
import os
import json
from typing import Dict, List


HEADINGS = {
    "about me": ["about me", "summary", "profile"],
    "experience": ["experience", "work experience", "professional experience"],
    "education": ["education", "academic background"],
    "training and certification": ["training", "certification", "certifications", "courses", "training and certification"],
    "skills": ["skills", "technical skills", "tools"],
    "languages": ["languages", "language"]
}


def detect_heading(line: str) -> str:
    line_clean = line.lower().strip(":")
    for section, aliases in HEADINGS.items():
        if line_clean in aliases:
            return section
    return None


def chunk(text: str) -> List:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    chunks = {}
    current_section = None

    for line in lines:
        detected = detect_heading(line)
        if detected:
            current_section = detected
            chunks[current_section] = []
            continue
        if current_section:
            chunks[current_section].append(line)

    raw_chunk = {section: "\n".join(value)
                 for section, value in chunks.items()}

    chunk_result = [{
        "section": section,
        "text": "".join(value)
    }
        for section, value in raw_chunk.items()]
    return chunk_result
