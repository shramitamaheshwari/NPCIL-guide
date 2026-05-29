from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/jobs")
def get_jobs():

    url = "https://npcilcareers.co.in/MainSiten/DefaultInfo.aspx"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    base_url = "https://npcilcareers.co.in/MainSiten/"

    rows = soup.find_all("tr")

    for row in rows:

        text = row.get_text(" ", strip=True)

        links = row.find_all("a")

        if len(text) > 50 and links:

            first_link = links[0]

            href = first_link.get("href")

            if href:

                full_link = urljoin(base_url, href)

                # Clean title
                clean_title = text.split("(Advt)")[0].strip()

                # Extract dates
                dates = re.findall(r'\d{2}/\d{2}/\d{4}', text)

                start_date = dates[0] if len(dates) >= 1 else "N/A"
                last_date = dates[1] if len(dates) >= 2 else "N/A"

                status = "Open"

                try:

                    last_date_obj = datetime.strptime(last_date, "%d/%m/%Y")

                    current_date = datetime.now()

                    if current_date > last_date_obj:
                        status = "Closed"

                except:
                    status = "Unknown"

                jobs.append({
                    "title": clean_title,
                    "start_date": start_date,
                    "last_date": last_date,
                    "status": status,
                    "link": full_link
                })

    return jobs