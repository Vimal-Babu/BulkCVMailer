import smtplib
import pandas as pd
import os
import time
import logging
import json
from datetime import datetime
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

load_dotenv()

# ── Config ────────────────────────────────────────────────
EMAIL_ADDRESS  = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Use Gmail App Password (not account password)

RESUME_FILE    = "Vimal_Babu_Python_Django_Developer.pdf"
CONTACTS_FILE  = "contacts.csv"
LOG_FILE       = "send_log.json"
DELAY_SECONDS  = 5   # Wait between sends to avoid Gmail spam flags
MAX_RETRIES    = 2

# ── Logging ───────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers=[
        logging.FileHandler("mailer.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)
# ── Email content ─────────────────────────────────────────
SUBJECT = "Application for Python / Django Backend Developer Role"

PLAIN_TEXT = """\
Hello,

I hope you are doing well.

I am writing to express my interest in a Python / Django Backend Developer role at your organisation. Please find my resume attached for your review.

About me:
I am currently working as a Junior Python / Django Backend Developer (Intern) at Zecser Business LLP, where I contribute to developing and maintaining live production Django applications. I work with Python, Django, Django REST Framework, PostgreSQL, Git, and Postman to build backend features, fix production issues, and collaborate with the development team. Alongside my professional experience, I have built multiple end-to-end backend applications that demonstrate scalable API design and clean backend architecture.

Current work & recent projects:
• ZecPath             – Contributing to a production Django platform by developing backend features, implementing business logic, fixing bugs, and integrating database functionality.
• WinnersClubX        – Maintaining a live MLM platform through bug fixes, feature enhancements, and day-to-day backend maintenance.
• FieldOps Backend    – Production-grade Django REST Framework backend featuring JWT authentication, three-role RBAC, service request workflow, analytics APIs, and PostgreSQL.
• AutoSpeech2Text     – Flask + React application integrating OpenAI Whisper for speech-to-text processing with production deployment.

My GitHub showcases additional backend projects, including Barcode Scanner, Django Google Connect, GreatEKart, and other Django applications with documentation and live demos where applicable.

I would welcome the opportunity to discuss how I can contribute to your engineering team.

Thank you for your time and consideration.

Best regards,
Vimal Babu

📞 +91 9567250335
GitHub:    https://github.com/Vimal-Babu
LinkedIn:  https://www.linkedin.com/in/vimalpython3609
Portfolio: https://vimal-babu.github.io/portfolio
"""

HTML_BODY = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
body{
    font-family:'Segoe UI',Arial,sans-serif;
    font-size:15px;
    color:#222;
    line-height:1.7;
    margin:0;
    padding:0;
}

.wrap{
    max-width:600px;
    margin:32px auto;
    padding:0 24px;
}

h2{
    font-size:18px;
    font-weight:600;
    color:#1a1a1a;
    margin-bottom:8px;
}

ul{
    padding-left:20px;
}

li{
    margin-bottom:10px;
}

.proj{
    font-weight:600;
    color:#1a5276;
}

.badge{
    display:inline-block;
    background:#eaf3fb;
    color:#1a5276;
    border-radius:4px;
    padding:2px 8px;
    font-size:12px;
    margin-right:4px;
    margin-bottom:4px;
}

.links{
    margin-top:24px;
    padding-top:16px;
    border-top:1px solid #e5e5e5;
    font-size:13px;
    color:#555;
}

.links a{
    color:#1a5276;
    text-decoration:none;
}

.links a:hover{
    text-decoration:underline;
}
</style>
</head>

<body>

<div class="wrap">

<p>Hello,</p>

<p>I hope you are doing well.</p>

<p>
I am writing to express my interest in a
<strong>Python / Django Backend Developer</strong> role at your organisation.
Please find my resume attached for your review.
</p>

<h2>About me</h2>

<p>
I am currently working as a
<strong>Junior Python / Django Backend Developer (Intern)</strong>
at <strong>Zecser Business LLP</strong>, contributing to the development and maintenance of
live production Django applications using
<span class="badge">Python</span>
<span class="badge">Django</span>
<span class="badge">Django REST Framework</span>
<span class="badge">PostgreSQL</span>
<span class="badge">Git</span>
<span class="badge">REST APIs</span>.

My responsibilities include developing backend features, fixing production bugs,
maintaining existing systems, and collaborating with the development team.
Alongside my professional experience, I have built several end-to-end backend
projects that demonstrate scalable API design and clean backend architecture.
</p>

<h2>Current Work &amp; Recent Projects</h2>

<ul>

<li>
<span class="proj">ZecPath</span> —
Contributing to a production Django platform by developing backend features,
implementing business logic, fixing bugs, and integrating database functionality.
</li>

<li>
<span class="proj">WinnersClubX</span> —
Maintaining a live MLM platform through bug fixes,
feature enhancements, and day-to-day backend maintenance.
</li>

<li>
<span class="proj">FieldOps Backend</span> —
Production-grade Django REST Framework backend featuring JWT authentication,
three-role RBAC, service request workflow, analytics APIs, and PostgreSQL.
</li>

<li>
<span class="proj">AutoSpeech2Text</span> —
Flask + React application integrating OpenAI Whisper for speech-to-text
processing with production deployment.
</li>

</ul>

<p>
My GitHub showcases additional backend projects including
<strong>Barcode Scanner</strong>,
<strong>Django Google Connect</strong>,
<strong>GreatEKart</strong>, and other Django applications with
documentation and live demos where applicable.
</p>

<p>
I would welcome the opportunity to discuss how I can contribute to your engineering team.
Thank you for your time and consideration.
</p>

<p>
Best regards,<br>
<strong>Vimal Babu</strong>
</p>

<div class="links">
📞 +91 9567250335 &nbsp;|&nbsp;
<a href="https://github.com/Vimal-Babu">GitHub</a>
&nbsp;|&nbsp;
<a href="https://www.linkedin.com/in/vimalpython3609">LinkedIn</a>
&nbsp;|&nbsp;
<a href="https://vimal-babu.github.io/portfolio">Portfolio</a>
</div>

</div>

</body>
</html>
"""

# ── Send log helpers ──────────────────────────────────────
def load_log() -> dict:
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_log(data: dict):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ── Email builder ─────────────────────────────────────────
def build_message(to_address: str) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["From"]    = EMAIL_ADDRESS
    msg["To"]      = to_address
    msg["Subject"] = SUBJECT

    msg.attach(MIMEText(PLAIN_TEXT, "plain"))
    msg.attach(MIMEText(HTML_BODY,  "html"))   # HTML version takes precedence in modern clients
    return msg

def attach_resume(msg: MIMEMultipart):
    with open(RESUME_FILE, "rb") as f:
        part = MIMEApplication(f.read(), _subtype="pdf")
        part.add_header("Content-Disposition", "attachment", filename="Vimal_Babu_Python_Django_Developer.pdf")
    msg.attach(part)

# ── Main ──────────────────────────────────────────────────
def main():
    contacts = pd.read_csv(CONTACTS_FILE, header=None, names=["Email"])
    send_log = load_log()

    sent = skipped = failed = 0

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        log.info("[OK] Logged in to Gmail SMTP")

        for _, row in contacts.iterrows():
            email = row["Email"].strip().rstrip(".")

            if not email or "@" not in email:
                log.warning(f"[SKIP] Invalid address: {email!r}")
                skipped += 1
                continue

            if send_log.get(email, {}).get("status") == "sent":
                log.info(f"[SKIP]  Already sent to {email}, skipping")
                skipped += 1
                continue

            for attempt in range(1, MAX_RETRIES + 2):
                try:
                    msg = build_message(email)
                    attach_resume(msg)
                    server.send_message(msg)

                    send_log[email] = {
                        "status": "sent",
                        "timestamp": datetime.now().isoformat(),
                    }
                    save_log(send_log)
                    log.info(f"[SENT] {email}")
                    sent += 1
                    break

                except smtplib.SMTPRecipientsRefused:
                    log.error(f"[FAIL] Invalid recipient: {email}")
                    send_log[email] = {"status": "invalid", "timestamp": datetime.now().isoformat()}
                    save_log(send_log)
                    failed += 1
                    break

                except Exception as exc:
                    if attempt <= MAX_RETRIES:
                        log.warning(f"⚠️  Attempt {attempt} failed for {email}: {exc}. Retrying…")
                        time.sleep(3)
                    else:
                        log.error(f"❌  All retries exhausted for {email}: {exc}")
                        send_log[email] = {"status": "failed", "error": str(exc), "timestamp": datetime.now().isoformat()}
                        save_log(send_log)
                        failed += 1

            time.sleep(DELAY_SECONDS)   # Rate limit between sends

    log.info(f"\n[DONE] Sent: {sent}  |  Skipped: {skipped}  |  Failed: {failed}")

if __name__ == "__main__":
    main()