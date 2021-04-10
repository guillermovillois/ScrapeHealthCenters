import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import json

with open("cosas.json") as f:
    data = json.load(f)


def send_email(file):
    sender_email = data['sender_email']
    sender_name = data['sender_name']

    receiver_email = data['receiver_email']
    receiver_name = data['receiver_name']

    filename = file

    email_body = """
    <h1> Hi, today's document is attached </h1>"""

    print("Sending the email....")

    # msg = MIMEText(email_body, 'html')
    msg = MIMEMultipart()
    msg["To"] = formataddr((receiver_name, receiver_email))
    msg["From"] = formataddr((sender_name, sender_email))
    msg["Subject"] = "Document" + receiver_name

    msg.attach(MIMEText(email_body, "html"))

    # In[13]:

    try:
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename={filename}",
        )
        msg.attach(part)
    except Exception as e:
        print(f"oh no we didint fioudn the attahcemnt{e}")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        context = ssl.create_default_context()
        server.starttls(context=context)
        server.login(sender_email, data["pica"])
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent")
    except Exception as e:
        print(f"Oh no! Something bad happened!\n{e}")
    finally:
        print("Closing the server...")
        server.quit()
