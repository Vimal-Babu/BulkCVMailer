# BulkCVMailer v2.0

Automated resume email sender built with Python. Sends personalized HTML emails with a PDF resume attachment to a list of contacts from a CSV file.

---

## Features

- HTML email body with project badges (looks professional in Gmail, Outlook)
- Persistent send log — skips already-sent contacts on re-run, no duplicates
- Retry logic — retries failed sends up to 2 times before marking as failed
- Rate limiting — configurable delay between sends to avoid Gmail spam flags
- Structured logging — saves full activity log to `mailer.log`

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Vimal-Babu/BulkCVMailer.git
cd BulkCVMailer
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a Gmail App Password

Regular Gmail passwords won't work. You need an **App Password**:

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Security → 2-Step Verification → App passwords
3. Create one for "Mail" — copy the 16-character code

### 5. Create a `.env` file

```env
EMAIL_ADDRESS=youremail@gmail.com
EMAIL_PASSWORD=your_16_char_app_password
```

> Never commit this file. It is already in `.gitignore`.

### 6. Add your contacts

Create a `contacts.csv` file with one email per line, no header:

```
hr@company1.com
careers@company2.com
jobs@company3.com
```

### 7. Add your resume

Place your resume PDF in the project folder and update this line in `send_bulk_emails.py`:

```python
RESUME_FILE = "Your_Resume.pdf"
```

### 8. Customize the email body

Edit the `PLAIN_TEXT` and `HTML_BODY` variables in `send_bulk_emails.py` with your own name, projects, and links.

---

## Run

```bash
python send_bulk_emails.py
```

### Sample output

```
2026-06-01 12:39:38  INFO  [OK] Logged in to Gmail SMTP
2026-06-01 12:39:42  INFO  [SENT] hr@company1.com
2026-06-01 12:39:47  INFO  [DONE] Sent: 1  |  Skipped: 0  |  Failed: 0
```

---

## Configuration

Inside `send_bulk_emails.py` you can adjust:

| Variable | Default | Description |
|---|---|---|
| `DELAY_SECONDS` | `5` | Wait time between sends |
| `MAX_RETRIES` | `2` | Retry attempts for failed sends |
| `RESUME_FILE` | `Vimal_Babu_Resume.pdf` | Your resume filename |
| `LOG_FILE` | `send_log.json` | Persistent send history |

---

## Files

```
BulkCVMailer/
├── send_bulk_emails.py       # Main script
├── contacts.csv              # Your recipient list (not committed)
├── send_log.json             # Auto-generated send history
├── mailer.log                # Activity log
├── .env                      # Your credentials (not committed)
├── .gitignore
└── requirements.txt
```

---

## Version History

### v2.0 (2026)
- HTML email with styled project badges
- Persistent send log with skip-already-sent logic
- Retry logic with backoff
- Rate limiting between sends
- Windows UTF-8 encoding fix

### v1.0 (2025)
- Basic SMTP send using plain text
- CSV contact list via pandas
- PDF resume attachment

---

## Author

**Vimal Babu** — Python / Django Backend Developer

- GitHub: [github.com/Vimal-Babu](https://github.com/Vimal-Babu)
- LinkedIn: [linkedin.com/in/vimalpython3609](https://www.linkedin.com/in/vimalpython3609)
- Portfolio: [vimal-babu.github.io/portfolio](https://vimal-babu.github.io/portfolio)