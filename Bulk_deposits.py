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

    # ==================================================
    # SECTION HEADING
    # ==================================================

    section_text = page.locator(
        "#note"
    ).first.inner_text().strip()

    print("\nSECTION:")
    print(section_text)

    # ==================================================
    # EFFECTIVE DATE
    # ==================================================

    effective_date = ""

    match = re.search(
        r'(\d{2}\.\d{2}\.\d{4})',
        section_text
    )

    if match:

        effective_date = match.group(1)

    print(
        f"\nEffective Date: {effective_date}"
    )

    # ==================================================
    # TABLE
    # ==================================================

    table = page.locator(
        "#note"
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

        if len(cols) < 4:
            continue

        all_data.append({

            "Section":
                section_text,

            "Effective Date":
                effective_date,
                
            "Deposit period":
                cols[1].inner_text().strip(),

            "Single Term Deposit Rs. 3 Cr and above and upto & including Rs. 10.00 Cr - Rate of Interest":
                cols[2].inner_text().strip(),

            "Single Non-Callable Bulk Term Deposit Rs. 3 Cr & above upto and including Rs. 10.00 Cr - Rate of Interest":
                cols[3].inner_text().strip()

        })

    browser.close()

# ==================================================
# EXPORT
# ==================================================

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
    f"Bulk_Deposits_{today}.xlsx"
)

df.to_excel(
    output_file,
    index=False
)

print(
    f"\nExcel Saved Successfully: {output_file}"
)