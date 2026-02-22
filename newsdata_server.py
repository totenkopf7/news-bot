import requests
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

load_dotenv()

app = Flask(__name__)

EMAIL_ADDRESS = "kurdishlearner2018@gmail.com"
NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")
APP_PASSWORD = os.getenv("APP_PASSWORD")


# =========================
# Fetch Latest News
# =========================
def get_latest_news():
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWSDATA_API_KEY,
        "country": "iq",
        "language": "en",
        "q": "Iraq OR Kurdistan"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" not in data:
        return "No news found."

    articles = data["results"][:5]
    message = "Latest Iraq & Kurdistan News\n\n"

    for article in articles:
        message += f"{article.get('title')}\n\n"

    return message


# =========================
# Send Email
# =========================
def send_email():
    news_content = get_latest_news()

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = "Iraq & Kurdistan News Update"

    msg.attach(MIMEText(news_content, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)


# =========================
# Scheduler Loop
# =========================
def run_scheduler():
    schedule.every(2).hours.do(send_email)

    while True:
        schedule.run_pending()
        time.sleep(30)


# =========================
# Dummy Route (Required)
# =========================
@app.route("/")
def home():
    return "News bot is running!"


# =========================
# Start Everything
# =========================
if __name__ == "__main__":
    Thread(target=run_scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))