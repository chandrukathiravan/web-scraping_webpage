import smtplib
import os

from email.message import EmailMessage
from datetime import datetime

# ==========================================
# CONFIGURATION
# ==========================================

EMAIL_ID = "webscraperpython6@gmail.com"

APP_PASSWORD = "ykegeilhqlpjwkka"

RECIPIENTS = [

    "chandru.k@uco.bank.in",

    "sayani.das@uco.bank.in"

]

# ==========================================
# DATE FOLDER
# ==========================================

today = datetime.now().strftime("%d%m%Y")

folder = os.path.join(
    "Output",
    today
)

print(
    f"\nLooking for files in:\n{folder}"
)

# ==========================================
# EMAIL
# ==========================================

msg = EmailMessage()

msg["Subject"] = (
    f"UCO Interest Rate Reports - {today}"
)

msg["From"] = EMAIL_ID

msg["To"] = ",".join(
    RECIPIENTS
)

msg.set_content(
    f"""
Dear Team,

Please find attached the latest UCO Bank Interest Rate reports.

Reports Included:

1. Savings Bank Rates
2. Domestic Term Deposits
3. Additional Interest
4. UCO Green Deposit Scheme
5. Bulk Term Deposits (Rs.3 Cr to Rs.10 Cr)

Generated Date:
{today}

Regards,
Automated Web Scraper
"""
)

# ==========================================
# ATTACH ALL EXCEL FILES
# ==========================================

attached_count = 0

for file in os.listdir(folder):

    if file.endswith(".xlsx"):

        file_path = os.path.join(
            folder,
            file
        )

        print(
            f"Attaching: {file}"
        )

        with open(
            file_path,
            "rb"
        ) as f:

            msg.add_attachment(

                f.read(),

                maintype="application",

                subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                filename=file

            )

        attached_count += 1

print(
    f"\nTotal Attachments: {attached_count}"
)

# ==========================================
# SEND EMAIL
# ==========================================

smtp = smtplib.SMTP(
    "smtp.gmail.com",
    587
)

smtp.starttls()

smtp.login(
    EMAIL_ID,
    APP_PASSWORD
)

smtp.send_message(
    msg
)

smtp.quit()

print(
    "\nEmail Sent Successfully"
)