import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email account credentials
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"  # Use an app password for Gmail

# Email details
recipients = ["recipient1@example.com", "recipient2@example.com"]
subject = "Test Email"
body = "This is a test email sent from Python."

# Create the email
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = ", ".join(recipients)
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

try:
    # Connect to Gmail SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipients, msg.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")