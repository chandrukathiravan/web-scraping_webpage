from playwright.sync_api import sync_playwright
import pandas as pd
import re
from datetime import datetime
import os

URL = "https://www.uco.bank.in/web/guest/interest-rates-on-deposit-schemes"

data = []

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(
        URL,
        wait_until="domcontentloaded",
        timeout=300000
    )

    page.wait_for_timeout(10000)

    heading_locator = page.locator(
        "h4"
    ).filter(
        has_text="Rate(s) of interest on Domestic Term Deposits less than Rs.3 Crore"
    )

    heading = heading_locator.first.inner_text().strip()

    date_match = re.search(
        r'(\d+\.\d+\.\d+)',
        heading
    )

    effective_date = ""

    if date_match:
        effective_date = date_match.group(1)

    note = page.locator(
        "text=444 Day Special Scheme"
    ).first.inner_text().strip()

    table = heading_locator.locator(
        "xpath=following::table[1]"
    )

    rows = table.locator("tbody tr").all()

    for row in rows:

        cols = row.locator("td").all()

        if len(cols) >= 3:

            data.append({

                "Section":
                    "Domestic Schemes",

                "Heading":
                    heading,

                "Effective Date":
                    effective_date,

                "Maturity Period":
                    cols[0].inner_text().strip(),

                "Rate % p.a.":
                    cols[1].inner_text().strip(),

                "Yield %":
                    cols[2].inner_text().strip(),

                "Notes":
                    note

            })

    browser.close()

df = pd.DataFrame(data)

today = datetime.now().strftime("%d%m%Y")

output_folder = os.path.join(
    "Output",
    today
)

os.makedirs(
    output_folder,
    exist_ok=True
)

output_file = os.path.join(
    output_folder,
    f"ROI_less_than_3cr_{today}.xlsx"
)

df.to_excel(
    output_file,
    index=False
)

print(df)