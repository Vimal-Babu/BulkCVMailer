import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Load your contact list from CSV
contacts = pd.read_csv('contacts.csv', header=None, names=['Email'])

#contacts = pd.read_csv('contacts.csv', names=['Email'])
#print(contacts, "Email is Going to Sent to This Mail Id ")

# Your email credentials
EMAIL_ADDRESS = "vimalbabu3609@gmail.com"
EMAIL_PASSWORD = "mibhmbdcbipglczo"

# Email setup
subject = "Application for Python Django Developer"
body_template = """

Hello,

I hope this message finds you well. I am excited to apply for the Python Django role. Please find my resume attached for your review.

I am a software developer skilled in building web applications using Python and Django, with PostgreSQL as my preferred database for creating scalable and reliable applications. I enjoy designing and implementing robust solutions while continuously expanding my knowledge in backend development.

Here are some of my highlighted projects:

GreateKart: An e-commerce website featuring a custom admin page, showcasing my expertise in designing user-friendly interfaces and robust backend functionalities.
Bulk-Email-Sent: A tool for sending bulk emails to recruiters or other recipients. By simply pasting email IDs into a CSV file, users can quickly and efficiently send emails with consistent content.
Car-For-All: A project focused on brushing up my Django skills. It explores class-based views and includes advanced filtering features.
Expense Calculator: A personal project to track expenses, currently under development. I aim to integrate React Native for a seamless mobile experience.
All project code is hosted on my GitHub profile, with demos and highlights available on my LinkedIn and portfolio.

I am confident that my technical expertise, coupled with my experience in Python, Django, and PostgreSQL, makes me a strong candidate for this role. I would love the opportunity to discuss how I can contribute to Our Company.

Thank you for your time and for reviewing my profile.

Sincerely,
Vimal Babu
+91 9567250335
GitHub: https://github.com/Vimal-Babu
LinkedIn: https://www.linkedin.com/in/vimalbabu369/
Portfolio: https://vimal-babu.github.io/Personal/#
"""

# Connect to the SMTP server
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    for _, row in contacts.iterrows():
        email_address = row['Email']  # Fetch email from the row
        print(f"Sending email to: {email_address}")  # Debugging line
        
        # Set up email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email_address
        msg['Subject'] = subject

        # Attach the text and PDF files
        msg.attach(MIMEText(body_template, 'plain'))

        # Attach resume
        with open("VimalPython Resume.pdf", "rb") as f:
            resume = MIMEApplication(f.read(), _subtype="pdf")
            resume.add_header('Content-Disposition', 'attachment', filename="resume.pdf")
            msg.attach(resume)

        # Send the email
        server.send_message(msg)
        print(f"Succes!!!... Email sent to {email_address}")

