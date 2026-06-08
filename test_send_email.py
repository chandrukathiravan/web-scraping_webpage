import smtplib
from email.message import EmailMessage

EMAIL_ID = "webscraperpython6@gmail.com"
APP_PASSWORD = "ykegeilhqlpjwkka"

msg = EmailMessage()

msg["Subject"] = "Test Mail"

msg["From"] = EMAIL_ID

msg["To"] = "chandru.k@uco.bank.in"

msg.set_content(
    "This is a test email from Python."
)

smtp = smtplib.SMTP("smtp.gmail.com", 587)

smtp.starttls()

smtp.login(
    EMAIL_ID,
    APP_PASSWORD
)

smtp.send_message(msg)

smtp.quit()

print("Email Sent Successfully")