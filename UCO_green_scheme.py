from playwright.sync_api import sync_playwright
import pandas as pd
import re
from datetime import datetime
import os

URL = "https://www.uco.bank.in/web/guest/interest-rates-on-deposit-schemes"

green_data = []
interest_data = []

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
    # GREEN DEPOSIT SECTION
    # ==================================================

    section_name = page.locator(
        "text=Rate of Interest for 'UCO Green Deposits'"
    ).first.inner_text().strip()

    scheme_name = page.locator(
        "h3"
    ).filter(
        has_text="UCO GREEN DEPOSIT SCHEME"
    ).first.inner_text().strip()

    green_table = page.locator(
        "h3"
    ).filter(
        has_text="UCO GREEN DEPOSIT SCHEME"
    ).locator(
        "xpath=following::table[1]"
    )

    green_rows = green_table.locator(
        "tr"
    ).all()

    common_rate = ""

    # ==================================================
    # EXTRACT NOTE FROM SECOND TABLE
    # ==================================================

    interest_heading = page.locator(
        "th"
    ).filter(
        has_text="Rate of Interest for Senior Citizen"
    ).first.inner_text().strip()

    interest_table = page.locator(
        "th"
    ).filter(
        has_text="Rate of Interest for Senior Citizen"
    ).locator(
        "xpath=ancestor::table"
    )

    note = ""

    temp_rows = interest_table.locator(
        "tbody tr"
    ).all()

    for row in temp_rows:

        cols = row.locator("td").all()

        # Note row has colspan=3
        if len(cols) == 1:

            note = cols[0].inner_text().strip()

            print("\nNOTE FOUND:")
            print(note)

            break

    # ==================================================
    # GREEN DEPOSIT DATA
    # ==================================================

    for idx, row in enumerate(green_rows):

        cols = row.locator("td").all()

        if idx == 0:
            continue

        if len(cols) == 3:

            tenor = cols[0].inner_text().strip()

            common_rate = cols[1].inner_text().strip()

            effective_roi = cols[2].inner_text().strip()

        elif len(cols) == 2:

            tenor = cols[0].inner_text().strip()

            effective_roi = cols[1].inner_text().strip()

        else:

            continue

        green_data.append({

            "Section":
                section_name,

            "Scheme":
                scheme_name,

            "Tenor":
                tenor,

            "Rate":
                common_rate,

            "Effective ROI":
                effective_roi,

            "Note":
                note

        })

    # ==================================================
    # ADDITIONAL INTEREST DATA
    # ==================================================

    interest_rows = interest_table.locator(
        "tbody tr"
    ).all()

    for row in interest_rows:

        cols = row.locator("td").all()

        # Skip note row
        if len(cols) != 3:
            continue

        interest_data.append({

            "Section":
                section_name,

            "Scheme Name":
                interest_heading,

            "Category":
                cols[0].inner_text().strip(),

            "Additional Interest Up to 1 Yr":
                cols[1].inner_text().strip(),

            "Additional Interest Above 1 Yr":
                cols[2].inner_text().strip()

        })

    browser.close()

# ==================================================
# EXPORT GREEN DEPOSIT EXCEL
# ==================================================

green_df = pd.DataFrame(green_data)

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
    f"UCO_GREEN_DEPOSIT_SCHEME_{today}.xlsx"
)

green_df.to_excel(
    output_file,
    index=False
)

print(
    f"\nSaved: {output_file}"
)

# ==================================================
# EXPORT ADDITIONAL INTEREST EXCEL
# ==================================================

interest_df = pd.DataFrame(interest_data)

output_file = os.path.join(
    output_folder,
    f"UCO_GREEN_DEPOSIT_ADDITIONAL_INTEREST_{today}.xlsx"
)

interest_df.to_excel(
    output_file,
    index=False
)

print(
    f"Saved: UCO_GREEN_DEPOSIT_ADDITIONAL_INTEREST_{today}.xlsx"
)

print("\nCompleted Successfully.")