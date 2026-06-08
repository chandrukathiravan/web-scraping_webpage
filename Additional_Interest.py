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

    print("Opening Page...")

    page.goto(
        URL,
        wait_until="domcontentloaded",
        timeout=300000
    )

    page.wait_for_timeout(10000)

    # ==========================================
    # EFFECTIVE DATE
    # ==========================================

    heading = page.locator(
        "h4"
    ).filter(
        has_text="Rate(s) of interest on Domestic Term Deposits less than Rs.3 Crore"
    ).first.inner_text().strip()

    print("\nHeading:")
    print(heading)

    effective_date = ""

    match = re.search(
        r'(\d+\.\d+\.\d+)',
        heading
    )

    if match:

        effective_date = match.group(1)

    print(
        f"\nEffective Date: {effective_date}"
    )

    # ==========================================
    # DESCRIPTION
    # ==========================================

    description = page.locator(
        "text=The Additional Interest payable on deposits"
    ).first.inner_text().strip()

    print("\nDescription:")
    print(description)

    # ==========================================
    # TABLE
    # ==========================================

    table = page.locator(
        "text=The Additional Interest payable on deposits"
    ).locator(
        "xpath=following::table[1]"
    )

    rows = table.locator(
        "tbody tr"
    ).all()

    print(
        f"\nRows Found: {len(rows)}"
    )

    for row in rows:

        cols = row.locator("td").all()

        if len(cols) == 2:

            category = cols[0].inner_text().strip()

            up_to_one_year = cols[1].inner_text().strip()

            above_one_year = cols[1].inner_text().strip()

        elif len(cols) >= 3:

            category = cols[0].inner_text().strip()

            up_to_one_year = cols[1].inner_text().strip()

            above_one_year = cols[2].inner_text().strip()

        else:

            continue

        all_data.append({

            "Section":
                "Additional Interest",

            "Effective Date":
                effective_date,

            "Description":
                description,

            "Category":
                category,

            "Tenor Up To One Year":
                up_to_one_year,

            "Tenor Above One Year":
                above_one_year

        })

    browser.close()

# ==========================================
# EXPORT
# ==========================================

df = pd.DataFrame(all_data)

print("\nData Extracted:")
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
    f"Additional_Interest_{today}.xlsx"
)


df.to_excel(
    output_file,
    index=False
)

print(
    f"\nExcel Saved Successfully: {output_file}"
)