import smtplib

smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.starttls()

smtp.login(
    "webscraperpython6@gmail.com",
    "ykegeilhqlpjwkka"
)

print("Login Successful")

smtp.quit()