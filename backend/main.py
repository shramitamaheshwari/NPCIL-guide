from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv

import fitz
import requests
import os
import re

load_dotenv()

# =========================
# GEMINI
# =========================

client = genai.Client(
    api_key=os.getenv("API_KEY")
)

# =========================
# FASTAPI
# =========================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# REQUEST MODEL
# =========================

class ChatRequest(BaseModel):
    message: str


# =========================
# PDF PARSER
# =========================

from datetime import datetime

def extract_pdf_details(pdf_url):

    try:
        response = requests.get(pdf_url, timeout=30)
        pdf_bytes = response.content

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        text = ""

        for page in doc[:3]:
            text += page.get_text()

        doc.close()

        text = re.sub(r"\s+", " ", text)

        # -------------------------
        # Better Title Extraction
        # -------------------------

        title = "NPCIL Recruitment"

        patterns = [
            r"Advertisement No.*?(?=NPCIL|$)",
            r"Recruitment.*?(?=Advertisement|$)",
            r"Executive Trainees.*?(?=Advertisement|$)",
            r"Trade Apprentices.*?(?=Advertisement|$)",
            r"Assistant Grade.*?(?=Advertisement|$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)

            if match:
                title = match.group(0).strip()
                break

        # fallback
        if title == "NPCIL Recruitment":

            lines = text.split(" ")

            title = " ".join(lines[:12])

        # -------------------------
        # Dates
        # -------------------------

        dates = re.findall(
            r"\d{2}[./-]\d{2}[./-]\d{4}",
            text
        )

        start_date = dates[0] if len(dates) > 0 else "N/A"
        last_date = dates[-1] if len(dates) > 1 else "N/A"

        # -------------------------
        # Status
        # -------------------------

        status = "Unknown"

        try:

            parsed = datetime.strptime(
                last_date.replace(".", "/").replace("-", "/"),
                "%d/%m/%Y"
            )

            status = (
                "Open"
                if parsed >= datetime.now()
                else "Closed"
            )

        except:
            pass

        # -------------------------
        # Vacancies
        # -------------------------

        vacancies = "Not Available"

        vacancy_patterns = [
            r"Total Vacancies\s*[:\-]?\s*(\d+)",
            r"Number of Posts\s*[:\-]?\s*(\d+)",
            r"Vacancies\s*[:\-]?\s*(\d+)"
        ]

        for pattern in vacancy_patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                vacancies = match.group(1)
                break

        # -------------------------
        # Eligibility
        # -------------------------

        eligibility = "Check Advertisement PDF"

        patterns = [
            r"Educational Qualification(.*?)(Age Limit)",
            r"Eligibility Criteria(.*?)(Selection Process)",
            r"Qualification(.*?)(Experience)"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                eligibility = (
                    match.group(1)
                    .strip()
                    .replace("\n", " ")
                )[:300]

                break

        return {
            "title": title,
            "start_date": start_date,
            "last_date": last_date,
            "status": status,
            "vacancies": vacancies,
            "eligibility": eligibility
        }

    except Exception as e:

        return {
            "title": "NPCIL Recruitment",
            "start_date": "N/A",
            "last_date": "N/A",
            "status": "Unknown",
            "vacancies": "N/A",
            "eligibility": "N/A",
            "error": str(e)
        }

# =========================
# SCRAPER
# =========================

def get_jobs():

    session = requests.Session()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/149.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9"
    }

    session.get(
        "https://www.npcilcareers.co.in/MainSiten/default.aspx",
        headers=headers,
        timeout=30
    )

    response = session.get(
        "https://www.npcilcareers.co.in/MainSiten/DefaultInfo.aspx",
        headers={
            **headers,
            "Referer":
                "https://www.npcilcareers.co.in/MainSiten/default.aspx"
        },
        timeout=30
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    jobs = []

    base_url = (
        "https://www.npcilcareers.co.in/MainSiten/"
    )

    links = soup.find_all("a")

    for i, link in enumerate(links):

        href = link.get("href")

        if not href:
            continue

        if "documents/advt.pdf" in href.lower():

            advertisement_link = urljoin(
                base_url,
                href
            )

            try:
                job_code = href.split("/")[1]
            except:
                job_code = "NPCIL"

            apply_link = None

            for j in range(
                i + 1,
                min(i + 4, len(links))
            ):

                next_href = links[j].get("href")

                if (
                    next_href
                    and "candidate"
                    in next_href.lower()
                ):

                    apply_link = urljoin(
                        base_url,
                        next_href
                    )

                    break

            pdf_data = extract_pdf_details(
                advertisement_link
            )

            jobs.append({
                "job_code": job_code,
                "title": pdf_data["title"],
                "status": pdf_data["status"],
                "start_date": pdf_data["start_date"],
                "last_date": pdf_data["last_date"],
                "vacancies": pdf_data["vacancies"],
                "eligibility": pdf_data["eligibility"],
                "advertisement": advertisement_link,
                "apply_link": apply_link
            })

    print(f"Jobs Found: {len(jobs)}")

    return jobs


# =========================
# ROUTES
# =========================

@app.get("/")
def root():
    return {
        "message":
            "NPCIL Career Assistant Running"
    }


@app.get("/jobs")
def jobs():
    return get_jobs()


@app.post("/chat")
def chat(request: ChatRequest):

    jobs = get_jobs()

    if not jobs:

        return {
            "response":
                "No recruitment data found."
        }

    context = ""

    for job in jobs:

        context += f"""
Job Title: {job['title']}
Job Code: {job['job_code']}
Status: {job['status']}
Start Date: {job['start_date']}
Last Date: {job['last_date']}   
Vacancies: {job['vacancies']}
Eligibility: {job['eligibility']}
Advertisement: {job['advertisement']}
Apply Link: {job['apply_link']}
"""

    prompt = f"""
You are an NPCIL Career Assistant.

Answer ONLY from the provided
recruitment information.

Recruitment Data:
{context}

User Question:
{request.message}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return {
            "response": response.text
        }

    except Exception as e:

        return {
            "response": str(e)
        }


# =========================
# RUN
# =========================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )