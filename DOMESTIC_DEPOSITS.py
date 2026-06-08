from playwright.sync_api import sync_playwright
import pandas as pd
import re
from datetime import datetime
import os

URL = "https://www.uco.bank.in/web/guest/interest-rates-on-deposit-schemes"

all_data = []

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    print("Opening UCO Bank Page...")

    page.goto(
        URL,
        wait_until="domcontentloaded",
        timeout=300000
    )

    page.wait_for_timeout(10000)

    print("Page Title:")
    print(page.title())

    # ==================================
    # SECTION HEADINGS
    # ==================================

    section_name = ""

    try:

        section_name = page.locator(
            "h3"
        ).filter(
            has_text="Domestic Schemes"
        ).first.inner_text().strip()

    except:

        section_name = "Domestic Schemes"

    try:

        sub_section = page.locator(
            "h4"
        ).filter(
            has_text="DOMESTIC DEPOSITS"
        ).first.inner_text().strip()

    except:

        sub_section = "DOMESTIC DEPOSITS"

    try:

        heading = page.locator(
            "h4"
        ).filter(
            has_text="Savings Bank Rate of Interest"
        ).first.inner_text().strip()

    except:

        heading = ""

    print("\nSECTION :", section_name)
    print("SUBSECTION :", sub_section)
    print("HEADING :", heading)

    effective_date = ""

    m = re.search(
        r'(\d{2}-\d{2}-\d{4})',
        heading
    )

    if m:

        effective_date = m.group(1)

    # ==================================
    # TABLE
    # ==================================

    tables = page.locator("table")

    print(
        "\nTables Found:",
        tables.count()
    )

    table = tables.nth(0)

    rows = table.locator("tr").all()

    print(
        "Rows Found:",
        len(rows)
    )

    for row in rows[2:]:

        cols = row.locator("td").all()

        if len(cols) >= 4:

            existing_balance = cols[0].inner_text().strip()

            existing_roi = cols[1].inner_text().strip()

            revised_balance = cols[2].inner_text().strip()

            revised_roi = cols[3].inner_text().strip()

            all_data.append({

                "Section":
                    section_name,

                "Sub Section":
                    sub_section,

                "Heading":
                    heading,

                "Effective Date":
                    effective_date,

                "Existing Balance":
                    existing_balance,

                "Existing ROI":
                    existing_roi,

                "Revised Balance":
                    revised_balance,

                "Revised ROI":
                    revised_roi

            })

    browser.close()

# ==================================
# EXPORT
# ==================================

df = pd.DataFrame(all_data)

print("\nDATA EXTRACTED:")
print(df)


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
    f"Savings_Bank_Rates_{today}.xlsx"
)

df.to_excel(
    output_file,
    index=False
)

print(
    f"\nExcel Saved: {output_file}"
)