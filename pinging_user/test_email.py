import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, datetime

sender_email = "projektflask@gmail.com"
receiver_email = "pawelbaluszynski16@gmail.com"
# password = input("Type your password and press enter:")

message = MIMEMultipart("alternative")
message["Subject"] = f"WEATHER-mistyfikacja - informacja {date.today()} godzina: {datetime.now().hour}"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message

html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>
"""

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(MIMEText(html, "html"))

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, "Rokoko123!@")
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )