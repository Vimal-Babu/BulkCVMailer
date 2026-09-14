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

RESUME_FILE    = "Vimal_Babu_Python_Django_Backend_Developer_Resume.pdf"
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
I recently completed a 3-month Python Django Backend Developer internship at Zecser Business LLP, where I contributed to the development and maintenance of live production Django applications using Python, Django, Django REST Framework, PostgreSQL, Redis, Celery, Git, and AWS.

During the internship, I contributed 41 Git commits to the ZecPath AI Platform and worked on backend features including job SEO APIs, notifications, ID verification workflows, dashboard APIs, account lifecycle management, and production bug fixes. I also gained hands-on experience working with production code, AWS EC2, Redis, Celery, and PostgreSQL.

Alongside my professional experience, I have built several end-to-end backend applications using Django and Flask, giving me practical experience in REST API development, authentication, database design, and backend application development.

Current Work & Recent Projects:
• ZecPath             – Built and maintained backend features including public job SEO and XML sitemap APIs, job-post notifications using Celery + Redis, ID proof upload and verification workflows, employer/admin dashboard APIs, and candidate/employer account lifecycle features.
• WinnersClubX        – Maintaining a live production MLM platform through backend bug fixes, code cleanup, maintenance, and AWS deployment alignment.
• FieldOps Backend    – Django REST Framework backend with JWT authentication, three-role RBAC, service request lifecycle, dashboard analytics, and PostgreSQL.
• AutoSpeech2Text     – Flask + React application integrating OpenAI Whisper for speech-to-text processing, deployed using Render and Netlify.

My GitHub showcases additional backend projects, including BulkCVMailer, Barcode Scanner, Django Google Connect, GreatEKart, and other Django applications with documentation and live demos where applicable.

I also have experience with REST API development, JWT authentication, Google OAuth 2.0, Redis caching, Celery, AWS EC2, Linux, Git/GitHub, and Postman.

I am currently looking for a full-time Python/Django backend development opportunity where I can contribute to a development team and continue growing as a backend engineer.

I would welcome the opportunity to discuss how I can contribute to your engineering team.

Thank you for your time and consideration.

Best regards,
Vimal Babu

📞 +91 9567250335
GitHub:    https://github.com/Vimal-Babu
LinkedIn:  https://www.linkedin.com/in/vimalpython3609
Portfolio: https://vimal-babu.github.io/portfolio/
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

```html
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
I recently completed a <strong>3-month Python / Django Backend Developer
internship</strong> at <strong>Zecser Business LLP</strong>, where I contributed
to the development and maintenance of live production Django applications using
<span class="badge">Python</span>
<span class="badge">Django</span>
<span class="badge">Django REST Framework</span>
<span class="badge">PostgreSQL</span>
<span class="badge">Redis</span>
<span class="badge">Celery</span>
<span class="badge">Git</span>
<span class="badge">AWS</span>.
</p>

<p>
During the internship, I contributed <strong>41 Git commits</strong> to the
<strong>ZecPath AI Platform</strong> and worked on backend features including
job SEO APIs, job notifications, ID verification workflows, dashboard APIs,
account lifecycle management, and production bug fixes. I also gained
hands-on experience working with production code, AWS EC2, Redis,
Celery, and PostgreSQL.
</p>

<p>
Alongside my professional experience, I have built several end-to-end backend
applications using Django and Flask, giving me practical experience in
REST API development, authentication, database design, and backend
application development.
</p>

<h2>Recent Experience &amp; Projects</h2>

<ul>

<li>
<span class="proj">ZecPath AI Platform</span> —
Production recruitment SaaS where I built and maintained backend features
including public job SEO and XML sitemap APIs, job-post notifications using
Celery + Redis, ID proof upload and verification workflows, employer/admin
dashboard APIs, and candidate/employer account lifecycle features.
</li>

<li>
<span class="proj">WinnersClubX</span> —
Production MLM platform where I worked on backend maintenance,
bug fixes, code cleanup, and AWS deployment alignment.
</li>

<li>
<span class="proj">FieldOps Backend</span> —
Django REST Framework backend featuring JWT authentication,
three-role RBAC, service request lifecycle, dashboard analytics,
and PostgreSQL.
</li>

<li>
<span class="proj">AutoSpeech2Text</span> —
Flask + React application integrating OpenAI Whisper for
speech-to-text processing, deployed on Render and Netlify.
</li>

</ul>

<p>
I also have experience with <strong>REST API development, JWT authentication,
Google OAuth 2.0, Redis caching, Celery, AWS EC2, Linux, Git/GitHub,
and Postman</strong>.
</p>

<p>
My GitHub also showcases additional backend projects including
<strong>BulkCVMailer</strong>,
<strong>Barcode Scanner</strong>,
<strong>Django Google Connect</strong>,
<strong>GreatEKart</strong>, and other Django applications with
documentation and live demos where applicable.
</p>

<p>
I am currently looking for a
<strong>full-time Python / Django backend development opportunity</strong>
where I can contribute to a development team and continue growing
as a backend engineer.
</p>

<p>
I would welcome the opportunity to discuss how I can contribute to your
engineering team. Thank you for your time and consideration.
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
<a href="https://vimal-babu.github.io/portfolio/">Portfolio</a>
</div>

</div>

</body>
```

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
        part.add_header("Content-Disposition", "attachment", filename="Vimal_Babu_Python_Django_Backend_Developer_Resume.pdf")
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