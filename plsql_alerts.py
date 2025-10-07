import feedparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import html
from datetime import datetime

FEEDS = [
    # Replace with real RSS URLs
    "https://www.google.com/alerts/feeds/your-google-alert-id",
]

KEYWORDS = ["plsql", "pl/sql", "oracle pl/sql"]

MY_EMAIL = "YOUR_EMAIL_HERE"  # where you receive alerts
SMTP_USER = "YOUR_EMAIL_HERE"
SMTP_PASS = "YOUR_APP_PASSWORD"

def matches_keywords(text):
    t = text.lower()
    return any(k in t for k in KEYWORDS)

def fetch_and_filter():
    results = []
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")
            summary = entry.get("summary", "")
            if matches_keywords(title + summary):
                results.append({"title": title, "link": link, "summary": summary})
    return results

def make_html(results):
    header = f"<h2>PLSQL Job Alerts — {datetime.now().strftime('%Y-%m-%d')}</h2>"
    if not results:
        return header + "<p>No new jobs today.</p>"
    rows = ""
    for r in results:
        rows += f"<tr><td><a href='{r['link']}'>{html.escape(r['title'])}</a></td><td>{html.escape(r['summary'])}</td></tr>"
    table = f"<table border='1' cellpadding='6'><tr><th>Title</th><th>Summary</th></tr>{rows}</table>"
    return header + table

def send_email(html_content):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Daily PLSQL Job Alerts"
    msg['From'] = SMTP_USER
    msg['To'] = MY_EMAIL
    msg.attach(MIMEText(html_content, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASS)
    server.sendmail(SMTP_USER, [MY_EMAIL], msg.as_string())
    server.quit()

if __name__ == "__main__":
    items = fetch_and_filter()
    html_content = make_html(items)
    send_email(html_content)
    print("Done, jobs sent:", len(items))
